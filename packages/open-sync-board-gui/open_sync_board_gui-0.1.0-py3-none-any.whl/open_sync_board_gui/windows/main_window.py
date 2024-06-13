"""Main Window of the GUI."""
import sys
from datetime import datetime
from pathlib import Path
from time import sleep
from typing import Dict, List

from PySide2.QtCore import QTimer
from PySide2.QtGui import QIcon, Qt
from PySide2.QtWidgets import (
    QApplication,
    QComboBox,
    QFileDialog,
    QMessageBox,
    QProgressDialog,
    QToolButton,
    QWidget,
)

from open_sync_board_gui.components import Ui_MainWindowV3
from open_sync_board_gui.config.hardware_config import HardwareConfig, resolve_path
from open_sync_board_gui.constants import (
    ACTIVE_CONNECTION_COLOR,
    BLACK_FONT_COLOR,
    BOARD_VERSION_V3,
    COMMAND_FILE_PATH,
    CSV_SEPARATOR,
    ERROR_MODE,
    IDLE_MODE,
    INACTIVE_CONNECTION_COLOR,
    INPUT_CONNECTION,
    MESSAGE_START,
    MESSAGE_STOP,
    OUTPUT_CONNECTION,
    PAYLOAD_TIME,
    PAYLOAD_TYPE,
    RUNNING_MODE,
    START_MODE,
    START_SOURCE,
    STOP_MODE,
)
from open_sync_board_gui.dialogs import (
    ConfigImportDialog,
    InputConnectionConfigDialog,
    OutputConnectionConfigDialog,
    SourceConfigDialog,
)
from open_sync_board_gui.dialogs.connection_config_dialog import InputOutputConnectionConfigDialog
from open_sync_board_gui.dialogs.event_location_dialog import EventLogDialog
from open_sync_board_gui.utils import BoardConfig, BoardConnectionError, BoardConnector


