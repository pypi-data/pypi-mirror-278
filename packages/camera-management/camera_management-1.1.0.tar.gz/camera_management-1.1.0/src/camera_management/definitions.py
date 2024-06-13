"""Global variable definitions."""
from enum import IntEnum, unique


@unique
class SETTINGS(IntEnum):
    CAP_PROP_POS_MSEC: int = 0
    CAP_PROP_POS_FRAMES: int = 1
    CAP_PROP_POS_AVI_RATIO: int = 2
    CAP_PROP_FRAME_WIDTH: int = 3
    CAP_PROP_FRAME_HEIGHT: int = 4
    CAP_PROP_FPS: int = 5
    CAP_PROP_FOURCC: int = 6
    CAP_PROP_FRAME_COUNT: int = 7
    CAP_PROP_FORMAT: int = 8
    CAP_PROP_MODE: int = 9
    CAP_PROP_BRIGHTNESS: int = 10
    CAP_PROP_CONTRAST: int = 11
    CAP_PROP_SATURATION: int = 12
    CAP_PROP_HUE: int = 13
    CAP_PROP_GAIN: int = 14
    CAP_PROP_EXPOSURE: int = 15
    CAP_PROP_CONVERT_RGB: int = 16
    CAP_PROP_WHITE_BALANCE_BLUE_U: int = 17
    CAP_PROP_RECTIFICATION: int = 18
    CAP_PROP_MONOCHROME: int = 19
    CAP_PROP_SHARPNESS: int = 20
    CAP_PROP_AUTO_EXPOSURE: int = 21
    CAP_PROP_GAMMA: int = 22
    CAP_PROP_TEMPERATURE: int = 23
    CAP_PROP_TRIGGER: int = 24
    CAP_PROP_TRIGGER_DELAY: int = 25
    CAP_PROP_WHITE_BALANCE_RED_V: int = 26
    CAP_PROP_ZOOM: int = 27
    CAP_PROP_FOCUS: int = 28
    CAP_PROP_GUID: int = 29
    CAP_PROP_ISO_SPEED: int = 30
    CAP_PROP_BACKLIGHT: int = 31
    CAP_PROP_PAN: int = 32
    CAP_PROP_TILT: int = 33
    CAP_PROP_ROLL: int = 34
    CAP_PROP_IRIS: int = 35
    CAP_PROP_SETTINGS: int = 36
    CAP_PROP_BUFFERSIZE: int = 37
    CAP_PROP_AUTOFOCUS: int = 38
    CAP_PROP_SAR_NUM: int = 39
    CAP_PROP_SAR_DEN: int = 40
    CAP_PROP_BACKEND: int = 41
    CAP_PROP_CHANNEL: int = 42
    CAP_PROP_AUTO_WB: int = 43
    CAP_PROP_WB_TEMPERATURE: int = 44
    CAP_PROP_CODEC_PIXEL_FORMAT: int = 45
    CAP_PROP_BITRATE: int = 46
    CAP_PROP_ORIENTATION_META: int = 47
    CAP_PROP_ORIENTATION_AUTO: int = 48
    CAP_PROP_HW_ACCELERATION: int = 49
    CAP_PROP_HW_DEVICE: int = 50
    CAP_PROP_HW_ACCELERATION_USE_OPENCL: int = 51
    CAP_PROP_OPEN_TIMEOUT_MSEC: int = 52
    CAP_PROP_READ_TIMEOUT_MSEC: int = 53
    CAP_PROP_STREAM_OPEN_TIME_USEC: int = 54
    CAP_PROP_VIDEO_TOTAL_CHANNELS: int = 55
    CAP_PROP_VIDEO_STREAM: int = 56
    CAP_PROP_AUDIO_STREAM: int = 57
    CAP_PROP_AUDIO_POS: int = 58
    CAP_PROP_AUDIO_SHIFT_NSEC: int = 59
    CAP_PROP_AUDIO_DATA_DEPTH: int = 60
    CAP_PROP_AUDIO_SAMPLES_PER_SECOND: int = 61
    CAP_PROP_AUDIO_BASE_INDEX: int = 62
    CAP_PROP_AUDIO_TOTAL_CHANNELS: int = 63
    CAP_PROP_AUDIO_TOTAL_STREAMS: int = 64
    CAP_PROP_AUDIO_SYNCHRONIZE: int = 65
    CAP_PROP_LRF_HAS_KEY_FRAME: int = 66
    CAP_PROP_CODEC_EXTRADATA_INDEX: int = 67
    CAP_PROP_FRAME_TYPE: int = 68
    CAP_PROP_N_THREADS: int = 69
    ROI: int = 1070
    TEMPERATURE_SELECTOR: int = 1072
    SENSOR_RESOLUTION: int = 1071


class TimeoutValues:
    """Default timeout values in s"""

    camera_setting_timeout = 5  # timeout until camera setting is considered not set/get
    manager_timeout = 30  # timeout until the camera manager considers a camera not started
    processor_timeout = 15  # timeout until the image processor considers a camera not started


class TimeRecordFlags:
    dummy_data: int = 1


class ReturnFlags:
    not_implemented: int = -200
    error: int = -1
    success: int = 0

class _DescriptionModes:
    individual = "individual"
    type = "type"
