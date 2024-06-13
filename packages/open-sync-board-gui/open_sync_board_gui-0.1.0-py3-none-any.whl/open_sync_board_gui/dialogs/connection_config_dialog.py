"""Classes for all connection configuration dialogs."""

import abc
from typing import List

from PySide2.QtWidgets import QCheckBox, QDialog, QGroupBox, QLabel, QRadioButton, QSpinBox, QWidget

from open_sync_board_gui.components import (
    Ui_InOutConnectionConfigDialog,
    Ui_InputConnectionConfigDialog,
    Ui_OutputConnectionConfigDialog,
)
from open_sync_board_gui.constants import (
    DEFAULT_DEVICES,
    DEFAULT_SYNC_SIGNAL,
    DEFAULT_VALUE,
    DEVICE_SETTINGS,
    INPUT_CONNECTION,
    NO_DEFAULT_CONFIG,
    OUTPUT_CONNECTION,
    SYNC_SIGNAL_MAPPING_INPUT,
    SYNC_SIGNAL_MAPPING_OUTPUT,
    SYNC_SIGNAL_WITHOUT_DEGREE,
    SYNC_SIGNAL_WITHOUT_FREQ,
    SYNC_SIGNAL_WITHOUT_PULSE_LENGTH,
    SYNC_SIGNAL_WITHOUT_STOP_TRIGGER,
)
from open_sync_board_gui.utils import Connection


class ConnectionConfigDialog(QDialog):
    """Base class for all connection configuration dialogs."""

    __metaclass__ = abc.ABCMeta

    def __init__(self, main_window: QWidget, conn: Connection, conn_idx: int):
        super().__init__()
        self.main_window = main_window
        self.connection = conn
        self.connection_index = conn_idx
        self.connection_update_command = ""
        self.user_hint = ""
        self.optional_update_command = ""

    def get_data(self):
        """Return the data entered by the user after dialog closes."""
        return self.connection_update_command, self.user_hint

    def _setup_ui(self):
        self.ui.setupUi(self)
        self.ui.buttonBox.accepted.connect(self.update_connection)
        self.ui.buttonBox.rejected.connect(self.reject)
        self.ui.delay.setValue(self.connection.delay)
        self.ui.sync_signal.setCurrentIndex(self.connection.sync_signal)

    @abc.abstractmethod
    def update_connection(self):
        """Update connection according to the selected settings."""
        return


class InputConnectionConfigDialog(ConnectionConfigDialog):
    """Dialog for configuring input connections."""

    def __init__(self, main_window: QWidget, conn: Connection, conn_idx: int):
        super().__init__(main_window, conn, conn_idx)
        self.ui = Ui_InputConnectionConfigDialog()
        self._setup_ui()
        self.ui.sync_signal.setCurrentIndex(self.connection.sync_signal)

    def update_connection(self):
        """Update connection according to the selected settings."""
        delay = self.ui.delay.value()
        sync_signal = self.ui.sync_signal.currentText()
        sync_signal = SYNC_SIGNAL_MAPPING_INPUT.index(sync_signal)
        self.connection_update_command = self.connection.update_connection(
            self.main_window.board_config.command_dict,
            conn_idx=self.connection_index,
            is_active=True,
            delay=delay,
            sync_signal=sync_signal,
        )


