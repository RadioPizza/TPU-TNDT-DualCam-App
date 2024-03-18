# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'PaleteDialog.ui'
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
    QLabel, QPushButton, QSizePolicy, QWidget)
import res_rs

class Ui_PaletteDialog(object):
    def setupUi(self, PaletteDialog):
        if not PaletteDialog.objectName():
            PaletteDialog.setObjectName(u"PaletteDialog")
        PaletteDialog.resize(400, 300)
        PaletteDialog.setStyleSheet(u"background: #FFFFFF;\n"
"font-family: Segoe UI;\n"
"")
        self.PaletteFrame = QFrame(PaletteDialog)
        self.PaletteFrame.setObjectName(u"PaletteFrame")
        self.PaletteFrame.setGeometry(QRect(20, 20, 360, 260))
        self.PaletteFrame.setStyleSheet(u"QFrame {\n"
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
        self.PaletteFrame.setFrameShape(QFrame.StyledPanel)
        self.PaletteFrame.setFrameShadow(QFrame.Raised)
        self.PaletteLabel = QLabel(self.PaletteFrame)
        self.PaletteLabel.setObjectName(u"PaletteLabel")
        self.PaletteLabel.setGeometry(QRect(40, 20, 400, 32))
        self.PaletteLabel.setStyleSheet(u"width: 337px;\n"
"height: 80px;\n"
"color: #252525;\n"
"font-size: 24px;\n"
"font-family: Segoe UI;\n"
"font-weight: 600;\n"
"line-height: 28px; \n"
"word-wrap: break-word;\n"
"")
        self.PaletteComboBox = QComboBox(self.PaletteFrame)
        self.PaletteComboBox.addItem("")
        self.PaletteComboBox.addItem("")
        self.PaletteComboBox.addItem("")
        self.PaletteComboBox.addItem("")
        self.PaletteComboBox.setObjectName(u"PaletteComboBox")
        self.PaletteComboBox.setGeometry(QRect(40, 70, 250, 32))
        self.PaletteComboBox.setStyleSheet(u"QComboBox {\n"
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
        self.PaletteComboBox.setIconSize(QSize(16, 16))
        self.PalleteIconLabel = QLabel(self.PaletteFrame)
        self.PalleteIconLabel.setObjectName(u"PalleteIconLabel")
        self.PalleteIconLabel.setGeometry(QRect(40, 130, 250, 20))
        self.PalleteIconLabel.setPixmap(QPixmap(u":/icons/icons/palette_bw.svg"))
        self.PaletteReturnButton = QPushButton(self.PaletteFrame)
        self.PaletteReturnButton.setObjectName(u"PaletteReturnButton")
        self.PaletteReturnButton.setGeometry(QRect(40, 190, 120, 40))
        self.PaletteReturnButton.setStyleSheet(u"QPushButton {\n"
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

        self.retranslateUi(PaletteDialog)

        QMetaObject.connectSlotsByName(PaletteDialog)
    # setupUi

    def retranslateUi(self, PaletteDialog):
        PaletteDialog.setWindowTitle(QCoreApplication.translate("PaletteDialog", u"Dialog", None))
        self.PaletteLabel.setText(QCoreApplication.translate("PaletteDialog", u"Select palette", None))
        self.PaletteComboBox.setItemText(0, QCoreApplication.translate("PaletteDialog", u"b/w", None))
        self.PaletteComboBox.setItemText(1, QCoreApplication.translate("PaletteDialog", u"iron", None))
        self.PaletteComboBox.setItemText(2, QCoreApplication.translate("PaletteDialog", u"rainbow", None))
        self.PaletteComboBox.setItemText(3, QCoreApplication.translate("PaletteDialog", u"soil", None))

        self.PaletteComboBox.setCurrentText("")
        self.PaletteComboBox.setPlaceholderText("")
        self.PalleteIconLabel.setText("")
        self.PaletteReturnButton.setText(QCoreApplication.translate("PaletteDialog", u"Return", None))
    # retranslateUi

