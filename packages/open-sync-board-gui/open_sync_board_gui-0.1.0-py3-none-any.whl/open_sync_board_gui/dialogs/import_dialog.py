"""Import connection configuration from a file."""

from pathlib import Path
from typing import Union

from PySide2.QtWidgets import QCompleter, QDialog, QDirModel, QFileDialog, QWidget

from open_sync_board_gui.components import Ui_ConfigImportDialog
from open_sync_board_gui.constants import CONFIG_FILE_TYPE


class ConfigImportDialog(QDialog):
    """Dialog for importing connection configuration from a file."""

    def __init__(self, main_window: QWidget):
        super().__init__()
        self.main_window = main_window
        self.ui = Ui_ConfigImportDialog()
        self.ui.setupUi(self)
        self.ui.buttonBox.accepted.connect(self.update_path)
        self.ui.buttonBox.rejected.connect(self.reject)
        self.ui.select_config_path_button.clicked.connect(self.open_config_file_dialog)
        # set config path based on previous selections
        if self.main_window.config_path:
            self.ui.board_config_path.setText(str(self.main_window.config_path))
            self.config_path = self.main_window.config_path
        else:
            self.ui.board_config_path.setPlaceholderText("Config File Path")
            self.config_path = None

        # set line edit options
        config_completer = QCompleter(self)
        config_completer.setModel(QDirModel(config_completer))  # autocomplete path
        self.ui.board_config_path.setCompleter(config_completer)  # allow drag&drop
        self.ui.board_config_path.setAcceptDrops(True)

    def get_data(self) -> Union[Path, None]:
        """Return path after dialog closes."""
        return self.config_path

    def update_path(self):
        """Update path based on user input."""
        # set paths to line edit value
        if self.ui.board_config_path.text():
            self.config_path = Path(self.ui.board_config_path.text())
        # check validity of paths
        if self.config_path and not self._path_valid(self.config_path, CONFIG_FILE_TYPE):
            self.config_path = None  # reset invalid path

    @staticmethod
    def _path_valid(path: Path, ending: str):
        if all([Path.exists(path), Path.is_file(path), str(path).endswith(ending)]):
            return True
        return False

    def open_config_file_dialog(self):
        """Open file dialog to select board configuration file."""
        file_name = QFileDialog.getOpenFileName(
            self,
            caption="Select board configuration file",
            dir=str(Path.cwd()),
            filter=f"*{CONFIG_FILE_TYPE}-files (*{CONFIG_FILE_TYPE})",
        )[0]
        self.ui.board_config_path.setText(file_name)
