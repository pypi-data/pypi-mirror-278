import copy
import logging
import pickle
import threading
import time

import requests
from urllib3.exceptions import NewConnectionError

from camera_management.dataclasses.general_dataclasses import ImageProcessorData, MeasurementData, TimeRecord
from camera_management.definitions import TimeRecordFlags

logger = logging.getLogger("camera_management.receiver")


class BaseReceiver(threading.Thread):
    def __init__(self, url: str, name: str = "BaseRecorder", stop_evt: threading.Event = None):
        super().__init__(name=name, daemon=True)
        self.url = url

        if stop_evt is None:
            self.stop_evt = threading.Event()
        else:
            self.stop_evt = stop_evt

    def run(self) -> None:
        """
        INSERT USEFUL DESCRIPTION WHEN SEEING THIS.
        """
        self.start_time = time.time()

        while not self.stop_evt.is_set():
            try:
                response = requests.get(self.url)
                self.logic(response)
            except (requests.ConnectionError, NewConnectionError) as ce:
                logger.warning(f"{ce}, please start the REST-API Application or connect network.")
                time.sleep(1)

    def logic(self, response: requests.Response) -> None:
        """
        INSERT USEFUL DESCRIPTION WHEN SEEING THIS.
        """
        pass

    def stop(self):
        """
        Stop recording.

        Joins thread and stores collected data to file.
        """
        self.stop_evt.set()
        self.join()
        # self.store_to_file()


class LogReceiver(BaseReceiver):
    def __init__(self, url: str, cb=None, name: str = "LogRecorder", stop_evt: threading.Event = None):
        super().__init__(url=url, name=name, stop_evt=stop_evt)

        self.last_index = -1
        self.cb = cb

    def logic(self, response: requests.Response) -> None:
        """
        INSERT USEFUL DESCRIPTION WHEN SEEING THIS
        """
        data = response.json()
        last_index = data["index"]
        if last_index > self.last_index:
            if self.cb:
                self.cb(data)
            self.last_index = last_index
        time.sleep(0.05)


class PDReceiver(BaseReceiver):
    def __init__(self, url: str, name: str = "ProcessedDataRecorder", stop_evt: threading.Event = None):
        super().__init__(url=url, name=name, stop_evt=stop_evt)

        self.last_update = -1
        self._data: MeasurementData = MeasurementData()

    def fetch_data(self) -> MeasurementData:
        """
        INSERT USEFUL DESCRIPTION WHEN SEEING THIS
        """
        return self._data

    def logic(self, response: requests.Response) -> None:
        """
        INSERT USEFUL DESCRIPTION WHEN SEEING THIS
        """
        data = pickle.loads(response.content)
        if data.timestamp > self.last_update:
            self.last_update = data.timestamp
            self._data = data
        else:
            time.sleep(0.01)


class ImageReceiver(BaseReceiver):
    def __init__(self, url: str, name: str = "ImageRecorder", stop_evt: threading.Event = None):
        super().__init__(url=url, name=name, stop_evt=stop_evt)

        self._data = ImageProcessorData.generate_dummy_data((1920, 1080), 2)
        self._data.add_record("frontend-receiver")
        self.last_frame_id = self._data.id

    def fetch_data(self) -> ImageProcessorData:
        """
        Fetch the latest image.
        """
        self._data.complete_last_record("frontend-receiver")
        return self._data

    def logic(self, response: requests.Response) -> None:
        """
        INSERT USEFUL DESCRIPTION WHEN SEEING THIS
        """
        data: ImageProcessorData = pickle.loads(response.content)
        data.add_record("frontend-receiver")
        if self.last_frame_id != data.id:
            self._data = data
        self.last_frame_id = copy.copy(data.id)
