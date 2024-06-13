"""module loading hardware-version specific configuration."""

import sys
from configparser import ConfigParser
from pathlib import Path

from open_sync_board_gui.constants import (
    BOARD_VERSION_V3,
    CONFIG_FILE_PATH,
    CONFIG_LOCATIONS,
    CONNECTION_CONFIG,
    CONNECTION_MAPPING,
    CONNECTION_NAMES,
    CONNECTION_TYPES,
    CONNECTIONS_BIDIRECTIONAL,
    MESSAGE_CONFIG,
    MESSAGE_SIZE,
    SOURCE_CONFIG,
    SOURCE_WITH_EDGE,
    START_SOURCE_MAPPING,
    STOP_SOURCE_MAPPING,
)


def resolve_path(path):
    """Resolve the given path to the correct absolute path.

    Based on whether the application is frozen (bundled as an executable file) or not.
    """
    if getattr(sys, "frozen", False):
        resolved_path = Path.resolve(Path(sys._MEIPASS).joinpath(path))
    else:
        resolved_path = Path.resolve(Path.cwd().joinpath(path))
    return resolved_path


def _convert_to_list(to_split: str, to_int: bool = False):
    result = []
    if to_split:  # is not an empty string
        result = to_split.split(",")
        if to_int:
            result = [int(el) for el in result]
    return result


class HardwareConfig:
    """Class for storing hardware-version specific configuration of the Open Sync Board."""

    def __init__(self, version=BOARD_VERSION_V3):
        self.version = version
        self.config = ConfigParser()
        self.connection_mapping = []
        self.connection_names = []
        self.connection_types = []
        self.bidirectional_connections = []
        self.start_source_mapping = []
        self.stop_source_mapping = []
        self.source_with_edge = []
        self.message_size = 0

    def load(self):
        """Load the configuration details for the given hardware version from the corresponding .ini-file."""
        if self.version not in CONFIG_LOCATIONS.keys():
            raise NotImplementedError(f"There is no software available for version {self.version}!")

        config_path = Path(resolve_path(CONFIG_FILE_PATH)).joinpath(CONFIG_LOCATIONS[self.version])
        self.config.read(config_path)
        self.connection_mapping = _convert_to_list(self.config.get(CONNECTION_CONFIG, CONNECTION_MAPPING))
        self.connection_names = _convert_to_list(self.config.get(CONNECTION_CONFIG, CONNECTION_NAMES))
        self.connection_types = _convert_to_list(self.config.get(CONNECTION_CONFIG, CONNECTION_TYPES), to_int=True)
        self.bidirectional_connections = _convert_to_list(self.config.get(CONNECTION_CONFIG, CONNECTIONS_BIDIRECTIONAL))
        self.start_source_mapping = _convert_to_list(self.config.get(SOURCE_CONFIG, START_SOURCE_MAPPING))
        self.stop_source_mapping = _convert_to_list(self.config.get(SOURCE_CONFIG, STOP_SOURCE_MAPPING))
        self.source_with_edge = _convert_to_list(self.config.get(SOURCE_CONFIG, SOURCE_WITH_EDGE))
        self.message_size = int(self.config.get(MESSAGE_CONFIG, MESSAGE_SIZE))
        return self
