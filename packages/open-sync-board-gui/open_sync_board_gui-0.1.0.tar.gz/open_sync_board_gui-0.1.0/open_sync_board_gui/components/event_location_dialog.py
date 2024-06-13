# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'event_location_dialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

import resources_rc


class Ui_EventLogDialog(object):
    def setupUi(self, EventLogDialog):
        if not EventLogDialog.objectName():
            EventLogDialog.setObjectName("EventLogDialog")
        EventLogDialog.resize(496, 225)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(EventLogDialog.sizePolicy().hasHeightForWidth())
        EventLogDialog.setSizePolicy(sizePolicy)
        EventLogDialog.setStyleSheet("")
        self.verticalLayout_2 = QVBoxLayout(EventLogDialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.log_path_label = QLabel(EventLogDialog)
        self.log_path_label.setObjectName("log_path_label")
        self.log_path_label.setStyleSheet("background-color: {rgb(185, 212, 125)}")
        self.log_path_label.setWordWrap(True)

        self.verticalLayout.addWidget(self.log_path_label)

        self.file_location_label = QLabel(EventLogDialog)
        self.file_location_label.setObjectName("file_location_label")

        self.verticalLayout.addWidget(self.file_location_label)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.log_path = QLineEdit(EventLogDialog)
        self.log_path.setObjectName("log_path")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.log_path.sizePolicy().hasHeightForWidth())
        self.log_path.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.log_path)

        self.select_location_button = QToolButton(EventLogDialog)
        self.select_location_button.setObjectName("select_location_button")
        icon = QIcon()
        icon.addFile(":/icons/folder.png", QSize(), QIcon.Normal, QIcon.Off)
        self.select_location_button.setIcon(icon)
        self.select_location_button.setIconSize(QSize(25, 25))

        self.horizontalLayout.addWidget(self.select_location_button)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.file_name_label = QLabel(EventLogDialog)
        self.file_name_label.setObjectName("file_name_label")

        self.verticalLayout.addWidget(self.file_name_label)

        self.event_file_name = QLineEdit(EventLogDialog)
        self.event_file_name.setObjectName("event_file_name")

        self.verticalLayout.addWidget(self.event_file_name)

        self.buttonBox = QDialogButtonBox(EventLogDialog)
        self.buttonBox.setObjectName("buttonBox")
        self.buttonBox.setStyleSheet("")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)

        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(EventLogDialog)
        self.buttonBox.rejected.connect(EventLogDialog.reject)
        self.buttonBox.accepted.connect(EventLogDialog.accept)

        QMetaObject.connectSlotsByName(EventLogDialog)

    # setupUi

    def retranslateUi(self, EventLogDialog):
        EventLogDialog.setWindowTitle(QCoreApplication.translate("EventLogDialog", "Set Eventlog Location", None))
        self.log_path_label.setText(
            QCoreApplication.translate(
                "EventLogDialog",
                "Welcome!\n" "Please select where you want to store the event logs of this session.",
                None,
            )
        )
        self.file_location_label.setText(QCoreApplication.translate("EventLogDialog", "Event File Location:", None))
        # if QT_CONFIG(tooltip)
        self.log_path.setToolTip(
            QCoreApplication.translate(
                "EventLogDialog", "<html><head/><body><p>Path to board configuration file</p></body></html>", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        # if QT_CONFIG(tooltip)
        self.select_location_button.setToolTip(
            QCoreApplication.translate(
                "EventLogDialog",
                "<html><head/><body><p>Select location of board configuration file</p></body></html>",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.select_location_button.setText(QCoreApplication.translate("EventLogDialog", "...", None))
        self.file_name_label.setText(QCoreApplication.translate("EventLogDialog", "Event File Name:", None))

    # retranslateUi
