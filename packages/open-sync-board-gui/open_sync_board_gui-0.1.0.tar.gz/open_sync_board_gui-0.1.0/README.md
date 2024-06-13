# Open Sync Board GUI

[![PyPI](https://img.shields.io/pypi/v/empkins-sync-board-gui)](https://pypi.org/project/open-sync-board-gui/)
![GitHub](https://img.shields.io/github/license/empkins/open-sync-board-gui)
[![Linting](https://github.com/empkins/open-sync-board-gui/actions/workflows/lint.yml/badge.svg)](https://github.com/empkins/open-sync-board-gui/actions/workflows/lint.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Description

This Repository is part of the [Open Sync Board](https://github.com/empkins/open-sync-board) project. The Open Sync Board (OSB) can be used
to **precisely synchronize different measurement modalities** on hardware level.
The accompanying **Graphical User Interface (GUI)** allows to easily adjust the outputs
of the OSB with the required synchronization signals for the connected modalities, and is also **suited for non-technical users**.

<img src="img/osb_gui.png">

The main UI window resembles the layout of the OSB, and thus enables an intuitive workflow. The GUI allows to:
- Select and deselect outputs to use
- Configure the behavior of each output signal either manually or by selecting a connected device from a list of default devices
- Select and configure input ports to process received signals, e.g., for triggered measurements
- Start and stop measurements
- Log status changes and external events, e.g. button press
- Export current configuration to easily restore them for the next measurement session

## Installation

To use the GUI **out-of-the-box** without any adaptations, you can download the **standalone executable** for Windows or MacOs from the [releases page]().
If you are comfortable with python/pip, or if you are a linux user, please install the package **via pip**:

```bash
pip install open_sync_board_gui
```

To use the GUI, make sure you have the readily flashed OSB connected to your computer via USB.
You can then run the GUI by executing the following command in your shell:

```bash
run-sync-board
```

If you are on Linux and the board is not recognized, check out
the [Setup remarks when using Linux](#setup-remarks-when-using-linux) section below.

## Usage

Before starting the GUI, make sure the **OSB is connected** to your computer **via USB**.
When executing the GUI, at first, a dialog will pop up asking you for the storage location and name of the log files that will be generated.

<img src="img/configure_path.png" width="300">

Every time the GUI is executed, a new file is created storing the timestamps when a measurement is started or stopped, and when an event (e.g., Button press, Input trigger) is reported.
Select a path and filename of your choice and click `OK`.

Afterwards, the **main window** of the GUI will open. The main UI window resembles the layout of the OSB, and thus simplifies setting up the GUI as well as the OSB correctly.
First, you can select the connections (measuring devices) that you want to use for connecting devices. Activated connections are highlighted in green and provide a settings button to configure their behavior.

### Configuration of Measurement Device (MD) Ports

The connections MD1-MD4 and MD7 are **output ports**, i.e., they send a synchronization signal of your choice after starting the measurement. When clicking the settings button, a dialog will open that allows you to configure the behavior of the selected output connection.
You can either select a **default device** from the list of available devices, or configure the behavior manually. In the latter case, **depending on the sychronization signal** that you choose from the `Sync Signal` dropdown, different properties are available for configuration. Click `OK` to save your changes and close the dialog.
In case you selected a default device, you will be prompted how to proceed with connecting the device to the OSB, more precisely, which plug to use for the connection, and which voltage level to use. To configure the voltage level, you have to move the little plastic jumper that you can find next to the corresponding connection to the desired position. It should be either placed at the `1.8`, `3.3`, or `5` position labeled in the GUI and moved to the position you are prompted to use. If your device requires a different logic level (between 1V and 7.5V), you may use the `NC` position and solder in a suitable resistor. If your device doesn't bring its own power supply for regulating the logic level, make sure you have another jumper set on `Vint`. Otherwise, move this jumper to the `NC` position next to `Vint`.
If you chose manual configuration, you need to figure out the required logic level for your device from its manual.

<img src="img/default_config.png" width="300">
<img src="img/manual_config.png" width="300">

The connections MD5 and MD6 can be configured either as **output ports** analogously to the other connections, or as **input ports**. On one hand, you can use the input ports to connect some kind of switch to the OSB and log every time it sends the selected signal. This can i.e. be used for event logging, and can thus be achieved by selecting the `Event Input` option in the connection settings. 
On the other hand, a connected input can be used to start or stop the measurement. This can be configured in the [source settings](todo#configuration-of-sources).
When using MD5 or MD6, make sure to move the plastic jumper for switching between input and output mode as prompted by the GUI.

<img src="img/event_config.png" width="300">

### Configuration of Sources

The start and stop source are used to launch and terminate the measurement (i.e. the output of synchronization signals to all connected devices), respectively. 
When selecting `GUI` from the respective dropdown lists, you can start/stop the measurement with the start/stop button in the GUI. Alternatively, you could control the measurement with the buttons on the OSB (labeled Button1 and Button2, also schematically displayed in the GUI).
To trigger a measurement from an input source, select the input port you want to connect this external source to. 
In this case, you must select the desired receive signal by clicking on the source configuration button and choosing from the `Sync Signal` dropdown.
For all types of sources, you can also set a delay for the measurement to start/stop in the source settings.

<img src="img/source_config.png" width="300">

### During the measurement

When you are all set up, you can start the measurement from the selected source and monitor the Sync Board its status via the GUI as well as the OSB by its status LED. When the LED is turned off, the board is in idle state. When the LED is blue, the measurement is running. When the LED is red, an error has occurred that will be displayed to you in the GUI.  

<img src="img/led.png" width="150">

### Save and load configurations

When you need to reuse a configuration several times, e.g., for a study with several participants/iterations, you can save the current configuration to a file using the `Export` button, and import it in the next session using the `Import` button.

<img src="img/import_export.png" width="200">

## Postprocessing of the recorded data

For synchronization of the recorded data, we provide a [Python package](TODO:Link).
The logs of all events recorded by the GUI can be accessed at the location specified when starting the GUI.

## Quickstart for Developers

If you want to modify the GUI, **add** your own **default devices**, or **adapt it** to **hardware modifications**.
The [Installation](#installation) of a standalone or via pip might not be sufficient.
In this case, make sure you have Python (Version >=3.7.1,<3.10) and an IDE with Python support (e.g., Visual Studio Code
or PyCharm) installed on your machine.
Furthermore, for dependency management, this package uses [poetry](https://python-poetry.org/). Installation
instructions are provided on [their homepage](https://python-poetry.org/docs/).

After you have ensured all prerequisites are installed, run the following commands to get the latest version, initialize
a virtual environment, and install all development dependencies:

With ssh access:

```bash
git clone git@github.com:empkins/open-sync-board-gui.git
cd open-sync-board-gui
poetry install
```

With https access:

```bash
git clone https://github.com/empkins/open-sync-board-gui.git
cd open-sync-board-gui
poetry install
```

Afterwards open a shell inside the project folder (`your_path_to/open-sync-board-gui`) and enter the following commands

```bash
poetry shell
cd open_sync_board_gui
python start_gui.py
```

to start the GUI.

### General Project Structure

The repository is structured as follows:

```bash
├── open_sync_board_gui/                                  
     ├── components/    # Contains automatically compiled ui files. Do not modify!                                         
     ├── config/        # Contains hardware configuration files. When hardware is adapted, changes might be required!
     ├── constants/     # Contains general constants, command messages for board interface, and default devices 
     ├── dialogs/       # Custom dialogs/pop-up windows used in the GUI
     ├── events/        # Default storage location for event logs. A new file is created every time the GUI is started
     ├── logs/          # Log files from board connector. Can be helpful when board connection fails
     ├── scripts/       # Contains the main script to start the GUI `start_gui.py`
     ├── ui/            # Files generated and modified with Qt Designer. Do not modify raw files! 
     |    └── icons/    # Icons and images used in the GUI
     ├── utils/         # Classes that store the current state and configuration of GUI and handle the communication with the board
     └── windows/       # Contains the main window of the GUI
└── scripts/            # Script for compiling the ui files 
```
### Mock mode
For experimenting and debugging, there is a mock mode available.
In this mode, the GUI does not require a connection to a physical SyncBoard, but instead simulates the behavior of the board.
To enable the mock mode, set the `mock_mode` variable in the entry script `open_sync_board_gui/script/start_gui.py` to `True`.

### Adding a new default device

All default devices are defined in the `open_sync_board_gui/constants/default_devices.py` file. To add a new device,
you need to add its name to the comma separated list of `DEFAULT_DEVICES` and add a new entry to the `DEVICE_SETTINGS`
dictionary. The key of the dictionary entry is the name of the device, and the value is a dictionary containing the
following keys:
| Key | Type | Required | Value | Description |
|----------------|---------|----------|----------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------|
| "sync_signal"  | Integer | - [x]    | 0 (Falling Trigger) <br> 1 (Rising Trigger)<br> 2 (Falling Edge)<br> 3 (Rising Edge)<br> 4 (Falling Clock) <br>5 (Rising Clock)<br> 6 (M-Sequence) | Synchronization signal that will be output to the respective device |
| "logic_level"  | String | - [x]    | `LOGIC_LEVEL_18` ("low")<br> `LOGIC_LEVEL_33` ("medium")<br> `LOGIC_LEVEL_50` ("high")                                                             | Logic level that is required for the respective device |
| "plug"         | String | - [x]    | e.g., "BNC",<br> "TRS Audio Plug"                                                                                                                  | Plug type of sensor, i.e., required daughter board |
| "delay"        | Integer | - [ ]    | delay value in s | Delay before signal is sent to output |
| "pulse_length" | Integer | - [ ]    | pulse length value in ms | For Trigger Signals: length of the trigger signal |
| "freq"         | Integer | - [ ]    | frequency value in Hz | For clock & M-Sequence synchronization: desired frequency |
| "stop_trigger" | Boolean | - [ ]    | `False` <br> `True`                                                                                                                                | For trigger synchronization |
| "degree"       | Integer | - [ ]    | degree of M-Sequence | For M-Sequence synchronization: degree of M-Sequence |

The keys marked as required must be specified for every default device. Remaining keys are optional and can be added if
required. Note that some keys are only relevant for specific synchronization signals. For example, the `freq` key is
only relevant for clock and M-Sequence synchronization, as it can be taken from its description.
Unspecified properties will be set to zero/False by default.

### Modifying and Updating UI Elements

For designing UI components, the program *Qt Designer* (included in
the [Qt Development Tools](https://www.qt.io/download)) was utilized. To modify or add frontend components, the `*.ui`
-files from the `emkins_sync_board_gui/ui/` directory can be opened with *Qt Designer*. After modifying the UI,
the `*.ui`-files need to be converted to `*.py`-files. This can be done by executing the following command in
the `open-sync-board-gui` virtual environment:
```
poe update_ui
```
Under the hood, this command runs the `scripts/compile_ui_files.sh` bash script. The designer and resource files are
compiled using the `pyside2-uic` and `pyside2-rcc` command line tools and stored in
the `open_sync_board_gui/components/` directory.

## Setup remarks when using Linux

Due to restricted permissions under Linux, to open up a serial port for writing to and reading from the Sync Board, the
current user must be granted read and write permission for the respective tty device.
To do so, execute the following steps once:

1. Unplug the Sync board and run
   ```ls /dev/ > dev_list.txt```
2. Plug in the Sync board and afterward run

```
ls /dev/ | diff --suppress-common-lines -y - dev_list.txt
```

3. The output should include one line starting with `tty{...}`, which is the name of the device that is connected to the
   board.
4. You can delete the helper file now:

```
rm dev_list.txt
```

5. Now add read and write permissions for the current user by inserting the device name detected in step 2:

```
sudo chmod 666 /dev/tty{...}
```

6. To make the changes permanent even after restart, you finally need to add them as an udev rule:

```
echo 'KERNEL=="tty{...}", MODE="666"' | sudo tee /etc/udev/rules.d/sync-board-rule.rules
```

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing

We welcome contributions to `Open Sync Board GUI`! For more information, have a look at
the [Contributing Guidelines](CONTRIBUTING.md).
