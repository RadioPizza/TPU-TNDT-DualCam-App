# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'TrajectoryDialog.ui'
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

class Ui_TrajectoryDialog(object):
    def setupUi(self, TrajectoryDialog):
        if not TrajectoryDialog.objectName():
            TrajectoryDialog.setObjectName(u"TrajectoryDialog")
        TrajectoryDialog.resize(450, 450)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(TrajectoryDialog.sizePolicy().hasHeightForWidth())
        TrajectoryDialog.setSizePolicy(sizePolicy)
        TrajectoryDialog.setMinimumSize(QSize(450, 450))
        TrajectoryDialog.setMaximumSize(QSize(450, 450))
        TrajectoryDialog.setCursor(QCursor(Qt.ArrowCursor))
        TrajectoryDialog.setTabletTracking(False)
        TrajectoryDialog.setStyleSheet(u"")
        self.TrajectoryFrame = QFrame(TrajectoryDialog)
        self.TrajectoryFrame.setObjectName(u"TrajectoryFrame")
        self.TrajectoryFrame.setGeometry(QRect(25, 25, 400, 400))
        self.TrajectoryFrame.setStyleSheet(u"")
        self.TrajectoryFrame.setFrameShape(QFrame.StyledPanel)
        self.TrajectoryFrame.setFrameShadow(QFrame.Raised)
        self.TrajectoryTitle = QLabel(self.TrajectoryFrame)
        self.TrajectoryTitle.setObjectName(u"TrajectoryTitle")
        self.TrajectoryTitle.setGeometry(QRect(32, 40, 336, 72))
        self.TrajectoryTitle.setStyleSheet(u"")
        self.TrajectoryLeftButton = QPushButton(self.TrajectoryFrame)
        self.TrajectoryLeftButton.setObjectName(u"TrajectoryLeftButton")
        self.TrajectoryLeftButton.setGeometry(QRect(32, 120, 80, 60))
        self.TrajectoryLeftButton.setStyleSheet(u"")
        icon = QIcon()
        icon.addFile(u":/icons/icons/arrow_left.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.TrajectoryLeftButton.setIcon(icon)
        self.TrajectoryLeftButton.setIconSize(QSize(50, 50))
        self.TrajectoryUpButton = QPushButton(self.TrajectoryFrame)
        self.TrajectoryUpButton.setObjectName(u"TrajectoryUpButton")
        self.TrajectoryUpButton.setGeometry(QRect(117, 120, 80, 60))
        self.TrajectoryUpButton.setStyleSheet(u"")
        icon1 = QIcon()
        icon1.addFile(u":/icons/icons/arrow_up.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.TrajectoryUpButton.setIcon(icon1)
        self.TrajectoryUpButton.setIconSize(QSize(50, 50))
        self.TrajectoryDownButton = QPushButton(self.TrajectoryFrame)
        self.TrajectoryDownButton.setObjectName(u"TrajectoryDownButton")
        self.TrajectoryDownButton.setGeometry(QRect(202, 120, 80, 60))
        self.TrajectoryDownButton.setStyleSheet(u"")
        icon2 = QIcon()
        icon2.addFile(u":/icons/icons/arrow_down.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.TrajectoryDownButton.setIcon(icon2)
        self.TrajectoryDownButton.setIconSize(QSize(50, 50))
        self.TrajectoryRightButton = QPushButton(self.TrajectoryFrame)
        self.TrajectoryRightButton.setObjectName(u"TrajectoryRightButton")
        self.TrajectoryRightButton.setGeometry(QRect(288, 120, 80, 60))
        self.TrajectoryRightButton.setStyleSheet(u"")
        icon3 = QIcon()
        icon3.addFile(u":/icons/icons/arrow_right.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.TrajectoryRightButton.setIcon(icon3)
        self.TrajectoryRightButton.setIconSize(QSize(50, 50))
        self.TrajectoryRepeatButton = QPushButton(self.TrajectoryFrame)
        self.TrajectoryRepeatButton.setObjectName(u"TrajectoryRepeatButton")
        self.TrajectoryRepeatButton.setGeometry(QRect(32, 280, 336, 40))
        self.TrajectoryRepeatButton.setStyleSheet(u"")
        self.TrajectoryPreviewButton = QPushButton(self.TrajectoryFrame)
        self.TrajectoryPreviewButton.setObjectName(u"TrajectoryPreviewButton")
        self.TrajectoryPreviewButton.setGeometry(QRect(32, 230, 336, 40))
        self.TrajectoryPreviewButton.setStyleSheet(u"")
        self.TrajectoryFinishButton = QPushButton(self.TrajectoryFrame)
        self.TrajectoryFinishButton.setObjectName(u"TrajectoryFinishButton")
        self.TrajectoryFinishButton.setGeometry(QRect(32, 330, 336, 40))
        self.TrajectoryFinishButton.setStyleSheet(u"")

        self.retranslateUi(TrajectoryDialog)

        QMetaObject.connectSlotsByName(TrajectoryDialog)
    # setupUi

    def retranslateUi(self, TrajectoryDialog):
        TrajectoryDialog.setWindowTitle(QCoreApplication.translate("TrajectoryDialog", u"Zone testing completed!", None))
        self.TrajectoryTitle.setText(QCoreApplication.translate("TrajectoryDialog", u"<html><head/><body><p><span style=\" font-size:24px; font-weight:600; color:#252525;\">Zone testing completed!<br/></span><br/><span style=\" font-size:14px; color:#252525;\">Select the location of the next testing zone<br/><br/></span></p></body></html>", None))
        self.TrajectoryLeftButton.setText("")
        self.TrajectoryUpButton.setText("")
        self.TrajectoryDownButton.setText("")
        self.TrajectoryRightButton.setText("")
        self.TrajectoryRepeatButton.setText(QCoreApplication.translate("TrajectoryDialog", u"Repeat", None))
        self.TrajectoryPreviewButton.setText(QCoreApplication.translate("TrajectoryDialog", u"Preview", None))
        self.TrajectoryFinishButton.setText(QCoreApplication.translate("TrajectoryDialog", u"Finish", None))
    # retranslateUi

