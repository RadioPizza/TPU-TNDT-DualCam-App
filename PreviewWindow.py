# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'PreviewWindow.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QGraphicsView,
    QLabel, QPushButton, QSizePolicy, QSlider,
    QWidget)
import res_rs

class Ui_PreviewWindow(object):
    def setupUi(self, PreviewWindow):
        if not PreviewWindow.objectName():
            PreviewWindow.setObjectName(u"PreviewWindow")
        PreviewWindow.resize(1920, 1200)
        PreviewWindow.setMinimumSize(QSize(1920, 1200))
        PreviewWindow.setMaximumSize(QSize(1920, 1200))
        PreviewWindow.setStyleSheet(u"background: #FFFFFF;\n"
"font-family: Segoe UI;\n"
"\n"
"")
        self.PreviewTitle = QLabel(PreviewWindow)
        self.PreviewTitle.setObjectName(u"PreviewTitle")
        self.PreviewTitle.setGeometry(QRect(50, 50, 600, 90))
        self.PreviewTitle.setStyleSheet(u"color: #000000;\n"
"font-size: 36pt;\n"
"")
        self.PreviewHomeButton = QPushButton(PreviewWindow)
        self.PreviewHomeButton.setObjectName(u"PreviewHomeButton")
        self.PreviewHomeButton.setGeometry(QRect(1570, 1070, 240, 80))
        self.PreviewHomeButton.setStyleSheet(u"QPushButton {\n"
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
        self.PreviewHomeButton.setIcon(icon)
        self.PreviewHomeButton.setIconSize(QSize(60, 60))
        self.PreviewFinishButton = QPushButton(PreviewWindow)
        self.PreviewFinishButton.setObjectName(u"PreviewFinishButton")
        self.PreviewFinishButton.setGeometry(QRect(1310, 1070, 240, 80))
        self.PreviewFinishButton.setStyleSheet(u"QPushButton {\n"
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
        self.PreviewFinishButton.setIconSize(QSize(60, 60))
        self.PreviewGraphFrame = QFrame(PreviewWindow)
        self.PreviewGraphFrame.setObjectName(u"PreviewGraphFrame")
        self.PreviewGraphFrame.setGeometry(QRect(988, 160, 882, 700))
        self.PreviewGraphFrame.setStyleSheet(u"QFrame {\n"
"	background: #F5F5F5;\n"
"	border-radius: 10px;\n"
"}\n"
"\n"
"QPushButton {\n"
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
"	background: #D1D1D1;;\n"
"}\n"
"\n"
"QPushButton:checked {\n"
"	border: 2px solid #4F52B2;\n"
"	border-radius: 10px;\n"
"}")
        self.PreviewGraphFrame.setFrameShape(QFrame.StyledPanel)
        self.PreviewGraphFrame.setFrameShadow(QFrame.Raised)
        self.PreviewGraph2DButton = QPushButton(self.PreviewGraphFrame)
        self.PreviewGraph2DButton.setObjectName(u"PreviewGraph2DButton")
        self.PreviewGraph2DButton.setGeometry(QRect(600, 20, 120, 40))
        self.PreviewGraph2DButton.setStyleSheet(u"")
        self.PreviewGraph2DButton.setCheckable(True)
        self.PreviewGraphView = QGraphicsView(self.PreviewGraphFrame)
        self.PreviewGraphView.setObjectName(u"PreviewGraphView")
        self.PreviewGraphView.setGeometry(QRect(32, 70, 818, 600))
        self.PreviewGraphView.viewport().setProperty("cursor", QCursor(Qt.CrossCursor))
        self.PreviewGraphView.setStyleSheet(u"QGraphicsView {\n"
"	border: 1px solid #E1DFDD;\n"
"	border-radius: 10px;\n"
"	background: #FFFFFF;\n"
"}")
        self.PreviewGraph3DButton = QPushButton(self.PreviewGraphFrame)
        self.PreviewGraph3DButton.setObjectName(u"PreviewGraph3DButton")
        self.PreviewGraph3DButton.setGeometry(QRect(730, 20, 120, 40))
        self.PreviewGraph3DButton.setStyleSheet(u"")
        self.PreviewGraph3DButton.setCheckable(True)
        self.PreviewGraphLabel = QLabel(self.PreviewGraphFrame)
        self.PreviewGraphLabel.setObjectName(u"PreviewGraphLabel")
        self.PreviewGraphLabel.setGeometry(QRect(32, 20, 400, 32))
        self.PreviewGraphLabel.setStyleSheet(u"color: #252525;\n"
"font-size: 24px; \n"
"font-weight: 600;")
        self.PreviewMapFrame = QFrame(PreviewWindow)
        self.PreviewMapFrame.setObjectName(u"PreviewMapFrame")
        self.PreviewMapFrame.setGeometry(QRect(50, 160, 882, 700))
        self.PreviewMapFrame.setStyleSheet(u"QFrame {\n"
"	background: #F5F5F5;\n"
"	border-radius: 10px;\n"
"}")
        self.PreviewMapFrame.setFrameShape(QFrame.StyledPanel)
        self.PreviewMapFrame.setFrameShadow(QFrame.Raised)
        self.PreviewMapView = QGraphicsView(self.PreviewMapFrame)
        self.PreviewMapView.setObjectName(u"PreviewMapView")
        self.PreviewMapView.setGeometry(QRect(32, 70, 818, 600))
        self.PreviewMapView.viewport().setProperty("cursor", QCursor(Qt.CrossCursor))
        self.PreviewMapView.setStyleSheet(u"QGraphicsView {\n"
"	border: 1px solid #E1DFDD;\n"
"	border-radius: 10px;\n"
"	background: #FFFFFF;\n"
"}")
        self.PreviewMapReturnButton = QPushButton(self.PreviewMapFrame)
        self.PreviewMapReturnButton.setObjectName(u"PreviewMapReturnButton")
        self.PreviewMapReturnButton.setGeometry(QRect(730, 20, 120, 40))
        self.PreviewMapReturnButton.setStyleSheet(u"QPushButton {\n"
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
        self.PreviewMapTitle = QLabel(self.PreviewMapFrame)
        self.PreviewMapTitle.setObjectName(u"PreviewMapTitle")
        self.PreviewMapTitle.setGeometry(QRect(32, 20, 400, 32))
        self.PreviewMapTitle.setStyleSheet(u"color: #252525;\n"
"font-size: 24px; \n"
"font-weight: 600;")
        self.PreviewMapPaletteButton = QPushButton(self.PreviewMapFrame)
        self.PreviewMapPaletteButton.setObjectName(u"PreviewMapPaletteButton")
        self.PreviewMapPaletteButton.setGeometry(QRect(600, 20, 120, 40))
        self.PreviewMapPaletteButton.setStyleSheet(u"QPushButton {\n"
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
        self.PreviewAlgFrame = QFrame(PreviewWindow)
        self.PreviewAlgFrame.setObjectName(u"PreviewAlgFrame")
        self.PreviewAlgFrame.setGeometry(QRect(988, 875, 882, 130))
        self.PreviewAlgFrame.setStyleSheet(u"QFrame {\n"
"	background: #F5F5F5;\n"
"	border-radius: 10px;\n"
"}\n"
"\n"
"QPushButton {\n"
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
"	background: #D1D1D1;;\n"
"}\n"
"\n"
"QPushButton:checked {\n"
"	border: 2px solid #4F52B2;\n"
"	border-radius: 10px;\n"
"}")
        self.PreviewAlgFrame.setFrameShape(QFrame.StyledPanel)
        self.PreviewAlgFrame.setFrameShadow(QFrame.Raised)
        self.PreviewAlgAVGButton = QPushButton(self.PreviewAlgFrame)
        self.PreviewAlgAVGButton.setObjectName(u"PreviewAlgAVGButton")
        self.PreviewAlgAVGButton.setGeometry(QRect(430, 70, 120, 40))
        self.PreviewAlgAVGButton.setStyleSheet(u"")
        self.PreviewAlgAVGButton.setCheckable(True)
        self.PreviewAlgFFTButton = QPushButton(self.PreviewAlgFrame)
        self.PreviewAlgFFTButton.setObjectName(u"PreviewAlgFFTButton")
        self.PreviewAlgFFTButton.setGeometry(QRect(170, 70, 120, 40))
        self.PreviewAlgFFTButton.setStyleSheet(u"")
        self.PreviewAlgFFTButton.setCheckable(True)
        self.PreviewAlgPCAButton = QPushButton(self.PreviewAlgFrame)
        self.PreviewAlgPCAButton.setObjectName(u"PreviewAlgPCAButton")
        self.PreviewAlgPCAButton.setGeometry(QRect(300, 70, 120, 40))
        self.PreviewAlgPCAButton.setStyleSheet(u"")
        self.PreviewAlgPCAButton.setCheckable(True)
        self.PreviewAlgLabel = QLabel(self.PreviewAlgFrame)
        self.PreviewAlgLabel.setObjectName(u"PreviewAlgLabel")
        self.PreviewAlgLabel.setGeometry(QRect(40, 20, 400, 32))
        self.PreviewAlgLabel.setStyleSheet(u"width: 337px;\n"
"height: 80px;\n"
"color: #252525;\n"
"font-size: 24px;\n"
"font-family: Segoe UI;\n"
"font-weight: 600;\n"
"line-height: 28px; \n"
"word-wrap: break-word;\n"
"")
        self.PreviewAlgBGButton = QPushButton(self.PreviewAlgFrame)
        self.PreviewAlgBGButton.setObjectName(u"PreviewAlgBGButton")
        self.PreviewAlgBGButton.setGeometry(QRect(40, 70, 120, 40))
        self.PreviewAlgBGButton.setStyleSheet(u"")
        self.PreviewAlgBGButton.setCheckable(True)
        self.PreviewSettingsFrame = QFrame(PreviewWindow)
        self.PreviewSettingsFrame.setObjectName(u"PreviewSettingsFrame")
        self.PreviewSettingsFrame.setGeometry(QRect(50, 875, 882, 271))
        self.PreviewSettingsFrame.setStyleSheet(u"QFrame {\n"
"	background: #F5F5F5;\n"
"	border-radius: 10px;\n"
"}\n"
"\n"
"QPushButton {\n"
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
"	background: #D1D1D1;;\n"
"}\n"
"\n"
"QPushButton:checked {\n"
"	border: 2px solid #4F52B2;\n"
"	border-radius: 10px;\n"
"}")
        self.PreviewSettingsFrame.setFrameShape(QFrame.StyledPanel)
        self.PreviewSettingsFrame.setFrameShadow(QFrame.Raised)
        self.PreviewOverlayPlusButton = QPushButton(self.PreviewSettingsFrame)
        self.PreviewOverlayPlusButton.setObjectName(u"PreviewOverlayPlusButton")
        self.PreviewOverlayPlusButton.setGeometry(QRect(820, 180, 32, 32))
        self.PreviewOverlayPlusButton.setStyleSheet(u"QPushButton {\n"
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
        self.PreviewTCamLabel = QLabel(self.PreviewSettingsFrame)
        self.PreviewTCamLabel.setObjectName(u"PreviewTCamLabel")
        self.PreviewTCamLabel.setGeometry(QRect(460, 160, 350, 24))
        self.PreviewTCamLabel.setStyleSheet(u"QLabel {\n"
"	color: #252525;\n"
"	font-size: 14px;\n"
"	qproperty-alignment: AlignRight;\n"
"}")
        self.PreviewOverlaySlider = QSlider(self.PreviewSettingsFrame)
        self.PreviewOverlaySlider.setObjectName(u"PreviewOverlaySlider")
        self.PreviewOverlaySlider.setGeometry(QRect(82, 180, 730, 32))
        self.PreviewOverlaySlider.setStyleSheet(u"QSlider {\n"
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
        self.PreviewOverlaySlider.setOrientation(Qt.Horizontal)
        self.PreviewFrameMinusButton = QPushButton(self.PreviewSettingsFrame)
        self.PreviewFrameMinusButton.setObjectName(u"PreviewFrameMinusButton")
        self.PreviewFrameMinusButton.setGeometry(QRect(34, 70, 32, 32))
        self.PreviewFrameMinusButton.setStyleSheet(u"QPushButton {\n"
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
        self.PreviewOverlayMinusButton = QPushButton(self.PreviewSettingsFrame)
        self.PreviewOverlayMinusButton.setObjectName(u"PreviewOverlayMinusButton")
        self.PreviewOverlayMinusButton.setGeometry(QRect(34, 180, 32, 32))
        self.PreviewOverlayMinusButton.setStyleSheet(u"QPushButton {\n"
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
        self.PreviewFramePlusButton = QPushButton(self.PreviewSettingsFrame)
        self.PreviewFramePlusButton.setObjectName(u"PreviewFramePlusButton")
        self.PreviewFramePlusButton.setGeometry(QRect(820, 70, 32, 32))
        self.PreviewFramePlusButton.setStyleSheet(u"QPushButton {\n"
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
        self.PreviewFrameSlider = QSlider(self.PreviewSettingsFrame)
        self.PreviewFrameSlider.setObjectName(u"PreviewFrameSlider")
        self.PreviewFrameSlider.setGeometry(QRect(82, 70, 730, 32))
        self.PreviewFrameSlider.setStyleSheet(u"QSlider {\n"
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
        self.PreviewFrameSlider.setOrientation(Qt.Horizontal)
        self.PreviewOverlayButton = QPushButton(self.PreviewSettingsFrame)
        self.PreviewOverlayButton.setObjectName(u"PreviewOverlayButton")
        self.PreviewOverlayButton.setGeometry(QRect(387, 210, 120, 40))
        self.PreviewOverlayButton.setStyleSheet(u"QPushButton {\n"
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
        self.PreviewParametersTitle = QLabel(self.PreviewSettingsFrame)
        self.PreviewParametersTitle.setObjectName(u"PreviewParametersTitle")
        self.PreviewParametersTitle.setGeometry(QRect(34, 20, 400, 32))
        self.PreviewParametersTitle.setStyleSheet(u"width: 337px;\n"
"height: 80px;\n"
"color: #252525;\n"
"font-size: 24px;\n"
"font-family: Segoe UI;\n"
"font-weight: 600;\n"
"line-height: 28px; \n"
"word-wrap: break-word;\n"
"")
        self.PreviewCamLabel = QLabel(self.PreviewSettingsFrame)
        self.PreviewCamLabel.setObjectName(u"PreviewCamLabel")
        self.PreviewCamLabel.setGeometry(QRect(82, 160, 350, 24))
        self.PreviewCamLabel.setStyleSheet(u"QLabel {\n"
"	color: #252525;\n"
"	font-size: 14px;\n"
"	qproperty-alignment: AlignLeft;\n"
"}")
        self.PreviewFramePlayButton = QPushButton(self.PreviewSettingsFrame)
        self.PreviewFramePlayButton.setObjectName(u"PreviewFramePlayButton")
        self.PreviewFramePlayButton.setGeometry(QRect(387, 100, 55, 40))
        self.PreviewFramePlayButton.setStyleSheet(u"QPushButton {\n"
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
        self.PreviewFrameStopButton = QPushButton(self.PreviewSettingsFrame)
        self.PreviewFrameStopButton.setObjectName(u"PreviewFrameStopButton")
        self.PreviewFrameStopButton.setGeometry(QRect(452, 100, 55, 40))
        self.PreviewFrameStopButton.setStyleSheet(u"QPushButton {\n"
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

        self.retranslateUi(PreviewWindow)

        QMetaObject.connectSlotsByName(PreviewWindow)
    # setupUi

    def retranslateUi(self, PreviewWindow):
        PreviewWindow.setWindowTitle(QCoreApplication.translate("PreviewWindow", u"Preview", None))
        self.PreviewTitle.setText(QCoreApplication.translate("PreviewWindow", u"<html><head/><body><p><span style=\" font-size:58px; color:#000000;\">Preview</span></p></body></html>", None))
        self.PreviewHomeButton.setText(QCoreApplication.translate("PreviewWindow", u"Home", None))
        self.PreviewFinishButton.setText(QCoreApplication.translate("PreviewWindow", u"Finish", None))
        self.PreviewGraph2DButton.setText(QCoreApplication.translate("PreviewWindow", u"2D", None))
        self.PreviewGraph3DButton.setText(QCoreApplication.translate("PreviewWindow", u"3D", None))
        self.PreviewGraphLabel.setText(QCoreApplication.translate("PreviewWindow", u"Graph", None))
        self.PreviewMapReturnButton.setText(QCoreApplication.translate("PreviewWindow", u"Return", None))
        self.PreviewMapTitle.setText(QCoreApplication.translate("PreviewWindow", u"Map", None))
        self.PreviewMapPaletteButton.setText(QCoreApplication.translate("PreviewWindow", u"Palette", None))
        self.PreviewAlgAVGButton.setText(QCoreApplication.translate("PreviewWindow", u"AVG", None))
        self.PreviewAlgFFTButton.setText(QCoreApplication.translate("PreviewWindow", u"FFT", None))
        self.PreviewAlgPCAButton.setText(QCoreApplication.translate("PreviewWindow", u"PCA", None))
        self.PreviewAlgLabel.setText(QCoreApplication.translate("PreviewWindow", u"Post-processing algorithms", None))
        self.PreviewAlgBGButton.setText(QCoreApplication.translate("PreviewWindow", u"-BG", None))
        self.PreviewOverlayPlusButton.setText(QCoreApplication.translate("PreviewWindow", u"+", None))
        self.PreviewTCamLabel.setText(QCoreApplication.translate("PreviewWindow", u"Thermographic imager", None))
        self.PreviewFrameMinusButton.setText(QCoreApplication.translate("PreviewWindow", u"-", None))
        self.PreviewOverlayMinusButton.setText(QCoreApplication.translate("PreviewWindow", u"-", None))
        self.PreviewFramePlusButton.setText(QCoreApplication.translate("PreviewWindow", u"+", None))
        self.PreviewOverlayButton.setText(QCoreApplication.translate("PreviewWindow", u"Overlay", None))
        self.PreviewParametersTitle.setText(QCoreApplication.translate("PreviewWindow", u"Display parameters", None))
        self.PreviewCamLabel.setText(QCoreApplication.translate("PreviewWindow", u"Visible camera", None))
        self.PreviewFramePlayButton.setText(QCoreApplication.translate("PreviewWindow", u"Play", None))
        self.PreviewFrameStopButton.setText(QCoreApplication.translate("PreviewWindow", u"Stop", None))
    # retranslateUi

