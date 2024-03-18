# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindow_v10.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
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
from PySide6.QtWidgets import (QApplication, QGraphicsView, QLabel, QMainWindow,
    QProgressBar, QPushButton, QSizePolicy, QWidget)
import res-rs_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1920, 1200)
        MainWindow.setMinimumSize(QSize(1920, 1200))
        MainWindow.setMaximumSize(QSize(1920, 1200))
        MainWindow.setBaseSize(QSize(0, 0))
        MainWindow.setStyleSheet(u"background: #FFFFFF;\n"
"font-family: Segoe UI;\n"
"\n"
"")
        self.CentralWidget = QWidget(MainWindow)
        self.CentralWidget.setObjectName(u"CentralWidget")
        self.MainCameraTitle = QLabel(self.CentralWidget)
        self.MainCameraTitle.setObjectName(u"MainCameraTitle")
        self.MainCameraTitle.setGeometry(QRect(120, 50, 600, 90))
        self.MainCameraTitle.setStyleSheet(u"color: #000000;\n"
"font-size: 36pt;\n"
"")
        self.MainTCameraTitle = QLabel(self.CentralWidget)
        self.MainTCameraTitle.setObjectName(u"MainTCameraTitle")
        self.MainTCameraTitle.setGeometry(QRect(992, 50, 600, 86))
        self.MainTCameraTitle.setStyleSheet(u"color: #000000;\n"
"font-size: 36pt;\n"
"")
        self.MainCameraView = QGraphicsView(self.CentralWidget)
        self.MainCameraView.setObjectName(u"MainCameraView")
        self.MainCameraView.setGeometry(QRect(120, 140, 808, 611))
        self.MainCameraView.setMinimumSize(QSize(779, 437))
        self.MainCameraView.setStyleSheet(u"QGraphicsView {\n"
"	border: 1px solid #E1DFDD;\n"
"	border-radius: 10px;\n"
"}")
        self.MainTCameraView = QGraphicsView(self.CentralWidget)
        self.MainTCameraView.setObjectName(u"MainTCameraView")
        self.MainTCameraView.setGeometry(QRect(992, 140, 808, 611))
        self.MainTCameraView.setStyleSheet(u"QGraphicsView {\n"
"	border: 1px solid #E1DFDD;\n"
"	border-radius: 10px;\n"
"}")
        self.MainPlayButton = QPushButton(self.CentralWidget)
        self.MainPlayButton.setObjectName(u"MainPlayButton")
        self.MainPlayButton.setGeometry(QRect(705, 930, 240, 80))
        self.MainPlayButton.setStyleSheet(u"QPushButton {\n"
"	color: white;\n"
"	font-size: 36px;\n"
"	background: #5B5FC7; \n"
"    border-radius: 10px;\n"
"}\n"
"\n"
"QPushButton::hover::!pressed {\n"
"  background: #4F52B2;\n"
"}\n"
"\n"
"QPushButton::pressed {\n"
"	background:  #161987; \n"
"}")
        self.MainPlayButton.setIconSize(QSize(16, 16))
        self.MainStopButton = QPushButton(self.CentralWidget)
        self.MainStopButton.setObjectName(u"MainStopButton")
        self.MainStopButton.setGeometry(QRect(975, 930, 240, 80))
        self.MainStopButton.setStyleSheet(u"QPushButton {\n"
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
        self.MainStopButton.setIconSize(QSize(16, 16))
        self.MainSettingsButton = QPushButton(self.CentralWidget)
        self.MainSettingsButton.setObjectName(u"MainSettingsButton")
        self.MainSettingsButton.setGeometry(QRect(1570, 1070, 240, 80))
        self.MainSettingsButton.setStyleSheet(u"QPushButton {\n"
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
        icon.addFile(u":/icons/icons/settings.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.MainSettingsButton.setIcon(icon)
        self.MainSettingsButton.setIconSize(QSize(60, 60))
        self.MainProgressBar = QProgressBar(self.CentralWidget)
        self.MainProgressBar.setObjectName(u"MainProgressBar")
        self.MainProgressBar.setGeometry(QRect(120, 870, 1680, 30))
        self.MainProgressBar.setStyleSheet(u"QProgressBar {\n"
"    border: 1px solid #E1DFDD;\n"
"    border-radius: 10px;\n"
"}\n"
"\n"
"QProgressBar::chunk {\n"
"    background: #4F52B2;\n"
"	border-radius: 10px;\n"
"}\n"
"")
        self.MainProgressBar.setValue(24)
        self.MainProgressBar.setTextVisible(False)
        self.MainProcessLabel = QLabel(self.CentralWidget)
        self.MainProcessLabel.setObjectName(u"MainProcessLabel")
        self.MainProcessLabel.setGeometry(QRect(135, 820, 211, 41))
        self.MainProcessLabel.setStyleSheet(u"color: #252525;\n"
"font-size: 24px; ")
        self.MainProcessLabel.setTextInteractionFlags(Qt.LinksAccessibleByMouse|Qt.TextSelectableByMouse)
        MainWindow.setCentralWidget(self.CentralWidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Portable Thermal Control", None))
        self.MainCameraTitle.setText(QCoreApplication.translate("MainWindow", u"Camera", None))
        self.MainTCameraTitle.setText(QCoreApplication.translate("MainWindow", u"Thermographic imager", None))
        self.MainPlayButton.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.MainStopButton.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
        self.MainSettingsButton.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.MainProgressBar.setFormat("")
        self.MainProcessLabel.setText(QCoreApplication.translate("MainWindow", u"Heating...", None))
    # retranslateUi

