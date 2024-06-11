"""
IndyCAREReporter.py
@create on Jan 7 2024
    version: v3.2.0.1
"""

from __future__ import annotations

import traceback
from abc import abstractmethod, ABC

import re, sys, json, glob, time, signal, shutil, logging, subprocess
import cv2

from pathlib import Path
from zipfile import ZipFile
from datetime import datetime
from pyngrok import ngrok, conf, process
from neuromeka_indycare.indycare_utils import indy_command
from neuromeka_indycare.indycare_utils import config
from neuromeka_indycare.indycare_utils.mqtt_client import MQTTSession
from multiprocessing.managers import BaseManager
from multiprocessing import Process, Event, Queue, Manager
from logging.handlers import RotatingFileHandler
from os import path, remove, stat, wait


# path for logs and videos
BASE_DIR = Path(__file__).resolve().parent
ZIP_FILE_DIR_PATH = "/home/user/release/IndyCARELog"
PROGRAM_LOG_DIR_PATH = "/home/user/release/IndyCARELog/logs/"
VIDEO_FILE_DIR_PATH = "/home/user/release/IndyCARELog/videos/"
LOG_FILE_DIR_PATH = "/home/user/release/IndyDeployment/LogData/Server/"
DALIWORKS_DIR_PATH = BASE_DIR / "daliworks_software"


CONTY_DEFAULT_PORT = 20131
PROCESS_CHECKING_INTERVAL = 300  # (seconds)
TIMER_RECONNECT_TO_CAMERA = 10  # (seconds)
TIMER_RECONNECT_TO_NGROK = 10  # (seconds)
TIMER_WAIT_FOR_SERVER = 10  # (seconds) not smaller than 7s
DALIWORKS_DOMAIN_TIMEOUT = 30  # (seconds)

# create log folder if not exist
Path(ZIP_FILE_DIR_PATH).mkdir(parents=True, exist_ok=True)
Path(VIDEO_FILE_DIR_PATH).mkdir(parents=True, exist_ok=True)
Path(PROGRAM_LOG_DIR_PATH).mkdir(parents=True, exist_ok=True)


# Logger function: create and write log
def _logger(logger_name):
    _log_path = path.join(PROGRAM_LOG_DIR_PATH, logger_name)
    _log_max_size = (1 * 1024 * 1024)  # 1MB
    _log_backup_count = 100  # number of log files
    _logging_level = logging.DEBUG
    _log = logging.getLogger(logger_name)
    fileHandler = RotatingFileHandler(filename=_log_path, maxBytes=_log_max_size, backupCount=_log_backup_count)
    formatter = logging.Formatter('[%(levelname)s | %(filename)s:%(lineno)s]\t%(asctime)s\t> %(message)s')
    fileHandler.setFormatter(formatter)
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)
    _log.setLevel(_logging_level)
    _log.addHandler(fileHandler)
    _log.addHandler(streamHandler)


def set_proc_name(newname):
    from ctypes import cdll, byref, create_string_buffer
    libc = cdll.LoadLibrary('libc.so.6')
    buff = create_string_buffer(len(newname) + 1)
    buff.value = newname
    libc.prctl(15, byref(buff), 0, 0, 0)


set_proc_name(b'IndyCAREReport')


