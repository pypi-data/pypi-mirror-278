"""Entry point for the GUI application in mock mode for testing."""
from open_sync_board_gui.scripts.start_gui import start_gui

if __name__ == "__main__":
    # switch to mock mode to test without a board here
    start_gui(mock_mode=False)
