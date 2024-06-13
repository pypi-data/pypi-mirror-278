# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window_v3.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

import resources_rc


class Ui_MainWindowV3(object):
    def setupUi(self, MainWindowV3):
        if not MainWindowV3.objectName():
            MainWindowV3.setObjectName("MainWindowV3")
        MainWindowV3.resize(1027, 898)
        MainWindowV3.setAutoFillBackground(False)
        MainWindowV3.setStyleSheet("background-color: rgb(255, 255, 255);\n" "")
        self.board_connections = QLabel(MainWindowV3)
        self.board_connections.setObjectName("board_connections")
        self.board_connections.setGeometry(QRect(240, 30, 587, 771))
        self.board_connections.setPixmap(QPixmap(":/icons/SyncBoard_PCB_V3_resized.png"))
        self.md1_button = QToolButton(MainWindowV3)
        self.md1_button.setObjectName("md1_button")
        self.md1_button.setGeometry(QRect(250, 108, 156, 181))
        self.md1_button.setStyleSheet("background-color: rgb(251, 217, 221);\n" "color: rgb(0, 0, 0);")
        self.md2_button = QToolButton(MainWindowV3)
        self.md2_button.setObjectName("md2_button")
        self.md2_button.setGeometry(QRect(432, 46, 181, 155))
        self.md2_button.setStyleSheet("background-color: rgb(251, 217, 221);\n" "color: rgb(0, 0, 0);")
        self.md3_button = QToolButton(MainWindowV3)
        self.md3_button.setObjectName("md3_button")
        self.md3_button.setGeometry(QRect(643, 108, 156, 181))
        self.md3_button.setStyleSheet("background-color: rgb(251, 217, 221);\n" "color: rgb(0, 0, 0);")
        self.md4_button = QToolButton(MainWindowV3)
        self.md4_button.setObjectName("md4_button")
        self.md4_button.setGeometry(QRect(643, 300, 156, 181))
        self.md4_button.setStyleSheet("background-color: rgb(251, 217, 221);\n" "color: rgb(0, 0, 0);")
        self.md7_button = QToolButton(MainWindowV3)
        self.md7_button.setObjectName("md7_button")
        self.md7_button.setGeometry(QRect(250, 300, 156, 181))
        self.md7_button.setStyleSheet("background-color: rgb(251, 217, 221);\n" "color: rgb(0, 0, 0);")
        self.md6_button = QToolButton(MainWindowV3)
        self.md6_button.setObjectName("md6_button")
        self.md6_button.setGeometry(QRect(250, 492, 156, 181))
        self.md6_button.setStyleSheet("background-color: rgb(251, 217, 221);\n" "color: rgb(0, 0, 0);")
        self.md5_button = QToolButton(MainWindowV3)
        self.md5_button.setObjectName("md5_button")
        self.md5_button.setGeometry(QRect(643, 492, 156, 181))
        self.md5_button.setStyleSheet("background-color: rgb(251, 217, 221);\n" "color: rgb(0, 0, 0);")
        self.md1_settings = QToolButton(MainWindowV3)
        self.md1_settings.setObjectName("md1_settings")
        self.md1_settings.setGeometry(QRect(307, 222, 41, 41))
        icon = QIcon()
        icon.addFile(":/icons/settings.png", QSize(), QIcon.Normal, QIcon.Off)
        self.md1_settings.setIcon(icon)
        self.md1_settings.setIconSize(QSize(30, 30))
        self.md2_settings = QToolButton(MainWindowV3)
        self.md2_settings.setObjectName("md2_settings")
        self.md2_settings.setGeometry(QRect(502, 140, 41, 41))
        self.md2_settings.setIcon(icon)
        self.md2_settings.setIconSize(QSize(30, 30))
        self.md3_settings = QToolButton(MainWindowV3)
        self.md3_settings.setObjectName("md3_settings")
        self.md3_settings.setGeometry(QRect(700, 222, 41, 41))
        self.md3_settings.setIcon(icon)
        self.md3_settings.setIconSize(QSize(30, 30))
        self.md4_settings = QToolButton(MainWindowV3)
        self.md4_settings.setObjectName("md4_settings")
        self.md4_settings.setGeometry(QRect(700, 413, 41, 41))
        self.md4_settings.setIcon(icon)
        self.md4_settings.setIconSize(QSize(30, 30))
        self.md5_settings = QToolButton(MainWindowV3)
        self.md5_settings.setObjectName("md5_settings")
        self.md5_settings.setGeometry(QRect(700, 602, 41, 41))
        self.md5_settings.setIcon(icon)
        self.md5_settings.setIconSize(QSize(30, 30))
        self.md6_settings = QToolButton(MainWindowV3)
        self.md6_settings.setObjectName("md6_settings")
        self.md6_settings.setGeometry(QRect(307, 602, 41, 41))
        self.md6_settings.setIcon(icon)
        self.md6_settings.setIconSize(QSize(30, 30))
        self.md7_settings = QToolButton(MainWindowV3)
        self.md7_settings.setObjectName("md7_settings")
        self.md7_settings.setGeometry(QRect(307, 413, 41, 41))
        self.md7_settings.setIcon(icon)
        self.md7_settings.setIconSize(QSize(30, 30))
        self.layoutWidget = QWidget(MainWindowV3)
        self.layoutWidget.setObjectName("layoutWidget")
        self.layoutWidget.setGeometry(QRect(10, 830, 1001, 61))
        self.gridLayout = QGridLayout(self.layoutWidget)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.start_source_label_text = QLabel(self.layoutWidget)
        self.start_source_label_text.setObjectName("start_source_label_text")
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.start_source_label_text.setFont(font)
        self.start_source_label_text.setStyleSheet("color: rgb(0, 0, 0);")
        self.start_source_label_text.setScaledContents(True)

        self.gridLayout.addWidget(self.start_source_label_text, 3, 1, 1, 1)

        self.stop_settings = QToolButton(self.layoutWidget)
        self.stop_settings.setObjectName("stop_settings")
        self.stop_settings.setIcon(icon)
        self.stop_settings.setIconSize(QSize(30, 30))

        self.gridLayout.addWidget(self.stop_settings, 3, 16, 1, 1)

        self.config_export_button = QToolButton(self.layoutWidget)
        self.config_export_button.setObjectName("config_export_button")
        self.config_export_button.setStyleSheet("background-color: rgb(121, 195, 169);")
        icon1 = QIcon()
        icon1.addFile(":/icons/export-config.png", QSize(), QIcon.Normal, QIcon.Off)
        self.config_export_button.setIcon(icon1)
        self.config_export_button.setIconSize(QSize(30, 30))

        self.gridLayout.addWidget(self.config_export_button, 3, 9, 1, 1)

        self.stop_source_label_icon = QLabel(self.layoutWidget)
        self.stop_source_label_icon.setObjectName("stop_source_label_icon")
        self.stop_source_label_icon.setPixmap(QPixmap("../../../../../.designer/backup/icons/stop.svg"))
        self.stop_source_label_icon.setScaledContents(True)

        self.gridLayout.addWidget(self.stop_source_label_icon, 3, 10, 1, 1)

        self.stop_source = QComboBox(self.layoutWidget)
        self.stop_source.addItem("")
        self.stop_source.addItem("")
        self.stop_source.addItem("")
        self.stop_source.addItem("")
        self.stop_source.addItem("")
        self.stop_source.setObjectName("stop_source")
        font1 = QFont()
        font1.setPointSize(15)
        font1.setBold(False)
        font1.setWeight(50)
        self.stop_source.setFont(font1)
        self.stop_source.setStyleSheet("selection-color:rgb(0, 0, 0);\n" "color: rgb(0, 0, 0);")

        self.gridLayout.addWidget(self.stop_source, 3, 15, 1, 1)

        self.start_settings = QToolButton(self.layoutWidget)
        self.start_settings.setObjectName("start_settings")
        self.start_settings.setIcon(icon)
        self.start_settings.setIconSize(QSize(30, 30))

        self.gridLayout.addWidget(self.start_settings, 3, 5, 1, 1)

        self.play_button = QToolButton(self.layoutWidget)
        self.play_button.setObjectName("play_button")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.play_button.sizePolicy().hasHeightForWidth())
        self.play_button.setSizePolicy(sizePolicy)
        self.play_button.setStyleSheet("background-color: rgb(185, 212, 125);")
        icon2 = QIcon()
        icon2.addFile(":/icons/start.png", QSize(), QIcon.Normal, QIcon.Off)
        self.play_button.setIcon(icon2)
        self.play_button.setIconSize(QSize(40, 40))

        self.gridLayout.addWidget(self.play_button, 3, 8, 1, 1)

        self.start_source = QComboBox(self.layoutWidget)
        self.start_source.addItem("")
        self.start_source.addItem("")
        self.start_source.addItem("")
        self.start_source.addItem("")
        self.start_source.addItem("")
        self.start_source.setObjectName("start_source")
        self.start_source.setFont(font1)
        self.start_source.setStyleSheet("selection-color:rgb(0, 0, 0);\n" "color: rgb(0, 0, 0);")

        self.gridLayout.addWidget(self.start_source, 3, 4, 1, 1)

        self.start_source_label_icon = QLabel(self.layoutWidget)
        self.start_source_label_icon.setObjectName("start_source_label_icon")
        self.start_source_label_icon.setPixmap(QPixmap("../../../../../.designer/backup/icons/start.svg"))
        self.start_source_label_icon.setScaledContents(True)

        self.gridLayout.addWidget(self.start_source_label_icon, 3, 6, 1, 1)

        self.stop_source_label_text = QLabel(self.layoutWidget)
        self.stop_source_label_text.setObjectName("stop_source_label_text")
        self.stop_source_label_text.setFont(font)
        self.stop_source_label_text.setStyleSheet("color: rgb(0, 0, 0);")
        self.stop_source_label_text.setScaledContents(True)

        self.gridLayout.addWidget(self.stop_source_label_text, 3, 12, 1, 1)

        self.config_import_button = QToolButton(self.layoutWidget)
        self.config_import_button.setObjectName("config_import_button")
        self.config_import_button.setStyleSheet("background-color: rgb(121, 195, 169);")
        icon3 = QIcon()
        icon3.addFile(":/icons/import-config.png", QSize(), QIcon.Normal, QIcon.Off)
        self.config_import_button.setIcon(icon3)
        self.config_import_button.setIconSize(QSize(30, 30))

        self.gridLayout.addWidget(self.config_import_button, 3, 7, 1, 1)

        self.status_led_label = QLabel(MainWindowV3)
        self.status_led_label.setObjectName("status_led_label")
        self.status_led_label.setGeometry(QRect(520, 425, 16, 16))
        self.status_led_label.setStyleSheet(
            "background-color: rgba(255, 255, 255, 0);\n" "color: rgba(255, 255, 255, 0);"
        )
        self.status_led_label.setFrameShape(QFrame.WinPanel)
        QWidget.setTabOrder(self.config_import_button, self.start_source)
        QWidget.setTabOrder(self.start_source, self.stop_source)
        QWidget.setTabOrder(self.stop_source, self.md1_button)
        QWidget.setTabOrder(self.md1_button, self.md1_settings)
        QWidget.setTabOrder(self.md1_settings, self.md2_button)
        QWidget.setTabOrder(self.md2_button, self.md2_settings)
        QWidget.setTabOrder(self.md2_settings, self.md3_button)
        QWidget.setTabOrder(self.md3_button, self.md3_settings)
        QWidget.setTabOrder(self.md3_settings, self.md4_button)
        QWidget.setTabOrder(self.md4_button, self.md4_settings)
        QWidget.setTabOrder(self.md4_settings, self.md5_button)
        QWidget.setTabOrder(self.md5_button, self.md5_settings)
        QWidget.setTabOrder(self.md5_settings, self.md6_button)
        QWidget.setTabOrder(self.md6_button, self.md6_settings)
        QWidget.setTabOrder(self.md6_settings, self.md7_button)
        QWidget.setTabOrder(self.md7_button, self.md7_settings)
        QWidget.setTabOrder(self.md7_settings, self.play_button)

        self.retranslateUi(MainWindowV3)

        QMetaObject.connectSlotsByName(MainWindowV3)

    # setupUi

    def retranslateUi(self, MainWindowV3):
        MainWindowV3.setWindowTitle(QCoreApplication.translate("MainWindowV3", "Configuration Window", None))
        self.board_connections.setText("")
        self.md1_button.setText(QCoreApplication.translate("MainWindowV3", "MD1", None))
        self.md2_button.setText(QCoreApplication.translate("MainWindowV3", "MD2", None))
        self.md3_button.setText(QCoreApplication.translate("MainWindowV3", "MD3", None))
        self.md4_button.setText(QCoreApplication.translate("MainWindowV3", "MD4", None))
        self.md7_button.setText(QCoreApplication.translate("MainWindowV3", "MD7", None))
        self.md6_button.setText(QCoreApplication.translate("MainWindowV3", "MD6", None))
        self.md5_button.setText(QCoreApplication.translate("MainWindowV3", "MD5", None))
        self.md1_settings.setText(QCoreApplication.translate("MainWindowV3", "...", None))
        self.md2_settings.setText(QCoreApplication.translate("MainWindowV3", "...", None))
        self.md3_settings.setText(QCoreApplication.translate("MainWindowV3", "...", None))
        self.md4_settings.setText(QCoreApplication.translate("MainWindowV3", "...", None))
        self.md5_settings.setText(QCoreApplication.translate("MainWindowV3", "...", None))
        self.md6_settings.setText(QCoreApplication.translate("MainWindowV3", "...", None))
        self.md7_settings.setText(QCoreApplication.translate("MainWindowV3", "...", None))
        self.start_source_label_text.setText(QCoreApplication.translate("MainWindowV3", "Start Source:", None))
        self.stop_settings.setText(QCoreApplication.translate("MainWindowV3", "...", None))
        # if QT_CONFIG(tooltip)
        self.config_export_button.setToolTip(
            QCoreApplication.translate(
                "MainWindowV3", "<html><head/><body><p>Save the current board configuration</p></body></html>", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.config_export_button.setText(QCoreApplication.translate("MainWindowV3", "...", None))
        self.stop_source_label_icon.setText("")
        self.stop_source.setItemText(0, QCoreApplication.translate("MainWindowV3", "GUI", None))
        self.stop_source.setItemText(1, QCoreApplication.translate("MainWindowV3", "Button1", None))
        self.stop_source.setItemText(2, QCoreApplication.translate("MainWindowV3", "Button2", None))
        self.stop_source.setItemText(3, QCoreApplication.translate("MainWindowV3", "MD5", None))
        self.stop_source.setItemText(4, QCoreApplication.translate("MainWindowV3", "MD6", None))

        # if QT_CONFIG(tooltip)
        self.stop_source.setToolTip(
            QCoreApplication.translate(
                "MainWindowV3",
                "<html><head/><body><p>Configure how measurement will be stopped</p></body></html>",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.start_settings.setText(QCoreApplication.translate("MainWindowV3", "...", None))
        # if QT_CONFIG(tooltip)
        self.play_button.setToolTip(
            QCoreApplication.translate(
                "MainWindowV3", "<html><head/><body><p>Start Measurement</p></body></html>", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.play_button.setText(QCoreApplication.translate("MainWindowV3", "...", None))
        self.start_source.setItemText(0, QCoreApplication.translate("MainWindowV3", "GUI", None))
        self.start_source.setItemText(1, QCoreApplication.translate("MainWindowV3", "Button1", None))
        self.start_source.setItemText(2, QCoreApplication.translate("MainWindowV3", "Button2", None))
        self.start_source.setItemText(3, QCoreApplication.translate("MainWindowV3", "MD5", None))
        self.start_source.setItemText(4, QCoreApplication.translate("MainWindowV3", "MD6", None))

        # if QT_CONFIG(tooltip)
        self.start_source.setToolTip(
            QCoreApplication.translate(
                "MainWindowV3",
                "<html><head/><body><p>Configure how measurement will be started</p></body></html>",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.start_source_label_icon.setText("")
        self.stop_source_label_text.setText(QCoreApplication.translate("MainWindowV3", "Stop Source:", None))
        # if QT_CONFIG(tooltip)
        self.config_import_button.setToolTip(
            QCoreApplication.translate(
                "MainWindowV3", "<html><head/><body><p>Import board configuration from file</p></body></html>", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.config_import_button.setText(QCoreApplication.translate("MainWindowV3", "...", None))

    # retranslateUi