class MainWindow(QWidget):
    """Main Window class."""

    def __init__(self, mock_mode=True, version=BOARD_VERSION_V3):
        super().__init__()
        self.version = version
        # setup ui
        if version == BOARD_VERSION_V3:
            self.ui = Ui_MainWindowV3()
        # new versions can be added here
        else:
            raise NotImplementedError(f"There is no software available for version {version}!")
        self.hw_config = HardwareConfig(version).load()

        self.ui.setupUi(self)
        # connect signals and slots
        self.setting_buttons = self._setup_setting_buttons()
        self.connection_buttons = self._setup_connection_buttons()
        self.ui.config_import_button.clicked.connect(self.get_import_paths)
        self.ui.play_button.clicked.connect(self.toggle_measurement)
        self.ui.config_export_button.clicked.connect(self.export_config)
        self.ui.start_settings.clicked.connect(self.open_source_dialog)
        self.ui.stop_settings.clicked.connect(self.open_source_dialog)
        # setup helper objects
        self.connector = BoardConnector(parent=self, config=self.hw_config, mock=mock_mode)
        self.board_config = self._setup_board_config()
        self.board_config.setup_connections(connection_list=self.hw_config.connection_types)
        self.ui.start_source.setCurrentIndex(self.board_config.start_source.source)
        self.ui.stop_source.setCurrentIndex(self.board_config.stop_source.source)
        self.command_queue = []
        self.config_path = None
        self.logging_window = None
        self.measurement_is_running = False
        # connect to board connector - this might take a while
        self.connector_setup()
        # after successful connector setup, send first commands
        self.init_start_stop_source()
        self.activate_buttons()
        self.ui.start_source.currentIndexChanged.connect(self.change_start_source)
        self._set_source_button_activation(self.ui.start_source, mode=START_MODE)
        self.ui.stop_source.currentIndexChanged.connect(self.change_stop_source)
        self._set_source_button_activation(self.ui.stop_source, mode=STOP_MODE)
        self.event_log_path = self._get_log_location()
        if mock_mode:
            QTimer.singleShot(100, self._mock_mode_warning)

    def _mock_mode_warning(self):
        msg = QMessageBox()
        msg.setWindowTitle("Attention!")
        msg.setText(
            "You are currently in mock mode for debugging! No commands are sent to the SyncBoard. "
            "Change the mock_mode flag to `False` in start_gui.py if this is a mistake."
        )
        msg.setIcon(QMessageBox.Information)
        msg.exec_()

    def _get_log_location(self):
        d = EventLogDialog(self)
        d.exec_()
        d.show()
        return d.get_data()

    def _setup_board_config(self):
        bc = BoardConfig(self.hw_config)
        try:
            bc.setup_command_dict()
        except Exception as e:  # noqa: BLE001
            msg = QMessageBox()
            msg.setWindowTitle("Setup error")
            msg.setText(
                f"Reading of command file failed with the following error: {e}. "
                f"Make sure a file {Path(resolve_path(COMMAND_FILE_PATH[self.hw_config.version])).absolute()} exists!"
            )
            msg.setIcon(QMessageBox.Warning)
            ret = msg.exec_()
            if ret:
                self.close()
        return bc

    def _setup_setting_buttons(self) -> List[QToolButton]:
        setting_buttons = [
            button
            for name, button in sorted(self.ui.__dict__.items())
            if all([name.startswith("md"), name.endswith("settings")])
        ]
        for button in setting_buttons:
            button.setVisible(False)
            button.clicked.connect(self.open_config_dialog)
        return setting_buttons

    def _setup_connection_buttons(self) -> List[QToolButton]:
        connection_buttons = [
            button
            for name, button in sorted(self.ui.__dict__.items())
            if all([name.startswith("md"), name.endswith("button")])
        ]
        for button in connection_buttons:
            button.clicked.connect(self.toggle_connection)
        return connection_buttons

    def connector_setup(self):
        """Initialize board connector and start searching for port connected to board."""
        progress = QProgressDialog(labelText="Searching for Board...", cancelButtonText="Cancel", parent=self)
        progress.setWindowTitle("Please wait")
        progress.setWindowModality(Qt.WindowModal)
        progress.setValue(0)
        # needs to be called manually after every progress update bc. main event loop is blocked
        QApplication.processEvents()
        progress.show()
        try:
            self.connector.setup(progress)
            self.connector.error_signal.sig.connect(self.board_message_received)
            self.connector.status_signal.sig.connect(self.handle_status_change)
            self.connector.event_signal.sig.connect(self.log_event)
            self.connector.start()
            QApplication.processEvents()
        except BoardConnectionError as e:
            msg = QMessageBox()
            msg.setWindowTitle("Connection error")
            msg.setText(f"{e.message}")
            msg.setIcon(QMessageBox.Warning)
            ret = msg.exec_()
            if ret:
                sys.exit(1)

    def init_start_stop_source(self):
        """Set initial start and stop source for board."""
        # as board interprets "Button 1" as default values, we need to change it to USB on initialisation
        self.change_start_source()
        self.change_stop_source()

    def activate_buttons(self):
        """Activate buttons as possible event input sources.

        They are activated directly after startup and remain active during the entire measurement.
        """
        for cmd in self.board_config.activate_buttons():
            self.connector.send_command(cmd)

    def toggle_connection(self):
        """Toggle connection active/inactive."""
        button = self.sender()
        name = button.objectName().split("_")[0]
        connection_list_idx = self.hw_config.connection_names.index(name)
        connection = self.board_config.connections[connection_list_idx]
        is_visible = self._toggle_connection_frontend(button)
        self._toggle_connection_backend(connection, connection_list_idx, is_visible=is_visible)

    def _toggle_connection_frontend(self, button):
        button_list_idx = self.connection_buttons.index(button)
        # toggle visibility of settings button
        settings_button = self.setting_buttons[button_list_idx]
        is_visible = settings_button.isVisible()
        settings_button.setVisible(not is_visible)
        # toggle color
        if is_visible:
            button.setStyleSheet(f"background-color : {INACTIVE_CONNECTION_COLOR}; {BLACK_FONT_COLOR}")
        else:
            button.setStyleSheet(f"background-color : {ACTIVE_CONNECTION_COLOR}; {BLACK_FONT_COLOR}")
        return is_visible

    def _toggle_connection_backend(self, connection, index, is_visible):
        is_bidirectional = self.hw_config.connection_names[index] in self.hw_config.bidirectional_connections
        # update connection state
        update_command = connection.toggle_connection(
            self.board_config.command_dict, index, is_visible, is_bidirectional
        )
        self.connector.send_command(update_command)

    def _reset_connection_button(self, button: QToolButton):
        button_list_idx = self.connection_buttons.index(button)
        # reset visibility of settings button
        settings_button = self.setting_buttons[button_list_idx]
        settings_button.setVisible(False)
        # reset color
        button.setStyleSheet(f"background-color : {INACTIVE_CONNECTION_COLOR}; {BLACK_FONT_COLOR}")

    def open_source_dialog(self):
        """Open dialog to configure start/stop source."""
        name = self.sender().objectName().split("_")[0]
        source = self.board_config.start_source if name in START_SOURCE else self.board_config.stop_source
        d = SourceConfigDialog(self, source)
        d.exec_()
        d.show()
        update_command = d.get_data()
        if update_command:
            self.connector.send_command(update_command)

    def open_config_dialog(self):
        """Open dialog to configure connection."""
        if self.sender().isVisible():
            name = self.sender().objectName().split("_")[0]
            connection_list_idx = self.hw_config.connection_names.index(name)
            conn = self.board_config.connections[connection_list_idx]
            if name in self.hw_config.bidirectional_connections:  # md serves as in- and output
                d = InputOutputConnectionConfigDialog(self, conn, connection_list_idx)
            elif conn.conn_type == INPUT_CONNECTION:
                d = InputConnectionConfigDialog(self, conn, connection_list_idx)
            elif conn.conn_type == OUTPUT_CONNECTION:
                d = OutputConnectionConfigDialog(self, conn, connection_list_idx)
            else:
                raise ValueError(f"Invalid connection type {conn.conn_type}!")
            d.exec_()
            d.show()
            connection_update_command, user_hint = d.get_data()
            if connection_update_command:
                self.connector.send_command(connection_update_command)
            if user_hint:
                msg = QMessageBox()
                msg.setWindowTitle("Device selected! What's next?")
                msg.setText(f"{user_hint}")
                msg.setIcon(QMessageBox.Information)
                msg.exec_()

    def _set_source_button_activation(self, dropdown: QComboBox, mode: str):
        # either "start"-icon is currently displayed, board idle;
        # or "stop"-icon is currently displayed, measurement is running
        if any(
            [mode == START_MODE and not self.measurement_is_running, mode == STOP_MODE and self.measurement_is_running]
        ):
            is_usb = dropdown.currentText() == "GUI"
            # starting from GUI only possible when start source set to usb
            self.ui.play_button.setDisabled(not is_usb)

    def _handle_connection_activity(self, sources: List[QComboBox], changed_source_value=None):
        for conn in self.hw_config.bidirectional_connections:
            index = self.hw_config.connection_names.index(conn)
            settings_button = self.setting_buttons[index]
            connection_button = self.connection_buttons[index]
            is_visible = conn not in [source.currentText().lower() for source in sources]
            connection_button.setEnabled(is_visible)
            if not is_visible:
                settings_button.setVisible(is_visible)
                connection_button.setStyleSheet(f"background-color : {INACTIVE_CONNECTION_COLOR}; {BLACK_FONT_COLOR}")
                if changed_source_value.lower() in self.hw_config.bidirectional_connections:
                    user_hint = (
                        f"Please make sure the little plastic jumper next to {conn.upper()} "
                        f"is at the position marked with `IN`!"
                    )
                    msg = QMessageBox()
                    msg.setWindowTitle("Measurement Device selected as source! What's next?")
                    msg.setText(f"{user_hint}")
                    msg.setIcon(QMessageBox.Information)
                    msg.exec_()

    def change_start_source(self):
        """Change start source."""
        text = self.ui.start_source.currentText()
        idx = self.hw_config.start_source_mapping.index(text)
        update_command = self.board_config.start_source.update_source(
            self.board_config.command_dict,
            idx,
            self.board_config.start_source.delay,
            self.board_config.start_source.sync_signal,
        )
        self._set_source_button_activation(self.ui.start_source, mode=START_MODE)  # only enable when USB is selected
        self._handle_connection_activity(
            [self.ui.start_source, self.ui.stop_source], changed_source_value=self.ui.start_source.currentText()
        )
        self.connector.send_command(update_command)

    def change_stop_source(self):
        """Change stop source."""
        text = self.ui.stop_source.currentText()
        idx = self.hw_config.stop_source_mapping.index(text)
        update_command = self.board_config.stop_source.update_source(
            self.board_config.command_dict,
            idx,
            self.board_config.stop_source.delay,
            self.board_config.stop_source.sync_signal,
        )
        self._set_source_button_activation(self.ui.stop_source, mode=STOP_MODE)  # only enable when USB is selected
        self._handle_connection_activity(
            [self.ui.start_source, self.ui.stop_source], changed_source_value=self.ui.stop_source.currentText()
        )
        self.connector.send_command(update_command)

    def get_import_paths(self):
        """Open dialog to get paths to config and event file."""
        d = ConfigImportDialog(self)
        d.exec_()
        d.show()
        config_path = d.get_data()
        # update config
        if config_path:
            self.config_path = config_path
            self._update_config()

    def toggle_measurement(self):
        """Start or stop measurement."""
        if self.measurement_is_running:
            self._stop_measurement()
            self.measurement_is_running = not self.measurement_is_running
            self._set_source_button_activation(self.ui.start_source, mode=START_MODE)
        else:
            self._start_measurement()
            self.measurement_is_running = not self.measurement_is_running
            self._set_source_button_activation(self.ui.stop_source, mode=STOP_MODE)

    def _start_measurement(self, triggered_by_user=True):
        self.ui.play_button.setIcon(QIcon(":/icons/stop.png"))
        self._change_status_led(mode=RUNNING_MODE)
        # stopping from GUI only possible when stop source set to usb
        self._set_source_button_activation(self.ui.stop_source, mode=STOP_MODE)
        # send command to board (if start was triggered by user and not a status change of board)
        if triggered_by_user:
            cmd = self.board_config.start_measurement_command()
            self.connector.send_command(cmd)

    def _stop_measurement(self, triggered_by_user=True):
        self.ui.play_button.setIcon(QIcon(":/icons/start.png"))
        self._change_status_led(mode=IDLE_MODE)
        # stopping from GUI only possible when start source set to usb
        self._set_source_button_activation(self.ui.start_source, mode=START_MODE)
        # send command to board (if stop was triggered by user and not a status change of board)
        if triggered_by_user:
            cmd = self.board_config.stop_measurement_command()
            self.connector.send_command(cmd)

    def export_config(self):
        """Export current configuration to file."""
        file_path = QFileDialog.getSaveFileName(
            self,
            caption="Select storage location for configuration file",
            dir=str(Path.cwd()),
            filter="*.json-files (*.json)",
        )[0]
        if file_path:
            if not file_path.endswith("json"):
                # required for linux
                file_path = f"{file_path}.json"
            self.board_config.save_to_file(file_path)

    def _update_config(self):
        update_list = self.board_config.load_from_file(self.config_path)
        for cmd in update_list:
            self.connector.send_command(cmd)
        self._repaint_gui()

    def _repaint_gui(self):
        self.ui.start_source.setCurrentIndex(self.board_config.start_source.source)
        self.ui.stop_source.setCurrentIndex(self.board_config.stop_source.source)
        is_usb = self.ui.start_source.currentText() == "GUI"
        self.ui.play_button.setDisabled(not is_usb)
        assert len(self.board_config.connections) == len(
            self.hw_config.connection_names
        ), "Only usage of default connections is supported!"
        for _idx, (conn, name) in enumerate(zip(self.board_config.connections, self.hw_config.connection_names)):
            button_name = f"{name}_button"
            button = self.findChild(QToolButton, button_name)
            if conn.is_active:
                # reset connection button first
                self._reset_connection_button(button)
                # next, toggle as we can be sure that it switches to active now
                self._toggle_connection_frontend(button)

    def closeEvent(self, event) -> None:  # noqa: ARG002, N802
        """End board connection thread to shut down GUI without memory leak."""
        self.connector.requestInterruption()
        sleep(2.5)

    def _change_status_led(self, mode: str = IDLE_MODE):
        if mode == IDLE_MODE:
            self.ui.status_led_label.setVisible(False)
            return
        # measurement running (green), error state (red)
        color = "rgb(0, 170, 0)" if mode == RUNNING_MODE else "rgb(255, 0, 0)"
        self.ui.status_led_label.setVisible(True)
        self.ui.status_led_label.setStyleSheet(f"background-color: {color};color: {color};")

    def board_message_received(self, payload: Dict):
        """Handle messages received from board."""
        self._change_status_led(mode=ERROR_MODE)
        d = QMessageBox()
        d.setWindowTitle("Setup error")
        d.setText(
            f"Sync Board reported the following error: {payload[PAYLOAD_TYPE]}. Please check your settings accordingly!"
        )
        d.setIcon(QMessageBox.Warning)
        ret = d.exec_()
        # on close of the error popup, send board the command to reset error state
        if ret:
            self._change_status_led(mode=IDLE_MODE)
            command = self.board_config.build_error_reset_command()
            self.connector.send_command(command)

    def handle_status_change(self, payload):
        """Handle status changes of board."""
        if payload[PAYLOAD_TYPE] == MESSAGE_START:
            self._start_measurement(triggered_by_user=False)
            self.measurement_is_running = True
            self._set_source_button_activation(self.ui.stop_source, mode=STOP_MODE)
        elif payload[PAYLOAD_TYPE] == MESSAGE_STOP:
            self._stop_measurement(triggered_by_user=False)
            self.measurement_is_running = False
            self._set_source_button_activation(self.ui.start_source, mode=START_MODE)
        self.log_event(payload)

    def log_event(self, payload: Dict):
        """Log event to file."""
        # unix timestamp in milliseconds
        unix_time = int(payload[PAYLOAD_TIME] * 1000)
        utc_time = datetime.utcfromtimestamp(unix_time / 1000)
        event = f"{unix_time}{CSV_SEPARATOR}{utc_time}{CSV_SEPARATOR}{payload[PAYLOAD_TYPE]}\n"
        # add line to event logfile
        with Path.open(self.event_log_path, "a") as fp:
            fp.write(event)
