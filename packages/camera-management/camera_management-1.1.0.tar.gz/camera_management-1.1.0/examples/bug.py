import pathlib

import faulthandler
faulthandler.enable(all_threads=True)

from camera_management.tools.create_description import create_basic_description
from camera_management.frontends.basic_frontend import basic_Interface
from camera_management.camera_app.camera_interface import CameraApplication


def start_backend(backend: CameraApplication):
    """start backend and wait"""
    backend.start()

    while backend._status == "OFFLINE":
        pass
    while backend._preprocessing_thread.camera is None:
        pass

camera_backend = CameraApplication(port=8091, description_path=pathlib.Path('/Users/simonmichel/PycharmProjects/camera-management/examples/data/type_configs/GENERAL WEBCAM_0.json'))
camera_backend.start()
# start_backend(camera_backend)
print("camera backend was started")
camera_interface = basic_Interface(host="0.0.0.0", port=8091)
camera_interface.bw = True
camera_interface.rotate = 270

print("camera is configurerd over interface")
# del camera interface because i don't want
# * the image recorder thread or
# * the process data recorder thread
del camera_interface