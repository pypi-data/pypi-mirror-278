"""Configure start and stop sources."""


from PySide2.QtWidgets import QDialog, QWidget

from open_sync_board_gui.components.source_config_dialog import Ui_SourceConfigDialog
from open_sync_board_gui.constants import DEFAULT_SYNC_SIGNAL, SYNC_SIGNAL_MAPPING_SOURCE
from open_sync_board_gui.utils.board_configuration import Source


class SourceConfigDialog(QDialog):
    """Dialog for configuring a source."""

    def __init__(self, main_window: QWidget, source: Source):
        super().__init__()
        self.source = source
        self.main_window = main_window
        self.ui = Ui_SourceConfigDialog()
        self._setup_ui()
        self.update_command = ""

    def get_data(self):
        """Return update command after dialog closes."""
        return self.update_command

    def _setup_ui(self):
        self.ui.setupUi(self)
        self.ui.buttonBox.accepted.connect(self.update_source)
        self.ui.buttonBox.rejected.connect(self.reject)
        self.ui.delay.setValue(self.source.delay)
        sync_index = self.source.sync_signal or DEFAULT_SYNC_SIGNAL
        self.ui.sync_signal.setCurrentIndex(sync_index)
        edge_enabled = self.source.is_edge_enabled()
        self.ui.sync_signal.setEnabled(edge_enabled)
        self.ui.sync_signal_label.setEnabled(edge_enabled)

    def update_source(self):
        """Update source based on user input."""
        delay = self.ui.delay.value()
        if self.source.is_edge_enabled():
            sync_signal = self.ui.sync_signal.currentText()
            sync_signal = SYNC_SIGNAL_MAPPING_SOURCE.index(sync_signal)
        else:
            sync_signal = None
        self.update_command = self.source.update_source(
            self.main_window.board_config.command_dict,
            self.source.source,
            delay=delay,
            sync_signal=sync_signal,
        )
