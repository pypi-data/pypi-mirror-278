"""Board configuration classes."""

import json
from pathlib import Path
from typing import Dict, List, Sequence, Tuple, Union

from open_sync_board_gui.config.hardware_config import HardwareConfig, resolve_path
from open_sync_board_gui.constants import (
    COMMAND_FILE_PATH,
    DEFAULT_DEGREE,
    DEFAULT_DELAY,
    DEFAULT_DEVICE,
    DEFAULT_DEVICES,
    DEFAULT_FREQ,
    DEFAULT_PULSE_LENGTH,
    DEFAULT_SOURCE,
    DEFAULT_SYNC_SIGNAL,
    INPUT_CONNECTION,
    IS_ACTIVE,
    MAX_DEGREE,
    MAX_DELAY,
    MAX_FREQ,
    MAX_PULSE_LEN,
    MIN_DEGREE,
    MIN_DELAY,
    MIN_FREQ,
    MIN_PULSE_LEN,
    NO_DEFAULT_CONFIG,
    OUTPUT_CONNECTION,
    START_SOURCE,
    STOP_SOURCE,
    STOP_TRIGGER_MAPPING,
    SYNC_SIGNAL_MAPPING_INPUT,
    SYNC_SIGNAL_MAPPING_OUTPUT,
    SYNC_SIGNAL_MAPPING_SOURCE,
)


class BoardConfig:
    """Class for all board sources and connections."""

    def __init__(self, config: HardwareConfig):
        self.config = config
        self._start_source = Source(config=config, source_type=START_SOURCE)
        self._stop_source = Source(config=config, source_type=STOP_SOURCE)
        self.connections = []
        self.command_dict = {}

    def setup_command_dict(self):
        """Load command dictionary from json file."""
        try:
            with Path.open(Path(resolve_path(COMMAND_FILE_PATH[self.config.version]))) as fp:
                self.command_dict = json.load(fp)
        except Exception:
            raise

    def setup_connections(self, connection_list: List[int]):
        """Create connections based on the connection list.

        Currently, default connection list is always used, since the number of connections needs to be consistent
        with the number of connection selection buttons in the ui.
        """
        connections = []
        for _idx, el in enumerate(connection_list):
            if el == INPUT_CONNECTION:
                c = Connection(self.config.connection_names, self.config, el, DEFAULT_DELAY, DEFAULT_SYNC_SIGNAL)
            elif el == OUTPUT_CONNECTION:
                c = Connection(
                    self.config.connection_names,
                    self.config,
                    el,
                    DEFAULT_DELAY,
                    DEFAULT_SYNC_SIGNAL,
                    freq=DEFAULT_FREQ,
                    degree=DEFAULT_DEGREE,
                    pulse_length=DEFAULT_PULSE_LENGTH,
                )
            else:
                raise ValueError(f"Invalid connection type {el}!")
            connections.append(c)
        self.connections = connections

    def load_from_file(self, path: Path) -> List[bytes]:
        """Load board configuration from json file."""
        command_list = []
        with Path.open(path) as fp:
            board_config_dir = json.load(fp)
        self.start_source = Source(self.config, START_SOURCE)
        self.stop_source = Source(self.config, STOP_SOURCE)
        command_list.append(self.start_source.from_dict(board_config_dir["start_source"], self.command_dict))
        command_list.append(self.stop_source.from_dict(board_config_dir["stop_source"], self.command_dict))
        connections = []
        for idx, conn_dict in enumerate(board_config_dir["connections"]):
            conn = Connection(
                self.config.connection_names,
                self.config,
                conn_type=conn_dict["conn_type"],
                default_config=NO_DEFAULT_CONFIG,
            )
            conn_cmd = conn.from_dict(conn_dict, idx, self.command_dict)
            connections.append(conn)
            command_list.append(conn_cmd)
        self.connections = connections
        return command_list

    def save_to_file(self, path: str):
        """Save board configuration to json file."""
        board_config_dir = {
            "start_source": self._start_source.to_dict(),
            "stop_source": self._stop_source.to_dict(),
            "connections": [],
        }
        for c in self.connections:
            board_config_dir["connections"].append(c.to_dict())
        with Path.open(Path(path), "w") as fp:
            json.dump(board_config_dir, fp)

    def start_measurement_command(self) -> bytes:
        """Create start measurement command."""
        cmd = self.command_dict["hello"] + self.command_dict["start"]
        return bytes.fromhex(cmd)

    def stop_measurement_command(self) -> bytes:
        """Create stop measurement command."""
        cmd = self.command_dict["hello"] + self.command_dict["stop"]
        return bytes.fromhex(cmd)

    def get_event_command(self, event_id: int) -> bytes:
        """Return byte command to get event from command dict."""
        cmd = self.command_dict["hello"] + self.command_dict["event"]
        event_id = event_id.to_bytes(2, "big")
        cmd = bytes.fromhex(cmd) + event_id
        return cmd

    def activate_buttons(self) -> Tuple[bytes, bytes]:
        """Create command to activate buttons."""
        print(self.command_dict["trigger"])
        button_1_cmd = (
            self.command_dict["hello"]
            + self.command_dict["event"]
            + self.command_dict["trigger"][1]["Button1"]
            + IS_ACTIVE
            + self.command_dict["event_sync_signal"][2]["Any Edge"]
        )
        button_2_cmd = (
            self.command_dict["hello"]
            + self.command_dict["event"]
            + self.command_dict["trigger"][2]["Button2"]
            + IS_ACTIVE
            + self.command_dict["event_sync_signal"][2]["Any Edge"]
        )
        return bytes.fromhex(button_1_cmd), bytes.fromhex(button_2_cmd)

    @property
    def start_source(self):
        """Return start source."""
        return self._start_source

    @start_source.setter
    def start_source(self, src):
        """Set start source."""
        self._start_source = src

    @property
    def stop_source(self):
        """Return stop source."""
        return self._stop_source

    @stop_source.setter
    def stop_source(self, src):
        """Set stop source."""
        self._stop_source = src

    def build_error_reset_command(self):
        """Create command to reset error state."""
        cmd = bytes.fromhex(self.command_dict["hello"] + self.command_dict["reset_error_state"])
        return cmd


