"""Constants and abbreviations used for the sync board GUI."""

# version information
# new versions can be added here
BOARD_VERSION_V3 = "v3"
CONFIG_LOCATIONS = {BOARD_VERSION_V3: "v3.ini"}
CONFIG_FILE_PATH = "config"
COMMAND_FILE_PATH = {BOARD_VERSION_V3: "config/commands_v3.json"}
MESSAGE_FILE_PATH = {BOARD_VERSION_V3: "config/messages_v3.json"}

# connection information
INPUT_CONNECTION = 0
OUTPUT_CONNECTION = 1
IS_INACTIVE = "00"
IS_ACTIVE = "01"
CONNECTION_MAPPING = "mapping"
CONNECTION_CONFIG = "connections"
CONNECTION_NAMES = "names"
CONNECTION_TYPES = "types"
CONNECTIONS_BIDIRECTIONAL = "bidirectional"

# configuration information
SYNC_SIGNAL_MAPPING_OUTPUT = [
    "Falling Trigger",
    "Rising Trigger",
    "Falling Edge",
    "Rising Edge",
    "Falling Clock",
    "Rising Clock",
    "M-Sequence",
]
SYNC_SIGNAL_MAPPING_INPUT = ["Falling Edge", "Rising Edge", "Any Edge"]
SYNC_SIGNAL_WITHOUT_FREQ = ["Falling Trigger", "Rising Trigger", "Rising Edge", "Falling Edge"]
SYNC_SIGNAL_WITHOUT_DEGREE = [
    "Falling Trigger",
    "Rising Trigger",
    "Rising Edge",
    "Falling Edge",
    "Rising Clock",
    "Falling Clock",
]
SYNC_SIGNAL_WITHOUT_STOP_TRIGGER = [
    "Rising Edge",
    "Falling Edge",
    "Rising Clock",
    "Falling Clock",
    "M-Sequence",
]
SYNC_SIGNAL_WITHOUT_PULSE_LENGTH = [
    "Rising Edge",
    "Falling Edge",
    "Rising Clock",
    "Falling Clock",
    "M-Sequence",
]
SYNC_SIGNAL_MAPPING_SOURCE = ["Falling Edge", "Rising Edge", "Any Edge"]
DEFAULT_VALUE = 0
DEFAULT_DELAY = DEFAULT_VALUE
DEFAULT_FREQ = DEFAULT_VALUE
DEFAULT_DEGREE = DEFAULT_VALUE
DEFAULT_SYNC_SIGNAL = DEFAULT_VALUE
DEFAULT_PULSE_LENGTH = 4
START_SOURCE = "start_source"
STOP_SOURCE = "stop_source"
SOURCE_CONFIG = "sources"
START_SOURCE_MAPPING = "start_source"
STOP_SOURCE_MAPPING = "stop_source"
SOURCE_WITH_EDGE = "with_edge"
DEFAULT_SOURCE = 0
MIN_PULSE_LEN = 1
MAX_PULSE_LEN = 65535
MIN_DELAY = 0
MAX_DELAY = 65535
MIN_FREQ = 0
MAX_FREQ = 5100
MIN_DEGREE = 1
MAX_DEGREE = 11
STOP_TRIGGER_MAPPING = {False: "no_stop_trigger", True: "stop_trigger"}

# jumper information
LOGIC_LEVEL_18 = "1.8"
LOGIC_LEVEL_33 = "3.3"
LOGIC_LEVEL_50 = "5"
JUMPER_ON = "jumper"
INPUT = "input"
OUTPUT = "output"

# status information
START_MODE = "start"
STOP_MODE = "stop"
IDLE_MODE = "idle"
RUNNING_MODE = "running"
ERROR_MODE = "error"
