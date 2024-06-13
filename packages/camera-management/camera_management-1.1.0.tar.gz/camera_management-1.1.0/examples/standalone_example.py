import pathlib

from camera_management.camera_app.camera_interface import CameraApplication

# This is an example to show how to operate a camera without networking layer to increase performance

# To see the camera stream you have to run a viewing application in a second python process, since the OpenCV image viewer
# only runs in the main thread

# It is assumed there are camera description files available in data/type_configs

cam = CameraApplication(port=8091, description_path=pathlib.Path(__file__).parent / "data/type_configs/GENERAL_WEBCAM_0.json")
cam.start()

# use the pre-processing methods available

# set the image to black and white
cam.bw = True

# un-distort the image (only available if there are calibration values present in the .json config file on the backend)
# this should result in a warning, since the above generated description files do not contain calibration values
cam.undistort = True

# rotate the image by +90 degrees
cam.rotate = 0