class OutputConnectionConfigDialog(ConnectionConfigDialog):
    """Dialog for configuring output connections."""

    def __init__(
        self,
        main_window: QWidget,
        conn: Connection,
        conn_idx: int,
        init_ui: object = Ui_OutputConnectionConfigDialog(),
    ):
        super().__init__(main_window, conn, conn_idx)
        self.ui = init_ui
        self._setup_ui()
        self.ui.sync_signal.setCurrentIndex(self.connection.sync_signal)
        self.ui.sync_signal.currentIndexChanged.connect(self._control_sync_signal_dependent_boxes)
        self.ui.pulse_length.setValue(self.connection.pulse_length)
        self.ui.frequency.setValue(self.connection.freq)
        self.ui.stop_trigger.setChecked(self.connection.stop_trigger)
        self.ui.degree.setValue(self.connection.degree)
        self.ui.default_config_radio.toggled.connect(self._toggle_default_config)
        self.ui.manual_config_radio.toggled.connect(self._toggle_manual_config)
        self.ui.manual_config.setEnabled(False)
        self.ui.sensor.addItems(DEFAULT_DEVICES)
        self.ui.sensor.currentIndexChanged.connect(self._load_default_config)
        self._control_sync_signal_dependent_boxes()
        self._set_configuration_option()
        if self.connection.default_config is not NO_DEFAULT_CONFIG:
            self._load_default_config()

    def _load_default_config(self):
        properties = {
            "delay": self.ui.delay,
            "pulse_length": self.ui.pulse_length,
            "freq": self.ui.frequency,
            "stop_trigger": self.ui.stop_trigger,
            "degree": self.ui.degree,
        }
        """Load default properties based on the selected device."""
        selected_device = DEFAULT_DEVICES[self.ui.sensor.currentIndex()]
        self.ui.sync_signal.setCurrentIndex(DEVICE_SETTINGS[selected_device]["sync_signal"])
        self.ui.frequency.setValue(DEVICE_SETTINGS[selected_device]["freq"])
        self.ui.frequency.setDisabled(True)  # keep disabled even when value changes
        self.ui.stop_trigger.setChecked(DEVICE_SETTINGS[selected_device]["stop_trigger"])

        for name, component in properties.items():
            if name in DEVICE_SETTINGS[selected_device]:
                if isinstance(component, QSpinBox):
                    component.setValue(DEVICE_SETTINGS[selected_device][name])
                elif isinstance(component, QCheckBox):
                    component.setChecked(DEVICE_SETTINGS[selected_device][name])
                component.setDisabled(True)
            elif isinstance(component, QSpinBox):
                component.setValue(DEFAULT_VALUE)
            elif isinstance(component, QCheckBox):
                component.setChecked(False)

    def _control_sync_signal_dependent_boxes(self):
        """Enable some fields only when the sync signal is set to a certain value."""
        sync_signal = self.ui.sync_signal.currentText()
        self._control_spin_box(
            sync_signal,
            SYNC_SIGNAL_WITHOUT_PULSE_LENGTH,
            self.ui.pulse_length_label,
            self.ui.pulse_length,
            self.connection.pulse_length,
        )
        self._control_spin_box(
            sync_signal, SYNC_SIGNAL_WITHOUT_FREQ, self.ui.frequency_label, self.ui.frequency, self.connection.freq
        )
        self._control_spin_box(
            sync_signal, SYNC_SIGNAL_WITHOUT_DEGREE, self.ui.degree_label, self.ui.degree, self.connection.degree
        )
        self._control_check_box(sync_signal, SYNC_SIGNAL_WITHOUT_STOP_TRIGGER, self.ui.stop_trigger)

    def _control_spin_box(
        self,
        sync_signal: str,
        disabling_signals: List[str],
        label: QLabel,
        component: QSpinBox,
        default_value: int = 0,
    ):
        """Based on selected sync signal, decide whether it makes sense to enable the given component."""
        disable = False
        if sync_signal in disabling_signals:
            component.setValue(default_value)
            disable = True
        component.setDisabled(disable)
        label.setDisabled(disable)
        # disable after switching back from manual config
        if self.ui.default_config_radio.isChecked():
            component.setDisabled(True)
            label.setDisabled(True)

    def _control_check_box(
        self,
        sync_signal: str,
        disabling_signals: List[str],
        component: QSpinBox,
    ):
        disable = False
        if sync_signal in disabling_signals:
            component.setChecked(False)
            disable = True
        component.setDisabled(disable)
        # disable after switching back from manual config
        if self.ui.default_config_radio.isChecked():
            component.setDisabled(True)

    def _set_configuration_option(self):
        """Activate either default or manual configuration groupbox based on previous user input."""
        if self.connection.default_config == NO_DEFAULT_CONFIG:
            self.ui.default_config_radio.setChecked(False)
            self.ui.default_config.setEnabled(False)
            self.ui.manual_config_radio.setChecked(True)
            self.ui.manual_config.setEnabled(True)
        else:
            self.ui.default_config_radio.setChecked(True)
            self.ui.default_config.setEnabled(True)
            self.ui.manual_config_radio.setChecked(False)
            self.ui.manual_config.setEnabled(False)
            self.ui.sensor.setCurrentIndex(self.connection.default_config)

    def _toggle_default_config(self):
        is_checked = self.ui.default_config_radio.isChecked()
        self.ui.manual_config.setEnabled(not is_checked)
        self.ui.manual_config_radio.setChecked(not is_checked)
        self._control_sync_signal_dependent_boxes()
        if is_checked:
            self._load_default_config()

    def _toggle_manual_config(self):
        is_checked = self.ui.manual_config_radio.isChecked()
        self.ui.default_config.setEnabled(not is_checked)
        self.ui.default_config_radio.setChecked(not is_checked)
        self._control_sync_signal_dependent_boxes()

    def update_connection(self):
        """Update connection based on user input."""
        delay = self.ui.delay.value()
        sync_signal = self.ui.sync_signal.currentText()
        sync_signal = SYNC_SIGNAL_MAPPING_OUTPUT.index(sync_signal)
        pulse_length = self.ui.pulse_length.value()
        freq = self.ui.frequency.value()
        stop_trigger = self.ui.stop_trigger.isChecked()
        degree = self.ui.degree.value()
        self.connection_update_command = self.connection.update_connection(
            self.main_window.board_config.command_dict,
            conn_idx=self.connection_index,
            is_active=True,
            delay=delay,
            sync_signal=sync_signal,
            pulse_length=pulse_length,
            freq=freq,
            stop_trigger=stop_trigger,
            degree=degree,
        )
        # reset user hint
        self.user_hint = ""
        self._update_default_config()

    def _update_default_config(self, is_bidirectional: bool = False):
        # update default_config property
        if self.ui.default_config_radio.isChecked():
            # default device is specified
            self.connection.default_config = self.ui.sensor.currentIndex()
            if is_bidirectional:
                self.user_hint += (
                    f"Please move the other jumper to the position marked with "
                    f"{DEVICE_SETTINGS[DEFAULT_DEVICES[self.connection.default_config]]['logic_level']} [Volt] to set "
                    f"the right voltage.\n Furthermore, please use "
                    f"{DEVICE_SETTINGS[DEFAULT_DEVICES[self.connection.default_config]]['plug']}"
                )
            else:
                self.user_hint += (
                    f"Before connecting the device, please move the little plastic"
                    f" jumper regulating the voltage to the position marked with "
                    f"{DEVICE_SETTINGS[DEFAULT_DEVICES[self.connection.default_config]]['logic_level']} [Volt].\n"
                )
            self.user_hint += (
                f"Furthermore, please use {DEVICE_SETTINGS[DEFAULT_DEVICES[self.connection.default_config]]['plug']}"
                f" as plug for the selected device."
            )
        else:
            # configuration was done manually
            self.connection.default_config = NO_DEFAULT_CONFIG


