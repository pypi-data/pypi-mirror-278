import collections
import copy
import threading
import time
from pathlib import Path

import cv2
import numpy as np
from scapy.all import Packet, sniff

from camera_management.camera_app.camera_interface import CameraApplication
from camera_management.camera_management_app.manager_interface import ManagerApp
from camera_management.dataclasses.general_dataclasses import ImageProcessorData, TimeRecord
from camera_management.definitions import SETTINGS
from camera_management.frontends.basic_frontend import basic_Interface, manager_interface
from camera_management.tools.plotting import LatencyPlotting, LatencyResult, TimeRecordFlagsExtended


class LatencyMeasurement:
    ESCAPE_KEY = 27

    class _KeyboardThread(threading.Thread):
        """
        Helper class to get the brighntess threshold from user input.
        """

        def __init__(self, input=None, name="keyboard-input-thread"):
            self.input = input
            super().__init__(name=name)

        def run(self):
            """
            Runs the keyboard listening
            """
            while True:
                self.input[0] = int(input("Enter Brightness Threshold: "))  # waits to get input + Return
                print("Set brightness threshold to: ", self.input[0])

    class _MouseHandler:
        """
        Helper class to handle the onscreen bounding box selection.
        """

        drag_start = None
        selection = None

        def hasSelection(self):
            return self.selection is not None or self.selection == [0, 0, 0, 0]

        def hasValidSelection(self):
            return not (self.selection[0] == self.selection[2] or self.selection[1] == self.selection[3])

        def onmouse(self, event, x, y, flags, param, img):
            """
            Handler to get a selection from an OpenCV image.
            """
            if event == cv2.EVENT_LBUTTONDOWN:
                self.drag_start = x, y
                self.selection = [0, 0, 0, 0]
            elif self.drag_start:
                # print flags
                if flags & cv2.EVENT_FLAG_LBUTTON:
                    minpos = min(self.drag_start[0], x), min(self.drag_start[1], y)
                    maxpos = max(self.drag_start[0], x), max(self.drag_start[1], y)
                    self.selection = [minpos[0], minpos[1], maxpos[0], maxpos[1]]
                else:
                    self.drag_start = None

    class _PlottingHelper:
        def __init__(self, display_image: np.ndarray, padding: int, brightness_buffer: collections.deque, threshold: int):
            max_brightness = np.max(brightness_buffer)

            self.y_low = display_image.shape[0] - padding
            self.y_high = int(display_image.shape[0] * 0.75)
            self.y_range = self.y_high - self.y_low

            self.x_low = padding
            self.x_high = display_image.shape[1] - padding

            self.x = np.linspace(self.x_low, self.x_high, len(brightness_buffer), dtype=int)
            self.y = self.y_range * np.array(brightness_buffer) / max_brightness + self.y_low
            self.y_thresh = int(self.y_range * threshold / max_brightness + self.y_low)

        def isBigEnough(self):
            return self.x_high >= 100 and self.y_high >= 100

    @staticmethod
    def _listening_thread(interface: str, ip: str, time_stamps: list, stop_evt: threading.Event):
        def stopfilter(stop_event: threading.Event):
            if stop_event.is_set():
                return True
            return False

        def handle_packet(packet: Packet, res_list):
            if "Evt1" in (bytes(packet.payload).decode("UTF8", "replace")):
                res_list.append(TimeRecord(start=int(packet.time * 1e9), stop=int(packet.time * 1e9), process_name="led-udp-packets"))

        sniff(filter=f"udp and src {ip}", iface=interface, prn=lambda x: handle_packet(x, time_stamps), stop_filter=lambda x: stopfilter(stop_evt))

    def __init__(self, cam: CameraApplication | basic_Interface, ip="169.254.243.87", interface="enp8s0"):
        self.cam = cam
        self.brightness_buffer = collections.deque(maxlen=200)

        for _ in range(200):
            self.brightness_buffer.append(1)

        self._led_ip = ip
        self._led_interace = interface

        self._padding = 10
        self._threshold = [1]
        self._cv_text_args = (cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3, cv2.LINE_AA)
        self._bounding_box = [0, 0, 0, 0]
        self._led_timestamps = []
        self._cam_timestamps = []
        self._currently_on = False
        self._locked_bounding_box = False
        self._stop_evt = threading.Event()
        self._mh = self._MouseHandler()
        self._kt = self._KeyboardThread(self._threshold)
        self._udpt = threading.Thread(target=self._listening_thread, args=(interface, ip, self._led_timestamps, self._stop_evt), daemon=True)
        self._udpt.start()

    @staticmethod
    def _setup_cv_window(name="Latency Measurement") -> None:
        cv2.namedWindow(name, cv2.WINDOW_NORMAL)
        cv2.moveWindow(name, 0, 0)
        cv2.resizeWindow(name, (1920, 1080))

    def _was_key_pressed(self) -> bool:
        k = cv2.waitKey(1) & 0xFF
        return k == self.ESCAPE_KEY

    def _calculate_mean_brightness(self, display_image: np.ndarray, bounding_box: bool) -> float:
        if bounding_box:
            brightness = (
                np.mean(display_image[self._bounding_box[1] : self._bounding_box[3], self._bounding_box[0] : self._bounding_box[2], 0])
                + np.mean(display_image[self._bounding_box[1] : self._bounding_box[3], self._bounding_box[0] : self._bounding_box[2], 1])
                + np.mean(display_image[self._bounding_box[1] : self._bounding_box[3], self._bounding_box[0] : self._bounding_box[2], 2])
            )
        else:
            brightness = np.mean(display_image[:, :, 0]) + np.mean(display_image[:, :, 1]) + np.mean(display_image[:, :, 2])
        return brightness

    def _determine_brightness(self, display_image: np.ndarray) -> float:
        if not self._mh.hasSelection():
            brightness = self._calculate_mean_brightness(display_image, False)
        else:
            if not self._mh.hasValidSelection():
                brightness = 1
            else:
                for i in range(4):
                    self._bounding_box[i] = max(min(self._mh.selection[i], display_image.shape[(i + 1) % 2]), 0)
                brightness = self._calculate_mean_brightness(display_image, True)
        return brightness

    def _draw_to_image(self, display_image: np.ndarray) -> np.ndarray:
        res = None
        ph = self._PlottingHelper(display_image, self._padding, self.brightness_buffer, self._threshold[0])
        if ph.isBigEnough():
            res = np.vstack((ph.x, ph.y)).T.reshape((-1, 1, 2))
            res = res.astype(np.int32)

        if self._mh.selection is not None:
            display_image = cv2.rectangle(
                display_image, (self._mh.selection[0], self._mh.selection[1]), (self._mh.selection[2], self._mh.selection[3]), (0, 255, 255), 2
            )
        display_image = cv2.rectangle(
            display_image,
            (self._padding, int(display_image.shape[0] * 0.75)),
            (display_image.shape[1] - self._padding, display_image.shape[0] - self._padding),
            (255, 255, 255),
            -1,
        )
        display_image = cv2.putText(display_image, f"MIN: {np.min(self.brightness_buffer):3.2f}", (ph.x_low, ph.y_low - 5), *self._cv_text_args)
        display_image = cv2.putText(display_image, f"MAX: {np.max(self.brightness_buffer):3.2f}", (ph.x_low, ph.y_high + 30), *self._cv_text_args)
        if res is not None:
            display_image = cv2.polylines(display_image, [res], False, (255, 0, 0), 2)
        display_image = cv2.line(display_image, (ph.x_low, ph.y_thresh), (ph.x_high, ph.y_thresh), (0, 0, 255), 2)
        display_image = cv2.putText(display_image, f"Brightness: {self.brightness_buffer[-1]:3.2f}", (50, 50), *self._cv_text_args)
        display_image = cv2.putText(display_image, f"Threshold: {self._threshold[0]:3.2f}", (50, 100), *self._cv_text_args)

        return display_image

    def determine_brightness_and_bounding_box(self, image_call: callable) -> tuple[float, list[int]]:
        """
        Used to set the brightness and bounding box for a latency measurement.

        :param image_call: Callable, which returns an ImageProcessor object
        :return: A tuple containing the set brightness and the 4 edges of the set bounding box
        """

        self._setup_cv_window("Set Brightness Region")

        # register callback to opencv for bounding box selection
        cv2.setMouseCallback("Set Brightness Region", lambda x1, x2, x3, x4, x5: self._mh.onmouse(x1, x2, x3, x4, x5, bgr_image))

        # start input thread for brightness threshold selection from input
        self._kt.start()

        while cv2.getWindowProperty("Set Brightness Region", cv2.WND_PROP_VISIBLE) > 0:
            # get image
            bgr_image = image_call()
            display_image = copy.copy(bgr_image.image)

            # determine brightness
            brightness = self._determine_brightness(display_image)
            self.brightness_buffer.append(brightness)

            # draw everything to the image
            display_image = self._draw_to_image(display_image)
            cv2.imshow("Set Brightness Region", display_image)

            if self._was_key_pressed():
                cv2.destroyAllWindows()
                return self.brightness_threshold, self.bounding_box

    @property
    def brightness_threshold(self) -> float:
        """Gets the brightness threshold to detect a turned on LED (can also be set live)."""
        return self._threshold[0]

    @brightness_threshold.setter
    def brightness_threshold(self, val: float):
        """Sets the brightness threshold to detect a turned on LED (can also be set live)."""
        if 0 < val < 3 * 255:
            self._threshold[0] = val
        else:
            raise ValueError("Brightness threshold must be between 0 and 765.")

    @property
    def bounding_box(self) -> list[int]:
        """Gets the bounding box which will be used for estimation if the LED is on (can also be set live)."""
        return self._bounding_box

    @bounding_box.setter
    def bounding_box(self, val: list[int, int, int, int]):
        """Sets the bounding box which will be used for estimation if the LED is on (can also be set live)."""
        if len(val) == 4:
            self._bounding_box = val
        else:
            raise ValueError("You need to provide a list of 4 integer edges of the bounding box.")

    @property
    def results(self) -> LatencyResult:
        """Cleans and returns the measurement results."""
        while self._led_timestamps[0].start < self._cam_timestamps[0][0].start:
            self._led_timestamps = self._led_timestamps[1:]

        while self._led_timestamps[0].start > self._cam_timestamps[0][0].start:
            self._cam_timestamps = self._cam_timestamps[1:]

        return LatencyResult(self._led_timestamps, self._cam_timestamps)

    def detetermine_led_on(self, image: ImageProcessorData) -> ImageProcessorData:
        """
        Determines the latency of a given camera, accessed by the "image_call" parameter. Only works with ImageProcessor objects.

        :param image: An ImageProcessorObject to evaluate
        """

        # ----------------------------------------------------------------------------------------- start of processing
        bgr_image: ImageProcessorData = image
        display_image = copy.copy(bgr_image.image)

        if self._bounding_box is not None:
            display_image = cv2.rectangle(
                display_image, (self._bounding_box[0], self._bounding_box[1]), (self._bounding_box[2], self._bounding_box[3]), (0, 255, 255), 2
            )

        brightness = self._calculate_mean_brightness(display_image, self._bounding_box is not None)
        if brightness >= self.brightness_threshold:
            if not self._currently_on:
                self._currently_on = True
                for tr in bgr_image.timerecord:
                    tr.flag = TimeRecordFlagsExtended.led_on
        else:
            self._currently_on = False

        self._cam_timestamps.append(copy.deepcopy(bgr_image.timerecord))
        self._led_timestamps[-1].flag = copy.copy(bgr_image.id)

        ret = copy.copy(bgr_image)
        ret.image = display_image
        return ret

    @staticmethod
    def determine_latency_screen(cap: callable, threshold=128) -> None:
        """
        Simple way of determining the camera latency by using a flickering opencv window.

        :param cap: Callable which returns an ImageProcessor object
        :param threshold: Brightness threshold to detect a "white" image.
        """
        # setup window for camera stream
        img_name = "Latency Measurement"
        cv2.namedWindow(img_name, cv2.WINDOW_NORMAL)
        cv2.moveWindow(img_name, 0, 0)
        cv2.resizeWindow(img_name, 1920, 1080)

        frame_cnt = 0
        last_change_frame_cnt = 0

        frame = cap().image

        white = np.ones_like(frame) * 255
        black = np.zeros_like(frame)

        is_now_dark = False
        last_change_time = time.perf_counter()

        avg_time = 0
        avg_frames = 0

        change_cnt = -1

        while cv2.getWindowProperty(img_name, cv2.WND_PROP_VISIBLE) > 0:
            # ----------------------------------------------------------------------------------------- start of processing
            bgr_image = cap().image

            is_dark = np.average(bgr_image[:, :, 0]) < threshold

            if is_dark != is_now_dark:
                change_cnt += 1
                is_now_dark = is_dark

                change_time = time.perf_counter()
                div = change_cnt if change_cnt < 32 else 32

                diff_frame = frame_cnt - last_change_frame_cnt
                diff_time = change_time - last_change_time
                last_change_frame_cnt = frame_cnt
                last_change_time = change_time

                if change_cnt < 1:
                    continue

                avg_frames = (diff_frame + avg_frames * (div - 1)) / div
                avg_time = (diff_time + avg_time * (div - 1)) / div

            if is_dark:
                cv2.imshow(img_name, white)
            else:
                cv2.imshow(img_name, black)

            k = cv2.waitKey(1) & 0xFF
            frame_cnt += 1

            if k == LatencyMeasurement.ESCAPE_KEY or change_cnt == 300:
                return avg_time

        cv2.destroyAllWindows()


