import logging
import time

import cv2 as cv
import numpy as np
from pypylon import pylon

from camera_management.definitions import SETTINGS
from camera_management.tools._misc import calculate_offset_from_midpoint


class BaslerDeviceBase(cv.VideoCapture):
    def __init__(self):
        super().__init__()
        self._tlf = pylon.TlFactory.GetInstance()
        self._tl = self._tlf.CreateTl("BaslerUsb")
        self._dev = self._tl.CreateFirstDevice()
        self._cap = pylon.InstantCamera()
        self._cap.Attach(self._dev)
        self._cap.Open()
        self.converter = pylon.ImageFormatConverter()
        self.converter.OutputPixelFormat = pylon.PixelType_BGR8packed
        self.converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned
        if self._cap is None:
            raise RuntimeError("Unable to open external Basler camera.")
        self.resolution = None
        self._native_resolution = None
        # Init base class
        self.hdr_exposures = None
        self._default_temperature_selection = None
        self._cap.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)

    def set(self, arg, val):
        """
        This function is the pylon equivalent to the OpenCV class function VideoCapture.set(). It is here for a proper
        transition from OpenCV to pylon. From the outside it can take all the same parameters as the OpenCV function, but
        it uses pylon-calls internally, or at least that's the goal.
        :param arg: OpenCV parameter to be set.
        :param val: The value it should be set to.
        """

        match arg:
            case cv.CAP_PROP_FRAME_WIDTH:
                self.resolution[0] = int(val)
            case cv.CAP_PROP_FRAME_HEIGHT:
                self.resolution[1] = int(val)
            case cv.CAP_PROP_FOURCC:
                pass
            case cv.CAP_PROP_AUTO_EXPOSURE:
                self.AutoExposure = val
            case cv.CAP_PROP_FPS:
                self.fps = val
            case cv.CAP_PROP_GAIN:
                self.gain = val
            case SETTINGS.TEMPERATURE_SELECTOR:
                self.set_temperature_selector(val)
            case SETTINGS.ROI:
                if val == -1:
                    self.roi_size = [self._cap.Width.Max, self._cap.Height.Max]
            case _:
                raise TypeError(f"Setting {arg} is not implemented for this {self._cap.DeviceInfo.GetFriendlyName()} device.")

    def get(self, arg) -> int | tuple[str | int, int] | float:
        """
        This function is the pylon equivalent to the OpenCV class function VideoCapture.get(). It is here for a proper
        transition from OpenCV to pylon. From the outside it can take all the same parameters as the OpenCV function, but
        it uses pylon-calls internally, or at least that's the goal.
        :param arg: OpenCV parameter to be gotten.
        :return: The value of the property.
        """
        match arg:
            case cv.CAP_PROP_FRAME_WIDTH:
                # return self.cap.Width.GetValue()
                return self.resolution[0]
            case cv.CAP_PROP_FRAME_HEIGHT:
                # return self.cap.Height.GetValue()
                return self.resolution[1]
            case cv.CAP_PROP_FOURCC:
                return int.from_bytes(b"MJPG", "little")
            case cv.CAP_PROP_AUTO_EXPOSURE:
                return self.AutoExposure
            case cv.CAP_PROP_FPS:
                return self.fps
            case cv.CAP_PROP_GAIN:
                return self.gain
            case SETTINGS.CAP_PROP_TEMPERATURE:
                return self.temperature
            case SETTINGS.TEMPERATURE_SELECTOR:
                return self._cap.DeviceTemperatureSelector.Value
            case SETTINGS.ROI:
                return self.roi_size
            case _:
                raise TypeError(f"Setting {arg} is not implemented for this {self._cap.DeviceInfo.GetFriendlyName()} device.")

    @property
    def AutoExposure(self) -> tuple[str, int]:
        """
        Returns if auto exposure is enabled.
        :return: If AutoExposure is turned on and the value it is set to.
        """
        return self._cap.ExposureAuto.GetValue(), self._cap.AutoTargetBrightness.GetValue()

    @AutoExposure.setter
    def AutoExposure(self, val):
        """
        Set AutoExposureValue.
        :param val: The value it should be set to. Must be between 0 and 1.
        """
        if 1 >= val >= 0:
            self._cap.AutoTargetBrightness.SetValue(val)
        else:
            raise TypeError("Auto Brightness must be between 0 and 1.")
        # Turn on auto exposure
        self._cap.ExposureAuto.SetValue("Continuous")

    def isOpened(self) -> bool:
        """
        Check if the connection to the camera is opened.
        :return: If the connection is opened.
        """
        if self._cap is None:
            return False
        return True

    @property
    def fps(self) -> int:
        """
        Returns the frame rate limit.
        :return: Frame rate limit in frames/second.
        """
        return self._cap.AcquisitionFrameRate.GetValue()

    @fps.setter
    def fps(self, val):
        """
        Sets frame rate limit.
        :param fps: Upper FPS bound.
        """
        self._cap.AcquisitionFrameRateEnable.Value = True
        self._cap.AcquisitionFrameRate.SetValue(val)

    @property
    def throughputMode(self) -> str:
        """
        Check if the DeviceLinkThroughputLimitMode is activated.
        :return: The mode. Can be 'on' or 'Off'.
        """
        return self._cap.DeviceLinkThroughputLimitMode.GetValue()

    @throughputMode.setter
    def throughputMode(self, val):
        """
        Set the DeviceLinkThroughputLimitMode to either 'On' or 'Off'.
        :param val: The Mode to be set.
        """
        if val not in ["On", "Off"]:
            raise TypeError("ThroughputMode can only be 'On' or 'Off'.")
        self._cap.DeviceLinkThroughputLimitMode.SetValue(val)

    @property
    def autoGain(self) -> str:
        """
        Check if AutoGain is activated.
        :return: The mode. Can be 'Once' or 'TODO: FIND VALUES THAT CAN BE SET'.
        """
        return self._cap.GainAuto.GetValue()

    @autoGain.setter
    def autoGain(self, val):
        """
        Set the AutoGain Mode.
        :param val: The mode that should be set.
        """
        if val not in ["Once"]:
            raise TypeError("AutoGain can only be 'Once' or 'TODO: FIND VALUES THAT CAN BE SET'.")
        self._cap.GainAuto.SetValue(val)

    @property
    def gain(self) -> float:
        """
        Returns the set gain value.
        :return: The set value for the Gain.
        """
        return self._cap.Gain.GetValue()

    @gain.setter
    def gain(self, gain):
        """
        Turns off AutoGain and then sets a gain value manually.
        :param gain: The gain to be set. Must be between 0 and 1.
        """
        if 1 >= gain >= 0:
            self._cap.GainAuto.SetValue("Off")
            self._cap.Gain.SetValue(gain)
        else:
            raise TypeError("Gain must be between 0 and 1.")

    @property
    def roi_size(self) -> tuple[int, int]:
        """
        Returns a tuple (width, height) whcih describes the ROI in pixel. See https://docs.baslerweb.com/image-roi for more documentation.
        :return: A tuple of image width and image height.
        """
        roi = (self._cap.Width.GetValue(), self._cap.Height.GetValue())
        return roi

    @roi_size.setter
    def roi_size(self, val: tuple[int, int]):
        """
        Sets the image resolution of a region of interest.
        :param val: A tuple containing the image width and heigth.
        """
        self._cap.StopGrabbing()
        self._cap.Width.Value = val[0]
        self._cap.Height.Value = val[1]
        self.resolution = val
        self._cap.OffsetX.Value = calculate_offset_from_midpoint(self._cap.Width.Max, val[0])
        self._cap.OffsetY.Value = calculate_offset_from_midpoint(self._cap.Height.Max, val[1])
        self._cap.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)

    @property
    def acquisitionMode(self) -> str:
        """
        Get the set AcquisitionMode.
        :return: The AcquisitionMode.
        """
        return self._cap.AcquisitionMode.GetValue()

    @acquisitionMode.setter
    def acquisitionMode(self, val: str):
        """
        Set the AcquisitionMode. Should be "SingleFrame" or "Continuous".
        :param val: The AcquisitionMode.
        """
        if val not in ["SingleFrame", "Continuous"]:
            raise TypeError('AcquisitionMode can only be "SingleFrame" or "Continuous".')
        self._cap.AcquisitionMode.SetValue(val)

    @property
    def pixelDepthMode(self) -> str:
        """
        Get pixel depth mode of sensor values.
        :return: The pixel depth mode.
        """
        return self._cap.BslSensorBitDepthMode.GetValue()

    @pixelDepthMode.setter
    def pixelDepthMode(self, val):
        """
        Set pixel depth mode of sensor values.
        :param val: The pixel depth mode.
        """
        if val not in ["Auto", "Manual"]:
            raise TypeError('BslSensorBitDepthMode can only be "Auto" or "Manual".')
        self._cap.BslSensorBitDepthMode.SetValue(val)

    @property
    def pixelDepth(self) -> str:
        """
        Get pixel depth of sensor values.
        :return: The pixel depth mode.
        """
        return self._cap.BslSensorBitDepth.GetValue()

    @pixelDepth.setter
    def pixelDepth(self, val: str):
        """
        Set the pixel depth of the sensor. Should be one of: TODO: FIND OUT.
        :param val: The pixel depth.
        """
        # if val not in [8, 10, 12]:
        # raise TypeError("BslSensorBitDepth can only be TODO: FIND OUT.")
        if self.pixelDepthMode == "Auto":
            self.pixelDepthMode = "Manual"
        self._cap.BslSensorBitDepth.SetValue(val)

    @property
    def pixelFormat(self) -> str:
        """
        get the pixel Format if the pixel depth mode is set to 'Auto'
        :return: The pixel format.
        """
        return self._cap.PixelFormat.GetValue()

    @pixelFormat.setter
    def pixelFormat(self, val: str):
        """
        Set the pixel Format if the pixel depth mode is set to 'Auto'
        :param val: The pixel format.
        """
        self._cap.PixelFormat.setValue(val)

    @property
    def temperature(self) -> float:
        """
        Get the temperature measured on the selected part of the camera in °C.

        See set_temperature_selector() to select the part of the camera to measure the temperature at.

        !!! WARNING: Reading the temperature of anything else than the device standard selection requires stopping
        and restarting the grabbing process. The framerate will drop significantly when sampling those temperature
         values with a high polling rate. !!!
        """
        if self._cap.DeviceTemperatureSelector.Value != self._default_temperature_selection:
            self._cap.StopGrabbing()
            ret = self._cap.DeviceTemperature.Value
            self._cap.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
        else:
            ret = self._cap.DeviceTemperature.Value
        return ret

    def set_temperature_selector(self, selector: str):
        """
        Set the part of the camera the temperature shall be measured at.

        !!! WARNING: Reading the temperature of anything else than the device standard selection requires stopping
        and restarting the grabbing process. The framerate will drop significantly when sampling those temperature
         values with a high polling rate. !!!
        """
        if selector not in self._cap.DeviceTemperatureSelector.Symbolics:
            raise ValueError(
                f"{selector} is not a valid TemperatureSelector for this {self._cap.DeviceInfo.GetFriendlyName()} device. "
                f"Valid values for TemperatureSelector are: {self._cap.DeviceTemperatureSelector.Symbolics}."
            )
        self._cap.DeviceTemperatureSelector.Value = selector

    def setExposure(self, exposure):
        """
        ADD DOCUMENTATION AND TURN TO PROPERTY
        """
        # Set auto exposure off
        self._cap.ExposureAuto.SetValue("Off")
        # Set exposure value in microseconds
        self._cap.ExposureTime.SetValue(exposure)
        self.exposure = exposure

    def getExposure(self) -> float:
        """
        ADD DOCUMENTATION AND TURN TO PROPERTY
        """
        # Returns exposure value in microseconds
        return self._cap.ExposureTime.GetValue()

    def read(self, timeout=500) -> tuple[bool, np.array]:
        """
        Main function of interacting with the camera. Reads the latest image from the image buffer.
        :param timeout: Waiting time in ms.
        :return: A tuple containing a boolean value if the grab was successful and the actual grabbed image.
        """
        try:
            grabResult = self._cap.RetrieveResult(timeout, pylon.TimeoutHandling_ThrowException)
            if grabResult.GrabSucceeded():
                image = self.converter.Convert(grabResult)
                frame = image.GetArray()
                grabResult.Release()
                return True, cv.resize(frame, self.resolution, interpolation=cv.INTER_LINEAR)
            else:
                return False, None
        except SystemError as e:
            logging.warning(e)
            self.quit_and_open()
            return False, None

    def viewCameraStream(self):
        """
        Display live video data.
        """

        cv.namedWindow("Basler Machine Vision Stream", cv.WINDOW_AUTOSIZE)

        while self._cap.IsGrabbing():
            _, img = self.read()
            cv.imshow("Basler Machine Vision Stream", img)
            c = cv.waitKey(1)
            if c != -1:
                # When everything done, release the capture
                self._cap.StopGrabbing()
                cv.destroyAllWindows()
                break

    def release(self):
        """
        Close camera connection.
        """
        self._cap.StopGrabbing()
        self._cap.Close()
        self._tl.DestroyDevice(self._cap.DetachDevice())
        self._tlf.ReleaseTl(self._tl)

        del self._cap
        del self._dev
        del self._tl
        del self._tlf
        time.sleep(1)

    def quit_and_open(self):
        """
        Close and re-open camera connection.
        """
        # Close camera
        self._cap.Close()
        # Create new capture
        self._cap = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
        self._cap.Open()

    def getStatus(self):
        """
        Saves all parameters of the camera.
        """
        pylon.FeaturePersistence.Save("Basler_Specs.txt", self._cap.GetNodeMap())


class BaslerDevice_a2A5328_15ucBAS(BaslerDeviceBase):
    def __init__(self):
        super().__init__()
        self.resolution = [5328, 4608]  # resolution of the output image
        self._native_resolution = [5328, 4608]  # resolution of the actual camera sensor in pixels
        self._default_temperature_selection = "Coreboard"  # default place of temperature measurement


class BaslerDevice_acA5472_17uc(BaslerDeviceBase):
    def __init__(self):
        super().__init__()
        self.resolution = [5472, 3648]  # resolution of the output image
        self._native_resolution = [5472, 3648]  # resolution of the actual camera sensor in pixels
        self._default_temperature_selection = "Coreboard"  # default place of temperature measurement