class Source:
    """Class that holds information about a board source."""

    def __init__(
        self,
        config: HardwareConfig,
        source_type: str,
        source: int = DEFAULT_SOURCE,
        delay: int = DEFAULT_DELAY,
        sync_signal: Union[int, None] = None,
    ):
        self.config = config
        self._source_type = source_type
        self._source = source
        self._delay = delay
        self._sync_signal = sync_signal

    def update_source(
        self,
        command_dict: Dict[str, str],
        source: int,
        delay: Union[int, None] = DEFAULT_DELAY,
        sync_signal: Union[int, None] = DEFAULT_SYNC_SIGNAL,
    ):
        """Update source properties."""
        self.source = source
        self.delay = delay
        if self.source_type == START_SOURCE:
            source_name = self.config.start_source_mapping[self.source]
        else:
            source_name = self.config.stop_source_mapping[self.source]
        if source_name in self.config.source_with_edge:
            if sync_signal:
                self.sync_signal = sync_signal
            else:
                self.sync_signal = DEFAULT_SYNC_SIGNAL
        else:
            self.sync_signal = None
        return self._build_update_command(command_dict)

    def _build_update_command(self, command_dict: Dict[str, str]) -> bytes:
        hello = bytes.fromhex(command_dict["hello"])
        source_type = bytes.fromhex(command_dict[self._source_type])
        source_name = self._get_source_name()
        source = bytes.fromhex(command_dict["trigger"][self.source][source_name])
        sync_signal = b"\x00"
        delay = self._delay.to_bytes(2, "big")
        if self.sync_signal is not None:
            sync_signal = bytes.fromhex(
                command_dict["event_sync_signal"][self._sync_signal][SYNC_SIGNAL_MAPPING_SOURCE[self._sync_signal]]
            )
        cmd = hello + source_type + source + delay + sync_signal
        return cmd

    def to_dict(self):
        """Return source properties as dictionary."""
        source_dir = {
            "source_type": self._source_type,
            "source": self._source,
            "delay": self._delay,
            "sync_signal": self._sync_signal,
        }
        return source_dir

    def from_dict(self, source_dict, command_dict) -> bytes:
        """Update source properties based on dictionary content."""
        source = source_dict["source"]
        delay = source_dict["delay"]
        sync_signal = source_dict["sync_signal"]
        source_command = self.update_source(command_dict, source, delay, sync_signal)
        return source_command

    def _get_source_name(self) -> str:
        if self.source_type == START_SOURCE:
            source_name = self.config.start_source_mapping[self.source]
        else:
            source_name = self.config.stop_source_mapping[self.source]
        return source_name

    def is_edge_enabled(self) -> bool:
        """Return True if source is a connection."""
        edge_enabled = self._get_source_name() in self.config.source_with_edge
        return edge_enabled

    @property
    def source_type(self):
        """Return source type (start or stop source)."""
        return self._source_type

    @source_type.setter
    def source_type(self, source_type: str):
        """Set source type."""
        if source_type in [START_SOURCE, STOP_SOURCE]:
            self._source_type = source_type
        else:
            self._source_type = START_SOURCE

    @property
    def source(self):
        """Return source id."""
        return self._source

    @source.setter
    def source(self, source: int):
        """Set source id."""
        if self._source_type == START_SOURCE:
            source_max = len(self.config.start_source_mapping)
        else:
            source_max = len(self.config.stop_source_mapping)
        if 0 <= source < source_max:
            self._source = source
        else:
            self._source = 0

    @property
    def delay(self):
        """Return source delay."""
        return self._delay

    @delay.setter
    def delay(self, delay: int):
        """Set source delay."""
        if MIN_DELAY <= delay <= MAX_DELAY:
            self._delay = delay
        else:
            self._delay = DEFAULT_DELAY

    @property
    def sync_signal(self):
        """Return source sync signal."""
        return self._sync_signal

    @sync_signal.setter
    def sync_signal(self, sync_signal: Union[int, None]):
        """Set source sync signal."""
        if sync_signal:
            sync_signal_max = len(SYNC_SIGNAL_MAPPING_SOURCE)
            if 0 <= sync_signal < sync_signal_max:
                self._sync_signal = sync_signal
            else:
                self._sync_signal = 0
        else:
            self._sync_signal = sync_signal


