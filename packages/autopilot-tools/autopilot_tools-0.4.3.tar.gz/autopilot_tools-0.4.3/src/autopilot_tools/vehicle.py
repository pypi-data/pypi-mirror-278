#!/usr/bin/env python3
import logging
import math
import os
import sys
import time
from functools import partial
from io import BufferedIOBase
from typing import List, Union
from time import sleep
import serial
import yaml
from pymavlink import mavutil
from pymavlink.dialects.v20.ardupilotmega import \
    (MAVLink_mission_item_int_message, MAVLink_mission_count_message,
     MAV_MISSION_TYPE_FENCE, MAV_MISSION_TYPE_RALLY,
     MAV_MISSION_TYPE_MISSION, MAV_AUTOPILOT_ARDUPILOTMEGA,
     MAV_AUTOPILOT_PX4, enums, MAV_MISSION_ACCEPTED)
from pymavlink.mavutil import mavlink

from .enums import AutopilotTypes, Devices
from .logger import logger

from .configurator.mavlink_params import deserialize_param_value, \
    float_to_integer, serialize_param_value
from .mission_file.mission_file import Plan, MissionItem, ParamList
from .mission_file.mission_result import MissionResult, StatusCode, StatusText
from .exceptions import MavlinkTimeoutError
from .px4.px4_utils import upload_px4_log
from .utils import retry_command
from .mavlink_ftp.mavftputils import MavFTP

SOURCE_SYSTEM = 2
SOURCE_COMPONENT = 1
MAV_PARAM_TYPE_INT32 = 6
MAX_REQUESTED_SIZE = 90


