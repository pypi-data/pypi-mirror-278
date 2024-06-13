import atexit
import json
import os
import pathlib
import signal
import subprocess
import sys
import threading
import time

import requests
import tabulate
from flask import Flask, jsonify, render_template, request
from waitress import serve

from camera_management.dataclasses.camera_dataclasses import CameraDescription
from camera_management.dataclasses.general_dataclasses import CamStatus, VideoDevice
from camera_management.definitions import _DescriptionModes
from camera_management.tools.config_tools import check_config, write_configuration_file
from camera_management.tools.create_description import get_descriptions
from camera_management.tools.system_analyzer import get_connected_cams


class ManagerApp(threading.Thread):
    """
    This is the main backend class.

    It tries to connect to all physically connected camera devices and creates sockets for each device.
    This class runs on port 8090. Each socket for each camera runs on the nextmost port (8091+).
    """

    def __init__(self, path_to_descriptions: pathlib.Path, autostart: bool = True, choose_cameras=False, port=8090, host="0.0.0.0"):
        """
        This is the main backend class.

        It tries to connect to all physically connected camera devices and creates sockets for each device.
        This class runs on port 8090. Each socket for each camera runs on the nextmost port (8091+).

        :param path_to_descriptions: The path to the configs of the camera you want to use.
        :param autostart: If set to true the manager will automatically start sockets for all cameras that are configured (meaning: all cameras it finds a config file for)
        :param choose_cameras: If set to true the manager will ask which cameras you want to start.
        """
        super().__init__(name="Manager")

        self._flask = Flask(__name__)
        self._subprocess_dict = {}
        self._port = port
        self._host = host
        self._path = path_to_descriptions
        self._configs = {}
        self._chosen_cameras = None
        self._cam_config_path = pathlib.Path(__file__).parent.parent / "camera_app/temp/"
        self._cam_config_path.mkdir(parents=True, exist_ok=True)
        (self._cam_config_path / "configs").mkdir(parents=True, exist_ok=True)

        self.cam_status = []
        self.available_cameras = None

        if autostart and choose_cameras:
            raise ValueError("You can not use autostart and chose_cameras in conjunction.")

        if not autostart:
            if choose_cameras:
                self.available_cameras = self._get_video_device()
            else:
                while self.available_cameras is None:
                    time.sleep(1)
        else:
            self.available_cameras = get_connected_cams()

        @atexit.register
        def __exit():
            for key, value in self._subprocess_dict.items():
                os.kill(value.pid, signal.SIGTERM)

        @self._flask.get("/info")
        def get_camera_info():
            return jsonify(self.cam_status)

        @self._flask.get("/config")
        def get_cam_config():
            port = request.args.get("port", default=None, type=int)
            return jsonify(self._configs[port])

        @self._flask.get("/")
        def index():
            """
            Start page.
            """
            return render_template("index.html")

        @self._flask.get("/available_cams")
        def available_cams():
            """
            Get available cams.
            """
            cams = get_connected_cams()
            return jsonify([cam.to_dict() for cam in cams])

    def _wait_for_interface(self, port: int, timeout=10) -> bool:
        start = time.time()
        while time.time() - start < timeout:
            try:
                online_state = requests.get(f"http://{self._host}:{str(port)}/status").json()
            except requests.ConnectionError:
                time.sleep(0.1)
                continue
            return online_state["status"] == "ONLINE"
        return False

    def _start_cam(self, config, port_index: int, cam: VideoDevice, status: CamStatus, mode: str) -> int:
        port = self._port + port_index
        port_index += 1

        if mode == _DescriptionModes.individual:
            self._configs[port] = {"CONFIG TYPE": None, "CONFIG MODEL": config}
            status.CALIBRATION_AVAILABLE = True
        elif mode == _DescriptionModes.type:
            self._configs[port] = {"CONFIG TYPE": config, "CONFIG MODEL": None}
            status.CALIBRATION_AVAILABLE = config.calibration.available

        config.information.device = cam
        write_configuration_file(filename=f"{port}.json", cam_config_path=self._cam_config_path, content=config.model_dump())
        self._subprocess_dict[port] = subprocess.Popen(
            [sys.executable, f"{pathlib.Path(__file__).parent.parent / 'camera_app/camera_interface.py'}", f"{port}"]
        )
        status.CONFIG_INDIVIDUAL = True
        status.PORT = port
        status.PORT_ACTIVE = self._wait_for_interface(port)
        self.cam_status.append(status)

        return port_index

    def _prepare_cam_descriptions(self):
        configs = get_descriptions(self._path)
        ignored_configs = []
        i = 1

        for cam in self.available_cameras:
            status = CamStatus()
            status.CAM_TYPE = cam.product

            for config in configs:
                if config in ignored_configs:
                    continue
                with open(config) as cfg:
                    json_cfg = json.load(cfg)

                json_cfg = check_config(json_cfg, config_path=config)

                if json_cfg is None:
                    ignored_configs.append(config)
                    continue

                if json_cfg.calibration.mode == _DescriptionModes.individual:
                    if sys.platform.upper() == "DARWIN":
                        serial = cam.unique_id
                        json_serial = json_cfg.information.device.unique_id

                    else:
                        serial = cam.serial
                        json_serial = json_cfg.information.device.serial

                    status.CAM_SERIAL = serial

                    if json_serial == serial:
                        i = self._start_cam(json_cfg, i, cam, status, _DescriptionModes.individual)
                        break

                elif json_cfg.calibration.mode == _DescriptionModes.type:
                    status.CAM_SERIAL = cam.serial

                    if json_cfg.information.device.product == cam.product:
                        i = self._start_cam(json_cfg, i, cam, status, _DescriptionModes.type)
                        break

    @staticmethod
    def _get_video_device() -> list[VideoDevice]:
        streams: list[VideoDevice] = get_connected_cams(verbose=True)
        idx = [int(x) for x in input("\nEnter the stream indeces seperated by whitespace: ").split()]
        return [streams[i] for i in idx]

    def run(self):
        """
        Runs the manager application.
        """

        self._prepare_cam_descriptions()
        if not self.cam_status:
            raise ValueError(
                f"No valid Camera Descriptions were found in {self._path} or no matching camera was connected to this device."
                f" Please provide a valid .json file or check the connected camera."
            )

        serve(self._flask, host=self._host, port=self._port)

    def __str__(self) -> str:
        header = self.cam_status[0].as_dict().keys()
        rows = [x.as_dict().values() for x in self.cam_status]
        return tabulate.tabulate(rows, header)
