import atexit
import copy
import json
import logging
import pathlib
import pickle
import shutil
import threading
import time
from datetime import datetime

import cv2 as cv
from flask import Flask, Response, jsonify, make_response, request
from waitress import serve

from camera_management import SETTINGS
from camera_management.dataclasses import general_dataclasses
from camera_management.dataclasses.camera_dataclasses import ArucoSettings, CameraDescription, PreprocessingSettings
from camera_management.definitions import ReturnFlags
from camera_management.tools._image_processor import ImageProcessor
from camera_management.tools.config_tools import _rotate_file_bkup, check_preprocessing, write_configuration_file

logger = logging.getLogger("camera_management.camera_interface")


class CameraApplicationSettingsError(Exception):
    pass


class CameraApplication(threading.Thread):  # DONT change to Process, since it does not work on macOS
    """
    Handles the incoming calls to set camera/preprocessing settings and serves the camera stream.
    """

    def __init__(self, port: int, description_path: None | pathlib.Path = None):
        super().__init__(name=f"Camera Interface Port {port}")
        self.description: CameraDescription | None = None
        self.preprocessing_settings = PreprocessingSettings(bw=False, undistort=False, rotate=0, aruco=ArucoSettings())
        self._flask = Flask(__name__)
        self._flask.config["DEBUG"] = True

        self._port = port
        self._status = "OFFLINE"
        self._temp_path = pathlib.Path(__file__).parent / f"temp/configs/{self._port}.json"
        self._temp_path.parent.mkdir(parents=True, exist_ok=True)

        if description_path is not None:
            _rotate_file_bkup(self._temp_path, 4)
            shutil.copy(description_path, self._temp_path)

        self._wait_for_config()
        self._preprocessing_thread = ImageProcessor(cam_param=self.description, stop_event=None)
        self._preprocessing_thread.start()
        self._wait_for_preprocessing_thread()
        self._last_frame = general_dataclasses.ImageProcessorData.generate_dummy_data((1920, 1080), 3)

        @atexit.register
        def __exit():
            self._preprocessing_thread.stop()

        @self._flask.get("/data/imageProcessor")
        def img_processor():
            """
            Flask getter for the actual image data.
            """

            data: general_dataclasses.ImageProcessorData = self._preprocessing_thread.image_data
            data.add_record("camera-interface")
            if data.image is None:
                data = self._last_frame
            else:
                self._last_frame = copy.copy(data)
            data.complete_last_record("camera-interface")

            response = make_response(pickle.dumps(data))
            response.headers.set("content-type", "application/octet-stream")
            response.headers.set("digest", "TODO")
            response.headers.set("last_change", f"{self._preprocessing_thread._last_change}")

            return response

        @self._flask.get("/data/processed")
        def get_processed():
            """
            Flask getter for data from image measurement operators.
            """
            data: general_dataclasses.MeasurementData = self._preprocessing_thread.measure_data
            response = make_response(pickle.dumps(data))
            response.headers.set("content-type", "application/octet-stream")
            response.headers.set("digest", "TODO")
            response.headers.set("last_change", f"{self._preprocessing_thread._last_change}")

            return response

        @self._flask.get("/status")
        def get_status():
            """
            Flask getter for the camera status.
            """
            return jsonify({"status": self._status})

        @self._flask.route("/settings/pre_processing", methods=["GET", "POST"])
        def set_pre_processing_settings():
            """
            Flask route to set and get preprocessing settings.
            """
            if request.method == "POST":
                status, self.preprocessing_settings = check_preprocessing(request.json, self.preprocessing_settings)
                if status != "SUCCESS":
                    return status, 400
                self.description.pre_processing = self.preprocessing_settings

                if self.description.pre_processing.undistort and not self.description.calibration.available:
                    self.description.pre_processing.undistort = False
                    return "Can only undistort image if there are calibration values present. All pre-processing settings were rejected.", 400

                self._pre_processing_setter()
                return jsonify(self.preprocessing_settings.model_dump())

            elif request.method == "GET":
                return jsonify(self.preprocessing_settings.model_dump())
            else:
                return f"Request with method {request.method} was not accepted.", 400

        @self._flask.get("/description")
        def get_description():
            """
            Flask getter for the camera description.
            """
            return jsonify(self.description.model_dump())

        @self._flask.route("/settings/camera", methods=["GET", "POST"])
        def camera_settings():
            """
            Receives http requests and tries to set the values received.
            """

            if request.method == "POST":
                settings = json.loads(request.data)["settings"]
                status, ret = self._preprocessing_thread.set_camera_options(settings[0], settings[1])
                if status == ReturnFlags.error:
                    return Response(f"Error while trying to set {settings[0]}: {ret}", 400)
                self.description.config[settings[0]] = settings[1]
                self.description.debug.last_updated = datetime.today().strftime("%d-%m-%Y %H:%M:%S")
                write_configuration_file(
                    filename=f"{self._port}.json", cam_config_path=self._temp_path.parent.parent, content=self.description.model_dump()
                )

                return Response(
                    f"Tried to set {SETTINGS(settings[0]).name} to {settings[1]}. {SETTINGS(settings[0]).name} got set to {ret[settings[0]]}. "
                )
            elif request.method == "GET":
                settings = int(request.args.get("settings"))
                status, ret = self._preprocessing_thread.get_camera_options(settings)
                if status == ReturnFlags.error:
                    return Response(f"Error while trying to get setting {SETTINGS(settings).name}: Timed out after {ret}s", 400)
                if ret[0] == ReturnFlags.error:
                    return Response(f"Error while trying to get setting {SETTINGS(settings).name}: {ret[1]}", 400)
                return jsonify({SETTINGS(settings).name: ret[1]})
            else:
                return f"Request with method {request.method} was not accepted.", 400

        def _gen_frames():
            while True:
                ret, buffer = cv.imencode(".jpg", self._preprocessing_thread.image_data.image)
                frame = buffer.tobytes()
                yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")  # concat frame one by one and show result

        @self._flask.route("/video_feed")
        def video_feed():
            return Response(_gen_frames(), mimetype="multipart/x-mixed-replace; boundary=frame")

    def _pre_processing_setter(self):
        self._preprocessing_thread.update_description(self.description)
        self.description.debug.last_updated = datetime.today().strftime("%d-%m-%Y %H:%M:%S")
        write_configuration_file(filename=f"{self._port}.json", cam_config_path=self._temp_path.parent.parent, content=self.description.model_dump())

    def _wait_for_config(self):
        """
        If no config is found this function will wait until there is one.
        """
        already_waiting_for_config = False
        while self.description is None:
            try:
                self.description = CameraDescription.model_validate(json.load(open(self._temp_path)))
                logging.info(f"Port {self._port}: Found camera config.")
            except FileNotFoundError:
                if not already_waiting_for_config:
                    logging.warning(f"No config found in {self._temp_path}. Retrying.")
                    already_waiting_for_config = True
            time.sleep(1)

    def _wait_for_preprocessing_thread(self):
        while self._preprocessing_thread.status != "ONLINE":
            time.sleep(0.1)
        return

    def set_general_setting(self, argument: SETTINGS | int, value) -> str:
        """
        Sets the currently configured setting for the chosen argument.

        :param argument: The setting you want to query. Use cv2.CAP_xxx arguments.
        :param val: The value you want to set.
        """
        status, ret = self._preprocessing_thread.set_camera_options(argument, value)
        if status == ReturnFlags.error:
            raise CameraApplicationSettingsError(f"Error while trying to set {argument}: {ret}")
        self.description.config[argument] = value
        self.description.debug.last_updated = datetime.today().strftime("%d-%m-%Y %H:%M:%S")
        write_configuration_file(filename=f"{self._port}.json", cam_config_path=self._temp_path.parent.parent, content=self.description.model_dump())
        logger.info(f"Tried to set {SETTINGS(argument).name} to {value}. {SETTINGS(argument).name} got set to {ret[argument]}. ")

        return f"Tried to set {SETTINGS(argument).name} to {value}. {SETTINGS(argument).name} got set to {ret[argument]}. "

    def get_general_setting(self, argument: SETTINGS | int) -> dict | None:
        """
        Gets the currently configured setting for the chosen argument.

        :param argument: The setting you want to query. Use cv2.CAP_xxx arguments.
        :return: A dict containing the argument and the current value.
        """
        status, ret = self._preprocessing_thread.get_camera_options(argument)
        if status == ReturnFlags.error:
            raise CameraApplicationSettingsError(f"Error while trying to get setting {SETTINGS(argument).name}: Timed out after {ret}s")
        if ret[0] == ReturnFlags.error:
            raise CameraApplicationSettingsError(f"Error while trying to get setting {SETTINGS(argument).name}: {ret[1]}")
        return {SETTINGS(argument).name: ret[1]}

    def fetch_image_data(self):
        """
        Returns the latest camera image.
        """
        data: general_dataclasses.ImageProcessorData = self._preprocessing_thread.image_data
        if data.id == self._last_frame.id:
            data = self._last_frame
        else:
            data.add_record("camera-interface")
            self._last_frame = copy.copy(data)
        data.complete_last_record("camera-interface")
        return data

    def set_pre_processing_settings(self, pre_processing_settings: dict) -> int:
        """
        Sets a pre-processing setting.
        :param pre_processing_settings: A dict containing the setting and the value (e.g.: {'bw': True})
        :return: Success or fail flags
        """
        status, self.preprocessing_settings = check_preprocessing(pre_processing_settings, self.preprocessing_settings)
        if status != "SUCCESS":
            logger.warning(status)
            return ReturnFlags.error
        self.description.pre_processing = self.preprocessing_settings

        if self.description.pre_processing.undistort and not self.description.calibration.available:
            self.description.pre_processing.undistort = False
            logger.warning("Can only undistort image if there are calibration values present. All pre-processing settings were rejected.")
            return ReturnFlags.error

        self._pre_processing_setter()
        return ReturnFlags.success

    def get_pre_processing_settings(self) -> PreprocessingSettings:
        """
        Get the currently set preprocessing settings.

        :return: Currently active pre-processing settings object
        """
        return self.preprocessing_settings

    @property
    def undistort(self) -> bool:
        """
        Distortion setting of the camera stream.

        """
        return self.get_pre_processing_settings().undistort

    @undistort.setter
    def undistort(self, value: bool):
        if not isinstance(value, bool):
            logger.warning(f'{value} is of type {type(value)}. Only boolean values are allowed for "undistort" setting.')
        else:
            self.set_pre_processing_settings({"undistort": value})

    @property
    def bw(self) -> bool:
        """
        Black and white setting of the camera stream.
        """
        return self.get_pre_processing_settings().bw

    @bw.setter
    def bw(self, value: bool):
        if not isinstance(value, bool):
            logger.warning(f'{value} is of type {type(value)}. Only boolean values are allowed for "Black and White" setting.')
        else:
            self.set_pre_processing_settings({"bw": value})

    @property
    def rotate(self) -> int:
        """
        Image rotate setting of the camera stream.

        """
        return self.get_pre_processing_settings().rotate

    @rotate.setter
    def rotate(self, value: int):
        if not isinstance(value, int) or value not in [0, 90, 180, 270]:
            logger.warning(f'{value} is of type {type(value)}. Only int values in [0, 90, 180, 270] are allowed for "rotate" setting.')
        else:
            self.set_pre_processing_settings({"rotate": value})

    def run(self):
        """
        Run the server.
        """
        self._status = "ONLINE"
        serve(self._flask, host="0.0.0.0", port=self._port)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Start a Camera Application.")
    parser.add_argument("port", metavar="p", type=int, help="port for the camera application")
    args = parser.parse_args()

    cam_app = CameraApplication(args.port)
    cam_app.start()