# Template for all process
class ProcessTemplate(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def main_process(self, interval):
        pass

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def is_running(self):
        pass

    @abstractmethod
    def terminate(self):
        pass


# Shared object class
class MqttManager(BaseManager): pass


class Reporter(ProcessTemplate, ABC):
    """
     - get data from robot (IndyDCP3 for v3, IndyDCP for v2)
     - publish to mqtt broker
     - notify when event happen (zip file, on/off camera)
    """
    def __init__(self, _zip_log_event, _close_recorder_process):
        """ Logger """
        _logger("Reporter_log")
        self.Reporter_log = logging.getLogger("Reporter_log")

        """ Configurations """
        self._config = config.load_config()
        self._config[config.RTSP] = False

        """ Robot communication """
        self._dcp = indy_command.IndyCommand(indydcp_version="v3",
                                              joint_dof=self._config[config.CONFIG_KEY_ROBOT_DOF])

        # Shared object
        """ Create and run MQTT session """
        MqttManager.register('MQTT', MQTTSession)
        mqtt_session = MqttManager()
        mqtt_session.start()

        self._subscribe_msg_mqtt = Manager().Queue()
        self._session = mqtt_session.MQTT(
            self._subscribe_msg_mqtt,
            hostname=self._config[config.CONFIG_KEY_MQTT_BROKER_HOSTNAME],
            port=self._config[config.CONFIG_KEY_MQTT_BROKER_PORT],
            # username=self._config[config.CONFIG_KEY_MQTT_USERNAME],
            username=f"{self._config[config.CONFIG_KEY_MQTT_DEVICE_ID]}:{self._config[config.CONFIG_KEY_MQTT_USERNAME]}",
            password=self._config[config.CONFIG_KEY_MQTT_PASSWORD]
        )

        """ set config for ngrok """
        try:
            self._pyngrok_config = conf.PyngrokConfig(
                ngrok_path="/usr/bin/ngrok",
                # config_path="/home/user/.ngrok2/ngrok.yml",
                config_path="/root/.config/ngrok/ngrok.yml",
                # auth_token="24rZk.....",
                region=self._config[config.NGROK_REGION]
          )
            conf.set_default(self._pyngrok_config)
        except:
            print("Unable to configure ngrok line 266")

        self._broker_connect_enable = Event()

        self._zip_log_event = _zip_log_event
        self._close_recorder_process = _close_recorder_process
        reporter_frequency = 5  # Hz
        self._main_process = Process(target=self.main_process, args=((1 / reporter_frequency),))
        self._stop_requested = False
        self._tactTime = [0.0]

    def __connect_to_broker(self):
        """
        Broker?
        """
        try:
            while not self._session.is_connected() and not self._stop_requested:
                self._session.open()
                time.sleep(TIMER_WAIT_FOR_SERVER)
                if not self._session.is_connected():
                    self.Reporter_log.error("CANNOT connect to server, try again later...")
            if not self._stop_requested:
                self.Reporter_log.info("CONNECT MQTT broker success...subscribe")
                self._session.request_subscribe(self._config[config.CONFIG_KEY_MQTT_TOPIC_ATTRIBUTES])
        except Exception as e:
            self.Reporter_log.error("CANNOT connect to MQTT broker...: %s", str(e))
        self._broker_connect_enable.clear()

    def __connect_to_broker_process(self):
        self._broker_connect_enable.set()
        broker_process = Process(target=self.__connect_to_broker)
        broker_process.daemon = True
        broker_process.start()

    def __send_data_to_broker(self, data=None):
        try:
            if not self._broker_connect_enable.is_set():
                if self._session.is_connected():
                    self._session.publish(
                        topic=self._config[config.CONFIG_KEY_MQTT_TOPIC_TELEMETRY],
                        data=data
                    )
                    self.Reporter_log.info("DONE send data to server...")
                else:
                    # reconnect to server
                    self.Reporter_log.error("SERVER is not connected try to reconnect...")
                    self.__connect_to_broker_process()
        except Exception as e:
            self.Reporter_log.error("CANNOT send data to server...")
            self.Reporter_log.error("EXCEPTION MESSAGE: %s", str(e))

    def __connect_to_ngrok(self):
        try:
            self._ngrok_connection = ngrok.connect(CONTY_DEFAULT_PORT, "tcp")  # port, method
            self.Reporter_log.info("CONNECT ngrok server success...")
            self.Reporter_log.info("ADDRESS of ngrok server: %s", self._ngrok_connection.public_url)
        except Exception as e:
            self.Reporter_log.error("ngrok connection fail", str(e))

    @staticmethod
    def __timeout(sig, frm):
        self.Reporter_log.error("Reporter timeout error")
        raise Exception("Reporter timeout error")

    def main_process(self, interval):
        """ Check ngrok connection is valid """
        self.__connect_to_ngrok()

        """ Send data to MQTT broker """
        self.__connect_to_broker_process()
        time.sleep(TIMER_WAIT_FOR_SERVER * 1.5)
        # start_time = time.time()
        pre_timeNgrokConnection = 0
        pre_timeTransmitPeriod = 0
        pre_opState = ""
        msg_tactTime = ""
        Daliworks_urls = []
        pre_violationType = -1
        pre_conty_remote_connected = 0

        config_data = self._config[config.CONFIG_KEY_INDYCARE_TACTTIME_ADDR]
        value_prev = 0.0

        while not self._stop_requested:
            try:
                """ Conty communication (Tact Time)                 
                - return tactTime                                  
                """
                var = self._dcp.get_float_variable_data()
                for i, addr in enumerate(config_data):
                    # find value(tact Time) of specific addr(config_data)
                    value = next((item['value'] for item in var if item['addr'] == addr), None)
                    # self.Reporter_log.info(f'Value for addr {addr}: {value}')
                    self._tactTime[i] = value
                    if self._tactTime[i] and not value_prev:
                        if self._tactTime[i] > 0.0:
                            data = {
                                "tactTime": self._tactTime[i]
                            }
                            self.__send_data_to_broker(data)
                            self.Reporter_log.info(f"DATA: {data}")
                    value_prev = self._tactTime[i]

                """ Send Operation state                
                - get operation state for event condition
                - READY | SERVO_OFF | VIOLATE | RECOVER | IDLE | MOVING | TEACHING | COLLISION                                 
                """
                opState = ""

                try:
                    opState_data = self._dcp.get_robot_status()
                    program_state = self._dcp.get_program_state()
                    if opState_data["ready"] and program_state["stop"]:
                        opState = "IDLE"
                    if (opState_data["ready"] or opState_data["busy"]) and program_state["running"]:
                        opState = "MOVING"
                    # if not all motor are on => servo off
                    motor_state = self._dcp.get_motor_state()
                    if not all(motor_state):
                        opState = "SERVO_OFF"
                    if opState_data["direct_teaching"]:
                        opState = "TEACHING"
                    if opState_data["error"] or opState_data["emergency"]:
                        opState = "VIOLATE"
                    if opState_data["collision"]:
                        opState = "COLLISION"
                    if opState_data["resetting"]:
                        opState = "RECOVER"
                except Exception as e:
                    opState = "DCP_ERROR"
                    self.Reporter_log.error("OPERATION STATE error: %s", str(e))

                if opState != pre_opState:
                    data = {
                        "opState": opState,  # ",".join(opState_data)
                    }
                    self.__send_data_to_broker(data)
                    self.Reporter_log.info(f"Operation state data: {data}")
                    if opState == "VIOLATE" or opState == "COLLISION":
                        self._zip_log_event.set()
                    pre_opState = opState

                """ Send Violation type                
                -                                  
                """
                try:
                    violationType = self._dcp.get_last_emergency_info()['error_code']
                    violationStr = self._dcp.get_last_emergency_info()['violation_str']
                except Exception as e:
                    violationType = 0
                    self.Reporter_log.error("VIOLATION TYPE error. Please check if dcp3 exist.")
                    self.Reporter_log.error("EXCEPTION MESSAGE: %s", str(e), traceback.format_exc())

                if violationType != pre_violationType:
                    data = {
                        "violationType": violationType
                        # # EventList[self._dcp.get_last_emergency_info()['error_code']],
                    }
                    str_data = {
                        "violationStr": violationStr
                    }
                    self.__send_data_to_broker(data)
                    self.Reporter_log.info(f"DATA: {str_data}")
                    pre_violationType = violationType

                # COMMON DATA ===============================================================================
                # check pyngrok process
                """ check ngrok using pyngrok process """
                ngrok_ip = ""
                conty_remote_connected = 0
                try:
                    if process.is_process_running(self._pyngrok_config.ngrok_path):
                        ngrok_ip = self._ngrok_connection.public_url.replace('tcp://', '')
                        self._ngrok_connection.refresh_metrics()
                        metrics_json = json.dumps(self._ngrok_connection.metrics)
                        conty_remote_connected = json.loads(metrics_json)["conns"]["gauge"]
                        # print(conty_remote_connected)
                    elif (time.time() - pre_timeNgrokConnection) >= TIMER_RECONNECT_TO_NGROK:
                        self.Reporter_log.error("NGROK is not running...")
                        pre_timeNgrokConnection = time.time()
                        self.__connect_to_ngrok()
                except:
                    print("NGROK is not running line 474")

                if (time.time() - pre_timeTransmitPeriod) >= \
                        self._config[config.CONFIG_KEY_MQTT_TRANSMIT_PERIOD] or \
                        conty_remote_connected != pre_conty_remote_connected:

                    try:
                        # Prepare runningTime and temperatures data
                        runningTime = self._dcp.get_rt_data()
                        temperatures_np = self._dcp.get_temperature_data()
                        data = {
                            # "indycare": str(self._config[config.CONFIG_KEY_INDYCARE_VERSION]),
                            "timestamp": time.time(),
                            "time": runningTime['time'],  # runningTime['time'],
                            "q": ",".join(map(str, self._dcp.get_joint_pos())),
                            "qdot": ",".join(map(str, self._dcp.get_joint_vel())),
                            "p": ",".join(map(str, self._dcp.get_task_pos())),
                            "pdot": ",".join(map(str, self._dcp.get_task_vel())),
                            "tau": ",".join(map(str, self._dcp.get_actual_torque())),
                            "edot": ",".join(map(str, self._dcp.get_joint_vel_ref())),
                            "evel": ",".join(map(str, self._dcp.get_task_vel_ref())),
                            "extau": ",".join(map(str, self._dcp.get_external_torque())),
                            "qddot": ",".join(map(str, self._dcp.get_joint_acc())),
                            "pddot": ",".join(map(str, self._dcp.get_task_acc())),
                            "extaudot": ",".join(map(str, self._dcp.get_torque_ref())), # NOT IN DCP3
                            # "overruns": self._dcp.get_overruns(), # NOT IN DCP3
                            "overruns": 0, # NOT IN DCP3
                            # "computePeriod": runningTime['compute_time'], # NOT IN DCP3
                            # "computePeriodMax": runningTime['max_compute_time'], # NOT IN DCP3
                            "computePeriod": 0, # NOT IN DCP3
                            "computePeriodMax": 0, # NOT IN DCP3
                            "qd": ",".join(map(str, self._dcp.get_curr_joint_pos())),
                            "qdotd": ",".join(map(str, self._dcp.get_joint_vel_des())),
                            "pd": ",".join(map(str, self._dcp.get_curr_task_pos())),
                            "pdotd": ",".join(map(str, self._dcp.get_task_vel_des())),
                            "qddotd": ",".join(map(str, self._dcp.get_joint_acc_des())),
                            "pddotd": ",".join(map(str, self._dcp.get_task_acc_des())),
                            "sensitiveLevel": self._dcp.get_collision_level(),
                            "tempMotor": ",".join(map(str, temperatures_np)),
                            "ngrokIp": ngrok_ip,
                            "ngrokIsContyConnected": conty_remote_connected,
                            "fileURL": Daliworks_urls[0] if Daliworks_urls else "",
                            "terminalURL": Daliworks_urls[1] if Daliworks_urls else "",
                            "camURL": Daliworks_urls[2] if Daliworks_urls else ""
                        }
                    except Exception as e:
                        data = {
                            "timestamp": time.time(),
                            "time": 0,
                            "q": "0",
                            "qdot": "0",
                            "p": "0",
                            "pdot": "0",
                            "tau": "0",
                            "edot": "0",
                            "evel": "0",
                            "extau": "0",
                            "qddot": "0",
                            "pddot": "0",
                            "extaudot": "0",
                            "overruns": 0,
                            "computePeriod": 0,
                            "computePeriodMax": 0,
                            "qd": "0",
                            "qdotd": "0",
                            "pd": "0",
                            "pdotd": "0",
                            "qddotd": "0",
                            "pddotd": "0",
                            "sensitiveLevel": 0,
                            "tempMotor": "0",
                            "ngrokIp": ngrok_ip,
                            "ngrokIsContyConnected": conty_remote_connected,
                            "fileURL": Daliworks_urls[0] if Daliworks_urls else "",
                            "terminalURL": Daliworks_urls[1] if Daliworks_urls else "",
                            "camURL": Daliworks_urls[2] if Daliworks_urls else ""
                        }
                        self.Reporter_log.error("COMMON DATA error. Please check if dcp3 exist.")
                        self.Reporter_log.error("EXCEPTION MESSAGE: %s", str(e))

                    self.__send_data_to_broker(data)
                    self.Reporter_log.info(f"DATA: {data}")
                    pre_timeTransmitPeriod = time.time()
                    pre_conty_remote_connected = conty_remote_connected

                # PROCESS RECEIVED MESSAGES =======================================================================
                if not self._subscribe_msg_mqtt.empty():
                    # {"SET_REMOTE": "true"}
                    json_data = self._subscribe_msg_mqtt.get()
                    msg = json.loads(json_data)
                    self.Reporter_log.info("GOT msg from server: %s", msg)
                    if msg["SET_REMOTE"] == "true" and not Daliworks_urls:  # check if url list is empty
                        try:
                            self.Reporter_log.info("RECEIVED turn on REMOTE from server...")
                            self.Reporter_log.info("TURN ON Daliworks domain...")
                            output = subprocess.Popen(
                                DALIWORKS_DIR_PATH + "domain.on.sh",
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)

                            # set alarm if domain not work
                            self.Reporter_log.info("ENABLE timeout for Daliworks's domain")
                            signal.signal(signal.SIGALRM, self.__timeout)
                            signal.alarm(DALIWORKS_DOMAIN_TIMEOUT)

                            line1 = output.stdout.readline().decode("utf-8")
                            line2 = output.stdout.readline().decode("utf-8")
                            line3 = output.stdout.readline().decode("utf-8")

                            # if it is working, disable alarm
                            self.Reporter_log.info("Daliworks's domain start successful")
                            signal.alarm(0)

                            self.Reporter_log.info("GET Daliworks url_1: %s", line1)
                            self.Reporter_log.info("GET Daliworks url_2: %s", line2)
                            self.Reporter_log.info("GET Daliworks url_3: %s", line3)

                            line1_url = (re.search("(?P<url>https?://[^\s]+)", line1).group("url"))
                            line2_url = (re.search("(?P<url>https?://[^\s]+)", line2).group("url"))
                            line3_url = (re.search("(?P<url>https?://[^\s]+)", line3).group("url"))

                            Daliworks_urls.append(line1_url)
                            Daliworks_urls.append(line2_url)
                            Daliworks_urls.append(line3_url)
                            # print(Daliworks_urls)
                            subprocess.Popen(DALIWORKS_DIR_PATH + "service.on.sh",
                                             stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
                            self.Reporter_log.info("NOTIFY camera process to disconnect...")
                            self._close_recorder_process.set()

                        except Exception as e:
                            self.Reporter_log.error("CANNOT turn on Daliworks domain")
                            self.Reporter_log.error("EXCEPTION MESSAGE: %s", str(e))
                            Daliworks_urls = []
                            self._close_recorder_process.clear()
                            subprocess.Popen(DALIWORKS_DIR_PATH + "kill_process.sh", shell=True)
                            time.sleep(2)

                    elif msg["SET_REMOTE"] == "false" and Daliworks_urls:  # check if url list is NOT empty
                        self.Reporter_log.info("RECEIVED turn off REMOTE from server...")
                        subprocess.Popen(DALIWORKS_DIR_PATH + "kill_process.sh")
                        # subprocess.Popen("daliworks_software/turn_off_camera.sh", cwd=pathlib.Path.cwd())
                        time.sleep(3)
                        self._close_recorder_process.clear()
                        self.Reporter_log.info("RECONNECT to camera -- server-cmd...")
                        Daliworks_urls = []
                        # print("self._close_recorder_process.set() self._close_recorder_process.set()")

                time.sleep(interval)

            except Exception as e:
                self.Reporter_log.critical("Reporter error: %s", str(e))
                self._stop_requested = True

        try:
            process.kill_process(self._pyngrok_config.ngrok_path)
        except:
            print("error during kill process line 639")
        # self._session.close()
        time.sleep(1)
        self.Reporter_log.info("REPORTER TERMINATED === === === === === === === === === === === ===")
        self.Reporter_log = None

    def run(self):
        self.Reporter_log.info("REPORTER START === === === === === === === === === === === ===")
        self._main_process.start()

    def is_running(self):
        return self._main_process.is_alive()

    def terminate(self):
        self.Reporter_log.info("REPORTER WILL STOP === === === === === === === === === === === ===")
        self._stop_requested = True


class Recorder(ProcessTemplate, ABC):
    """
    Recorder:
        - capture images from camera
        - video storage and management
        - create zip files
        - turn on/off camera
    """
    def __init__(self, _zip_log_event, _close_recorder_process):
        _logger("Recorder_log")
        self.Recorder_log = logging.getLogger("Recorder_log")

        self._zip_log_event = _zip_log_event
        self._close_recorder_process = _close_recorder_process
        self._capture = None
        self._stop_requested = False
        self._config = config.load_config()
        self._frame_width = self._config[config.STREAMER_KEY_FRAME_WIDTH]
        self._frame_height = self._config[config.STREAMER_KEY_FRAME_HEIGHT]

        # interval = 1/(self._config[Config.STREAMER_KEY_VIDEO_FPS] * 10)
        recorder_frequency = 200  # Hz
        self._main_process = Process(target=self.main_process, args=((1 / recorder_frequency),))

    def __get_file_list(self, folder_dir, file_type, number_of_files=1):
        try:
            files = glob.glob(folder_dir + file_type)
            if len(files) == 0:
                return None
            elif number_of_files == 1:
                return max(files, key=path.getmtime)  # getctime
            else:
                return files
        except Exception as e:
            self.Recorder_log.error("CANNOT get file list...")
            self.Recorder_log.error("EXCEPTION MESSAGE: %s", str(e))
            return None

    # Remove old videos => follow config
    def __videos_manager(self):
        try:
            file_list = self.__get_file_list(VIDEO_FILE_DIR_PATH, "*.mp4", 0)  # 0 = all files
            for filename in sorted(file_list, key=path.getmtime)[
                            :-self._config[config.STREAMER_KEY_NUMBERS_OF_VIDEO]]:
                self.Recorder_log.info("REMOVE old video: %s", filename)
                remove(filename)
        except Exception as e:
            self.Recorder_log.error("CANNOT remove old video...")
            self.Recorder_log.error("EXCEPTION MESSAGE: %s", str(e))
            pass

    # Remove old zips => follow config
    def __zips_manager_by_capacity(self):
        try:
            # Get all files name
            file_list = self.__get_file_list(ZIP_FILE_DIR_PATH, "IndyCare_log*.zip", 0)  # 0 = all files
            if file_list is None:
                # self.Recorder_log.info("There is no zip files")
                return

            # Sort file name ascending (date modify)
            file_list.sort(key=path.getmtime, reverse=False)  # ascending
            # Remove the oldest file if exceed capacity
            for filename in file_list[:-1]:  # if exceed storage, remove zips but keep newest
                total, used, free = shutil.disk_usage("/")
                # free_in_GB = (free // (2 ** 30))
                remain_storage = (free * 100) / total
                # print("remain_storage: ", remain_storage)
                # print("filename: ", filename)
                if remain_storage < float(self._config[config.STREAMER_KEY_LIMIT_CAPACITY]):
                    self.Recorder_log.info("REMAIN STORAGE %f", remain_storage)
                    self.Recorder_log.info("REMOVE old zip [limit capacity]: %s", filename)
                    remove(filename)

            # Sort file name descending (date modify)
            # file_list.sort(key=path.getmtime, reverse=True)
            # sum_capacity = 0
            # Remove the oldest file if exceed capacity
            # for filename in file_list:
            #     if (sum_capacity / (1024 * 1024)) < self._config[config.STREAMER_KEY_LIMIT_CAPACITY]:
            #         sum_capacity = sum_capacity + stat(filename).st_size
            #     else:
            #         self.Recorder_log.info("REMOVE old zip [limit capacity]: %s", filename)
            #         remove(filename)
            # self.Recorder_log.info("SIZE of all zip files (Mb): %d", sum_capacity / (1024 * 1024))

        except Exception as e:
            self.Recorder_log.error("CANNOT remove zip files by capacity...")
            self.Recorder_log.error("EXCEPTION MESSAGE: %s", str(e))
            pass

    def __zips_manager_by_date(self):
        try:
            # Get all files name
            file_list = self.__get_file_list(ZIP_FILE_DIR_PATH, "IndyCare_log*.zip", 0)  # 0 = all files
            if file_list is None:
                # self.Recorder_log.info("There is no zip files")
                return

            # Remove the old file if exceed retention day
            now = time.time()
            for filename in file_list:
                if (now - stat(filename).st_mtime) > \
                        (self._config[config.STREAMER_KEY_RETENTION_PERIOD] * 86400):
                    self.Recorder_log.info("REMOVE old zip [retention period]: %s", filename)
                    remove(filename)
        except Exception as e:
            self.Recorder_log.error("CANNOT remove zip files by period...")
            self.Recorder_log.error("EXCEPTION MESSAGE: %s", str(e))
            pass

    def __zip_log_files(self, video_list):
        try:
            # Get file list
            # file_list = [self.__get_file_list(LOG_FILE_DIR_PATH, "EventLog*.txt"),
            #              self.__get_file_list(LOG_FILE_DIR_PATH, "Log*.txt"),
            #              self.__get_file_list(LOG_FILE_DIR_PATH, "SafetyStopLog*.csv"),
            #              self.__get_file_list(LOG_FILE_DIR_PATH, "EventBuffLog*.csv")]
            file_list = [self.__get_file_list(LOG_FILE_DIR_PATH, "*.log")]
            if video_list is not None:
                file_list.extend(video_list)
            self.Recorder_log.info("FILES add to zip: %s", file_list)
            # Create a ZipFile Object
            # Datetime object containing current date and time
            now = datetime.now()
            zip_name = ZIP_FILE_DIR_PATH + now.strftime("IndyCare_log-%b_%d_%Y-%H_%M_%S.zip")
            with ZipFile(zip_name, "w") as zip_data:
                # Add multiple files to the zip
                # print("zip: ", zip_name)
                for file in file_list:
                    if file is not None:
                        try:
                            zip_data.write(file, path.basename(file))
                        except:
                            self.Recorder_log.error("CANNOT copy file to zip: %s", file)
                            pass
            self.Recorder_log.info("DONE zip log files: %s", zip_name)
            self.__zips_manager_by_capacity()
            self.__zips_manager_by_date()
        except Exception as e:
            self.Recorder_log.error("ERROR zip log files...")
            self.Recorder_log.error("EXCEPTION MESSAGE: %s", str(e))

    def __connect_to_camera(self):
        # cam = cv2.CaptureVideo("/dev/video0")
        if not self._config[config.RTSP]:
            camera_list = [-1, 0, 1, 2]
            self.Recorder_log.info("WEB CAMERA set...")
        else:
            camera_list = [self._config[config.RTSP]]
            self.Recorder_log.info("IP CAMERA set...")

        try:
            # Start capture image
            for i in range(len(camera_list)):
                self._capture = cv2.VideoCapture(camera_list[i])
                if self._capture.isOpened():
                    # set capture jpeg
                    # if not camera will work with yuyv422 => low fps/resolution
                    self._capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
                    self._capture.set(cv2.CAP_PROP_FPS, self._config[config.STREAMER_KEY_VIDEO_FPS])
                    if not self._config[config.RTSP]:
                        self._frame_width = self._config[config.STREAMER_KEY_FRAME_WIDTH]
                        self._frame_height = self._config[config.STREAMER_KEY_FRAME_HEIGHT]
                    else:
                        self._frame_width = int(self._capture.get(cv2.CAP_PROP_FRAME_WIDTH))
                        self._frame_height = int(self._capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
                        self.Recorder_log.info(f"frame_size: {self._frame_width} X {self._frame_height}")
                    self._capture.set(cv2.CAP_PROP_FRAME_WIDTH, self._frame_width)
                    self._capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self._frame_height)
                    self.Recorder_log.info(f"CAMERA link: {camera_list[i]}")
                    self.Recorder_log.info("CAMERA connected...")
                    return True
                elif i == len(camera_list) - 1:
                    raise IOError("Cannot open camera")

        except Exception as e:
            self.Recorder_log.error("NO camera available..." + str(traceback.format_exc()))
            self.Recorder_log.error("EXCEPTION MESSAGE: %s", str(e))
            return False

    def main_process(self, interval):
        """
            To get image from camera
        """
        if not self.__connect_to_camera():
            self.Recorder_log.error("CANNOT connect to camera, try again later...")

        codec = cv2.VideoWriter_fourcc(*'mp4v')  # *'xdiv' *'mp4v'
        new_record = True
        video_list = None
        output_video = None
        start_time = 0
        camera_reconnect_timer = 0
        while not self._stop_requested:
            try:
                status, frame = self._capture.read()
                if status:
                    if new_record:
                        # Datetime object containing current date and time
                        now = datetime.now()
                        # mm/dd/YY H:M:S
                        # video_name = now.strftime("%b_%d_%Y-%H_%M_%S.mp4")
                        video_name = VIDEO_FILE_DIR_PATH + now.strftime("%b_%d_%Y-%H_%M_%S.mp4")
                        output_video = cv2.VideoWriter(video_name, codec,
                                                       self._config[config.STREAMER_KEY_VIDEO_FPS],
                                                       (self._frame_width, self._frame_height))

                        # print("Start record video: ", video_name)
                        self.Recorder_log.info("START record new video: %s", video_name)
                        start_time = time.time()
                        new_record = False

                    if time.time() - start_time <= self._config[config.STREAMER_KEY_RECORD_TIME]:
                        output_video.write(frame)
                    else:
                        output_video.release()
                        self.__videos_manager()
                        video_list = self.__get_file_list(VIDEO_FILE_DIR_PATH, "*.mp4", 0)
                        new_record = True
                        self.Recorder_log.info("END record new video")

                    if self._close_recorder_process.is_set():
                        self.Recorder_log.info("DISCONNECT to camera - server command...")
                        output_video.release()
                        video_list = None
                        new_record = True
                        time.sleep(0.5)
                        self._capture.release()
                        while self._capture.isOpened():
                            time.sleep(0.5)
                            self.Recorder_log.info("RELEASING camera...")
                        if not self._config[config.RTSP]:
                            self.Recorder_log.info("TURN ON Daliworks's service with WEB Camera...")
                            subprocess.Popen(DALIWORKS_DIR_PATH + "service_cam.on.sh",
                                             stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
                        else:
                            self.Recorder_log.info("TURN ON Daliworks's service with IP Camera...")
                            subprocess.Popen(DALIWORKS_DIR_PATH + "service_cam_rtsp.on.sh",
                                             stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)

                        # self.Recorder_log.info("CURRENT DIRECTORY: %s", pathlib.Path.cwd())
                        # subprocess.Popen("daliworks_software/turn_on_camera.sh", cwd=pathlib.Path.cwd())

                elif not self._close_recorder_process.is_set():
                    if time.time() - camera_reconnect_timer >= TIMER_RECONNECT_TO_CAMERA:
                        if not self.__connect_to_camera():
                            self.Recorder_log.error("CANNOT connect to camera, try again later...")
                        camera_reconnect_timer = time.time()

                if self._zip_log_event.is_set() and new_record:
                    try:
                        self.Recorder_log.info("AN EVENT OCCURRED: collect log files and create zip...")
                        zip_process = Process(target=self.__zip_log_files, args=(video_list,))
                        zip_process.daemon = True
                        zip_process.start()
                        self._zip_log_event.clear()
                    except Exception as e:
                        self.Recorder_log.error("ERROR when handle event...")
                        self.Recorder_log.error("EXCEPTION MESSAGE: %s", str(e))

                # if not use camera => reduce interval
                time.sleep(interval * 100) if self._close_recorder_process.is_set() else time.sleep(interval)

            except Exception as e:
                self.Recorder_log.critical("SOMETHING HAPPEN IN CAMERA PROCESS. PROCESS WILL CLOSE. PLEASE CHECK.")
                self.Recorder_log.critical("EXCEPTION MESSAGE: %s", str(e))
                self._stop_requested = True

        output_video.release()
        self._capture.release()
        self.Recorder_log.info("RECORDER Terminate")
        self.Recorder_log = None

    def run(self):
        self.Recorder_log.info("RECORDER Start")
        self._main_process.start()

    def is_running(self):
        return self._main_process.is_alive()

    def terminate(self):
        self.Recorder_log.info("RECORDER STOP")
        self._stop_requested = True


def signal_handler(signum, frame):
    reporter_process.terminate()
    recorder_process.terminate()
    global interrupted
    interrupted = True

def handleSIGCHLD(sig, fra):
    pid, exitcode = wait()


if __name__ == '__main__':
    """ Main logger """
    _logger("Main_log")
    Main_log = logging.getLogger("Main_log")

    """ define queue and event use in processes """
    msg_queue = Queue()
    zip_log_event = Event()
    shutdown_recorder_process = Event()

    """ Create processes """
    reporter_process = Reporter(zip_log_event, shutdown_recorder_process)
    recorder_process = Recorder(zip_log_event, shutdown_recorder_process)

    """ define signal handler """
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGCHLD, handleSIGCHLD)

    ## TODO: Wait for Indy turn on
    # TO-DO:

    # start processes
    Main_log.info("Start all processes")
    time.sleep(1)
    reporter_process.run()
    time.sleep(1)
    recorder_process.run()

    """ main loop to check all processes """
    interrupted = False
    while not interrupted:
        if reporter_process.is_running():
            Main_log.info("REPORTER is running...")
        else:
            Main_log.info("REPORTER is stop...")

        if recorder_process.is_running():
            Main_log.info("RECORDER is running...")
        else:
            Main_log.info("RECORDER is stop...")

        for i in range(PROCESS_CHECKING_INTERVAL):
            time.sleep(1)
            if interrupted:
                break

    # end program
    Main_log.info("Stop all processes")
    Main_log = None
