import copy
from pathlib import Path

import cv2
import cv2 as cv
import numpy as np

from camera_management.camera_app.camera_interface import CameraApplication
from camera_management.camera_management_app.manager_interface import ManagerApp
from camera_management.frontends.basic_frontend import manager_interface


def ResizeWithAspectRatio(image, width=None, height=None, inter=cv2.INTER_AREA):
    """TBD, this function may be removed soon"""
    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    return cv2.resize(image, dim, interpolation=inter)


def create_calibration_pictures(measurement_name: str, device_list: tuple[int] | None = None) -> None:
    """
    Main Function for creating calibration pictures. Usage:
        1. Place the calibration target in the scene
        2. Press the spacebar to save an image
            2a. If you chose to calibrate multiple cameras you have to press the spacebar for every camera (the stream will be shown)
        3. Repeat until you are done. To exit the application press 'q' for 'quit'.

    :param measurement_name: The name for the directory the images will be saved in
    :param device_list: If you want to take pictures for more than one camera, you can pass the ports of the cameras you want to consider.
        If you only want to consider one camera don't pass anything.
    """

    manager_backend = ManagerApp(Path(__file__).parent / "data", autostart=True)
    manager_backend.start()

    # Start the manager frontend with the IP and the port of the manager backend
    manager_frontend = manager_interface(host="localhost", port=8090, autostart=True, timeout=30)

    # Get info on which cam is actually configured, which cam thread is started on which port and more
    print(manager_frontend.get_configured_cams())

    devices = manager_frontend.get_configured_cams()
    interfaces = []

    if device_list:
        devices_new = []
        for dev in devices:
            if dev["PORT"] in device_list:
                devices_new.append(dev)
        devices = devices_new

    target_resolution = (1920, 1080)
    root_var = Path(__file__).parent

    # side_len = int(np.ceil(np.sqrt(len(devices))))
    # white_images = [np.ones((target_resolution[0], target_resolution[1], 3))*255]*(side_len - len(devices))
    names = []

    for dev in devices:
        camera_interface = manager_frontend.get_interface_by_port(dev["PORT"])
        camera_interface.set_general_setting(cv.CAP_PROP_FRAME_WIDTH, target_resolution[0])
        camera_interface.set_general_setting(cv.CAP_PROP_FRAME_HEIGHT, target_resolution[1])
        camera_interface.aruco_active = True
        names.append(camera_interface.description["information"]["device"]["serial"])
        root_var.joinpath(Path(f"data/{measurement_name}/{names[-1]}")).mkdir(parents=True, exist_ok=True)
        interfaces.append(camera_interface)

    n = 0
    cv.namedWindow("Machine Vision Stream", cv.WINDOW_AUTOSIZE)
    while True:
        images = []
        for interface in interfaces:
            img = interface.fetch_image_data().image
            display_image = copy.copy(img)
            images.append(display_image)
        final_v = ResizeWithAspectRatio(cv2.hconcat(images), width=1920)
        # final_v = images[-1]

        cv.imshow("Machine Vision Stream", final_v)
        c = cv.waitKey(1)

        if c == ord(" "):
            for img, name in zip(images, names):
                img_file = str(root_var.joinpath(f"data/{measurement_name}/{name}/img_{n:03d}.png"))
                cv.imwrite(img_file, img)
                print(f"Saved Image for cam {name}!")
            n += 1
        elif c == ord("q"):
            return


if __name__ == "__main__":
    create_calibration_pictures(measurement_name="2023-10-02_calib_imPRESSing")