class LatencyMeasurementDemo(LatencyMeasurement):
    def __init__(self, cam: CameraApplication | basic_Interface, ip="169.254.243.87", interface="enp8s0"):
        super().__init__(cam, ip, interface)
        self._stop_evt = threading.Event()
        self._cam = cam

    def run(self):
        """Starts the standalone latency measurement."""
        self.determine_brightness_and_bounding_box(self._cam.fetch_image_data)
        self._setup_cv_window("Latency Measurement")

        while not self._stop_evt.is_set():
            img = self._cam.fetch_image_data()
            img = self.detetermine_led_on(img)
            cv2.imshow("Latency Measurement", img.image)

            if self._was_key_pressed():
                cv2.destroyAllWindows()
                return self.results


if __name__ == "__main__":
    # listening_thread("enp8s0", "169.254.171.21", [], 200)

    # cam = CameraApplication(8091)
    # cam.start()

    manager_backend = ManagerApp(Path(__file__).parent.parent.parent / "examples" / "data", autostart=True)
    manager_backend.start()
    manager_frontend = manager_interface(host="localhost", port=8090, autostart=True, timeout=30)
    cam = manager_frontend.get_interface_by_port(8091)
    print(cam.get_general_setting(cv2.CAP_PROP_FRAME_WIDTH))
    print(cam.get_general_setting(cv2.CAP_PROP_FRAME_HEIGHT))
    print(cam.set_general_setting(SETTINGS.ROI, -1))

    lm = LatencyMeasurementDemo(cam, "169.254.243.87", "enp8s0")
    lm.brightness_threshold = 500
    latency = lm.run()

    plotter = LatencyPlotting()
    led_time = plotter.bar_plot_horizontal({"4K": latency})
    plotter.bar_plot_horzizontal_raw({"AVT": latency})
