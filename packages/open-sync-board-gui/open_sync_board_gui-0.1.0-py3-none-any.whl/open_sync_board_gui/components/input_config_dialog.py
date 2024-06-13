# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'input_config_dialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_InputConnectionConfigDialog(object):
    def setupUi(self, InputConnectionConfigDialog):
        if not InputConnectionConfigDialog.objectName():
            InputConnectionConfigDialog.setObjectName("InputConnectionConfigDialog")
        InputConnectionConfigDialog.resize(362, 194)
        self.buttonBox = QDialogButtonBox(InputConnectionConfigDialog)
        self.buttonBox.setObjectName("buttonBox")
        self.buttonBox.setGeometry(QRect(90, 130, 241, 32))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.delay_label = QLabel(InputConnectionConfigDialog)
        self.delay_label.setObjectName("delay_label")
        self.delay_label.setGeometry(QRect(30, 30, 141, 32))
        self.delay_label.setStyleSheet("background-color: {rgb(185, 212, 125)}")
        self.sync_signal_label = QLabel(InputConnectionConfigDialog)
        self.sync_signal_label.setObjectName("sync_signal_label")
        self.sync_signal_label.setGeometry(QRect(30, 70, 121, 32))
        self.delay = QSpinBox(InputConnectionConfigDialog)
        self.delay.setObjectName("delay")
        self.delay.setGeometry(QRect(170, 30, 161, 32))
        self.delay.setMaximum(65535)
        self.sync_signal = QComboBox(InputConnectionConfigDialog)
        self.sync_signal.addItem("")
        self.sync_signal.addItem("")
        self.sync_signal.setObjectName("sync_signal")
        self.sync_signal.setGeometry(QRect(170, 70, 161, 32))
        self.sync_signal.setStyleSheet("")

        self.retranslateUi(InputConnectionConfigDialog)
        self.buttonBox.accepted.connect(InputConnectionConfigDialog.accept)
        self.buttonBox.rejected.connect(InputConnectionConfigDialog.reject)

        QMetaObject.connectSlotsByName(InputConnectionConfigDialog)

    # setupUi

    def retranslateUi(self, InputConnectionConfigDialog):
        InputConnectionConfigDialog.setWindowTitle(
            QCoreApplication.translate("InputConnectionConfigDialog", "Input Connection Configuration", None)
        )
        self.delay_label.setText(QCoreApplication.translate("InputConnectionConfigDialog", "Delay:", None))
        self.sync_signal_label.setText(QCoreApplication.translate("InputConnectionConfigDialog", "Sync Signal:", None))
        self.delay.setSuffix(QCoreApplication.translate("InputConnectionConfigDialog", "ms", None))
        self.sync_signal.setItemText(0, QCoreApplication.translate("InputConnectionConfigDialog", "Rising Edge", None))
        self.sync_signal.setItemText(1, QCoreApplication.translate("InputConnectionConfigDialog", "Falling Edge", None))

    # retranslateUi
