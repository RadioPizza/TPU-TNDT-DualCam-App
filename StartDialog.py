# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'StartDialog.ui'
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
import res_rs

class Ui_StartDialog(object):
    def setupUi(self, StartDialog):
        if not StartDialog.objectName():
            StartDialog.setObjectName(u"StartDialog")
        StartDialog.resize(800, 800)
        StartDialog.setMinimumSize(QSize(800, 800))
        StartDialog.setMaximumSize(QSize(800, 800))
        StartDialog.setStyleSheet(u"background: #FFFFFF;\n"
"font-family: Segoe UI;\n"
"")
        self.Startframe = QFrame(StartDialog)
        self.Startframe.setObjectName(u"Startframe")
        self.Startframe.setGeometry(QRect(100, 160, 600, 550))
        self.Startframe.setStyleSheet(u"QFrame {\n"
"	background: #F5F5F5;\n"
"	border-radius: 10px;\n"
"}")
        self.Startframe.setFrameShape(QFrame.StyledPanel)
        self.Startframe.setFrameShadow(QFrame.Raised)
        self.StartStartButton = QPushButton(self.Startframe)
        self.StartStartButton.setObjectName(u"StartStartButton")
        self.StartStartButton.setGeometry(QRect(436, 490, 120, 40))
        self.StartStartButton.setStyleSheet(u"QPushButton {\n"
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
        self.StartAuthorisationTitle = QLabel(self.Startframe)
        self.StartAuthorisationTitle.setObjectName(u"StartAuthorisationTitle")
        self.StartAuthorisationTitle.setGeometry(QRect(48, 40, 508, 72))
        self.StartAuthorisationTitle.setStyleSheet(u"")
        self.StartNameLineEdit = QLineEdit(self.Startframe)
        self.StartNameLineEdit.setObjectName(u"StartNameLineEdit")
        self.StartNameLineEdit.setGeometry(QRect(196, 146, 360, 32))
        self.StartNameLineEdit.setStyleSheet(u"QLineEdit {\n"
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
"}")
        self.StartSurnameLineEdit = QLineEdit(self.Startframe)
        self.StartSurnameLineEdit.setObjectName(u"StartSurnameLineEdit")
        self.StartSurnameLineEdit.setGeometry(QRect(196, 210, 360, 32))
        self.StartSurnameLineEdit.setStyleSheet(u"QLineEdit {\n"
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
"}")
        self.StartObjectLineEdit = QLineEdit(self.Startframe)
        self.StartObjectLineEdit.setObjectName(u"StartObjectLineEdit")
        self.StartObjectLineEdit.setGeometry(QRect(196, 274, 360, 32))
        self.StartObjectLineEdit.setStyleSheet(u"QLineEdit {\n"
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
"}")
        self.StartExitButton = QPushButton(self.Startframe)
        self.StartExitButton.setObjectName(u"StartExitButton")
        self.StartExitButton.setGeometry(QRect(306, 490, 120, 40))
        self.StartExitButton.setStyleSheet(u"QPushButton {\n"
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
        self.StartNameLabel = QLabel(self.Startframe)
        self.StartNameLabel.setObjectName(u"StartNameLabel")
        self.StartNameLabel.setGeometry(QRect(48, 146, 110, 32))
        self.StartNameLabel.setStyleSheet(u"color: #252525;\n"
"font-size: 11px;\n"
"font-weight: 600;\n"
"text-transform: uppercase;")
        self.StartSurnameLabel = QLabel(self.Startframe)
        self.StartSurnameLabel.setObjectName(u"StartSurnameLabel")
        self.StartSurnameLabel.setGeometry(QRect(48, 210, 110, 32))
        self.StartSurnameLabel.setStyleSheet(u"color: #252525;\n"
"font-size: 11px;\n"
"font-weight: 600;\n"
"text-transform: uppercase;")
        self.StartObjectLabel = QLabel(self.Startframe)
        self.StartObjectLabel.setObjectName(u"StartObjectLabel")
        self.StartObjectLabel.setGeometry(QRect(48, 274, 110, 32))
        self.StartObjectLabel.setStyleSheet(u"color: #252525;\n"
"font-size: 11px;\n"
"font-weight: 600;\n"
"text-transform: uppercase;")
        self.StartPathLineEdit = QLineEdit(self.Startframe)
        self.StartPathLineEdit.setObjectName(u"StartPathLineEdit")
        self.StartPathLineEdit.setGeometry(QRect(196, 338, 255, 32))
        self.StartPathLineEdit.setAcceptDrops(False)
        self.StartPathLineEdit.setStyleSheet(u"QLineEdit {\n"
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
"}")
        self.StartPathLineEdit.setFrame(True)
        self.StartPathLineEdit.setReadOnly(True)
        self.StartPathLabel = QLabel(self.Startframe)
        self.StartPathLabel.setObjectName(u"StartPathLabel")
        self.StartPathLabel.setGeometry(QRect(48, 338, 110, 32))
        self.StartPathLabel.setStyleSheet(u"color: #252525;\n"
"font-size: 11px;\n"
"font-weight: 600;\n"
"text-transform: uppercase;")
        self.StartChangePathButton = QPushButton(self.Startframe)
        self.StartChangePathButton.setObjectName(u"StartChangePathButton")
        self.StartChangePathButton.setGeometry(QRect(460, 338, 96, 32))
        self.StartChangePathButton.setStyleSheet(u"QPushButton {\n"
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
        self.StartNameLabel.raise_()
        self.StartStartButton.raise_()
        self.StartAuthorisationTitle.raise_()
        self.StartNameLineEdit.raise_()
        self.StartSurnameLineEdit.raise_()
        self.StartObjectLineEdit.raise_()
        self.StartExitButton.raise_()
        self.StartSurnameLabel.raise_()
        self.StartObjectLabel.raise_()
        self.StartPathLineEdit.raise_()
        self.StartPathLabel.raise_()
        self.StartChangePathButton.raise_()
        self.StartTitle = QLabel(StartDialog)
        self.StartTitle.setObjectName(u"StartTitle")
        self.StartTitle.setGeometry(QRect(100, 50, 600, 100))
        self.StartTitle.setStyleSheet(u"color: #000000;\n"
"font-size: 36pt;")

        self.retranslateUi(StartDialog)

        QMetaObject.connectSlotsByName(StartDialog)
    # setupUi

    def retranslateUi(self, StartDialog):
        StartDialog.setWindowTitle(QCoreApplication.translate("StartDialog", u"Start thermal testing", None))
        self.StartStartButton.setText(QCoreApplication.translate("StartDialog", u"Start", None))
        self.StartAuthorisationTitle.setText(QCoreApplication.translate("StartDialog", u"<html><head/><body><p><span style=\" font-size:24px; font-weight:600; color:#252525;\">Authorisation<br/></span><br/><span style=\" font-size:14px; color:#252525;\">Enter your first name, last name and the name of the testing object<br/></span></p></body></html>", None))
        self.StartExitButton.setText(QCoreApplication.translate("StartDialog", u"Exit", None))
#if QT_CONFIG(whatsthis)
        self.StartNameLabel.setWhatsThis(QCoreApplication.translate("StartDialog", u"<html><head/><body><p><br/></p></body></html>", None))
#endif // QT_CONFIG(whatsthis)
        self.StartNameLabel.setText(QCoreApplication.translate("StartDialog", u"Name", None))
        self.StartSurnameLabel.setText(QCoreApplication.translate("StartDialog", u"Surname", None))
        self.StartObjectLabel.setText(QCoreApplication.translate("StartDialog", u"Object of testing", None))
        self.StartPathLineEdit.setText(QCoreApplication.translate("StartDialog", u"...", None))
        self.StartPathLabel.setText(QCoreApplication.translate("StartDialog", u"File saving path", None))
        self.StartChangePathButton.setText(QCoreApplication.translate("StartDialog", u"Change path", None))
        self.StartTitle.setText(QCoreApplication.translate("StartDialog", u"Start thermal testing", None))
    # retranslateUi