class Vehicle:
    def __init__(self) -> None:
        self.device_path = None
        self.autopilot: AutopilotTypes = AutopilotTypes.PX4
        self.device: Devices = Devices.serial
        self.master = None
        self.params = None
        self.mav_ftp = None

    def connect(self, device: Devices = "serial"):
        self.device = device
        if device == Devices.serial:
            self._connect_serial()
        elif device == Devices.udp:
            self.device_path = 'udpin:localhost:14540'
            self._connect()
            logger.info(f"Connected: {self.device_path}")
        else:
            logger.critical(
                f"Unknown device {device}: it should be {Devices.udp} or {Devices.serial}")

    def configure(self, file_with_params, reboot=True):
        self._read_yaml_parameters(file_with_params)
        num_of_recv_params = 0

        logger.debug(f"Trying to write {len(self.params)} params...")
        for param_name in self.params:
            set_param_value = self.params[param_name]
            if self.set_specific_param(param_name, set_param_value):
                num_of_recv_params += 1
        logger.info(f"Successfully written {num_of_recv_params}/{len(self.params)} params.")

        if reboot:
            time.sleep(2)
            self.reboot()
            time.sleep(2)
            self.connect()

    def download_px4_log(self, output_dir, output_file_name=""):
        myfile = open("log.ulg", "wb")

        self.master.mav.log_request_list_send(
            self.master.target_system,
            self.master.target_component,
            0,
            1024)
        log_entry_msg = self.master.recv_match(type='LOG_ENTRY', blocking=True)
        last_log_num = log_entry_msg.last_log_num
        last_log_size_kbytes = int(log_entry_msg.size / 1024)
        logger.debug(f"Last log number is {last_log_num}. "
                     f"The size is {last_log_size_kbytes} KBytes.")
        logger.debug(f"Output file will be: {output_dir}/{output_file_name}")

        start_time = time.time()

        for ofs in range(0, log_entry_msg.size, MAX_REQUESTED_SIZE):
            self.master.mav.log_request_dataА_send(
                self.master.target_system,
                self.master.target_component,
                id=last_log_num,
                ofs=ofs,
                count=MAX_REQUESTED_SIZE)

            log_data_msg = self.master.recv_match(type='LOG_DATA', blocking=True)

            data = bytearray(log_data_msg.data)
            myfile.write(data)

            sys.stdout.write("\033[K")
            identifier = log_data_msg.id
            ofs_kbytes = int(log_data_msg.ofs / 1024)
            elapsed_time = int(time.time() - start_time)
            if logger.level < logging.INFO:
                msg = (f"\r{identifier}, {elapsed_time} sec: "
                       f"{ofs_kbytes} / {last_log_size_kbytes} KB.")
                print(msg, end='', flush=True)

            if log_data_msg.count < MAX_REQUESTED_SIZE:
                break

        myfile.close()

    def read_all_params(self):
        self.master.mav.param_request_list_send(
            self.master.target_system, self.master.target_component
        )
        self.params = {}
        prev_recv_time_sec = time.time()
        while prev_recv_time_sec + 1.0 > time.time():
            time.sleep(0.01)
            recv_msg = self.master.recv_match(type='PARAM_VALUE', blocking=False)
            if recv_msg is not None:
                if recv_msg.param_type == MAV_PARAM_TYPE_INT32:
                    recv_msg.param_value = float_to_integer(recv_msg.param_value)
                recv_msg = recv_msg.to_dict()
                self.params[recv_msg['param_id']] = recv_msg['param_value']
                logger.debug(f"name: {recv_msg['param_id']} value: {recv_msg['param_value']}")
                prev_recv_time_sec = time.time()
        logger.info("Done reading parameters")

    def read_specific_param(self, param_name, number_of_attempts=100):
        """Non-blocking read of the specific parameter. Several attemps until fail."""
        logger.debug(f"{param_name: <18}", end='', flush=True)

        recv_msg = None
        value = None
        for _ in range(number_of_attempts):
            self.master.mav.param_request_read_send(
                self.master.target_system,
                self.master.target_component,
                bytes(param_name, 'utf-8'),
                -1
            )

            recv_msg = self.master.recv_match(type='PARAM_VALUE', blocking=False)
            if recv_msg is None:
                time.sleep(0.1)
                continue

            recv_param_name, param_type, value = deserialize_param_value(self.autopilot, recv_msg)
            if recv_param_name == param_name:
                logger.debug(f"{param_type: <6} {value}")
                break

        if recv_msg is None:
            logger.warning(f'Reading {param_name} failed {number_of_attempts} times.')
        return value

    def set_specific_param(self, param_name, param_value, number_of_attempts=50):
        """Non-blocking set of the specific parameter. Return True in success, otherwise False."""
        self.master.mav.param_set_send(
            self.master.target_system,
            self.master.target_component,
            bytes(param_name, 'utf-8'),
            *serialize_param_value(param_value)
        )
        for _ in range(number_of_attempts):
            recv_msg = self.master.recv_match(type='PARAM_VALUE', blocking=False)
            if recv_msg is None:
                time.sleep(0.01)
                continue

            recv_name, recv_type, recv_value = deserialize_param_value(self.autopilot, recv_msg)
            if recv_name != param_name:
                time.sleep(0.01)
                continue

            if math.isclose(recv_value, param_value, rel_tol=1e-4):
                logger.info(f"{recv_name: <18} {recv_type: <6} {recv_value}")
                return True

            logger.warning(f'{param_name}: expected {param_value}, received {recv_value}.')
            return False

        logger.warning(f'Writing {param_name} failed {number_of_attempts} times.')
        return False

    def reset_params_to_default(self):
        self._reset_params_to_default()
        self.reboot()
        time.sleep(2)
        self.connect()

    def force_calibrate(self):
        param2 = 76
        param5 = 76
        self.master.mav.command_long_send(self.master.target_system, self.master.target_component,
                                          mavutil.mavlink.MAV_CMD_PREFLIGHT_CALIBRATION, 0,
                                          0, param2, 0, 0, param5, 0, 0)

    def reboot(self):
        self.master.reboot_autopilot()
        self.master.close()

    def download_mission(self) -> List[MAVLink_mission_item_int_message]:

        def get_count() -> MAVLink_mission_count_message:
            self.master.mav.mission_request_list_send(
                self.master.target_system, self.master.target_component)
            return self.master.recv_match(type='MISSION_COUNT', blocking=True, timeout=1)

        count = retry_command(get_count)
        if count is None:
            raise MavlinkTimeoutError

        data = []
        i = 0
        while i < count.count:

            def get_mission_item() -> MAVLink_mission_item_int_message:
                self.master.mav.mission_request_int_send(
                    self.master.target_system, self.master.target_component, i)
                return self.master.recv_match(type='MISSION_ITEM_INT', blocking=True, timeout=1)

            data_item = retry_command(get_mission_item)
            if data_item is None:
                raise MavlinkTimeoutError

            if data_item.seq == i:
                i += 1
                data.append(data_item)
        self.master.mav.mission_ack_send(
            self.master.target_system, self.master.target_component, MAV_MISSION_ACCEPTED)
        return data

    def load_mission(self, path: str) -> StatusCode:
        mission_file = Plan(path)

        fence_items = mission_file.geofence.get_mission_item_representation()
        rally_points_length = mission_file.rally_points.get_mission_item_representation()
        mission_length = mission_file.mission.get_mission_item_representation()

        def send_mission_items(
                count: int, item_list: List[MissionItem], mission_type: int) -> StatusCode:
            self.master.mav.mission_count_send(
                self.master.target_system, self.master.target_component,
                count, mission_type
            )
            if not item_list:
                return StatusCode.EMPTY_MISSION_ITEM_LIST
            reached_last_item = False
            next_item = -1
            while not reached_last_item:
                res = self.master.recv_match(
                    type=['MISSION_REQUEST_INT', 'MISSION_REQUEST'], blocking=True, timeout=0.5)
                if res is None:
                    return StatusCode.MAVLINK_ERROR
                next_item = res.seq
                logger.debug(f"Sending {item_list[next_item]} with id {next_item}")

                to_send = item_list[next_item]

                params = ParamList(
                    *[x if x is not None else math.nan for x in to_send.params]
                )
                self.master.mav.mission_item_int_send(
                    self.master.target_system, self.master.target_component,
                    to_send.arguments.seq,
                    to_send.arguments.frame,
                    to_send.arguments.command,
                    to_send.arguments.current,
                    to_send.arguments.auto_continue,
                    params.param1,
                    params.param2,
                    params.param3,
                    params.param4,
                    params.x,
                    params.y,
                    params.z,
                    to_send.mission_type
                )

                if next_item == count - 1:
                    reached_last_item = True

            res = self.master.recv_match(type='MISSION_ACK', blocking=True, timeout=0.5)

            return StatusCode.OK if res is not None else StatusCode.MAVLINK_ERROR

        result = retry_command(
            partial(send_mission_items, *fence_items, MAV_MISSION_TYPE_FENCE),
            test=lambda x: x in [StatusCode.OK, StatusCode.EMPTY_MISSION_ITEM_LIST])
        if result is None:
            raise MavlinkTimeoutError

        result = retry_command(
            partial(send_mission_items, *rally_points_length, MAV_MISSION_TYPE_RALLY),
            test=lambda x: x in [StatusCode.OK, StatusCode.EMPTY_MISSION_ITEM_LIST])
        if result is None:
            raise MavlinkTimeoutError

        result = retry_command(
            partial(send_mission_items, *mission_length, MAV_MISSION_TYPE_MISSION),
            test=lambda x: x in [StatusCode.OK, StatusCode.EMPTY_MISSION_ITEM_LIST])
        if result is None:
            raise MavlinkTimeoutError
        logger.info('Mission upload complete')
        return StatusCode.OK

    def get_autopilot_type(self):
        return self.autopilot

    def run_mission(self, path: str = None, timeout: int = 100) -> MissionResult:
        if path is not None:
            self.load_mission(path)

        mission_data = self.download_mission()
        sleep(5)
        seq = 0
        start_time = time.time()
        time_elapsed = 0
        self.master.mav.command_long_send(
            self.master.target_system, self.master.target_component,
            mavutil.mavlink.MAV_CMD_MISSION_START,
            0,
            0, len(mission_data) - 1, 0, 0, 0, 0, 0
        )

        seq_zeroed = False
        logger.info(f"starting mission from {seq} mission_item")

        status_texts = []

        while not seq_zeroed and time_elapsed < timeout:
            msg = self.master.recv_match(type='MISSION_CURRENT', blocking=False)
            status = self.master.recv_match(type='STATUSTEXT', blocking=False)
            if status:
                status_texts.append(StatusText(status.severity, status.text))

            if msg is None:
                time.sleep(0.01)
                continue

            if msg.seq != seq:
                if msg.seq == 0:
                    seq_zeroed = True
                else:
                    seq = msg.seq
                    logger.info(f"mission_item {msg.seq} reached")
            time_elapsed = time.time() - start_time
        return MissionResult(
            StatusCode.OK if time_elapsed < timeout else StatusCode.MISSION_TIMEOUT,
            int(time_elapsed),
            len(mission_data),
            status_texts
        )

    def _connect_serial(self):
        while True:
            try:
                self.device_path, self.autopilot = Vehicle._get_autopilot_serial_path()
                if self.device_path is not None:
                    self._connect()
                    logger.info(f"Connected: {self.device_path}")
                    break
            except serial.serialutil.SerialException:
                pass

            time.sleep(1)
            logger.info(f"Waiting for the Autopilot {self.device_path}...")

    @staticmethod
    def _get_autopilot_serial_path():
        serial_devices = retry_command(
            lambda: os.listdir('/dev/serial/by-id'),
            delay=5, times=6
        )
        return Vehicle.get_autopilot_type_by_serial_devices(serial_devices)

    @staticmethod
    def get_autopilot_type_by_serial_devices(serial_devices):
        if len(serial_devices) < 1:
            return None, None

        device_path = None
        autopilot_type = None
        for serial_device in serial_devices:
            if -1 != serial_device.find(AutopilotTypes.ArduPilot):
                device_path = f"/dev/serial/by-id/{serial_device}"
                autopilot_type = AutopilotTypes.ArduPilot
                break
            if -1 != serial_device.find(AutopilotTypes.PX4):
                device_path = f"/dev/serial/by-id/{serial_device}"
                autopilot_type = AutopilotTypes.PX4
                break

        return device_path, autopilot_type

    def get_log_folder(self) -> Union[str, None]:
        folder = {
            (Devices.udp, AutopilotTypes.PX4): '/log',
            (Devices.udp, AutopilotTypes.ArduPilot): None,
            (Devices.serial, AutopilotTypes.PX4): '/fs/microsd/log/',
            (Devices.serial, AutopilotTypes.ArduPilot): '/APM/LOGS'
        }.get((self.device, self.autopilot))
        if folder is None:
            logger.critical(f"For now only {AutopilotTypes.PX4} SITL is supported")
        return folder

    def _reset_params_to_default(self):
        self.master.mav.command_long_send(
            self.master.target_system,
            self.master.target_component,
            mavutil.mavlink.MAV_CMD_PREFLIGHT_STORAGE,
            0,
            2, -1, 0, 0, 0, 0, 0)

    def _read_yaml_parameters(self, filename):
        with open(filename, encoding='UTF-8') as file_descriptor:
            self.params = yaml.load(file_descriptor, Loader=yaml.FullLoader)

        logger.debug(f"{filename} has : {self.params}")

    def _connect(self):
        self.master = mavutil.mavlink_connection(
            self.device_path,
            source_component=SOURCE_COMPONENT,
            source_system=SOURCE_SYSTEM)
        self.master.mav.heartbeat_send(
            type=mavlink.MAV_TYPE_CHARGING_STATION,
            autopilot=6,
            base_mode=12,
            custom_mode=0,
            system_status=4)
        hb = self.master.wait_heartbeat(timeout=20)

        if hb is None:
            logger.critical('Failed to receive a heartbeat from the FMU. '
                            'Please check your setup. Terminating.')
            sys.exit(1)

        self.mav_ftp = MavFTP(self.master)
        self.autopilot = {
            MAV_AUTOPILOT_ARDUPILOTMEGA: AutopilotTypes.ArduPilot,
            MAV_AUTOPILOT_PX4: AutopilotTypes.PX4
        }.get(hb.autopilot)

        if self.autopilot is None:
            logger.error(
                f'You are connected to unsupported autopilot: '
                f' {enums["MAV_AUTOPILOT"][hb.autopilot].name}. '
                f'Proceed with caution')

        system_str = f"system {self.master.target_system}"
        component_str = f"component {self.master.target_component}"
        logger.info(f"Heartbeat from system ({system_str} {component_str})")

    def analyze_log(self, log: Union[str, bytes, BufferedIOBase, os.PathLike]) -> Union[str, None]:
        if isinstance(log, (str, os.PathLike)):
            with open(log, 'rb') as f:
                log = f.read()

        if isinstance(log, BufferedIOBase):
            log = log.read()

        if self.autopilot == AutopilotTypes.PX4:
            return upload_px4_log(log)
        if self.autopilot == AutopilotTypes.ArduPilot:
            logger.critical("For now only PX4 log analysis is supported")
        return None
