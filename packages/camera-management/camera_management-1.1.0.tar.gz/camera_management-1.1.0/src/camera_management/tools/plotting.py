import copy
import dataclasses
from collections.abc import Mapping

import matplotlib.pyplot as plt
import numpy as np

from camera_management.dataclasses.general_dataclasses import TimeRecord
from camera_management.definitions import TimeRecordFlags


class TimeRecordFlagsExtended(TimeRecordFlags):
    led_on = 2


@dataclasses.dataclass
class LatencyResult:
    led_timestamps: list[TimeRecord] = dataclasses.field(default_factory=list)
    cam_timestamps: list[list[TimeRecord]] = dataclasses.field(default_factory=list)


class LatencyPlotting:
    COLORMAPPING = {"camera-thread": "tab:blue", "camera-interface": "tab:orange", "pre-processing": "tab:green", "frontend-receiver": "tab:red"}

    def bar_plot(self, val_dict: Mapping[str, LatencyResult], raw=False) -> None:
        """Wrapper for the two different plotting functions."""
        if raw:
            self.bar_plot_horzizontal_raw(val_dict)
        else:
            self.bar_plot_horizontal(val_dict)

    @staticmethod
    def bar_plot_horzizontal_raw(val_dict: Mapping[str, LatencyResult]) -> None:
        """
        Plots the raw timestamps in a horizontal bar plot.

        :param val_dict: Dictionary containing the plotting values.
        """
        fig = plt.figure()
        ax = fig.add_subplot(111)
        labels_list = []
        image_timestamps = []
        last_ts = -100000
        i, i_max = 0, 0

        for attribute, measurement in val_dict.items():
            led_timestamps = np.array([led.start for led in measurement.led_timestamps]) / 1e9
            minimum_timestamp = np.min(led_timestamps)

        for attribute, measurement in val_dict.items():
            led_timestamps = led_timestamps - minimum_timestamp
            labels_list.append(attribute)
            image_timestamps = np.unique(image_timestamps, axis=0)

            for tr_list in measurement.cam_timestamps:
                if last_ts < tr_list[0].start:
                    i = 0
                else:
                    i += 1

                if i >= i_max:
                    i_max = i

                last_ts = copy.copy(tr_list[-1].stop)

                alpha = 0.2
                if any([tr.flag == TimeRecordFlagsExtended.led_on for tr in tr_list]):
                    alpha = 1
                elif any([tr.flag == TimeRecordFlagsExtended.dummy_data for tr in tr_list]):
                    continue

                plotting_helper = np.array([(tr.start / 1e9 - minimum_timestamp, tr.stop / 1e9 - tr.start / 1e9) for tr in tr_list])
                ax.broken_barh(plotting_helper, (i, 0.5), facecolors=[LatencyPlotting.COLORMAPPING[tr.process_name] for tr in tr_list], alpha=alpha)

            for led_ts in led_timestamps:
                ax.vlines(led_ts, 0, i_max + 1)

        ax.grid(True)
        ax.set_xlabel("Time [s]")
        ax.legend()
        plt.tight_layout()
        plt.show()

    @staticmethod
    def bar_plot_horizontal(val_dict: Mapping[str, LatencyResult]) -> float:
        """
        Plots average values of latency in a horizontal bar plot.

        :param val_dict: Dictionary containing the plotting values per camera
        :return: The latency in s
        """

        fig = plt.figure()
        ax = fig.add_subplot(111)
        measurements_list = []
        labels_list = []
        raw_list = []
        groups = []

        for attribute, measurement in val_dict.items():
            i = 0
            while len(groups) == 0:
                groups = [tr.process_name for tr in measurement.cam_timestamps[i] if tr.flag != TimeRecordFlags.dummy_data]
                i += 1

            led_timestamps = [i for i in measurement.led_timestamps]
            led_timestamp_min = led_timestamps[0]
            cam_timestamps = measurement.cam_timestamps

            for cam in cam_timestamps:
                if cam[0].flag == TimeRecordFlagsExtended.led_on and cam[0].start > led_timestamp_min.start:
                    if len(raw_list) == 0:
                        raw_list.append(cam)
                    elif raw_list[-1][0].start != cam[0].start:
                        raw_list.append(cam)

            measurement = np.array([[c.stop - led.start for c in cam] for cam, led in zip(raw_list, led_timestamps)])
            measurement = np.mean(measurement, axis=0) / 1e9
            helper = [0]
            helper.extend(measurement[:-1])
            measurement = [m - h for m, h in zip(measurement, helper)]
            measurements_list.append(measurement)
            labels_list.append(attribute)

        measurements_list = np.array(measurements_list).T

        for i, m in enumerate(measurements_list):
            if i > 0:
                ax.barh(labels_list, m, align="center", height=0.25, label=groups[i], left=np.sum(measurements_list[:i], axis=0))
            else:
                ax.barh(labels_list, m, align="center", height=0.25, label=groups[i])

        ax.grid(True)
        ax.legend()
        plt.tight_layout()
        plt.show()

        return np.sum(measurements_list)


def comparison_plotter(vals: dict) -> None:
    """
    Plot the data to compare.

    :param vals: Dictionary of values to compare
    """
    sorted_dict = dict(sorted(vals.items(), key=lambda item: item[1][1]))

    names = list(sorted_dict.keys())
    meas_values = np.array(list(sorted_dict.values()))

    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.scatter(names, meas_values[:, 0], label="screen measurement")
    ax.scatter(names, meas_values[:, 1], label="led measurement")

    ax.grid(True)
    ax.legend()
    plt.ylabel("Latency [s]")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    meas_dict = {
        "4K CAM STANDALONE @ 1920x1080": (0.12864095742751444, 0.06036933713333333),
        "4K CAM NETWORK @ 1920x1080": (0.15302706795429588, 0.11056531373076924),
        "4K CAM STANDALONE @ 3840x2160": (0.25432940493180933, 0.25282128607142856),
        "4K CAM NETWORK @ 3840x2160": (0.4429754351305888, 0.4400621708333333),
        "AVT STANDALONE @ 2464x2056": (0.15511318302428076, 0.09751050642857144),
        "AVT NETWORK @ 2464x2056": (0.26826711025428934, 0.22697539957142857),
        "AVT NETWORK @ 512x512": (0.10476176029974849, 0.056211082545454545),
        "AVT STANDALONE @ 512x512": (0.07646897745087133, 0.028487280454545454),
        "BASLER NETWORK @ 512x512": (0.0834152655566686, 0.04941892775),
        "BASLER STANDALONE @512x512": (0.060166045276197594, 0.0181485801875),
        "BASLER STANDALONE @5328x4608": (0.4858882861615913, 0.2785599265217391),
        "BASLER NETWORK @5328x4608": (1.6223921114761608, 1.4770104735),
        "GENERAL_WEBCAM NETWORK @ 1920x1090": (0.24555957792414979, 0.23451011166666666),
        "OAK-1 STANDALONE @ 1920x1080": (0.117826713637763, 0.0558737965625),
        "OAK-1 NETWORK @ 1920x1080": (0.17985024797292876, 0.13129229940384615),
        "OAK-1 STANDALONE @ 4056x3040": (0.2448975357047491, 0.168293006),
        "OAK-1 NETWORK @ 4056x3040": (0.4327662875979676, 0.36918173917647057),
    }
    comparison_plotter(meas_dict)
