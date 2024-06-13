# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'source_config_dialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_SourceConfigDialog(object):
    def setupUi(self, SourceConfigDialog):
        if not SourceConfigDialog.objectName():
            SourceConfigDialog.setObjectName("SourceConfigDialog")
        SourceConfigDialog.resize(362, 194)
        self.buttonBox = QDialogButtonBox(SourceConfigDialog)
        self.buttonBox.setObjectName("buttonBox")
        self.buttonBox.setGeometry(QRect(90, 130, 241, 32))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.delay_label = QLabel(SourceConfigDialog)
        self.delay_label.setObjectName("delay_label")
        self.delay_label.setGeometry(QRect(30, 30, 141, 32))
        self.delay_label.setStyleSheet("background-color: {rgb(185, 212, 125)}")
        self.sync_signal_label = QLabel(SourceConfigDialog)
        self.sync_signal_label.setObjectName("sync_signal_label")
        self.sync_signal_label.setGeometry(QRect(30, 70, 121, 32))
        self.delay = QSpinBox(SourceConfigDialog)
        self.delay.setObjectName("delay")
        self.delay.setGeometry(QRect(170, 30, 161, 32))
        self.delay.setMaximum(65535)
        self.sync_signal = QComboBox(SourceConfigDialog)
        self.sync_signal.addItem("")
        self.sync_signal.addItem("")
        self.sync_signal.addItem("")
        self.sync_signal.setObjectName("sync_signal")
        self.sync_signal.setGeometry(QRect(170, 70, 161, 32))
        self.sync_signal.setStyleSheet("")

        self.retranslateUi(SourceConfigDialog)
        self.buttonBox.accepted.connect(SourceConfigDialog.accept)
        self.buttonBox.rejected.connect(SourceConfigDialog.reject)

        QMetaObject.connectSlotsByName(SourceConfigDialog)

    # setupUi

    def retranslateUi(self, SourceConfigDialog):
        SourceConfigDialog.setWindowTitle(
            QCoreApplication.translate("SourceConfigDialog", "Source Configuration", None)
        )
        self.delay_label.setText(QCoreApplication.translate("SourceConfigDialog", "Delay:", None))
        self.sync_signal_label.setText(QCoreApplication.translate("SourceConfigDialog", "Sync Signal:", None))
        self.delay.setSuffix(QCoreApplication.translate("SourceConfigDialog", "ms", None))
        self.sync_signal.setItemText(0, QCoreApplication.translate("SourceConfigDialog", "Falling Edge", None))
        self.sync_signal.setItemText(1, QCoreApplication.translate("SourceConfigDialog", "Rising Edge", None))
        self.sync_signal.setItemText(2, QCoreApplication.translate("SourceConfigDialog", "Any Edge", None))

    # retranslateUi
