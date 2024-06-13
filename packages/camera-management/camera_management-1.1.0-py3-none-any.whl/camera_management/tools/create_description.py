import json
import os
import pathlib
import sys
from datetime import datetime

from camera_management.dataclasses.aruco_dataclasses import ArucoParaSet, ArucoSettings
from camera_management.dataclasses.camera_dataclasses import (
    CameraCalibrationData,
    CameraDebug,
    CameraDescription,
    CameraInformation,
    ImageResolution,
    PreprocessingSettings,
)
from camera_management.dataclasses.general_dataclasses import VideoDevice
from camera_management.definitions import _DescriptionModes
from camera_management.tools.system_analyzer import get_connected_cams


def get_descriptions(path: pathlib.Path) -> list:
    """
    Get all .json files in a given directory.

    :param path: Directory to search in.
    :return: A list of the filenames
    """
    configs = list(path.glob("*.json"))
    return configs


def _create_information_section(dev: VideoDevice) -> CameraInformation:
    dev.serial = None
    ret = CameraInformation(
        standard_resolution=ImageResolution(x=1920, y=1080, channels=3),
        available_resolutions=[ImageResolution(x=1920, y=1080, channels=3)],
        device=dev,
        resolution_roi_coupled=False,
    )
    return ret


def _create_calibration_section() -> CameraCalibrationData:
    mode = _DescriptionModes.type
    ret = CameraCalibrationData(mode=mode, available=False, values=None, model=None)
    return ret


def _create_debug_section() -> CameraDebug:
    today = datetime.today().strftime("%d-%m-%Y %H:%M:%S")
    ret = CameraDebug(last_updated=today, created_on_platform=sys.platform)
    return ret


def _create_config_section() -> dict:
    ret = {}
    return ret


def _create_preprocessing_section() -> PreprocessingSettings:
    aruco = ArucoSettings(dict_name="DICT_4X4_1000", para_set=ArucoParaSet.DEFAULT, active=False, draw_active=False, draw_rgb=(0, 255, 0))
    ret = PreprocessingSettings(bw=False, undistort=False, rotate=0, aruco=aruco)
    return ret


def create_basic_description(path: pathlib.Path):
    """
    Creates a config .json file, which will be accepted but will probably not be filled with the right parameters.

    :param path: The path where the config shall be created to.
    """
    devices = get_connected_cams()

    if len(devices) == 0:
        raise RuntimeError("No valid cameras found.")

    path.mkdir(parents=True, exist_ok=True)

    for dev in devices:
        information = _create_information_section(dev=dev)
        calibration = _create_calibration_section()
        config = _create_config_section()
        debug = _create_debug_section()
        pre_processing = _create_preprocessing_section()

        descr = CameraDescription(information=information, calibration=calibration, config=config, debug=debug, pre_processing=pre_processing)

        i = 0
        while os.path.isfile(path / f"{dev.product}_{i}.json"):
            i += 1

        with open(path / f"{dev.product}_{i}.json", "w", encoding="utf-8") as f:
            json.dump(descr.model_dump(), f, ensure_ascii=False, indent=4)
