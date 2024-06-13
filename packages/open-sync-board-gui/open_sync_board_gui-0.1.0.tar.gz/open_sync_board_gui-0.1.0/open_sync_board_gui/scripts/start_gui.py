"""Entry point for the GUI application, installed as binary during poetry install."""

import sys

from PySide2.QtWidgets import QApplication

from open_sync_board_gui.constants import BOARD_VERSION_V3
from open_sync_board_gui.windows import MainWindow


# switch to a new board version here
def start_gui(mock_mode=False, version=BOARD_VERSION_V3):
    """Start the GUI application."""
    app = QApplication()
    form = MainWindow(mock_mode, version)
    form.show()
    sys.exit(app.exec_())


def run():
    """Run the GUI application without mock mode."""
    start_gui(mock_mode=True)
