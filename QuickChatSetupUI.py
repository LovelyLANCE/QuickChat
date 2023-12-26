# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'QuickChatSetupUI.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
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
from PySide6.QtWidgets import (QApplication, QComboBox, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QWidget)
import image_rc

class Ui_QuickChatSetup(object):
    def setupUi(self, QuickChatSetup):
        if not QuickChatSetup.objectName():
            QuickChatSetup.setObjectName(u"QuickChatSetup")
        QuickChatSetup.setEnabled(True)
        QuickChatSetup.resize(400, 233)
        QuickChatSetup.setMinimumSize(QSize(400, 233))
        QuickChatSetup.setMaximumSize(QSize(400, 233))
        font = QFont()
        font.setPointSize(15)
        QuickChatSetup.setFont(font)
        QuickChatSetup.setStyleSheet(u"QWidget{\n"
"	background-color: white\n"
"}")
        self.adapterBox = QComboBox(QuickChatSetup)
        self.adapterBox.setObjectName(u"adapterBox")
        self.adapterBox.setGeometry(QRect(140, 140, 211, 22))
        self.portBox = QLineEdit(QuickChatSetup)
        self.portBox.setObjectName(u"portBox")
        self.portBox.setGeometry(QRect(140, 170, 211, 21))
        self.adapterLabel = QLabel(QuickChatSetup)
        self.adapterLabel.setObjectName(u"adapterLabel")
        self.adapterLabel.setGeometry(QRect(40, 140, 81, 20))
        font1 = QFont()
        font1.setPointSize(10)
        self.adapterLabel.setFont(font1)
        self.portLabel = QLabel(QuickChatSetup)
        self.portLabel.setObjectName(u"portLabel")
        self.portLabel.setGeometry(QRect(40, 170, 81, 20))
        self.portLabel.setFont(font1)
        self.label_3 = QLabel(QuickChatSetup)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(60, 10, 91, 91))
        self.label_3.setPixmap(QPixmap(u":/image/icon.png"))
        self.label_3.setScaledContents(True)
        self.label_4 = QLabel(QuickChatSetup)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(170, 30, 91, 51))
        font2 = QFont()
        font2.setPointSize(25)
        self.label_4.setFont(font2)
        self.label_4.setStyleSheet(u"QLabel{\n"
"	color: rgb(2, 174, 255)\n"
"}")
        self.label_5 = QLabel(QuickChatSetup)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(260, 30, 81, 51))
        self.label_5.setFont(font2)
        self.label_5.setStyleSheet(u"QLabel {\n"
"	color: rgb(13, 95, 172)\n"
"}")
        self.setupButton = QPushButton(QuickChatSetup)
        self.setupButton.setObjectName(u"setupButton")
        self.setupButton.setGeometry(QRect(140, 200, 120, 25))
        self.setupButton.setFont(font1)
        self.portLabel_2 = QLabel(QuickChatSetup)
        self.portLabel_2.setObjectName(u"portLabel_2")
        self.portLabel_2.setGeometry(QRect(40, 110, 81, 20))
        self.portLabel_2.setFont(font1)
        self.nameBox = QLineEdit(QuickChatSetup)
        self.nameBox.setObjectName(u"nameBox")
        self.nameBox.setGeometry(QRect(140, 110, 211, 21))

        self.retranslateUi(QuickChatSetup)

        QMetaObject.connectSlotsByName(QuickChatSetup)
    # setupUi

    def retranslateUi(self, QuickChatSetup):
        QuickChatSetup.setWindowTitle(QCoreApplication.translate("QuickChatSetup", u"Setup", None))
        self.adapterLabel.setText(QCoreApplication.translate("QuickChatSetup", u"\u7f51\u7edc\u9002\u914d\u5668\uff1a", None))
        self.portLabel.setText(QCoreApplication.translate("QuickChatSetup", u"\u542f\u52a8\u7aef\u53e3\u53f7\uff1a", None))
        self.label_3.setText("")
        self.label_4.setText(QCoreApplication.translate("QuickChatSetup", u"Quick", None))
        self.label_5.setText(QCoreApplication.translate("QuickChatSetup", u"Chat", None))
        self.setupButton.setText(QCoreApplication.translate("QuickChatSetup", u"\u542f\u52a8", None))
        self.portLabel_2.setText(QCoreApplication.translate("QuickChatSetup", u"\u7528\u6237\u540d\u79f0\uff1a", None))
    # retranslateUi

