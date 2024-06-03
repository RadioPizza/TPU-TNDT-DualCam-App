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
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)
import res_rs

class Ui_StartDialog(object):
    def setupUi(self, StartDialog):
        if not StartDialog.objectName():
            StartDialog.setObjectName(u"StartDialog")
        StartDialog.setWindowModality(Qt.ApplicationModal)
        StartDialog.resize(1920, 1200)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(StartDialog.sizePolicy().hasHeightForWidth())
        StartDialog.setSizePolicy(sizePolicy)
        StartDialog.setStyleSheet(u"")
        StartDialog.setSizeGripEnabled(False)
        self.horizontalLayout = QHBoxLayout(StartDialog)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(641, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalSpacer = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.StartTitle = QLabel(StartDialog)
        self.StartTitle.setObjectName(u"StartTitle")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.StartTitle.sizePolicy().hasHeightForWidth())
        self.StartTitle.setSizePolicy(sizePolicy1)
        self.StartTitle.setMinimumSize(QSize(600, 100))
        self.StartTitle.setStyleSheet(u"font-size: 36pt;")

        self.verticalLayout.addWidget(self.StartTitle)

        self.Startframe = QFrame(StartDialog)
        self.Startframe.setObjectName(u"Startframe")
        sizePolicy1.setHeightForWidth(self.Startframe.sizePolicy().hasHeightForWidth())
        self.Startframe.setSizePolicy(sizePolicy1)
        self.Startframe.setMinimumSize(QSize(600, 550))
        self.Startframe.setStyleSheet(u"")
        self.Startframe.setFrameShape(QFrame.StyledPanel)
        self.Startframe.setFrameShadow(QFrame.Raised)
        self.StartStartButton = QPushButton(self.Startframe)
        self.StartStartButton.setObjectName(u"StartStartButton")
        self.StartStartButton.setGeometry(QRect(436, 490, 120, 40))
        sizePolicy1.setHeightForWidth(self.StartStartButton.sizePolicy().hasHeightForWidth())
        self.StartStartButton.setSizePolicy(sizePolicy1)
        self.StartStartButton.setStyleSheet(u"")
        self.StartAuthorisationTitle = QLabel(self.Startframe)
        self.StartAuthorisationTitle.setObjectName(u"StartAuthorisationTitle")
        self.StartAuthorisationTitle.setGeometry(QRect(48, 40, 508, 72))
        self.StartAuthorisationTitle.setStyleSheet(u"")
        self.StartNameLineEdit = QLineEdit(self.Startframe)
        self.StartNameLineEdit.setObjectName(u"StartNameLineEdit")
        self.StartNameLineEdit.setGeometry(QRect(196, 146, 360, 32))
        self.StartNameLineEdit.setStyleSheet(u"")
        self.StartSurnameLineEdit = QLineEdit(self.Startframe)
        self.StartSurnameLineEdit.setObjectName(u"StartSurnameLineEdit")
        self.StartSurnameLineEdit.setGeometry(QRect(196, 210, 360, 32))
        self.StartSurnameLineEdit.setStyleSheet(u"")
        self.StartObjectLineEdit = QLineEdit(self.Startframe)
        self.StartObjectLineEdit.setObjectName(u"StartObjectLineEdit")
        self.StartObjectLineEdit.setGeometry(QRect(196, 274, 360, 32))
        self.StartObjectLineEdit.setStyleSheet(u"")
        self.StartExitButton = QPushButton(self.Startframe)
        self.StartExitButton.setObjectName(u"StartExitButton")
        self.StartExitButton.setGeometry(QRect(306, 490, 120, 40))
        sizePolicy1.setHeightForWidth(self.StartExitButton.sizePolicy().hasHeightForWidth())
        self.StartExitButton.setSizePolicy(sizePolicy1)
        self.StartExitButton.setStyleSheet(u"")
        self.StartNameLabel = QLabel(self.Startframe)
        self.StartNameLabel.setObjectName(u"StartNameLabel")
        self.StartNameLabel.setGeometry(QRect(48, 146, 110, 32))
        self.StartNameLabel.setStyleSheet(u"")
        self.StartSurnameLabel = QLabel(self.Startframe)
        self.StartSurnameLabel.setObjectName(u"StartSurnameLabel")
        self.StartSurnameLabel.setGeometry(QRect(48, 210, 110, 32))
        self.StartSurnameLabel.setStyleSheet(u"")
        self.StartObjectLabel = QLabel(self.Startframe)
        self.StartObjectLabel.setObjectName(u"StartObjectLabel")
        self.StartObjectLabel.setGeometry(QRect(48, 274, 110, 32))
        self.StartObjectLabel.setStyleSheet(u"")
        self.StartPathLineEdit = QLineEdit(self.Startframe)
        self.StartPathLineEdit.setObjectName(u"StartPathLineEdit")
        self.StartPathLineEdit.setGeometry(QRect(196, 338, 255, 32))
        self.StartPathLineEdit.setAcceptDrops(False)
        self.StartPathLineEdit.setStyleSheet(u"")
        self.StartPathLineEdit.setFrame(True)
        self.StartPathLineEdit.setReadOnly(True)
        self.StartPathLabel = QLabel(self.Startframe)
        self.StartPathLabel.setObjectName(u"StartPathLabel")
        self.StartPathLabel.setGeometry(QRect(48, 338, 110, 32))
        self.StartPathLabel.setStyleSheet(u"")
        self.StartChangePathButton = QPushButton(self.Startframe)
        self.StartChangePathButton.setObjectName(u"StartChangePathButton")
        self.StartChangePathButton.setGeometry(QRect(460, 338, 96, 32))
        sizePolicy1.setHeightForWidth(self.StartChangePathButton.sizePolicy().hasHeightForWidth())
        self.StartChangePathButton.setSizePolicy(sizePolicy1)
        self.StartChangePathButton.setStyleSheet(u"font-size: 13px;")
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

        self.verticalLayout.addWidget(self.Startframe)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_2)


        self.horizontalLayout.addLayout(self.verticalLayout)

        self.horizontalSpacer_2 = QSpacerItem(641, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)


        self.retranslateUi(StartDialog)

        QMetaObject.connectSlotsByName(StartDialog)
    # setupUi

    def retranslateUi(self, StartDialog):
        StartDialog.setWindowTitle(QCoreApplication.translate("StartDialog", u"Start thermal testing", None))
        self.StartTitle.setText(QCoreApplication.translate("StartDialog", u"Start thermal testing", None))
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
    # retranslateUi

