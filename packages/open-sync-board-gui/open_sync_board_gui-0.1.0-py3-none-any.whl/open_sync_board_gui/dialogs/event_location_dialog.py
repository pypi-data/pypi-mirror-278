"""Dialog for setting event log file location."""
from datetime import datetime
from pathlib import Path

from PySide2.QtWidgets import QCompleter, QDialog, QDirModel, QFileDialog, QWidget

from open_sync_board_gui.components import Ui_EventLogDialog
from open_sync_board_gui.constants import EVENT_LOG_FILE_TYPE, EVENT_LOG_HEADER


class EventLogDialog(QDialog):
    """Dialog for setting event log file location."""

    def __init__(self, main_window: QWidget):
        super().__init__()
        self.main_window = main_window
        self.ui = Ui_EventLogDialog()
        self.ui.setupUi(self)
        self.ui.buttonBox.accepted.connect(self.create_log_file)
        self.ui.buttonBox.rejected.connect(self.reject)
        self.ui.select_location_button.clicked.connect(self.open_log_file_dialog)
        self.ui.log_path.editingFinished.connect(self.validate_input)
        self.ui.log_path.hasAcceptableInput()
        self.ui.event_file_name.editingFinished.connect(self.validate_input)
        # set event log path
        self.event_log_path = None
        self.event_log_dir = None
        self.event_log_filename = None
        self._set_default_path()
        self.ui.log_path.setText(str(self.event_log_dir))
        self.ui.event_file_name.setText(self.event_log_file_name)
        # set line edit options
        config_completer = QCompleter(self)
        config_completer.setModel(QDirModel(config_completer))  # autocomplete path
        self.ui.log_path.setCompleter(config_completer)  # allow drag&drop
        self.ui.log_path.setAcceptDrops(True)

    def _set_default_path(self):
        # set default path
        start = datetime.now()
        curr_date = str(datetime.date(start))
        curr_time = str(datetime.time(start)).replace(":", "-")[:8]
        self.event_log_file_name = f"events_{curr_date}_{curr_time}.csv"
        self.event_log_dir = Path.home()
        self.event_log_path = self.event_log_dir.joinpath(self.event_log_file_name)

    def get_data(self) -> Path:
        """Return the path to the event log file after dialog closes."""
        return self.event_log_path

    def create_log_file(self):
        """Create event log file."""
        # set paths to line edit value
        self.validate_input()
        if self.ui.log_path.text() and self.ui.event_file_name.text():
            self.event_log_path = Path(self.ui.log_path.text()).joinpath(Path(self.ui.event_file_name.text()))
        with Path.open(self.event_log_path, "w+") as fp:
            fp.write(EVENT_LOG_HEADER)

    def is_path_valid(self):
        """Check if the given path is valid."""
        event_dir = Path(self.ui.log_path.text())
        file_name = self.ui.event_file_name.text()
        path = event_dir.joinpath(file_name)
        if event_dir and file_name:
            path = path.with_suffix(EVENT_LOG_FILE_TYPE)
            return all(
                [
                    Path.exists(event_dir),
                    Path.is_dir(event_dir),
                    not Path.exists(path),
                ]
            )
        return False

    def validate_input(self):
        """Validate the input of the line edit."""
        is_enabled = self.is_path_valid()
        self.ui.buttonBox.setEnabled(is_enabled)

    def open_log_file_dialog(self):
        """Open file dialog to select event log file."""
        # only allow directories
        QFileDialog.getExistingDirectory(
            self,
            caption="Select directory for event log file",
            dir=str(Path.home()),
        )

    def closeEvent(self, event):  # noqa: N802
        """Prevent closing the dialog when no valid path was entered."""
        if self.is_path_valid():
            super().closeEvent(event)
        else:
            event.ignore()
