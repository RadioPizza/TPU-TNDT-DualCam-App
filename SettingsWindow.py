# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'SettingsWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.6.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QFrame,
    QGraphicsView, QLabel, QPushButton, QSizePolicy,
    QSlider, QWidget)
import res_rs

class Ui_SettingsWindow(object):
    def setupUi(self, SettingsWindow):
        if not SettingsWindow.objectName():
            SettingsWindow.setObjectName(u"SettingsWindow")
        SettingsWindow.resize(1920, 1200)
        SettingsWindow.setMinimumSize(QSize(1920, 1200))
        SettingsWindow.setMaximumSize(QSize(1920, 1200))
        SettingsWindow.setStyleSheet(u"background: #FFFFFF;\n"
"font-family: Segoe UI;\n"
"")
        SettingsWindow.setInputMethodHints(Qt.ImhNone)
        self.SettingsTitle = QLabel(SettingsWindow)
        self.SettingsTitle.setObjectName(u"SettingsTitle")
        self.SettingsTitle.setGeometry(QRect(120, 50, 600, 100))
        self.SettingsTitle.setStyleSheet(u"color: #000000;\n"
"font-size: 36pt;\n"
"")
        self.SettingsUIFrame = QFrame(SettingsWindow)
        self.SettingsUIFrame.setObjectName(u"SettingsUIFrame")
        self.SettingsUIFrame.setGeometry(QRect(992, 742, 400, 268))
        self.SettingsUIFrame.setStyleSheet(u"QFrame {\n"
"	background: #F5F5F5;\n"
"	border-radius: 10px;\n"
"}\n"
"\n"
"QComboBox {\n"
"    border: 1px solid #E1DFDD;\n"
"    border-radius: 10px;\n"
"    padding: 5px;\n"
"    background-color: #FFFFFF;\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"	subcontrol-origin: padding;\n"
"	subcontrol-position: top right;\n"
"	width: 32px;\n"
"	border-left-width: 1px;\n"
"	border-left-color: #E1DFDD;\n"
"	border-left-style: solid;\n"
"	border-top-right-radius: 10px;\n"
"	border-bottom-right-radius: 10px;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"	image: url(:/icons/icons/combo_box_arrow.svg);\n"
"}\n"
"\n"
"QComboBox:hover {\n"
"    border: 1px solid #5B5FC7;\n"
"    background-color: #E1DFDD;\n"
"}")
        self.SettingsUIFrame.setFrameShape(QFrame.StyledPanel)
        self.SettingsUIFrame.setFrameShadow(QFrame.Raised)
        self.SettingsThemeLabel = QLabel(self.SettingsUIFrame)
        self.SettingsThemeLabel.setObjectName(u"SettingsThemeLabel")
        self.SettingsThemeLabel.setGeometry(QRect(42, 170, 350, 24))
        self.SettingsThemeLabel.setStyleSheet(u"color: #252525;\n"
"font-size: 14px; ")
        self.SettingsThemeComboBox = QComboBox(self.SettingsUIFrame)
        self.SettingsThemeComboBox.addItem("")
        self.SettingsThemeComboBox.addItem("")
        self.SettingsThemeComboBox.setObjectName(u"SettingsThemeComboBox")
        self.SettingsThemeComboBox.setGeometry(QRect(32, 200, 250, 32))
        self.SettingsThemeComboBox.setStyleSheet(u"")
        self.SettingsLangLabel = QLabel(self.SettingsUIFrame)
        self.SettingsLangLabel.setObjectName(u"SettingsLangLabel")
        self.SettingsLangLabel.setGeometry(QRect(42, 90, 350, 24))
        self.SettingsLangLabel.setStyleSheet(u"color: #252525;\n"
"font-size: 14px; ")
        self.SettingsLangComboBox = QComboBox(self.SettingsUIFrame)
        self.SettingsLangComboBox.addItem("")
        self.SettingsLangComboBox.addItem("")
        self.SettingsLangComboBox.setObjectName(u"SettingsLangComboBox")
        self.SettingsLangComboBox.setGeometry(QRect(32, 120, 250, 32))
        self.SettingsLangComboBox.setStyleSheet(u"")
        self.SettingsUITitle = QLabel(self.SettingsUIFrame)
        self.SettingsUITitle.setObjectName(u"SettingsUITitle")
        self.SettingsUITitle.setGeometry(QRect(32, 40, 350, 32))
        self.SettingsUITitle.setStyleSheet(u"color: #252525;\n"
"font-size: 24px; \n"
"font-weight: 600;")
        self.SettingsHeaterFrame = QFrame(SettingsWindow)
        self.SettingsHeaterFrame.setObjectName(u"SettingsHeaterFrame")
        self.SettingsHeaterFrame.setGeometry(QRect(992, 542, 400, 170))
        self.SettingsHeaterFrame.setStyleSheet(u"QFrame {\n"
"	background: #F5F5F5;\n"
"	border-radius: 10px;\n"
"}")
        self.SettingsHeaterFrame.setFrameShape(QFrame.StyledPanel)
        self.SettingsHeaterFrame.setFrameShadow(QFrame.Raised)
        self.SettingsHeaterLabel = QLabel(self.SettingsHeaterFrame)
        self.SettingsHeaterLabel.setObjectName(u"SettingsHeaterLabel")
        self.SettingsHeaterLabel.setGeometry(QRect(32, 40, 350, 32))
        self.SettingsHeaterLabel.setStyleSheet(u"color: #252525;\n"
"font-size: 24px; \n"
"font-weight: 600;")
        self.SettingsStopButton = QPushButton(self.SettingsHeaterFrame)
        self.SettingsStopButton.setObjectName(u"SettingsStopButton")
        self.SettingsStopButton.setGeometry(QRect(170, 90, 120, 40))
        self.SettingsStopButton.setStyleSheet(u"QPushButton {\n"
"	text-align: center;\n"
"	color: white;\n"
"	font-size: 18px;\n"
"	font-weight: 600;\n"
"	background: #5B5FC7; \n"
"	border-radius: 10px;\n"
"}\n"
"\n"
"QPushButton::hover::!pressed {\n"
"	background: #4F52B2;\n"
"}\n"
"\n"
"QPushButton::pressed {\n"
"	background:  #161987; \n"
"}")
        self.SettingsHeatButton = QPushButton(self.SettingsHeaterFrame)
        self.SettingsHeatButton.setObjectName(u"SettingsHeatButton")
        self.SettingsHeatButton.setGeometry(QRect(32, 90, 120, 40))
        self.SettingsHeatButton.setStyleSheet(u"QPushButton {\n"
"	text-align: center;\n"
"	color: black;\n"
"	font-size: 18px;\n"
"	font-weight: 600;\n"
"	border: 1px solid #E1DFDD;\n"
"	border-radius: 10px;\n"
"}\n"
"\n"
"QPushButton::hover::!pressed {\n"
"	background: #E1DFDD;\n"
"}\n"
"\n"
"QPushButton::pressed {\n"
"	background: #8B8B8B;\n"
"}")
        self.SettingsCamFrame = QFrame(SettingsWindow)
        self.SettingsCamFrame.setObjectName(u"SettingsCamFrame")
        self.SettingsCamFrame.setGeometry(QRect(120, 610, 800, 400))
        self.SettingsCamFrame.setStyleSheet(u"QFrame {\n"
"	background: #F5F5F5;\n"
"	border-radius: 10px;\n"
"}\n"
"\n"
"QComboBox {\n"
"    border: 1px solid #E1DFDD;\n"
"    border-radius: 10px;\n"
"    padding: 5px;\n"
"    background-color: #FFFFFF;\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"	subcontrol-origin: padding;\n"
"	subcontrol-position: top right;\n"
"	width: 32px;\n"
"	border-left-width: 1px;\n"
"	border-left-color: #E1DFDD;\n"
"	border-left-style: solid;\n"
"	border-top-right-radius: 10px;\n"
"	border-bottom-right-radius: 10px;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"	image: url(:/icons/icons/combo_box_arrow.svg);\n"
"}\n"
"\n"
"QComboBox:hover {\n"
"    border: 1px solid #5B5FC7;\n"
"    background-color: #E1DFDD;\n"
"}")
        self.SettingsCamFrame.setFrameShape(QFrame.StyledPanel)
        self.SettingsCamFrame.setFrameShadow(QFrame.Raised)
        self.SettingsCamResLabel = QLabel(self.SettingsCamFrame)
        self.SettingsCamResLabel.setObjectName(u"SettingsCamResLabel")
        self.SettingsCamResLabel.setGeometry(QRect(42, 170, 350, 24))
        self.SettingsCamResLabel.setStyleSheet(u"color: #252525;\n"
"font-size: 14px; ")
        self.SettingsCamResComboBox = QComboBox(self.SettingsCamFrame)
        self.SettingsCamResComboBox.addItem("")
        self.SettingsCamResComboBox.setObjectName(u"SettingsCamResComboBox")
        self.SettingsCamResComboBox.setGeometry(QRect(32, 200, 180, 32))
        self.SettingsCamFPSComboBox = QComboBox(self.SettingsCamFrame)
        self.SettingsCamFPSComboBox.addItem("")
        self.SettingsCamFPSComboBox.addItem("")
        self.SettingsCamFPSComboBox.setObjectName(u"SettingsCamFPSComboBox")
        self.SettingsCamFPSComboBox.setGeometry(QRect(32, 280, 120, 32))
        self.SettingsCamComboBox = QComboBox(self.SettingsCamFrame)
        self.SettingsCamComboBox.addItem("")
        self.SettingsCamComboBox.setObjectName(u"SettingsCamComboBox")
        self.SettingsCamComboBox.setGeometry(QRect(32, 120, 250, 32))
        self.SettingsCamComboBox.setStyleSheet(u"")
        self.SettingsCamComboBox.setIconSize(QSize(16, 16))
        self.SettingsCamFPSLabel = QLabel(self.SettingsCamFrame)
        self.SettingsCamFPSLabel.setObjectName(u"SettingsCamFPSLabel")
        self.SettingsCamFPSLabel.setGeometry(QRect(42, 250, 350, 24))
        self.SettingsCamFPSLabel.setStyleSheet(u"color: #252525;\n"
"font-size: 14px; ")
        self.SettingsCamConnectButton = QPushButton(self.SettingsCamFrame)
        self.SettingsCamConnectButton.setObjectName(u"SettingsCamConnectButton")
        self.SettingsCamConnectButton.setGeometry(QRect(290, 120, 96, 32))
        self.SettingsCamConnectButton.setStyleSheet(u"QPushButton {\n"
"	text-align: center;\n"
"	color: white;\n"
"	font-size: 13px;\n"
"	font-weight: 600;\n"
"	background: #5B5FC7; \n"
"	border-radius: 10px;\n"
"}\n"
"\n"
"QPushButton::hover::!pressed {\n"
"	background: #4F52B2;\n"
"}\n"
"\n"
"QPushButton::pressed {\n"
"	background:  #161987; \n"
"}")
        self.SettingsCamTitle = QLabel(self.SettingsCamFrame)
        self.SettingsCamTitle.setObjectName(u"SettingsCamTitle")
        self.SettingsCamTitle.setGeometry(QRect(32, 40, 400, 32))
        self.SettingsCamTitle.setStyleSheet(u"color: #252525;\n"
"font-size: 24px; \n"
"font-weight: 600;")
        self.SettingsCamView = QGraphicsView(self.SettingsCamFrame)
        self.SettingsCamView.setObjectName(u"SettingsCamView")
        self.SettingsCamView.setGeometry(QRect(400, 71, 381, 241))
        self.SettingsCamView.setStyleSheet(u"QGraphicsView {\n"
"	border: 1px solid #E1DFDD;\n"
"	border-radius: 10px;\n"
"	background: #FFFFFF;\n"
"}")
        self.SettingsCamLabel = QLabel(self.SettingsCamFrame)
        self.SettingsCamLabel.setObjectName(u"SettingsCamLabel")
        self.SettingsCamLabel.setGeometry(QRect(42, 90, 350, 24))
        self.SettingsCamLabel.setStyleSheet(u"color: #252525;\n"
"font-size: 14px; ")
        self.SettingsCamLabel.raise_()
        self.SettingsCamResLabel.raise_()
        self.SettingsCamResComboBox.raise_()
        self.SettingsCamFPSComboBox.raise_()
        self.SettingsCamComboBox.raise_()
        self.SettingsCamFPSLabel.raise_()
        self.SettingsCamConnectButton.raise_()
        self.SettingsCamTitle.raise_()
        self.SettingsCamView.raise_()
        self.SettingsTCamFrame = QFrame(SettingsWindow)
        self.SettingsTCamFrame.setObjectName(u"SettingsTCamFrame")
        self.SettingsTCamFrame.setGeometry(QRect(120, 160, 800, 420))
        self.SettingsTCamFrame.setStyleSheet(u"QFrame {\n"
"	background: #F5F5F5;\n"
"	border-radius: 10px;\n"
"}\n"
"\n"
"QComboBox {\n"
"    border: 1px solid #E1DFDD;\n"
"    border-radius: 10px;\n"
"    padding: 5px;\n"
"    background-color: #FFFFFF;\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"	subcontrol-origin: padding;\n"
"	subcontrol-position: top right;\n"
"	width: 32px;\n"
"	border-left-width: 1px;\n"
"	border-left-color: #E1DFDD;\n"
"	border-left-style: solid;\n"
"	border-top-right-radius: 10px;\n"
"	border-bottom-right-radius: 10px;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"	image: url(:/icons/icons/combo_box_arrow.svg);\n"
"}\n"
"\n"
"QComboBox:hover {\n"
"    border: 1px solid #5B5FC7;\n"
"    background-color: #E1DFDD;\n"
"}")
        self.SettingsTCamFrame.setFrameShape(QFrame.StyledPanel)
        self.SettingsTCamFrame.setFrameShadow(QFrame.Raised)
        self.SettingsTCamConnectButton = QPushButton(self.SettingsTCamFrame)
        self.SettingsTCamConnectButton.setObjectName(u"SettingsTCamConnectButton")
        self.SettingsTCamConnectButton.setGeometry(QRect(290, 120, 96, 32))
        self.SettingsTCamConnectButton.setStyleSheet(u"QPushButton {\n"
"	text-align: center;\n"
"	color: white;\n"
"	font-size: 13px;\n"
"	font-weight: 600;\n"
"	background: #5B5FC7; \n"
"	border-radius: 10px;\n"
"}\n"
"\n"
"QPushButton::hover::!pressed {\n"
"	background: #4F52B2;\n"
"}\n"
"\n"
"QPushButton::pressed {\n"
"	background:  #161987; \n"
"}")
        self.SettingsTCamResLabel = QLabel(self.SettingsTCamFrame)
        self.SettingsTCamResLabel.setObjectName(u"SettingsTCamResLabel")
        self.SettingsTCamResLabel.setGeometry(QRect(42, 170, 350, 24))
        self.SettingsTCamResLabel.setStyleSheet(u"color: #252525;\n"
"font-size: 14px; ")
        self.SettingsTCamLabel = QLabel(self.SettingsTCamFrame)
        self.SettingsTCamLabel.setObjectName(u"SettingsTCamLabel")
        self.SettingsTCamLabel.setGeometry(QRect(42, 90, 350, 24))
        self.SettingsTCamLabel.setStyleSheet(u"color: #252525;\n"
"font-size: 14px; ")
        self.SettingsTCamComboBox = QComboBox(self.SettingsTCamFrame)
        self.SettingsTCamComboBox.setObjectName(u"SettingsTCamComboBox")
        self.SettingsTCamComboBox.setGeometry(QRect(32, 120, 250, 32))
        self.SettingsTCamTitle = QLabel(self.SettingsTCamFrame)
        self.SettingsTCamTitle.setObjectName(u"SettingsTCamTitle")
        self.SettingsTCamTitle.setGeometry(QRect(32, 40, 400, 32))
        self.SettingsTCamTitle.setStyleSheet(u"color: #252525;\n"
"font-size: 24px; \n"
"font-weight: 600;")
        self.SettingsTCamFPSLabel = QLabel(self.SettingsTCamFrame)
        self.SettingsTCamFPSLabel.setObjectName(u"SettingsTCamFPSLabel")
        self.SettingsTCamFPSLabel.setGeometry(QRect(42, 250, 350, 24))
        self.SettingsTCamFPSLabel.setStyleSheet(u"color: #252525;\n"
"font-size: 14px; ")
        self.SettingsTCamView = QGraphicsView(self.SettingsTCamFrame)
        self.SettingsTCamView.setObjectName(u"SettingsTCamView")
        self.SettingsTCamView.setGeometry(QRect(400, 71, 381, 241))
        self.SettingsTCamView.setStyleSheet(u"QGraphicsView {\n"
"	border: 1px solid #E1DFDD;\n"
"	border-radius: 10px;\n"
"	background: #FFFFFF;\n"
"}")
        self.SettingsTCamResComboBox = QComboBox(self.SettingsTCamFrame)
        self.SettingsTCamResComboBox.setObjectName(u"SettingsTCamResComboBox")
        self.SettingsTCamResComboBox.setGeometry(QRect(32, 200, 180, 32))
        self.SettingsTCamFPSComboBox = QComboBox(self.SettingsTCamFrame)
        self.SettingsTCamFPSComboBox.setObjectName(u"SettingsTCamFPSComboBox")
        self.SettingsTCamFPSComboBox.setGeometry(QRect(32, 280, 150, 32))
        self.SettingsTCamFPSComboBox.setStyleSheet(u"")
        self.SettingsTCamCalibrationButton = QPushButton(self.SettingsTCamFrame)
        self.SettingsTCamCalibrationButton.setObjectName(u"SettingsTCamCalibrationButton")
        self.SettingsTCamCalibrationButton.setGeometry(QRect(485, 340, 96, 32))
        self.SettingsTCamCalibrationButton.setStyleSheet(u"QPushButton {\n"
"	text-align: center;\n"
"	color: black;\n"
"	font-size: 13px;\n"
"	font-weight: 600;\n"
"	border: 1px solid #E1DFDD;\n"
"	border-radius: 10px;\n"
"}\n"
"\n"
"QPushButton::hover::!pressed {\n"
"	background: #E1DFDD;\n"
"}\n"
"\n"
"QPushButton::pressed {\n"
"	background: #8B8B8B;\n"
"}")
        self.SettingsTCamFocusButton = QPushButton(self.SettingsTCamFrame)
        self.SettingsTCamFocusButton.setObjectName(u"SettingsTCamFocusButton")
        self.SettingsTCamFocusButton.setGeometry(QRect(600, 340, 96, 32))
        self.SettingsTCamFocusButton.setStyleSheet(u"QPushButton {\n"
"	text-align: center;\n"
"	color: black;\n"
"	font-size: 13px;\n"
"	font-weight: 600;\n"
"	border: 1px solid #E1DFDD;\n"
"	border-radius: 10px;\n"
"}\n"
"\n"
"QPushButton::hover::!pressed {\n"
"	background: #E1DFDD;\n"
"}\n"
"\n"
"QPushButton::pressed {\n"
"	background: #8B8B8B;\n"
"}")
        self.SettingsTCamFPSComboBox.raise_()
        self.SettingsTCamResComboBox.raise_()
        self.SettingsTCamConnectButton.raise_()
        self.SettingsTCamResLabel.raise_()
        self.SettingsTCamLabel.raise_()
        self.SettingsTCamComboBox.raise_()
        self.SettingsTCamTitle.raise_()
        self.SettingsTCamFPSLabel.raise_()
        self.SettingsTCamView.raise_()
        self.SettingsTCamCalibrationButton.raise_()
        self.SettingsTCamFocusButton.raise_()
        self.SettingsTestingFrame = QFrame(SettingsWindow)
        self.SettingsTestingFrame.setObjectName(u"SettingsTestingFrame")
        self.SettingsTestingFrame.setGeometry(QRect(992, 160, 800, 352))
        self.SettingsTestingFrame.setStyleSheet(u"QFrame {\n"
"	background: #F5F5F5;\n"
"	border-radius: 10px;\n"
"}\n"
"\n"
"QComboBox {\n"
"    border: 1px solid #E1DFDD;\n"
"    border-radius: 10px;\n"
"    padding: 5px;\n"
"    background-color: #FFFFFF;\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"	subcontrol-origin: padding;\n"
"	subcontrol-position: top right;\n"
"	width: 32px;\n"
"	border-left-width: 1px;\n"
"	border-left-color: #E1DFDD;\n"
"	border-left-style: solid;\n"
"	border-top-right-radius: 10px;\n"
"	border-bottom-right-radius: 10px;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"	image: url(:/icons/icons/combo_box_arrow.svg);\n"
"}\n"
"\n"
"QComboBox:hover {\n"
"    border: 1px solid #5B5FC7;\n"
"    background-color: #E1DFDD;\n"
"}")
        self.SettingsTestingFrame.setFrameShape(QFrame.StyledPanel)
        self.SettingsTestingFrame.setFrameShadow(QFrame.Raised)
        self.SettingsTestingDurationSlider = QSlider(self.SettingsTestingFrame)
        self.SettingsTestingDurationSlider.setObjectName(u"SettingsTestingDurationSlider")
        self.SettingsTestingDurationSlider.setGeometry(QRect(80, 120, 640, 32))
        self.SettingsTestingDurationSlider.setStyleSheet(u"QSlider {\n"
"	background-color: #F5F5F5;\n"
"}\n"
"\n"
"QSlider::groove:horizontal {\n"
"	background-color: #8B8B8B;\n"
"	height: 7px;\n"
"}\n"
"\n"
"QSlider::sub-page:horizontal {\n"
"	background-color: #4F52B2;\n"
"	border-radius: 10px;\n"
"}\n"
"\n"
"QSlider::handle:horizontal {\n"
"	background-color: #4F52B2;\n"
"	width: 10px;\n"
"	margin-top: -10px;\n"
"	margin-bottom: -10px;\n"
"	border-radius: 4px;\n"
"}\n"
"\n"
"QSlider::handle:horizontal:pressed {\n"
"	background-color: #161987;\n"
"	width: 10px;\n"
"	margin-top: -10px;\n"
"	margin-bottom: -10px;\n"
"	border-radius: 4px;\n"
"}")
        self.SettingsTestingDurationSlider.setOrientation(Qt.Horizontal)
        self.SettingsHeatingDurationSlider = QSlider(self.SettingsTestingFrame)
        self.SettingsHeatingDurationSlider.setObjectName(u"SettingsHeatingDurationSlider")
        self.SettingsHeatingDurationSlider.setGeometry(QRect(80, 200, 640, 32))
        self.SettingsHeatingDurationSlider.setStyleSheet(u"QSlider {\n"
"	background-color: #F5F5F5;\n"
"}\n"
"\n"
"QSlider::groove:horizontal {\n"
"	background-color: #8B8B8B;\n"
"	height: 7px;\n"
"}\n"
"\n"
"QSlider::sub-page:horizontal {\n"
"	background-color: #4F52B2;\n"
"	border-radius: 10px;\n"
"}\n"
"\n"
"QSlider::handle:horizontal {\n"
"	background-color: #4F52B2;\n"
"	width: 10px;\n"
"	margin-top: -10px;\n"
"	margin-bottom: -10px;\n"
"	border-radius: 4px;\n"
"}\n"
"\n"
"QSlider::handle:horizontal:pressed {\n"
"	background-color: #161987;\n"
"	width: 10px;\n"
"	margin-top: -10px;\n"
"	margin-bottom: -10px;\n"
"	border-radius: 4px;\n"
"}")
        self.SettingsHeatingDurationSlider.setOrientation(Qt.Horizontal)
        self.SettingsHeatingDurationLabel = QLabel(self.SettingsTestingFrame)
        self.SettingsHeatingDurationLabel.setObjectName(u"SettingsHeatingDurationLabel")
        self.SettingsHeatingDurationLabel.setGeometry(QRect(42, 170, 400, 24))
        self.SettingsHeatingDurationLabel.setStyleSheet(u"color: #252525;\n"
"font-size: 14px; ")
        self.SettingsTestingTitle = QLabel(self.SettingsTestingFrame)
        self.SettingsTestingTitle.setObjectName(u"SettingsTestingTitle")
        self.SettingsTestingTitle.setGeometry(QRect(32, 40, 400, 32))
        self.SettingsTestingTitle.setStyleSheet(u"color: #252525;\n"
"font-size: 24px; \n"
"font-weight: 600;")
        self.SettingsTestingDurationLabel = QLabel(self.SettingsTestingFrame)
        self.SettingsTestingDurationLabel.setObjectName(u"SettingsTestingDurationLabel")
        self.SettingsTestingDurationLabel.setGeometry(QRect(42, 90, 400, 24))
        self.SettingsTestingDurationLabel.setStyleSheet(u"color: #252525;\n"
"font-size: 14px; ")
        self.SettingsRecordFPSLabel = QLabel(self.SettingsTestingFrame)
        self.SettingsRecordFPSLabel.setObjectName(u"SettingsRecordFPSLabel")
        self.SettingsRecordFPSLabel.setGeometry(QRect(42, 250, 400, 24))
        self.SettingsRecordFPSLabel.setStyleSheet(u"color: #252525;\n"
"font-size: 14px; ")
        self.SettingsRecordFPSComboBox = QComboBox(self.SettingsTestingFrame)
        self.SettingsRecordFPSComboBox.addItem("")
        self.SettingsRecordFPSComboBox.addItem("")
        self.SettingsRecordFPSComboBox.addItem("")
        self.SettingsRecordFPSComboBox.addItem("")
        self.SettingsRecordFPSComboBox.addItem("")
        self.SettingsRecordFPSComboBox.addItem("")
        self.SettingsRecordFPSComboBox.addItem("")
        self.SettingsRecordFPSComboBox.setObjectName(u"SettingsRecordFPSComboBox")
        self.SettingsRecordFPSComboBox.setGeometry(QRect(32, 280, 120, 32))
        self.SettingsHeatingDurationPlusButton = QPushButton(self.SettingsTestingFrame)
        self.SettingsHeatingDurationPlusButton.setObjectName(u"SettingsHeatingDurationPlusButton")
        self.SettingsHeatingDurationPlusButton.setGeometry(QRect(736, 200, 32, 32))
        self.SettingsHeatingDurationPlusButton.setStyleSheet(u"QPushButton {\n"
"	text-align: center;\n"
"	color: black;\n"
"	font-size: 13px;\n"
"	font-weight: 600;\n"
"	border: 1px solid #E1DFDD;\n"
"	border-radius: 10px;\n"
"}\n"
"\n"
"QPushButton::hover::!pressed {\n"
"	background: #E1DFDD;\n"
"}\n"
"\n"
"QPushButton::pressed {\n"
"	background: #8B8B8B;\n"
"}")
        self.SettingsTestingDurationPlusButton = QPushButton(self.SettingsTestingFrame)
        self.SettingsTestingDurationPlusButton.setObjectName(u"SettingsTestingDurationPlusButton")
        self.SettingsTestingDurationPlusButton.setGeometry(QRect(736, 120, 32, 32))
        self.SettingsTestingDurationPlusButton.setStyleSheet(u"QPushButton {\n"
"	text-align: center;\n"
"	color: black;\n"
"	font-size: 13px;\n"
"	font-weight: 600;\n"
"	border: 1px solid #E1DFDD;\n"
"	border-radius: 10px;\n"
"}\n"
"\n"
"QPushButton::hover::!pressed {\n"
"	background: #E1DFDD;\n"
"}\n"
"\n"
"QPushButton::pressed {\n"
"	background: #8B8B8B;\n"
"}")
        self.SettingsTestingDurationMinusButton = QPushButton(self.SettingsTestingFrame)
        self.SettingsTestingDurationMinusButton.setObjectName(u"SettingsTestingDurationMinusButton")
        self.SettingsTestingDurationMinusButton.setGeometry(QRect(32, 120, 32, 32))
        self.SettingsTestingDurationMinusButton.setStyleSheet(u"QPushButton {\n"
"	text-align: center;\n"
"	color: black;\n"
"	font-size: 13px;\n"
"	font-weight: 600;\n"
"	border: 1px solid #E1DFDD;\n"
"	border-radius: 10px;\n"
"}\n"
"\n"
"QPushButton::hover::!pressed {\n"
"	background: #E1DFDD;\n"
"}\n"
"\n"
"QPushButton::pressed {\n"
"	background: #8B8B8B;\n"
"}")
        self.SettingsHeatingDurationMinusButton = QPushButton(self.SettingsTestingFrame)
        self.SettingsHeatingDurationMinusButton.setObjectName(u"SettingsHeatingDurationMinusButton")
        self.SettingsHeatingDurationMinusButton.setGeometry(QRect(32, 200, 32, 32))
        self.SettingsHeatingDurationMinusButton.setStyleSheet(u"QPushButton {\n"
"	text-align: center;\n"
"	color: black;\n"
"	font-size: 13px;\n"
"	font-weight: 600;\n"
"	border: 1px solid #E1DFDD;\n"
"	border-radius: 10px;\n"
"}\n"
"\n"
"QPushButton::hover::!pressed {\n"
"	background: #E1DFDD;\n"
"}\n"
"\n"
"QPushButton::pressed {\n"
"	background: #8B8B8B;\n"
"}")
        self.SettingsHomeButton = QPushButton(SettingsWindow)
        self.SettingsHomeButton.setObjectName(u"SettingsHomeButton")
        self.SettingsHomeButton.setGeometry(QRect(1570, 1070, 240, 80))
        self.SettingsHomeButton.setStyleSheet(u"QPushButton {\n"
"text-align: center;\n"
"color: black;\n"
"font-size: 36px;\n"
"border: 1px solid #E1DFDD;\n"
"border-radius: 10px;\n"
"}\n"
"\n"
"QPushButton::hover::!pressed {\n"
"background: #E1DFDD;\n"
"}\n"
"\n"
"QPushButton::pressed {\n"
"background: #8B8B8B;\n"
"}")
        icon = QIcon()
        icon.addFile(u":/icons/icons/home.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.SettingsHomeButton.setIcon(icon)
        self.SettingsHomeButton.setIconSize(QSize(60, 60))
        self.SettingsTitle.raise_()
        self.SettingsUIFrame.raise_()
        self.SettingsCamFrame.raise_()
        self.SettingsTCamFrame.raise_()
        self.SettingsTestingFrame.raise_()
        self.SettingsHomeButton.raise_()
        self.SettingsHeaterFrame.raise_()

        self.retranslateUi(SettingsWindow)

        QMetaObject.connectSlotsByName(SettingsWindow)
    # setupUi

    def retranslateUi(self, SettingsWindow):
        SettingsWindow.setWindowTitle(QCoreApplication.translate("SettingsWindow", u"Settings", None))
        self.SettingsTitle.setText(QCoreApplication.translate("SettingsWindow", u"<html><head/><body><p><span style=\" font-size:64px; color:#000000;\">Settings</span></p></body></html>", None))
        self.SettingsThemeLabel.setText(QCoreApplication.translate("SettingsWindow", u"Theme:", None))
        self.SettingsThemeComboBox.setItemText(0, QCoreApplication.translate("SettingsWindow", u"Light", None))
        self.SettingsThemeComboBox.setItemText(1, QCoreApplication.translate("SettingsWindow", u"Dark", None))

        self.SettingsLangLabel.setText(QCoreApplication.translate("SettingsWindow", u"Change language:", None))
        self.SettingsLangComboBox.setItemText(0, QCoreApplication.translate("SettingsWindow", u"English", None))
        self.SettingsLangComboBox.setItemText(1, QCoreApplication.translate("SettingsWindow", u"Russian", None))

        self.SettingsLangComboBox.setCurrentText(QCoreApplication.translate("SettingsWindow", u"English", None))
        self.SettingsUITitle.setText(QCoreApplication.translate("SettingsWindow", u"UI settings", None))
        self.SettingsHeaterLabel.setText(QCoreApplication.translate("SettingsWindow", u"Check heater", None))
        self.SettingsStopButton.setText(QCoreApplication.translate("SettingsWindow", u"Stop", None))
        self.SettingsHeatButton.setText(QCoreApplication.translate("SettingsWindow", u"Heat", None))
        self.SettingsCamResLabel.setText(QCoreApplication.translate("SettingsWindow", u"Resolution:", None))
        self.SettingsCamResComboBox.setItemText(0, QCoreApplication.translate("SettingsWindow", u"1936 x 1464", None))

        self.SettingsCamFPSComboBox.setItemText(0, QCoreApplication.translate("SettingsWindow", u"4 Hz", None))
        self.SettingsCamFPSComboBox.setItemText(1, QCoreApplication.translate("SettingsWindow", u"43 Hz", None))

        self.SettingsCamComboBox.setItemText(0, QCoreApplication.translate("SettingsWindow", u"Blackfly S BFS-PGE-27S5C", None))

        self.SettingsCamFPSLabel.setText(QCoreApplication.translate("SettingsWindow", u"FPS (preview):", None))
        self.SettingsCamConnectButton.setText(QCoreApplication.translate("SettingsWindow", u"Connect", None))
        self.SettingsCamTitle.setText(QCoreApplication.translate("SettingsWindow", u"Visible camera parameters", None))
        self.SettingsCamLabel.setText(QCoreApplication.translate("SettingsWindow", u"Use camera:", None))
        self.SettingsTCamConnectButton.setText(QCoreApplication.translate("SettingsWindow", u"Connect", None))
        self.SettingsTCamResLabel.setText(QCoreApplication.translate("SettingsWindow", u"Resolution:", None))
        self.SettingsTCamLabel.setText(QCoreApplication.translate("SettingsWindow", u"Use a thermal imager:", None))
        self.SettingsTCamTitle.setText(QCoreApplication.translate("SettingsWindow", u"IR camera parameters", None))
        self.SettingsTCamFPSLabel.setText(QCoreApplication.translate("SettingsWindow", u"FPS (preview):", None))
        self.SettingsTCamCalibrationButton.setText(QCoreApplication.translate("SettingsWindow", u"\u0421alibration", None))
        self.SettingsTCamFocusButton.setText(QCoreApplication.translate("SettingsWindow", u"Focus", None))
        self.SettingsHeatingDurationLabel.setText(QCoreApplication.translate("SettingsWindow", u"Heating duration: ... sec", None))
        self.SettingsTestingTitle.setText(QCoreApplication.translate("SettingsWindow", u"Thermal testing parameters", None))
        self.SettingsTestingDurationLabel.setText(QCoreApplication.translate("SettingsWindow", u"Duration of testing (heating + smooth cooling): ... sec", None))
        self.SettingsRecordFPSLabel.setText(QCoreApplication.translate("SettingsWindow", u"FPS (record):", None))
        self.SettingsRecordFPSComboBox.setItemText(0, QCoreApplication.translate("SettingsWindow", u"1 Hz", None))
        self.SettingsRecordFPSComboBox.setItemText(1, QCoreApplication.translate("SettingsWindow", u"2 Hz", None))
        self.SettingsRecordFPSComboBox.setItemText(2, QCoreApplication.translate("SettingsWindow", u"3 Hz", None))
        self.SettingsRecordFPSComboBox.setItemText(3, QCoreApplication.translate("SettingsWindow", u"10 Hz", None))
        self.SettingsRecordFPSComboBox.setItemText(4, QCoreApplication.translate("SettingsWindow", u"20 Hz", None))
        self.SettingsRecordFPSComboBox.setItemText(5, QCoreApplication.translate("SettingsWindow", u"30 Hz", None))
        self.SettingsRecordFPSComboBox.setItemText(6, QCoreApplication.translate("SettingsWindow", u"60 Hz", None))

        self.SettingsHeatingDurationPlusButton.setText(QCoreApplication.translate("SettingsWindow", u"+", None))
        self.SettingsTestingDurationPlusButton.setText(QCoreApplication.translate("SettingsWindow", u"+", None))
        self.SettingsTestingDurationMinusButton.setText(QCoreApplication.translate("SettingsWindow", u"-", None))
        self.SettingsHeatingDurationMinusButton.setText(QCoreApplication.translate("SettingsWindow", u"-", None))
        self.SettingsHomeButton.setText(QCoreApplication.translate("SettingsWindow", u"Home", None))
    # retranslateUi

