"""module containing dialogs of the Open Sync Board GUI."""

__version__ = "0.1.0"

from open_sync_board_gui.dialogs.connection_config_dialog import (
    InputConnectionConfigDialog,
    InputOutputConnectionConfigDialog,
    OutputConnectionConfigDialog,
)
from open_sync_board_gui.dialogs.event_location_dialog import EventLogDialog
from open_sync_board_gui.dialogs.import_dialog import ConfigImportDialog
from open_sync_board_gui.dialogs.source_config_dialog import SourceConfigDialog

__all__ = [
    "InputConnectionConfigDialog",
    "InputOutputConnectionConfigDialog",
    "OutputConnectionConfigDialog",
    "EventLogDialog",
    "ConfigImportDialog",
    "SourceConfigDialog",
]
