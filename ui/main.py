# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/main.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Main(object):
    def setupUi(self, Main):
        Main.setObjectName("Main")
        Main.resize(504, 300)
        font = QtGui.QFont()
        font.setFamily("Malgun Gothic")
        font.setPointSize(10)
        Main.setFont(font)
        self.plainTextEdit = QtWidgets.QPlainTextEdit(Main)
        self.plainTextEdit.setGeometry(QtCore.QRect(10, 90, 481, 161))
        self.plainTextEdit.setObjectName("plainTextEdit")

        self.retranslateUi(Main)
        QtCore.QMetaObject.connectSlotsByName(Main)

    def retranslateUi(self, Main):
        _translate = QtCore.QCoreApplication.translate
        Main.setWindowTitle(_translate("Main", "Dialog"))
