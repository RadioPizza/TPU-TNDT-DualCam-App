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
        PaletteDialog.resize(416, 339)
        PaletteDialog.setStyleSheet(u"")
        self.PaletteFrame = QFrame(PaletteDialog)
        self.PaletteFrame.setObjectName(u"PaletteFrame")
        self.PaletteFrame.setGeometry(QRect(20, 20, 360, 260))
        self.PaletteFrame.setStyleSheet(u"")
        self.PaletteFrame.setFrameShape(QFrame.StyledPanel)
        self.PaletteFrame.setFrameShadow(QFrame.Raised)
        self.PaletteLabel = QLabel(self.PaletteFrame)
        self.PaletteLabel.setObjectName(u"PaletteLabel")
        self.PaletteLabel.setGeometry(QRect(40, 20, 400, 32))
        self.PaletteLabel.setStyleSheet(u"")
        self.PaletteComboBox = QComboBox(self.PaletteFrame)
        self.PaletteComboBox.addItem("")
        self.PaletteComboBox.addItem("")
        self.PaletteComboBox.addItem("")
        self.PaletteComboBox.addItem("")
        self.PaletteComboBox.setObjectName(u"PaletteComboBox")
        self.PaletteComboBox.setGeometry(QRect(40, 70, 250, 32))
        self.PaletteComboBox.setStyleSheet(u"")
        self.PaletteComboBox.setIconSize(QSize(16, 16))
        self.PalleteIconLabel = QLabel(self.PaletteFrame)
        self.PalleteIconLabel.setObjectName(u"PalleteIconLabel")
        self.PalleteIconLabel.setGeometry(QRect(40, 130, 250, 20))
        self.PalleteIconLabel.setStyleSheet(u"")
        self.PalleteIconLabel.setPixmap(QPixmap(u":/icons/icons/palette_bw.svg"))
        self.PaletteReturnButton = QPushButton(self.PaletteFrame)
        self.PaletteReturnButton.setObjectName(u"PaletteReturnButton")
        self.PaletteReturnButton.setGeometry(QRect(40, 190, 120, 40))
        self.PaletteReturnButton.setStyleSheet(u"")

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

        self.PaletteComboBox.setCurrentText(QCoreApplication.translate("PaletteDialog", u"b/w", None))
        self.PaletteComboBox.setPlaceholderText("")
        self.PalleteIconLabel.setText("")
        self.PaletteReturnButton.setText(QCoreApplication.translate("PaletteDialog", u"Return", None))
    # retranslateUi

