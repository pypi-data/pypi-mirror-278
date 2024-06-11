"""
Guardian Bluetooth utils.
"""

import asyncio
import base64
import datetime
import gc
import logging
import platform
import time
import typing
from codecs import utf_8_encode

from bleak import BleakClient, BleakScanner, exc

from .debug_logs import *
from .guardian_recording import GuardianRecording
from .utils import now
from .websocket_messages import PublishRawMeasurements, EndOngoingRecording

SEARCH_BREAK = 3

UUID_MEAS_EEGIMU: str = "beffd56c-c915-48f5-930d-4c1feee0fcc4"
UUID_MEAS_IMP: str = "beffd56c-c915-48f5-930d-4c1feee0fcc8"
UUID_DEVICE_SERVICE: str = "0000180a-0000-1000-8000-00805f9b34fb"
UUID_MAC_ID: str = "00002a25-0000-1000-8000-00805f9b34fb"
UUID_FIRMWARE_VERSION: str = "00002a26-0000-1000-8000-00805f9b34fb"
UUID_CFG: str = "beffd56c-c915-48f5-930d-4c1feee0fcc9"
UUID_CMD: str = "beffd56c-c915-48f5-930d-4c1feee0fcca"
LED_ON_CFG: str = "d1"
LED_OFF_CFG: str = "d0"
NOTCH_FREQ_50_CFG: str = "n0"
NOTCH_FREQ_60_CFG: str = "n1"
START_CMD: str = "M"  #'\x62' #b -> start measurement
STOP_CMD: str = "S"  # '\x73' #s -> stop measurement
START_IMP_CMD: str = "Z"  # '\x7a' #z -> start impedance
STOP_IMP_CMD: str = "X"  # '\x78' #x -> stop impedance
UUID_BATT_GDK: str = "00002a19-0000-1000-8000-00805f9b34fb"

logger = logging.getLogger("idun_guardian_sdk")


