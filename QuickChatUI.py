# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'QuickChatUI.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QPushButton, QSizePolicy,
    QTextEdit, QWidget)

class Ui_QuickChat(object):
    def setupUi(self, QuickChat):
        if not QuickChat.objectName():
            QuickChat.setObjectName(u"QuickChat")
        QuickChat.resize(1080, 720)
        QuickChat.setMinimumSize(QSize(1080, 720))
        QuickChat.setMaximumSize(QSize(1080, 720))
        self.messageBox = QTextEdit(QuickChat)
        self.messageBox.setObjectName(u"messageBox")
        self.messageBox.setGeometry(QRect(20, 20, 750, 650))
        self.messageBox.setReadOnly(True)
        self.editBox = QTextEdit(QuickChat)
        self.editBox.setObjectName(u"editBox")
        self.editBox.setGeometry(QRect(20, 680, 661, 31))
        self.sendButton = QPushButton(QuickChat)
        self.sendButton.setObjectName(u"sendButton")
        self.sendButton.setGeometry(QRect(690, 680, 81, 31))
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.sendButton.setFont(font)
        self.memberBox = QTextEdit(QuickChat)
        self.memberBox.setObjectName(u"memberBox")
        self.memberBox.setGeometry(QRect(800, 70, 261, 281))
        self.memberBox.setReadOnly(True)
        self.label = QLabel(QuickChat)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(890, 30, 101, 31))
        font1 = QFont()
        font1.setPointSize(15)
        font1.setBold(True)
        self.label.setFont(font1)
        self.inviteBox = QTextEdit(QuickChat)
        self.inviteBox.setObjectName(u"inviteBox")
        self.inviteBox.setGeometry(QRect(800, 410, 261, 261))
        self.inviteButton = QPushButton(QuickChat)
        self.inviteButton.setObjectName(u"inviteButton")
        self.inviteButton.setGeometry(QRect(890, 680, 75, 31))
        self.inviteButton.setFont(font)
        self.label_2 = QLabel(QuickChat)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(820, 370, 261, 31))
        font2 = QFont()
        font2.setPointSize(12)
        font2.setBold(False)
        self.label_2.setFont(font2)

        self.retranslateUi(QuickChat)

        QMetaObject.connectSlotsByName(QuickChat)
    # setupUi

    def retranslateUi(self, QuickChat):
        QuickChat.setWindowTitle(QCoreApplication.translate("QuickChat", u"Form", None))
        self.sendButton.setText(QCoreApplication.translate("QuickChat", u"\u53d1\u9001", None))
        self.label.setText(QCoreApplication.translate("QuickChat", u"\u5728\u7ebf\u6210\u5458", None))
        self.inviteButton.setText(QCoreApplication.translate("QuickChat", u"\u9080\u8bf7", None))
        self.label_2.setText(QCoreApplication.translate("QuickChat", u"\u5728\u4e0b\u65b9\u8f93\u5165\u9080\u8bf7\u81f3\u804a\u5929\u5ba4\u7684\u6210\u5458", None))
    # retranslateUi

