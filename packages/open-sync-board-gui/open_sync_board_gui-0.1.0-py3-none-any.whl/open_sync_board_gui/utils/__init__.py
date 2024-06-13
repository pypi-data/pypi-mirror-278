"""Module for Open Sync Board utilities."""

__version__ = "0.1.0"

from open_sync_board_gui.utils.board_configuration import BoardConfig, Connection, Source
from open_sync_board_gui.utils.board_connector import BoardConnectionError, BoardConnector

__all__ = ["BoardConfig", "Source", "Connection", "BoardConnector", "BoardConnectionError"]
