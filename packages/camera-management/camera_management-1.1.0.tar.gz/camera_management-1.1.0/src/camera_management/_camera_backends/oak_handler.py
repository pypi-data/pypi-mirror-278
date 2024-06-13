import queue
import threading

import cv2
import depthai
import numpy as np

from camera_management.dataclasses.general_dataclasses import VideoDevice
from camera_management.definitions import SETTINGS, ReturnFlags


class DepthaiResolutions:
    color_resolutions: dict[tuple[int, int], depthai.ColorCameraProperties.SensorResolution] = {
        # IMX582 cropped
        (5312, 6000): depthai.ColorCameraProperties.SensorResolution.THE_5312X6000,
        (4208, 3120): depthai.ColorCameraProperties.SensorResolution.THE_13_MP,  # AR214
        # IMX378, IMX477, IMX577
        (4056, 3040): depthai.ColorCameraProperties.SensorResolution.THE_12_MP,
        # IMX582 with binning enabled
        (4000, 3000): depthai.ColorCameraProperties.SensorResolution.THE_4000X3000,
        (3840, 2160): depthai.ColorCameraProperties.SensorResolution.THE_4_K,
        (1920, 1200): depthai.ColorCameraProperties.SensorResolution.THE_1200_P,  # AR0234
        (1920, 1080): depthai.ColorCameraProperties.SensorResolution.THE_1080_P,
        (1440, 1080): depthai.ColorCameraProperties.SensorResolution.THE_1440X1080,
        (2592, 1944): depthai.ColorCameraProperties.SensorResolution.THE_5_MP,  # OV5645
        (1280, 800): depthai.ColorCameraProperties.SensorResolution.THE_800_P,  # OV9782
        (1280, 720): depthai.ColorCameraProperties.SensorResolution.THE_720_P,
    }

    IMX378: tuple[int, int] = (4056, 3040)
    OV9782: tuple[int, int] = (1280, 800)

    def _check_resolution(self, resolution: tuple[int, int]):
        return resolution in self.color_resolutions.keys()

    def get_resolution(self, resolution: tuple[int, int]) -> depthai.ColorCameraProperties.SensorResolution | None:
        """
        Checks the given resolution tuple and converts it to a depthai enum.

        :param resolution: Tuple of image width and height
        """
        if self._check_resolution(resolution):
            return self.color_resolutions[resolution]


class oak_base(cv2.VideoCapture):
    def __init__(self, device_info: depthai.DeviceInfo):
        super().__init__()
        self._pipeline = self._setup_pipeline(depthai.ColorCameraProperties.SensorResolution.THE_1080_P)
        self._stop_evt = threading.Event()
        self._device_mxid = device_info
        self._width = 1920
        self._height = 1080

        self.streaming_thread = threading.Thread(name="Streaming Thread", daemon=False, target=self._start_streaming_thread)
        self.open = True
        self.frame_queue = queue.Queue(maxsize=1)
        self.streaming_thread.start()
        self._native_resolution = None

    def _set_resolution(self, resolution: tuple[int, int]) -> None:
        res = DepthaiResolutions().get_resolution(resolution)
        if res is None:
            return
        self._stop_evt.set()
        self.streaming_thread.join()
        self._pipeline = self._setup_pipeline(res)
        self._stop_evt.clear()
        self.streaming_thread = threading.Thread(name="Streaming Thread", daemon=False, target=self._start_streaming_thread)
        self.streaming_thread.start()
        self.open = True

    def _setup_pipeline(self, resolution: depthai.ColorCameraProperties.SensorResolution) -> depthai.Pipeline:
        pipeline = depthai.Pipeline()

        # Define source and output
        camRgb = pipeline.create(depthai.node.ColorCamera)
        self._cam_rgb = camRgb
        xoutVideo = pipeline.create(depthai.node.XLinkOut)
        xoutVideo.setStreamName("rgb")

        xoutPreview = pipeline.create(depthai.node.XLinkOut)
        xoutPreview.setStreamName("preview")

        # Properties
        camRgb.setBoardSocket(depthai.CameraBoardSocket.CAM_A)
        camRgb.setResolution(resolution)
        camRgb.setPreviewSize(512, 512)

        xoutVideo.input.setBlocking(False)
        xoutVideo.input.setQueueSize(1)

        xoutPreview.input.setBlocking(False)
        xoutPreview.input.setQueueSize(1)

        # Linking
        camRgb.video.link(xoutVideo.input)
        camRgb.preview.link(xoutPreview.input)

        return pipeline

    def _start_streaming_thread(self):
        with depthai.Device(self._pipeline, self._device_mxid, maxUsbSpeed=depthai.UsbSpeed.SUPER_PLUS) as device:
            self._native_resolution = getattr(DepthaiResolutions, list(device.getConnectedCameraFeatures())[0].sensorName)
            q_rgb = device.getOutputQueue("rgb", maxSize=1, blocking=False)
            while not self._stop_evt.is_set():
                in_rgb = q_rgb.tryGet()
                try:
                    self.frame_queue.put(in_rgb)
                except queue.Full:
                    pass
            self.open = False

    def set(self, arg, val) -> None:
        """
        This function is the oak equivalent to the OpenCV class function VideoCapture.set(). It is here for a proper
        transition from OpenCV to vmbpy. From the outside it can take all the same parameters as the OpenCV function, but
        it uses vmbpy-calls internally, or at least that's the goal.
        :param arg: OpenCV parameter to be set.
        :param val: The value it should be set to.
        """
        match arg:
            case cv2.CAP_PROP_FRAME_WIDTH:
                self._width = val
                self._set_resolution((self._width, self._height))
            case cv2.CAP_PROP_FRAME_HEIGHT:
                self._height = val
                self._set_resolution((self._width, self._height))
            case cv2.CAP_PROP_FOURCC:
                pass
            case _:
                return

    def get(self, arg) -> int:
        """
        This function is the oak equivalent to the OpenCV class function VideoCapture.get(). It is here for a proper
        transition from OpenCV to vmbpy. From the outside it can take all the same parameters as the OpenCV function, but
        it uses vmbpy-calls internally, or at least that's the goal.
        :param arg: OpenCV parameter to be gotten.
        :return: The value of the property.
        """
        match arg:
            case cv2.CAP_PROP_FRAME_WIDTH:
                return self._cam_rgb.getResolutionWidth()
            case cv2.CAP_PROP_FRAME_HEIGHT:
                return self._cam_rgb.getResolutionHeight()
            case cv2.CAP_PROP_FOURCC:
                return int.from_bytes(b"MJPG", "little")
            case SETTINGS.SENSOR_RESOLUTION:
                return self._native_resolution
            case _:
                return ReturnFlags.not_implemented

    def read(self, timeout=5000) -> tuple[bool, np.ndarray | None]:
        """
        Main function of interacting with the camera. Reads the latest image from the image buffer.
        :param timeout: Waiting time in s.
        :return: A tuple containing a boolean value if the grab was successful and the actual grabbed image.
        """
        try:
            frame = self.frame_queue.get(block=True, timeout=timeout)
        except queue.Empty:
            return False, None

        if frame is None:
            return False, frame
        return True, frame.getCvFrame()

    def isOpened(self) -> bool:
        """
        Check if the connection to the camera is opened.
        :return: If the connection is opened.
        """
        return self.open


class oak_1(oak_base):
    def __init__(self, device: VideoDevice):
        info = depthai.DeviceInfo(device.path)
        super().__init__(info)