class InputOutputConnectionConfigDialog(OutputConnectionConfigDialog):
    """Dialog for configuring connections that can be used both as input and output connections."""

    def __init__(self, main_window: QWidget, conn: Connection, conn_idx: int):
        super().__init__(main_window, conn, conn_idx, init_ui=Ui_InOutConnectionConfigDialog())
        self.connection_update_command = ""
        self._set_configuration_option()

    def _setup_ui(self):
        super()._setup_ui()
        if self.connection.conn_type == INPUT_CONNECTION:
            event_signal = self.connection.sync_signal
        else:
            event_signal = DEFAULT_SYNC_SIGNAL
        self.ui.event_signal.setCurrentIndex(event_signal)
        self.ui.event_config_radio.toggled.connect(self._toggle_event_config)

    def _set_configuration_option(self):
        """Set configuration dialog according to selected options.

        Activate event configuration groupbox when md is set as input device,
        or either default or manual configuration groupbox based on previous user input when md is set as output device.
        """
        if self.connection.conn_type == INPUT_CONNECTION:
            self.ui.default_config_radio.setChecked(False)
            self.ui.default_config.setEnabled(False)
            self.ui.manual_config_radio.setChecked(False)
            self.ui.manual_config.setEnabled(False)
            self.ui.event_config_radio.setChecked(True)
            self.ui.event_config.setEnabled(True)
        else:
            has_default_config = self.connection.default_config != NO_DEFAULT_CONFIG
            self.ui.default_config_radio.setChecked(has_default_config)
            self.ui.default_config.setEnabled(has_default_config)
            self.ui.manual_config_radio.setChecked(not has_default_config)
            self.ui.manual_config.setEnabled(not has_default_config)
            self.ui.event_config_radio.setChecked(False)
            self.ui.event_config.setEnabled(False)
            if has_default_config:
                self.ui.sensor.setCurrentIndex(self.connection.default_config)

    def _toggle_default_config(self):
        is_checked = self.ui.default_config_radio.isChecked()
        if is_checked:
            self._handle_config(self.ui.default_config, self.ui.default_config_radio, is_checked)
            self._handle_config(self.ui.event_config, self.ui.event_config_radio, not is_checked)
            self._handle_config(self.ui.manual_config, self.ui.manual_config_radio, not is_checked)
            self._control_sync_signal_dependent_boxes()

    def _toggle_manual_config(self):
        is_checked = self.ui.manual_config_radio.isChecked()
        if is_checked:
            self._handle_config(self.ui.manual_config, self.ui.manual_config_radio, is_checked)
            self._handle_config(self.ui.event_config, self.ui.event_config_radio, not is_checked)
            self._handle_config(self.ui.default_config, self.ui.default_config_radio, not is_checked)
            self._control_sync_signal_dependent_boxes()

    def _toggle_event_config(self):
        is_checked = self.ui.event_config_radio.isChecked()
        if is_checked:
            self._handle_config(self.ui.event_config, self.ui.event_config_radio, is_checked)
            self._handle_config(self.ui.manual_config, self.ui.manual_config_radio, not is_checked)
            self._handle_config(self.ui.default_config, self.ui.default_config_radio, not is_checked)
        # self._control_sync_signal_dependent_boxes()

    def _handle_config(self, config: QGroupBox, radio: QRadioButton, enable=True):
        config.setEnabled(enable)
        radio.setChecked(enable)

    def update_connection(self):
        """Update connection based on user input."""
        self.user_hint = ""
        delay = self.ui.delay.value()
        sync_signal = self.ui.sync_signal.currentText()
        sync_signal = SYNC_SIGNAL_MAPPING_OUTPUT.index(sync_signal)
        event_signal = self.ui.event_signal.currentText()
        event_signal = SYNC_SIGNAL_MAPPING_INPUT.index(event_signal)
        freq = self.ui.frequency.value()
        stop_trigger = self.ui.stop_trigger.isChecked()
        degree = self.ui.degree.value()
        conn_type = INPUT_CONNECTION if self.ui.event_config_radio.isChecked() else OUTPUT_CONNECTION
        self.connection.conn_type = conn_type
        if conn_type == OUTPUT_CONNECTION:
            self.connection_update_command = self.connection.update_bidirectional_connection(
                self.main_window.board_config.command_dict,
                self.connection_index,
                delay=delay,
                sync_signal=sync_signal,
                freq=freq,
                stop_trigger=stop_trigger,
                degree=degree,
            )
            self.user_hint = "Please make sure one little plastic jumper is at the position marked with `OUT`!\n"

        else:
            self.connection_update_command = self.connection.update_bidirectional_connection(
                self.main_window.board_config.command_dict,
                self.connection_index,
                delay=delay,
                sync_signal=event_signal,
                freq=freq,
                stop_trigger=stop_trigger,
                degree=degree,
            )
            self.user_hint = "Please move the little plastic jumper to the position marked with `IN`!"

        self._update_default_config(is_bidirectional=True)

    def get_data(self):
        """Access connection update commands and user hint after dialog was closed."""
        return self.connection_update_command, self.user_hint