class GuardianBLE:
    """Main Guardian BLE client."""

    def __init__(self, address: str = "") -> None:
        """Initialize the Guardian BLE client.

        Args:
            address (str, optional): BLE device address. Defaults to "".
        """
        self.client: typing.Optional[BleakClient] = None

        self.address = address

        # Initial connection flags
        self.initialise_connection: bool = True
        self.connection_established = False
        self.time_left = True
        self.initial_time = True

        # Bluetooth reconnect delay
        self.original_time = time.time()
        self.reconnect_try_amount = 50
        self.try_to_connect_timeout = self.reconnect_try_amount

        # Bluetooth timings
        self.ble_delay = 1
        self.ble_stop_delay = 1
        self.device_lost = False

        # API timeings
        self.sent_final_package_time = 1

        # The timing constants
        self.sample_rate = 250
        self.amount_samples_packet = 20
        self.max_index = 256
        self.prev_index = 0
        self.prev_timestamp = 0
        self.sequence_number = 0

        self.remaining_time = 1

        self._get_ble_characteristic()
        self.device = None
        self.mac_id = ""
        self.platform = platform.system()
        self.teminating_ble_process = False

    def _get_ble_characteristic(self) -> None:
        """Get the environment variables."""
        # General information
        self.battery_id = UUID_BATT_GDK
        self.device_service = UUID_DEVICE_SERVICE
        self.mac_uuid = UUID_MAC_ID
        self.firmware_uuid = UUID_FIRMWARE_VERSION

        # EEG/IMU measurement
        self.meas_eeg_id = UUID_MEAS_EEGIMU
        self.command_id = UUID_CMD
        self.start_cmd = START_CMD
        self.stop_cmd = STOP_CMD

        # Impedance measurement
        self.meas_imp_id = UUID_MEAS_IMP
        self.start_imp_cmd = START_IMP_CMD
        self.stop_imp_cmd = STOP_IMP_CMD
        self.notch_freq_50_cfg = NOTCH_FREQ_50_CFG
        self.notch_freq_60_cfg = NOTCH_FREQ_60_CFG

        # LED control
        self.cfg_id = UUID_CFG
        self.led_on_cfg = LED_ON_CFG
        self.led_off_cfg = LED_OFF_CFG

    def _disconnected_callback(self, client):  # pylint: disable=unused-argument
        """
        Callback function when device is disconnected.

        Args:
            client (BleakClient): BleakClient object
        """
        logging_disconnected_recognised()
        self.connection_established = False
        self.initialise_connection = True

    async def get_ble_devices(self) -> list:
        """
        Scan for IGEB devices and return a list of devices.
        """
        devices_dict: dict = {}
        ble_device_list: list = []
        devices = await BleakScanner.discover()
        igeb_name = "IGEB"
        device_id = 0
        print("\n----- Available devices -----\n")
        print("Index | Name | Address")
        print("----------------------------")
        for _, device in enumerate(devices):
            # print device discovered
            if device.name == igeb_name:
                print(f"{device_id}     | {device.name} | {device.address}")
                devices_dict[device.address] = []
                devices_dict[device.address].append(device.name)
                ble_device_list.append(device.address)
                device_id += 1
        print("----------------------------\n")
        return ble_device_list

    async def get_device_mac(self) -> str:
        """
        Get the device MAC address.
        This is different from BLE device address
        (UUID on Mac or MAC address on Windows)

        Returns:
            str: MAC address
        """
        # async with BleakClient(self.address) as client:
        logging_searching()
        value = bytes(await self.client.read_gatt_char(self.mac_uuid))
        await asyncio.sleep(self.ble_delay)
        firmware_version = bytes(await self.client.read_gatt_char(self.firmware_uuid))
        mac_address = value.decode("utf-8")
        firmware_decoded = firmware_version.decode("utf-8")
        mac_address = mac_address.replace(":", "-")

        logging_device_info(mac_address, firmware_decoded)
        return mac_address

    async def search_device(self) -> str:
        """This function searches for the device and returns the address of the device.
        If the device is not found, it exits the program. If multiple devices are found,
        it asks the user to select the device. If one device is found, it returns the
        address of the device.

        Returns:
            str: Device address
        """

        while True:
            ble_device_list = await self.get_ble_devices()
            if len(ble_device_list) == 0:
                logging_device_not_found(SEARCH_BREAK)
                await asyncio.sleep(SEARCH_BREAK)

            elif len(ble_device_list) == 1:
                logging_device_found(ble_device_list)
                self.address = ble_device_list[0]
                break
            else:
                index_str = input(
                    "Enter the index of the GDK device you want to connect to \
                    \nIf cannot find the device, please restart the program and try again: "
                )
                index = int(index_str)
                self.address = ble_device_list[index]
                break

        logging_device_address(self.address)

        return self.address

    async def connect_to_device(self):
        """
        This function initialises the connection to the device.
        It finds the device using the address, sets up callback,
        and connects to the device.
        """
        logging_trying_to_connect(self.address)

        if not self.device:
            self.device = await BleakScanner.find_device_by_address(self.address, timeout=20.0)
        if not self.device:
            raise exc.BleakError(f"A device with address {self.address} could not be found.")

        if self.platform == "Windows":
            if not self.client:
                self.client = BleakClient(
                    self.device, disconnected_callback=self._disconnected_callback
                )
        else:
            self.client = None
            self.client = BleakClient(
                self.device, disconnected_callback=self._disconnected_callback
            )
        if self.client is not None:
            try:
                await asyncio.wait_for(self.client.connect(), timeout=4)
            except asyncio.TimeoutError:
                log_timeout_while_trying_connection()
                pass
            except Exception as err:
                log_exception_while_trying_connection(err)
                pass
            if self.client.is_connected:
                if self.mac_id == "":
                    try:
                        self.mac_id = await self.get_device_mac()

                    except Exception as err:
                        log_exception_unable_to_find_MACaddress(err)
                        self.initialise_connection = True
                        self.connection_established = False
                        return 0
                if self.mac_id:
                    self.connection_established = True
                    self.initialise_connection = False
                    logging_connected(self.address)
                    return 1

            else:
                log_no_connection_established()
                try:
                    await self.client.disconnect()
                    await asyncio.sleep(4)
                except Exception:
                    log_exception_in_disconnecting()
                gc.collect()
                self.initialise_connection = True
                self.connection_established = False
                return 0
        else:
            log_not_client_found()

    async def run_ble_record(
        self,
        guardian_recording: GuardianRecording,
        record_time: int = 60,
        led_sleep: bool = False,
    ) -> None:
        """
        This function runs the recording of the data. It sets up the bluetooth
        connection, starts the recording, and then reads the data and adds it to
        the queue. The API class then reads the data from the queue and sends it
        to the cloud.

        Args:
            guardian_recording (GuardianRecording): GuardianRecording object
            record_time (_type_): The time to record for
            led_sleep (_type_): Whether to turn off the LED

        Raises:
            BleakError: _description_
        """

        def time_stamp_creator(new_index):
            """
            This function creates a timestamp for the cloud based on the
            time the recording started. Each time stamp is based on the index
            of that is sent from the device. The index is the number of iterates
            between 0 and 256. The time stamp is the 1/250s multiplied by the
            index.

            Args:
                new_index (int): Index of the data point from the ble packet

            Returns:
                str: Timestamp in the format of YYYY-MM-DDTHH:MM:SS
            """
            index_diff = new_index - self.prev_index

            if self.prev_timestamp == 0:
                time_data = datetime.datetime.now().astimezone().isoformat()
                # convert time_data to a float in seconds
                time_data = time.mktime(
                    datetime.datetime.strptime(time_data, "%Y-%m-%dT%H:%M:%S.%f%z").timetuple()
                )
                new_time_stamp = time_data
            else:
                multiplier = (index_diff + self.max_index) % self.max_index
                new_time_stamp = (
                    self.amount_samples_packet * (1 / self.sample_rate) * multiplier
                ) + self.prev_timestamp

            self.prev_index = new_index
            self.prev_timestamp = new_time_stamp

            return new_time_stamp * 1000

        async def data_handler(_, data):
            """Data handler for the BLE client.
                Data is put in a queue and forwarded to the API.

            Args:
                callback (handler Object): Handler object
                data (bytes): Binary data package
            """
            data_base_64 = base64.b64encode(data).decode("ascii")
            new_time_stamp = time_stamp_creator(data[1])

            package = PublishRawMeasurements(
                event=data_base_64,
                deviceId=self.mac_id,
                deviceTs=new_time_stamp,
                recordingId=guardian_recording.recording_id,
                sequence=self.sequence_number,
            ).to_dict()
            guardian_recording.latency_map[self.sequence_number] = time.time()
            self.sequence_number += 1
            if not guardian_recording.data_queue.full():
                await asyncio.shield(guardian_recording.data_queue.put(package))
            else:
                msg = await asyncio.shield(guardian_recording.data_queue.get())
                logger.debug("data_queue is full discarding: ", msg)
                await asyncio.shield(guardian_recording.data_queue.put(package))

        async def wait_recording_id_set():
            """Wait for the recording ID to be set by the API."""
            while not guardian_recording.rec_started:
                logger.debug("[BLE]: Waiting recording id to be set by API")
                await asyncio.sleep(1)
            logger.debug(f"[BLE]: Recording ID Set: {guardian_recording.recording_id}")

        async def send_start_commands_recording():
            """Send start commands to the device."""
            logging_sending_start()

            # ------------------ Configuration ------------------
            if led_sleep:
                await asyncio.sleep(self.ble_delay)
                await self.client.write_gatt_char(self.cfg_id, utf_8_encode(self.led_off_cfg)[0])
            # ------------------ Subscribe to notifications ------------------
            # Notify the client that these two services are required
            logging_subscribing_eeg_notification()
            await asyncio.sleep(self.ble_delay)

            # Waiting recording Id to be set by API
            await asyncio.wait_for(
                wait_recording_id_set(), timeout=20
            )  # TODO: set better/configurable timeout

            await self.client.start_notify(self.meas_eeg_id, data_handler)

            # ------------------ Start commands ------------------
            # sleep so that cleint can respond
            await asyncio.sleep(self.ble_delay)
            # send start command for recording data
            await self.client.write_gatt_char(self.command_id, utf_8_encode(self.start_cmd)[0])

        async def stop_recording_timeout():
            """Stop recording gracefully."""
            logging_sending_stop_device()

            await self.client.write_gatt_char(self.command_id, utf_8_encode(self.stop_cmd)[0])

            await asyncio.sleep(self.ble_delay)

            # ------------------ Load final stop package ------------------
            package = EndOngoingRecording(
                self.mac_id, guardian_recording.recording_id, now()
            ).to_dict()
            if not guardian_recording.data_queue.full():
                await guardian_recording.data_queue.put(package)
            else:
                await guardian_recording.data_queue.get()
                await guardian_recording.data_queue.put(package)
            logging_sending_stop()
            # ------------------ API should send already loaded package  ------------------
            logging_giving_time_api()
            await asyncio.sleep(
                self.sent_final_package_time
            )  # This gives time for the api to send already loaded data

            if led_sleep:
                logging_turn_ble_on()
                await asyncio.sleep(self.ble_delay)
                await self.client.write_gatt_char(self.cfg_id, utf_8_encode(self.led_on_cfg)[0])
            # ------------------ Disconnect command to device ------------------
            logging_sending_disconnect()
            await asyncio.sleep(self.ble_stop_delay)
            await self.client.disconnect()
            await asyncio.sleep(self.ble_stop_delay)

            logging_recording_successfully_stopped()

        async def stop_recording_cancelled_script():
            """Stop recording abruptly."""
            logging_keyboard_interrupt()

            # ------------------ Send stop EEG recording command ------------------
            logging_sending_stop_device()
            await asyncio.sleep(self.ble_delay)
            try:
                await self.client.write_gatt_char(self.command_id, utf_8_encode(self.stop_cmd)[0])
            except Exception:
                log_device_not_connected_cannot_stop()

            await asyncio.sleep(self.ble_delay)

            # ------------------ Sending final API packages ------------------
            logging_giving_time_api()
            await asyncio.sleep(self.sent_final_package_time)  # Give API time to send last package
            # With its own interupt handling
            # ------------------ Configuring LED back on ------------------
            if led_sleep:
                logging_turn_led_on()
                await asyncio.sleep(self.ble_delay)
                await self.client.write_gatt_char(self.cfg_id, utf_8_encode(self.led_on_cfg)[0])
            # ------------------ Disconnecting commands ------------------
            logging_sending_disconnect()
            await asyncio.sleep(self.ble_stop_delay)

            await self.client.disconnect()

            await asyncio.sleep(self.ble_stop_delay)
            logging_recording_successfully_stopped()
            # ------------------ Sending final API packages ------------------
            logging_giving_time_api()
            await asyncio.sleep(self.sent_final_package_time)  # Give API time to send last package
            # With its own interupt handling

        async def stop_recording_device_lost():
            """Stop recording device lost."""
            logging_device_lost_give_up()
            # ------------------ Loading last package ------------------
            logging_sending_stop()
            package = EndOngoingRecording(
                self.mac_id, guardian_recording.recording_id, now()
            ).to_dict()
            # pack the stop command
            if not guardian_recording.data_queue.full():
                await guardian_recording.data_queue.put(package)
            else:
                await guardian_recording.data_queue.get()
                await guardian_recording.data_queue.put(package)
            # ------------------ Sending final API packages ------------------
            logging_giving_time_api()
            await asyncio.sleep(self.sent_final_package_time)  # Give API time to send last package
            return True

        async def bluetooth_reconnect():
            """Set flags to reconnect to bluetooth device."""
            self.try_to_connect_timeout = self.try_to_connect_timeout - 1
            if self.try_to_connect_timeout <= 0:
                self.device_lost = await stop_recording_device_lost()
            logging_trying_to_connect_again(self.try_to_connect_timeout)
            self.connection_established = False
            self.initialise_connection = True

        def initialise_timestamps():
            if self.initial_time:
                self.initial_time = False  # record that this is the initial time
                self.original_time = time.time()

        async def main_loop():
            while True:
                if self.connection_established:
                    await asyncio.shield(
                        asyncio.sleep(self.ble_delay)
                    )  # sleep so that everything can happen
                    self.remaining_time = record_time - (time.time() - self.original_time)
                    logger.debug(f"[BLE]: Time left: {round(self.remaining_time)}s")

                    if self.remaining_time <= 0:
                        logging_time_reached(self.original_time)
                        await stop_recording_timeout()
                        break

                else:
                    break

        # >>>>>>>>>>>>>>>>>>>>> Start of recording process <<<<<<<<<<<<<<<<<<<<<<<<
        # ------------------ Initialise values for timestamps ------------------
        self.prev_timestamp = 0
        self.prev_index = -1
        # ------------------ Initialise time values for recording timeout ------------------
        # This has been decoupled from the device timing for robustness
        self.original_time = time.time()
        self.initial_time = True
        self.time_left = True
        self.initial_time = True
        # ------------------ Initialise connection values for trying to connect again ------------------
        # self.connection_established = False
        self.try_to_connect_timeout = self.reconnect_try_amount

        while not self.teminating_ble_process:
            log_connection_flag(self.connection_established)
            log_connection_initialize_flag(self.initialise_connection)

            try:
                if self.initialise_connection:
                    while self.initialise_connection == True:
                        await self.connect_to_device()
                if self.client is not None:
                    if self.client.is_connected:
                        logging_device_connected_general()
                        # for windows reconnection
                        self.initialise_connection = True

                    await send_start_commands_recording()

                    logging_recording_started()
                    self.try_to_connect_timeout = self.reconnect_try_amount  # reset counter
                    # >>>>>>>>>>>>>>>>>>>>> Main loop <<<<<<<<<<<<<<<<<<<<<<<<
                    initialise_timestamps()
                    await asyncio.shield(main_loop())
                    # >>>>>>>>>>>>>>>>>>>>> Main loop <<<<<<<<<<<<<<<<<<<<<<<<

                if self.remaining_time <= 0:
                    self.teminating_ble_process = True
                    break

                if not self.connection_established:
                    logging_disconnected_recognised()
                    await bluetooth_reconnect()
                    if self.device_lost:
                        break

            except asyncio.CancelledError:
                await stop_recording_cancelled_script()
                self.teminating_ble_process = True
                self.connection_established = False
                self.initialise_connection = False
                break

            except Exception as error:
                logging_ble_client_lost(error)

            finally:
                logging_ensuring_ble_disconnected()
                await asyncio.sleep(self.ble_stop_delay)
                if self.client is not None:
                    if self.client.is_connected:
                        try:
                            logger.debug("[BLE]: Stop EEG notification")
                            await self.client.stop_notify(self.meas_eeg_id)
                            await asyncio.sleep(self.ble_delay)
                            await self.client.disconnect()
                            gc.collect()
                        except Exception:
                            log_exception_in_disconnecting()

                await asyncio.sleep(self.ble_stop_delay)
                self.connection_established = False

        logging_ble_complete()

    async def get_service_and_char(self) -> None:
        """Get the services and characteristics of the device."""
        try:
            async with BleakClient(self.address) as client:
                logging_device_connected_general()

                for service in client.services:
                    logging_device_info_uuid(service)

                    for char in service.characteristics:
                        if "read" in char.properties:
                            try:
                                value = bytes(await client.read_gatt_char(char.uuid))
                            except exc.BleakError as err:
                                value = str(err).encode()
                        else:
                            value = None
                        logging_device_info_characteristic(char, value)

                await asyncio.sleep(self.ble_stop_delay)
                await client.disconnect()
                await asyncio.sleep(self.ble_stop_delay)
                logging_sending_disconnect()

        except exc.BleakError as err:
            logging_device_connection_failed(err)

    async def read_battery_level(self) -> None:
        """Read the battery level of the device given pre-defined interval."""
        logging_reading_battery_level()
        while True:
            try:
                async with BleakClient(self.address) as client:
                    logging_device_connected_general()

                    await asyncio.sleep(self.ble_delay)
                    value = int.from_bytes(
                        (await client.read_gatt_char(self.battery_id)),
                        byteorder="little",
                    )
                    print("-----------------------------")
                    print(f"\nBattery level: {value}%\n")
                    print("-----------------------------")
                    logging_batterylevel_int(value)

                    await asyncio.sleep(self.ble_stop_delay)
                    await client.disconnect()
                    await asyncio.sleep(self.ble_stop_delay)
                    logging_sending_disconnect()
                    break

            except exc.BleakError as err:
                # log the error
                logging_device_connection_failed(err)
                await asyncio.sleep(3)
                continue

    async def get_device_information(self) -> dict:
        """Read the device information of the device."""

        device_info = {}

        async with BleakClient(self.address) as client:
            logging_device_connected_general()

            for service in client.services:
                if service.uuid == self.device_service:
                    for char in service.characteristics:
                        if "read" in char.properties:
                            try:
                                value = bytes(await client.read_gatt_char(char.uuid))
                            except exc.BleakError as err:
                                value = str(err).encode()
                        else:
                            value = None

                        print(f"{ char.description}:{str(value)}")
                        device_info[char.description] = str(value)
                        logging_device_description_list(char, value)

        return device_info

    async def stream_impedance(self, mains_freq_60hz: bool = False, handler: typing.Optional[callable] = None):
        """
        Stream impedance data from the Guardian Earbuds. Runs indefinitely until cancelled.

        Args:
            mains_freq_60hz (bool, optional): Set to True if the mains frequency is 60Hz. Defaults to False.
            handler: The callback function to handle the impedance data. If None is given, the default handler will be used.
                which simply logs the impedance value to the console.
        """

        def default_impedance_handler(data_int):
            logger.info(f"[BLE]: Impedance value : {round(data_int/1000,2)} kOhms")

        async def impedance_handler(_, data):
            """Impedance handler for the BLE client.
                Data is put in a queue and forwarded to the API.

            Args:
                callback (handler Object): Handler object
                data (bytes): Binary data package with impedance values
            """
            data_int = int.from_bytes(data, byteorder="little")
            if handler is not None:
                handler(data_int)
            else:
                default_impedance_handler(data_int)

        async def send_start_commands_impedance():
            # ----------------- Configuration -----------------
            if mains_freq_60hz:
                await asyncio.sleep(self.ble_delay)
                await self.client.write_gatt_char(
                    self.cfg_id, utf_8_encode(self.notch_freq_60_cfg)[0]
                )
            else:
                await asyncio.sleep(self.ble_delay)
                await self.client.write_gatt_char(
                    self.cfg_id, utf_8_encode(self.notch_freq_50_cfg)[0]
                )

            # ----------------- Subscribe -----------------
            logging_subscribing_impedance_notification()
            await asyncio.sleep(self.ble_delay)
            await self.client.start_notify(self.meas_imp_id, impedance_handler)

            # ----------------- Send start command -----------------
            logging_starting_impedance_measurement_commands()
            await asyncio.sleep(self.ble_delay)
            await self.client.write_gatt_char(self.command_id, utf_8_encode(self.start_imp_cmd)[0])

        async def main_loop():
            while True:
                await asyncio.sleep(1)

        async def stop_impedance_cancelled_script():
            # ------------------ Send stop impedance command ------------------
            logging_sending_stop_device()
            await self.client.write_gatt_char(self.command_id, utf_8_encode(self.stop_imp_cmd)[0])

            # ------------------ Disconnect command to device ------------------
            logging_sending_disconnect()
            await asyncio.sleep(self.ble_stop_delay)
            await self.client.disconnect()

        try:
            while self.initialise_connection == True:
                await self.connect_to_device()
            if self.client is not None:
                if self.client.is_connected:
                    logging_device_connected_general()

                await send_start_commands_impedance()
                logger.info("Impedance measurement started")

                # >>>>>>>>>>>>>>>>>>>>> Main loop <<<<<<<<<<<<<<<<<<<<<<<<
                await asyncio.shield(main_loop())
                # >>>>>>>>>>>>>>>>>>>>> Main loop <<<<<<<<<<<<<<<<<<<<<<<<

        except asyncio.CancelledError:
            logger.info("[BLE] Received Stop Signal. Gracefully stopping impedance streaming")
            await stop_impedance_cancelled_script()
        finally:
            logging_ensuring_ble_disconnected()
            await asyncio.sleep(self.ble_stop_delay)
            if self.client is not None:
                if self.client.is_connected:
                    try:
                        logger.debug("[BLE]: Stop impedance notification")
                        await self.client.stop_notify(self.meas_imp_id)
                        await asyncio.sleep(self.ble_delay)
                        await self.client.disconnect()
                        gc.collect()
                    except Exception:
                        log_exception_in_disconnecting()

            await asyncio.sleep(self.ble_stop_delay)
            self.connection_established = False
        logger.debug("Impedance measurement finished")
