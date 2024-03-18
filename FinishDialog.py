# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'FinishDialog.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QWidget)

class Ui_FinishDialog(object):
    def setupUi(self, FinishDialog):
        if not FinishDialog.objectName():
            FinishDialog.setObjectName(u"FinishDialog")
        FinishDialog.resize(450, 375)
        FinishDialog.setMinimumSize(QSize(450, 375))
        FinishDialog.setMaximumSize(QSize(450, 375))
        FinishDialog.setStyleSheet(u"background: #FFFFFF;\n"
"font-family: Segoe UI;\n"
"")
        self.FinishFrame = QFrame(FinishDialog)
        self.FinishFrame.setObjectName(u"FinishFrame")
        self.FinishFrame.setGeometry(QRect(25, 25, 400, 325))
        self.FinishFrame.setStyleSheet(u"QFrame {\n"
"	background: #F5F5F5;\n"
"	border-radius: 10px;\n"
"}")
        self.FinishFrame.setFrameShape(QFrame.StyledPanel)
        self.FinishFrame.setFrameShadow(QFrame.Raised)
        self.FinishTitle = QLabel(self.FinishFrame)
        self.FinishTitle.setObjectName(u"FinishTitle")
        self.FinishTitle.setGeometry(QRect(32, 40, 336, 72))
        self.FinishTitle.setCursor(QCursor(Qt.ArrowCursor))
        self.FinishTitle.setStyleSheet(u"")
        self.FinishNoButton = QPushButton(self.FinishFrame)
        self.FinishNoButton.setObjectName(u"FinishNoButton")
        self.FinishNoButton.setGeometry(QRect(248, 265, 120, 40))
        self.FinishNoButton.setStyleSheet(u"QPushButton {\n"
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
        self.FinishYesButton = QPushButton(self.FinishFrame)
        self.FinishYesButton.setObjectName(u"FinishYesButton")
        self.FinishYesButton.setGeometry(QRect(32, 265, 120, 40))
        self.FinishYesButton.setStyleSheet(u"QPushButton {\n"
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
        self.FinishChangePathButton = QPushButton(self.FinishFrame)
        self.FinishChangePathButton.setObjectName(u"FinishChangePathButton")
        self.FinishChangePathButton.setGeometry(QRect(272, 200, 96, 32))
        self.FinishChangePathButton.setStyleSheet(u"QPushButton {\n"
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
        self.FinishPathLabel = QLabel(self.FinishFrame)
        self.FinishPathLabel.setObjectName(u"FinishPathLabel")
        self.FinishPathLabel.setGeometry(QRect(32, 125, 110, 32))
        self.FinishPathLabel.setStyleSheet(u"color: #252525;\n"
"font-size: 11px;\n"
"font-weight: 600;\n"
"text-transform: uppercase;")
        self.FinishPathLineEdit = QLineEdit(self.FinishFrame)
        self.FinishPathLineEdit.setObjectName(u"FinishPathLineEdit")
        self.FinishPathLineEdit.setGeometry(QRect(32, 160, 336, 32))
        self.FinishPathLineEdit.setAcceptDrops(False)
        self.FinishPathLineEdit.setStyleSheet(u"QLineEdit {\n"
"	background: white;\n"
"	border-radius: 10px;\n"
"	align-items: center;\n"
"	overflow: hidden;\n"
"	padding: 5px 15px;\n"
"	border-bottom-color: #D1D1D1;\n"
"	border-bottom-style: solid;\n"
"	border-bottom-width: 1px;\n"
"}\n"
"\n"
"QLineEdit::hover::!focus {\n"
"	border-bottom-color: #252525;\n"
"}\n"
"\n"
"QLineEdit::focus {\n"
"	border-bottom-color: #5B5FC7;\n"
"}\n"
"\n"
"")
        self.FinishPathLineEdit.setFrame(True)
        self.FinishPathLineEdit.setReadOnly(True)

        self.retranslateUi(FinishDialog)

        QMetaObject.connectSlotsByName(FinishDialog)
    # setupUi

    def retranslateUi(self, FinishDialog):
        FinishDialog.setWindowTitle(QCoreApplication.translate("FinishDialog", u"Finish thermal testing", None))
        self.FinishTitle.setText(QCoreApplication.translate("FinishDialog", u"<html><head/><body><p><span style=\" font-size:24px; font-weight:600; color:#252525;\">Complete thermal testing?<br/></span><br/><span style=\" font-size:14px; color:#252525;\">Check the save path<br/></span></p></body></html>", None))
        self.FinishNoButton.setText(QCoreApplication.translate("FinishDialog", u"No", None))
        self.FinishYesButton.setText(QCoreApplication.translate("FinishDialog", u"Yes", None))
        self.FinishChangePathButton.setText(QCoreApplication.translate("FinishDialog", u"Change path", None))
        self.FinishPathLabel.setText(QCoreApplication.translate("FinishDialog", u"File saving path", None))
        self.FinishPathLineEdit.setText(QCoreApplication.translate("FinishDialog", u"...", None))
    # retranslateUi

