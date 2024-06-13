# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'output_config_dialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_OutputConnectionConfigDialog(object):
    def setupUi(self, OutputConnectionConfigDialog):
        if not OutputConnectionConfigDialog.objectName():
            OutputConnectionConfigDialog.setObjectName("OutputConnectionConfigDialog")
        OutputConnectionConfigDialog.resize(361, 464)
        self.buttonBox = QDialogButtonBox(OutputConnectionConfigDialog)
        self.buttonBox.setObjectName("buttonBox")
        self.buttonBox.setGeometry(QRect(40, 420, 291, 32))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.manual_config = QGroupBox(OutputConnectionConfigDialog)
        self.manual_config.setObjectName("manual_config")
        self.manual_config.setGeometry(QRect(10, 140, 341, 271))
        self.manual_config.setCheckable(False)
        self.frequency = QSpinBox(self.manual_config)
        self.frequency.setObjectName("frequency")
        self.frequency.setGeometry(QRect(160, 190, 161, 32))
        self.frequency.setStyleSheet("")
        self.frequency.setMaximum(5100)
        self.sync_signal = QComboBox(self.manual_config)
        self.sync_signal.addItem("")
        self.sync_signal.addItem("")
        self.sync_signal.addItem("")
        self.sync_signal.addItem("")
        self.sync_signal.addItem("")
        self.sync_signal.addItem("")
        self.sync_signal.addItem("")
        self.sync_signal.setObjectName("sync_signal")
        self.sync_signal.setGeometry(QRect(160, 70, 161, 32))
        self.sync_signal.setStyleSheet("")
        self.delay_label = QLabel(self.manual_config)
        self.delay_label.setObjectName("delay_label")
        self.delay_label.setGeometry(QRect(20, 30, 141, 32))
        self.delay_label.setStyleSheet("")
        self.sync_signal_label = QLabel(self.manual_config)
        self.sync_signal_label.setObjectName("sync_signal_label")
        self.sync_signal_label.setGeometry(QRect(20, 70, 121, 32))
        self.frequency_label = QLabel(self.manual_config)
        self.frequency_label.setObjectName("frequency_label")
        self.frequency_label.setGeometry(QRect(20, 190, 121, 32))
        self.delay = QSpinBox(self.manual_config)
        self.delay.setObjectName("delay")
        self.delay.setGeometry(QRect(160, 30, 161, 32))
        self.delay.setStyleSheet("")
        self.delay.setMaximum(65535)
        self.stop_trigger = QCheckBox(self.manual_config)
        self.stop_trigger.setObjectName("stop_trigger")
        self.stop_trigger.setGeometry(QRect(160, 230, 121, 23))
        self.stop_trigger.setLayoutDirection(Qt.LeftToRight)
        self.stop_trigger.setStyleSheet("")
        self.degree = QSpinBox(self.manual_config)
        self.degree.setObjectName("degree")
        self.degree.setGeometry(QRect(160, 150, 161, 32))
        self.degree.setStyleSheet("")
        self.degree.setMinimum(1)
        self.degree.setMaximum(11)
        self.degree_label = QLabel(self.manual_config)
        self.degree_label.setObjectName("degree_label")
        self.degree_label.setGeometry(QRect(20, 150, 121, 32))
        self.pulse_length = QSpinBox(self.manual_config)
        self.pulse_length.setObjectName("pulse_length")
        self.pulse_length.setGeometry(QRect(160, 110, 161, 32))
        self.pulse_length.setStyleSheet("")
        self.pulse_length.setMinimum(1)
        self.pulse_length.setMaximum(65535)
        self.pulse_length_label = QLabel(self.manual_config)
        self.pulse_length_label.setObjectName("pulse_length_label")
        self.pulse_length_label.setGeometry(QRect(20, 110, 121, 32))
        self.default_config = QGroupBox(OutputConnectionConfigDialog)
        self.default_config.setObjectName("default_config")
        self.default_config.setGeometry(QRect(10, 30, 341, 80))
        self.default_config.setCheckable(False)
        self.default_config.setChecked(False)
        self.sensor_label = QLabel(self.default_config)
        self.sensor_label.setObjectName("sensor_label")
        self.sensor_label.setGeometry(QRect(20, 30, 121, 32))
        self.sensor = QComboBox(self.default_config)
        self.sensor.setObjectName("sensor")
        self.sensor.setGeometry(QRect(160, 30, 161, 32))
        self.sensor.setStyleSheet("")
        self.manual_config_radio = QRadioButton(OutputConnectionConfigDialog)
        self.manual_config_radio.setObjectName("manual_config_radio")
        self.manual_config_radio.setGeometry(QRect(10, 120, 161, 23))
        self.default_config_radio = QRadioButton(OutputConnectionConfigDialog)
        self.default_config_radio.setObjectName("default_config_radio")
        self.default_config_radio.setGeometry(QRect(10, 10, 161, 23))
        self.manual_config.raise_()
        self.buttonBox.raise_()
        self.default_config.raise_()
        self.manual_config_radio.raise_()
        self.default_config_radio.raise_()
        QWidget.setTabOrder(self.default_config, self.sensor)
        QWidget.setTabOrder(self.sensor, self.manual_config)
        QWidget.setTabOrder(self.manual_config, self.delay)
        QWidget.setTabOrder(self.delay, self.sync_signal)
        QWidget.setTabOrder(self.sync_signal, self.frequency)
        QWidget.setTabOrder(self.frequency, self.stop_trigger)

        self.retranslateUi(OutputConnectionConfigDialog)
        self.buttonBox.accepted.connect(OutputConnectionConfigDialog.accept)
        self.buttonBox.rejected.connect(OutputConnectionConfigDialog.reject)

        QMetaObject.connectSlotsByName(OutputConnectionConfigDialog)

    # setupUi

    def retranslateUi(self, OutputConnectionConfigDialog):
        OutputConnectionConfigDialog.setWindowTitle(
            QCoreApplication.translate("OutputConnectionConfigDialog", "Output Connection Configuration", None)
        )
        self.manual_config.setTitle("")
        self.frequency.setSuffix(QCoreApplication.translate("OutputConnectionConfigDialog", "Hz", None))
        self.sync_signal.setItemText(
            0, QCoreApplication.translate("OutputConnectionConfigDialog", "Falling Trigger", None)
        )
        self.sync_signal.setItemText(
            1, QCoreApplication.translate("OutputConnectionConfigDialog", "Rising Trigger", None)
        )
        self.sync_signal.setItemText(
            2, QCoreApplication.translate("OutputConnectionConfigDialog", "Falling Edge", None)
        )
        self.sync_signal.setItemText(3, QCoreApplication.translate("OutputConnectionConfigDialog", "Rising Edge", None))
        self.sync_signal.setItemText(
            4, QCoreApplication.translate("OutputConnectionConfigDialog", "Falling Clock", None)
        )
        self.sync_signal.setItemText(
            5, QCoreApplication.translate("OutputConnectionConfigDialog", "Rising Clock", None)
        )
        self.sync_signal.setItemText(6, QCoreApplication.translate("OutputConnectionConfigDialog", "M-Sequence", None))

        self.delay_label.setText(QCoreApplication.translate("OutputConnectionConfigDialog", "Delay:", None))
        self.sync_signal_label.setText(QCoreApplication.translate("OutputConnectionConfigDialog", "Sync Signal:", None))
        self.frequency_label.setText(QCoreApplication.translate("OutputConnectionConfigDialog", "Frequency:", None))
        self.delay.setSuffix(QCoreApplication.translate("OutputConnectionConfigDialog", "ms", None))
        self.stop_trigger.setText(QCoreApplication.translate("OutputConnectionConfigDialog", "Stop Trigger", None))
        self.degree.setSuffix("")
        self.degree_label.setText(QCoreApplication.translate("OutputConnectionConfigDialog", "Degree:", None))
        self.pulse_length.setSuffix(QCoreApplication.translate("OutputConnectionConfigDialog", "ms", None))
        self.pulse_length_label.setText(
            QCoreApplication.translate("OutputConnectionConfigDialog", "Pulse Length:", None)
        )
        self.default_config.setTitle("")
        self.sensor_label.setText(QCoreApplication.translate("OutputConnectionConfigDialog", "Select Device:", None))
        self.manual_config_radio.setText(
            QCoreApplication.translate("OutputConnectionConfigDialog", "Manual Configuration", None)
        )
        self.default_config_radio.setText(
            QCoreApplication.translate("OutputConnectionConfigDialog", "Default Configuration", None)
        )

    # retranslateUi
