# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'RetestDialog.ui'
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
    QPushButton, QSizePolicy, QWidget)
import res_rs

class Ui_RetestDialog(object):
    def setupUi(self, RetestDialog):
        if not RetestDialog.objectName():
            RetestDialog.setObjectName(u"RetestDialog")
        RetestDialog.resize(450, 250)
        RetestDialog.setMinimumSize(QSize(450, 250))
        RetestDialog.setMaximumSize(QSize(450, 250))
        RetestDialog.setStyleSheet(u"")
        self.RetestFrame = QFrame(RetestDialog)
        self.RetestFrame.setObjectName(u"RetestFrame")
        self.RetestFrame.setGeometry(QRect(25, 25, 400, 200))
        self.RetestFrame.setStyleSheet(u"")
        self.RetestFrame.setFrameShape(QFrame.StyledPanel)
        self.RetestFrame.setFrameShadow(QFrame.Raised)
        self.RetestTitle = QLabel(self.RetestFrame)
        self.RetestTitle.setObjectName(u"RetestTitle")
        self.RetestTitle.setGeometry(QRect(32, 40, 336, 80))
        self.RetestTitle.setStyleSheet(u"")
        self.RetestYesButton = QPushButton(self.RetestFrame)
        self.RetestYesButton.setObjectName(u"RetestYesButton")
        self.RetestYesButton.setGeometry(QRect(248, 140, 120, 40))
        self.RetestYesButton.setStyleSheet(u"")
        self.RetestNoButton = QPushButton(self.RetestFrame)
        self.RetestNoButton.setObjectName(u"RetestNoButton")
        self.RetestNoButton.setGeometry(QRect(32, 140, 120, 40))
        self.RetestNoButton.setStyleSheet(u"")

        self.retranslateUi(RetestDialog)

        QMetaObject.connectSlotsByName(RetestDialog)
    # setupUi

    def retranslateUi(self, RetestDialog):
        RetestDialog.setWindowTitle(QCoreApplication.translate("RetestDialog", u"Test this zone again?", None))
        self.RetestTitle.setText(QCoreApplication.translate("RetestDialog", u"<html><head/><body><p><span style=\" font-size:24px; font-weight:600; color:#252525;\">Zone \u2116 ...<br/></span><br/><span style=\" font-size:14px; color:#252525;\">Do you want re-testing this zone?<br/></span></p></body></html>", None))
        self.RetestYesButton.setText(QCoreApplication.translate("RetestDialog", u"No", None))
        self.RetestNoButton.setText(QCoreApplication.translate("RetestDialog", u"Yes", None))
    # retranslateUi