class Connection:
    """Class that holds information about a board connection."""

    def __init__(
        self,
        connection_names: Sequence[str],
        config: HardwareConfig,
        conn_type: int = 0,
        delay: int = DEFAULT_DELAY,
        sync_signal: int = DEFAULT_SYNC_SIGNAL,
        is_active: bool = False,
        freq: Union[None, int] = None,
        degree: Union[None, int] = None,
        stop_trigger: bool = False,
        pulse_length: [None, int] = None,
        default_config: int = DEFAULT_DEVICE,
    ):
        self.connection_names = connection_names
        self.config = config
        self._conn_type = conn_type
        self._delay = delay
        self._sync_signal = sync_signal
        self._is_active = is_active
        self.freq = freq
        self.degree = degree
        self.pulse_length = pulse_length
        self._stop_trigger = stop_trigger
        self._default_config = default_config

    def update_connection(
        self,
        command_dict: Dict[str, str],
        conn_idx: int,
        is_active: bool,
        delay: int,
        sync_signal: int,
        freq: Union[None, int] = None,
        stop_trigger: Union[None, bool] = None,
        degree: Union[None, int] = None,
        pulse_length: Union[None, int] = None,
    ) -> bytes:
        """Update input/output connection properties."""
        self._is_active = is_active
        self.delay = delay
        self.sync_signal = sync_signal
        self.freq = freq
        self.stop_trigger = stop_trigger
        self.degree = degree
        self.pulse_length = pulse_length
        return self._build_update_command(command_dict, conn_idx)

    def update_bidirectional_connection(
        self,
        command_dict: Dict[str, str],
        conn_idx: int,
        delay: int,
        sync_signal: int,
        freq: Union[None, int] = None,
        stop_trigger: Union[None, bool] = None,
        degree: Union[None, int] = None,
        pulse_length: Union[None, int] = None,
    ):
        """Update bidirectional connection properties."""
        if self.conn_type == OUTPUT_CONNECTION:
            active_update_command = self.update_connection(
                command_dict,
                conn_idx,
                is_active=True,
                delay=delay,
                sync_signal=sync_signal,
                freq=freq,
                stop_trigger=stop_trigger,
                degree=degree,
                pulse_length=pulse_length,
            )

        else:
            # manipulate connection type to set output connection inactive first
            self.conn_type = OUTPUT_CONNECTION
            # reset connection type
            self.conn_type = INPUT_CONNECTION
            active_update_command = self._build_event_command(
                command_dict, conn_idx, is_active=True, sync_signal=sync_signal
            )
        return active_update_command

    def _toggle_bidirectional_connection(self, command_dict: Dict[str, str], conn_idx: int, is_visible) -> bytes:
        """Toggle bidirectional connection."""
        if self.conn_type == OUTPUT_CONNECTION:
            update_command = self.update_connection(
                command_dict,
                conn_idx,
                is_active=not self.is_active,
                delay=self.delay,
                sync_signal=self.sync_signal,
                freq=self.freq,
                stop_trigger=self.stop_trigger,
                degree=self.degree,
                pulse_length=self.pulse_length,
            )
        else:
            update_command = self._build_event_command(
                command_dict, conn_idx=conn_idx, is_active=not is_visible, sync_signal=self.sync_signal
            )
        return update_command

    def toggle_connection(
        self, command_dict: Dict[str, str], conn_idx, is_visible: bool, is_bidirectional: bool = False
    ) -> bytes:
        """Toggle connection active/inactive."""
        if is_bidirectional:
            return self._toggle_bidirectional_connection(command_dict, conn_idx, is_visible)
        self._is_active = not self._is_active
        return self._build_update_command(command_dict, conn_idx)

    def to_dict(self) -> dict:
        """Return connection properties as dictionary."""
        connection_dir = {
            "conn_type": self._conn_type,
            "delay": self._delay,
            "sync_signal": self._sync_signal,
            "pulse_length": self.pulse_length,
            "is_active": self._is_active,
            "freq": self.freq,
            "stop_trigger": self._stop_trigger,
            "degree": self.degree,
        }
        return connection_dir

    def from_dict(self, conn_dict, conn_idx, command_dict) -> Tuple[bytes, bytes]:
        """Update connection properties from dictionary content."""
        delay = conn_dict["delay"]
        sync_signal = conn_dict["sync_signal"]
        is_active = conn_dict["is_active"]
        freq = conn_dict["freq"]
        pulse_length = conn_dict["pulse_length"]
        degree = conn_dict["degree"]
        stop_trigger = conn_dict["stop_trigger"]
        connection_command = self.update_connection(
            command_dict, conn_idx, is_active, delay, sync_signal, freq, degree, stop_trigger, pulse_length
        )
        return connection_command

    def _build_update_command(self, command_dict, conn_idx) -> bytes:
        hello = bytes.fromhex(command_dict["hello"])
        conn_type = bytes.fromhex(command_dict[self.config.connection_mapping[self._conn_type]])
        conn_name = bytes.fromhex(command_dict["connection"][conn_idx][self.connection_names[conn_idx]])
        activity = bytes.fromhex(command_dict["activity"][int(self._is_active)][str(int(self._is_active))])
        delay = self._delay.to_bytes(2, "big")
        signal = bytes.fromhex(
            command_dict["sync_signal"][self._sync_signal][SYNC_SIGNAL_MAPPING_OUTPUT[self._sync_signal]]
        )
        pulse_length = self._pulse_length.to_bytes(2, "big")
        freq = self._freq.to_bytes(2, "big")
        if "trigger" in SYNC_SIGNAL_MAPPING_OUTPUT[self._sync_signal].lower():
            # trigger signal will break otherwise
            freq = DEFAULT_FREQ.to_bytes(2, "big")
        stop_trigger = bytes.fromhex(command_dict["stop_trigger"][STOP_TRIGGER_MAPPING[self._stop_trigger]])
        degree = self._degree.to_bytes(1, "big")

        cmd = hello + conn_type + conn_name + activity + delay + signal + pulse_length + freq + stop_trigger + degree
        return cmd

    def _build_event_command(self, command_dict, conn_idx, is_active, sync_signal):
        hello = bytes.fromhex(command_dict["hello"])
        event = bytes.fromhex(command_dict["event"])
        conn_name = bytes.fromhex(command_dict["connection"][conn_idx][self.connection_names[conn_idx]])
        activity = bytes.fromhex(command_dict["activity"][int(is_active)][str(int(is_active))])
        signal = bytes.fromhex(command_dict["event_sync_signal"][sync_signal][SYNC_SIGNAL_MAPPING_INPUT[sync_signal]])
        cmd = hello + event + conn_name + activity + signal
        return cmd

    @property
    def delay(self):
        """Return delay."""
        return self._delay

    @delay.setter
    def delay(self, delay: int):
        """Set delay."""
        if MIN_DELAY <= delay <= MAX_DELAY:
            self._delay = delay
        else:
            self._delay = DEFAULT_DELAY

    @property
    def sync_signal(self):
        """Return sync signal."""
        return self._sync_signal

    @sync_signal.setter
    def sync_signal(self, sync_signal: int):
        """Set sync signal."""
        if self.conn_type == INPUT_CONNECTION:
            sync_signal_max = len(SYNC_SIGNAL_MAPPING_INPUT)
        else:
            sync_signal_max = len(SYNC_SIGNAL_MAPPING_OUTPUT)
        if 0 <= sync_signal < sync_signal_max:
            self._sync_signal = sync_signal
        else:
            self._sync_signal = 0

    @property
    def pulse_length(self):
        """Return pulse length for triggers."""
        return self._pulse_length

    @pulse_length.setter
    def pulse_length(self, pulse_length: Union[None, int]):
        """Set trigger pulse length."""
        if pulse_length is not None:
            if MIN_PULSE_LEN <= pulse_length <= MAX_PULSE_LEN:
                self._pulse_length = pulse_length
            else:
                self._pulse_length = DEFAULT_PULSE_LENGTH
        elif self._conn_type == OUTPUT_CONNECTION:
            self._pulse_length = DEFAULT_PULSE_LENGTH
        else:
            self._pulse_length = None

    @property
    def freq(self):
        """Return clock frequency."""
        return self._freq

    @freq.setter
    def freq(self, freq: Union[None, int]):
        """Set clock frequency."""
        if freq is not None:
            if MIN_FREQ <= freq <= MAX_FREQ:
                self._freq = freq
            else:
                self._freq = DEFAULT_FREQ
        elif self._conn_type == OUTPUT_CONNECTION:
            self._freq = DEFAULT_FREQ
        else:
            self._freq = None

    @property
    def degree(self):
        """Return m-sequence degree."""
        return self._degree

    @degree.setter
    def degree(self, degree: Union[None, int]):
        """Set m-sequence degree."""
        if degree is not None:
            if MIN_DEGREE <= degree <= MAX_DEGREE:
                self._degree = degree
            else:
                self._degree = DEFAULT_DEGREE
        elif self._conn_type == OUTPUT_CONNECTION:
            self._degree = DEFAULT_DEGREE
        else:
            self._degree = None

    @property
    def conn_type(self):
        """Return connection type."""
        return self._conn_type

    @conn_type.setter
    def conn_type(self, conn_type: Union[None, int]):
        """Set connection type."""
        if 0 <= conn_type < len(self.config.connection_mapping):
            self._conn_type = conn_type
        else:
            self._conn_type = 0

    @property
    def stop_trigger(self):
        """Return stop trigger."""
        return self._stop_trigger

    @stop_trigger.setter
    def stop_trigger(self, stop_trigger: Union[None, bool]):
        """Set stop trigger."""
        self._stop_trigger = stop_trigger

    @property
    def default_config(self):
        """Return default configuration."""
        return self._default_config

    @default_config.setter
    def default_config(self, default_config: int):
        """Set default configuration."""
        # NO_DEFAULT_CONFIG = -1 => manual configuration selected instead
        if NO_DEFAULT_CONFIG <= default_config < len(DEFAULT_DEVICES):
            self._default_config = default_config
        else:
            self._default_config = DEFAULT_DEVICE

    @property
    def is_active(self):
        """Return whether connection is active."""
        return self._is_active
