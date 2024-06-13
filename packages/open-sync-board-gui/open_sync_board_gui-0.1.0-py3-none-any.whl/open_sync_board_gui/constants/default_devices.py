"""Default devices and their settings."""

from open_sync_board_gui.constants import LOGIC_LEVEL_18, LOGIC_LEVEL_33, LOGIC_LEVEL_50

DEFAULT_DEVICES = [
    "EmpkinS",
    "Biopac",
    "Somnomedics PSG",
    "Azure Kinect",
    "Intel RealSense",
    "Qualisys",
    "OptiTrack",
    "NilsPod",
    "XSens"
]

# indices of sync_signal property refer to sync signals specified in `board_constants.SYNC_SIGNAL_MAPPING_OUTPUT`
DEVICE_SETTINGS = {
    "EmpkinS": {
        "sync_signal": 6,
        "freq": 10,
        "logic_level": LOGIC_LEVEL_50,
        "stop_trigger": False,
        "plug": "Screw Terminal",
        "degree": 11,
    },
    "Biopac": {
        "sync_signal": 0,
        "freq": 0,
        "pulse_length": 4,
        "logic_level": LOGIC_LEVEL_50,
        "stop_trigger": False,
        "plug": "Screw Terminal",
    },
    "Somnomedics PSG": {
        "sync_signal": 6,
        "freq": 10,
        "logic_level": LOGIC_LEVEL_50,
        "stop_trigger": False,
        "plug": "Screw Terminal",
        "degree": 11,
    },
    "Azure Kinect": {
        "sync_signal": 5,
        "freq": 30,
        "logic_level": LOGIC_LEVEL_50,
        "stop_trigger": False,
        "plug": "TRS Audio Plug",
    },
    "Intel RealSense": {
        "sync_signal": 5,
        "freq": 30,
        "logic_level": LOGIC_LEVEL_18,
        "stop_trigger": False,
        "plug": "Screw Terminal",
    },
    "Qualisys": {
        "sync_signal": 0,
        "freq": 0,
        "pulse_length": 4,
        "logic_level": LOGIC_LEVEL_50,
        "stop_trigger": True,
        "plug": "BNC",
    },
    "OptiTrack": {"sync_signal": 5, "freq": 100, "logic_level": LOGIC_LEVEL_33, "stop_trigger": False, "plug": "BNC"},
    "NilsPod": {
        "sync_signal": 0,
        "freq": 0,
        "pulse_length": 4,
        "logic_level": LOGIC_LEVEL_33,
        "stop_trigger": False,
        "plug": "BNC",
    },
    "XSens": {
        "sync_signal": 0,
        "freq": 0,
        "pulse_length": 4,
        "logic_level": LOGIC_LEVEL_50,
        "stop_trigger": False,
        "plug": "BNC",
    },
}
DEFAULT_DEVICE = 0
NO_DEFAULT_CONFIG = -1
