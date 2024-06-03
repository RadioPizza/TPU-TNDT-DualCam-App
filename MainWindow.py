# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindow.ui'
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
from PySide6.QtWidgets import (QApplication, QGraphicsView, QHBoxLayout, QLabel,
    QMainWindow, QProgressBar, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)
import res_rs

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1920, 1200)
        MainWindow.setMinimumSize(QSize(0, 0))
        MainWindow.setBaseSize(QSize(0, 0))
        MainWindow.setStyleSheet(u"")
        self.CentralWidget = QWidget(MainWindow)
        self.CentralWidget.setObjectName(u"CentralWidget")
        self.verticalLayout_5 = QVBoxLayout(self.CentralWidget)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalSpacer_2 = QSpacerItem(20, 13, QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.verticalLayout_5.addItem(self.verticalSpacer_2)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.MainCameraTitle = QLabel(self.CentralWidget)
        self.MainCameraTitle.setObjectName(u"MainCameraTitle")
        self.MainCameraTitle.setStyleSheet(u"font-size: 36pt;\n"
"")

        self.verticalLayout.addWidget(self.MainCameraTitle)

        self.MainCameraView = QGraphicsView(self.CentralWidget)
        self.MainCameraView.setObjectName(u"MainCameraView")
        self.MainCameraView.setMinimumSize(QSize(250, 200))
        self.MainCameraView.setStyleSheet(u"")

        self.verticalLayout.addWidget(self.MainCameraView)


        self.horizontalLayout_2.addLayout(self.verticalLayout)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.MainTCameraTitle = QLabel(self.CentralWidget)
        self.MainTCameraTitle.setObjectName(u"MainTCameraTitle")
        self.MainTCameraTitle.setStyleSheet(u"font-size: 36pt;\n"
"")

        self.verticalLayout_2.addWidget(self.MainTCameraTitle)

        self.MainTCameraView = QGraphicsView(self.CentralWidget)
        self.MainTCameraView.setObjectName(u"MainTCameraView")
        self.MainTCameraView.setMinimumSize(QSize(250, 200))
        self.MainTCameraView.setStyleSheet(u"")

        self.verticalLayout_2.addWidget(self.MainTCameraView)


        self.horizontalLayout_2.addLayout(self.verticalLayout_2)


        self.verticalLayout_5.addLayout(self.horizontalLayout_2)

        self.verticalSpacer = QSpacerItem(20, 150, QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.verticalLayout_5.addItem(self.verticalSpacer)

        self.MainProcessLabel = QLabel(self.CentralWidget)
        self.MainProcessLabel.setObjectName(u"MainProcessLabel")
        self.MainProcessLabel.setStyleSheet(u"")
        self.MainProcessLabel.setTextInteractionFlags(Qt.LinksAccessibleByMouse|Qt.TextSelectableByMouse)

        self.verticalLayout_5.addWidget(self.MainProcessLabel)

        self.MainProgressBar = QProgressBar(self.CentralWidget)
        self.MainProgressBar.setObjectName(u"MainProgressBar")
        self.MainProgressBar.setStyleSheet(u"")
        self.MainProgressBar.setValue(24)
        self.MainProgressBar.setTextVisible(False)

        self.verticalLayout_5.addWidget(self.MainProgressBar)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_3)

        self.MainStopButton = QPushButton(self.CentralWidget)
        self.MainStopButton.setObjectName(u"MainStopButton")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MainStopButton.sizePolicy().hasHeightForWidth())
        self.MainStopButton.setSizePolicy(sizePolicy)
        self.MainStopButton.setMinimumSize(QSize(120, 40))
        self.MainStopButton.setStyleSheet(u"")
        self.MainStopButton.setIconSize(QSize(16, 16))

        self.horizontalLayout.addWidget(self.MainStopButton)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.MainPlayButton = QPushButton(self.CentralWidget)
        self.MainPlayButton.setObjectName(u"MainPlayButton")
        sizePolicy.setHeightForWidth(self.MainPlayButton.sizePolicy().hasHeightForWidth())
        self.MainPlayButton.setSizePolicy(sizePolicy)
        self.MainPlayButton.setMinimumSize(QSize(120, 40))
        self.MainPlayButton.setStyleSheet(u"")
        self.MainPlayButton.setIconSize(QSize(16, 16))

        self.horizontalLayout.addWidget(self.MainPlayButton)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_4)


        self.verticalLayout_5.addLayout(self.horizontalLayout)

        self.verticalSpacer_3 = QSpacerItem(20, 50, QSizePolicy.Minimum, QSizePolicy.Preferred)

        self.verticalLayout_5.addItem(self.verticalSpacer_3)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer_2 = QSpacerItem(40, 40, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)

        self.MainSettingsButton = QPushButton(self.CentralWidget)
        self.MainSettingsButton.setObjectName(u"MainSettingsButton")
        sizePolicy.setHeightForWidth(self.MainSettingsButton.sizePolicy().hasHeightForWidth())
        self.MainSettingsButton.setSizePolicy(sizePolicy)
        self.MainSettingsButton.setMinimumSize(QSize(120, 40))
        self.MainSettingsButton.setStyleSheet(u"")
        icon = QIcon()
        icon.addFile(u":/icons/icons/settings.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.MainSettingsButton.setIcon(icon)
        self.MainSettingsButton.setIconSize(QSize(30, 30))

        self.horizontalLayout_3.addWidget(self.MainSettingsButton)


        self.verticalLayout_5.addLayout(self.horizontalLayout_3)

        self.verticalSpacer_4 = QSpacerItem(20, 50, QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.verticalLayout_5.addItem(self.verticalSpacer_4)

        MainWindow.setCentralWidget(self.CentralWidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Portable Thermal Control", None))
        self.MainCameraTitle.setText(QCoreApplication.translate("MainWindow", u"Camera", None))
        self.MainTCameraTitle.setText(QCoreApplication.translate("MainWindow", u"Thermographic imager", None))
        self.MainProcessLabel.setText(QCoreApplication.translate("MainWindow", u"Heating...", None))
        self.MainProgressBar.setFormat("")
        self.MainStopButton.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
        self.MainPlayButton.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.MainSettingsButton.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
    # retranslateUi

