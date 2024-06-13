# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'config_import_dialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

import resources_rc


class Ui_ConfigImportDialog(object):
    def setupUi(self, ConfigImportDialog):
        if not ConfigImportDialog.objectName():
            ConfigImportDialog.setObjectName("ConfigImportDialog")
        ConfigImportDialog.resize(385, 121)
        ConfigImportDialog.setStyleSheet("")
        self.buttonBox = QDialogButtonBox(ConfigImportDialog)
        self.buttonBox.setObjectName("buttonBox")
        self.buttonBox.setGeometry(QRect(22, 70, 341, 32))
        self.buttonBox.setStyleSheet("")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.board_config_path_label = QLabel(ConfigImportDialog)
        self.board_config_path_label.setObjectName("board_config_path_label")
        self.board_config_path_label.setGeometry(QRect(20, 20, 141, 32))
        self.board_config_path_label.setStyleSheet("background-color: {rgb(185, 212, 125)}")
        self.board_config_path = QLineEdit(ConfigImportDialog)
        self.board_config_path.setObjectName("board_config_path")
        self.board_config_path.setGeometry(QRect(160, 20, 161, 32))
        self.select_config_path_button = QToolButton(ConfigImportDialog)
        self.select_config_path_button.setObjectName("select_config_path_button")
        self.select_config_path_button.setGeometry(QRect(330, 20, 33, 34))
        icon = QIcon()
        icon.addFile(":/icons/folder.png", QSize(), QIcon.Normal, QIcon.Off)
        self.select_config_path_button.setIcon(icon)
        self.select_config_path_button.setIconSize(QSize(25, 25))

        self.retranslateUi(ConfigImportDialog)
        self.buttonBox.accepted.connect(ConfigImportDialog.accept)
        self.buttonBox.rejected.connect(ConfigImportDialog.reject)

        QMetaObject.connectSlotsByName(ConfigImportDialog)

    # setupUi

    def retranslateUi(self, ConfigImportDialog):
        ConfigImportDialog.setWindowTitle(
            QCoreApplication.translate("ConfigImportDialog", "Import Board Configuration", None)
        )
        self.board_config_path_label.setText(
            QCoreApplication.translate("ConfigImportDialog", "Board Configuration:", None)
        )
        # if QT_CONFIG(tooltip)
        self.board_config_path.setToolTip(
            QCoreApplication.translate(
                "ConfigImportDialog", "<html><head/><body><p>Path to board configuration file</p></body></html>", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        # if QT_CONFIG(tooltip)
        self.select_config_path_button.setToolTip(
            QCoreApplication.translate(
                "ConfigImportDialog",
                "<html><head/><body><p>Select location of board configuration file</p></body></html>",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.select_config_path_button.setText(QCoreApplication.translate("ConfigImportDialog", "...", None))

    # retranslateUi
