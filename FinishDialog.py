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
        FinishDialog.setStyleSheet(u"")
        self.FinishFrame = QFrame(FinishDialog)
        self.FinishFrame.setObjectName(u"FinishFrame")
        self.FinishFrame.setGeometry(QRect(25, 25, 400, 325))
        self.FinishFrame.setStyleSheet(u"")
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
        self.FinishNoButton.setStyleSheet(u"")
        self.FinishYesButton = QPushButton(self.FinishFrame)
        self.FinishYesButton.setObjectName(u"FinishYesButton")
        self.FinishYesButton.setGeometry(QRect(32, 265, 120, 40))
        self.FinishYesButton.setStyleSheet(u"")
        self.FinishChangePathButton = QPushButton(self.FinishFrame)
        self.FinishChangePathButton.setObjectName(u"FinishChangePathButton")
        self.FinishChangePathButton.setGeometry(QRect(272, 200, 96, 32))
        self.FinishChangePathButton.setStyleSheet(u"")
        self.FinishPathLabel = QLabel(self.FinishFrame)
        self.FinishPathLabel.setObjectName(u"FinishPathLabel")
        self.FinishPathLabel.setGeometry(QRect(32, 125, 110, 32))
        self.FinishPathLabel.setStyleSheet(u"")
        self.FinishPathLineEdit = QLineEdit(self.FinishFrame)
        self.FinishPathLineEdit.setObjectName(u"FinishPathLineEdit")
        self.FinishPathLineEdit.setGeometry(QRect(32, 160, 336, 32))
        self.FinishPathLineEdit.setAcceptDrops(False)
        self.FinishPathLineEdit.setStyleSheet(u"")
        self.FinishPathLineEdit.setFrame(True)
        self.FinishPathLineEdit.setReadOnly(True)

        self.retranslateUi(FinishDialog)

        QMetaObject.connectSlotsByName(FinishDialog)
    # setupUi

    def retranslateUi(self, FinishDialog):
        FinishDialog.setWindowTitle(QCoreApplication.translate("FinishDialog", u"Завершение теплового контроля", None))
        self.FinishTitle.setText(QCoreApplication.translate("FinishDialog", u"<html><head/><body><p><span style=\" font-size:24px; font-weight:600; color:#252525;\">Завершить тепловой контроль?<br/></span><br/><span style=\" font-size:14px; color:#252525;\">Проверьте путь сохранения<br/></span></p></body></html>", None))
        self.FinishNoButton.setText(QCoreApplication.translate("FinishDialog", u"Нет", None))
        self.FinishYesButton.setText(QCoreApplication.translate("FinishDialog", u"Да", None))
        self.FinishChangePathButton.setText(QCoreApplication.translate("FinishDialog", u"Изменить путь", None))
        self.FinishPathLabel.setText(QCoreApplication.translate("FinishDialog", u"Путь сохранения файлов", None))
        self.FinishPathLineEdit.setText(QCoreApplication.translate("FinishDialog", u"...", None))
    # retranslateUi
    