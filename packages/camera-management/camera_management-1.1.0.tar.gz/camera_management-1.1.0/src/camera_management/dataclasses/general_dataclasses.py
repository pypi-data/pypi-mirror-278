from __future__ import annotations

import dataclasses
import time
import uuid

import numpy as np
from pydantic import BaseModel

from camera_management.dataclasses.aruco_dataclasses import ArucoData
from camera_management.definitions import TimeRecordFlags


class MeasurementData(BaseModel):
    aruco: ArucoData = ArucoData(detectedIDs=[], rejected_bboxs=np.empty(0), values={})
    timestamp: float = -1.0
    id: uuid.UUID | None = None


class ImageResolution(BaseModel):
    """
    x or width -> image width
    y or height -> image height
    ch -> color channels (1 = gray, 3 = rgb or bgr ...)
    """

    x: int | None = 1280
    y: int | None = 720
    channels: int | None = 1

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.channels == other.channels

    def __str__(self):
        resolution_string = f"resolution: {self.x} x {self.y} px, ch: {self.channels}"
        return resolution_string

    def to_dict(self, build_in_types=True) -> dict:
        """
        Helper function to get the core content as dict.
        """
        output = {
            "x": self.x,
            "y": self.y,
            "channels": self.channels,
        }
        if build_in_types:
            for k, v in output.items():
                output[k] = float(v)

        return output


@dataclasses.dataclass
class TimeRecord:
    start: int = None
    stop: int = None
    process_name: str = None
    flag: int = None


@dataclasses.dataclass
class TimeRecordList:
    timerecord: dict[str, TimeRecord] = dataclasses.field(default_factory=dict)

    def add_record(self, name: str) -> None:
        """
        Adds a new TimeRecord object to the list.

        :param name: The name description of the TimeRecord
        """
        self.timerecord[name] = TimeRecord(start=time.time_ns(), process_name=name)

    def complete_last_record(self, name: str) -> None:
        """
        Completes the last record with the given name.

        :param name: The name of the last timestamp to complete
        """
        self.timerecord[name].stop = time.time_ns()


@dataclasses.dataclass
class ImageProcessorData(TimeRecordList):
    """Event to carry current frame data of one thread."""

    # custom_cam_name: str
    image: np.ndarray = None
    id: uuid.UUID | None = None

    @staticmethod
    def generate_dummy_data(resolution: tuple[int, int], length: int) -> ImageProcessorData:
        """
        Generates a dummy ImageProcessorData object.

        :param resolution: Resolution of the dummy data
        :param length: Length of the dummy data timerecordlist.
        """

        tr = {f"dummy_{i}": TimeRecord(-1, -1, "dummy", TimeRecordFlags.dummy_data) for i in range(length)}
        return ImageProcessorData(image=np.ones((*resolution, 3)), timerecord=tr)


@dataclasses.dataclass(slots=True)
class VideoDevice:
    path: str | int  # means OpenCV stream Index
    vendor_id: int | str | None
    product_id: int | str | None
    vendor: str | None
    product: str
    serial: str | None
    backend: int | str | None  # name of the backend

    # ------ Only applies for AVFoundation devices ------------
    transp_type: str | None = None  # bltn, pci, usb, 1394, ntwk, wrls, othr, blue, virt  -> https://github.com/phracker/MacOSX-SDKs/blob/master/MacOSX10.5.sdk/System/Library/Frameworks/IOKit.framework/Versions/A/Headers/audio/IOAudioTypes.h
    unique_id: str | None = None
    device_type: str | None = None
    is_used: bool | None = None

    def __repr__(self):
        return (
            f"\t{self.path}\t-\t{self.product} \n"
            f" \t\t Product ID:\t\t\t{self.product_id}\n"
            f" \t\t Vendor ID:\t\t\t\t{self.vendor_id}\n"
            f" \t\t Vendor: \t\t\t\t{self.vendor}\n"
            f" \t\t Serial Number:\t\t\t{self.serial}\n\n "
            f"\t\t=== AVFoundation specific ===\n"
            f" \t\t Transport Type: \t\t{self.transp_type}\n"
            f" \t\t Unique ID: \t\t\t{self.unique_id}\n"
            f" \t\t Device Type: \t\t\t{self.device_type}\n"
            f" \t\t Used by another App: \t{self.is_used}\n"
        )

    def to_dict(self, build_in_types=True) -> dict:
        """
        Helper function to get core content as dict.
        """
        output = dict()
        for d in self.__slots__:
            content = getattr(self, d)
            if hasattr(content, "to_dict"):
                output[d] = content.to_dict(build_in_types=build_in_types)
            else:
                output[d] = content
        return output


@dataclasses.dataclass
class CamStatus:
    CAM_TYPE: str | None = None
    CAM_SERIAL: str | None = None
    CONFIG_TYPE: bool = False
    CONFIG_INDIVIDUAL: bool = False
    PORT: int | None = None
    PORT_ACTIVE: bool = False
    CALIBRATION_AVAILABLE: bool = False

    def as_dict(self) -> dict:
        """
        Returns the dataclass as a dict.

        :return: A dict representation of the dataclass.
        """
        return {k: str(v) for k, v in dataclasses.asdict(self).items()}
