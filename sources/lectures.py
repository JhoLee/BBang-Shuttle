# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/lectures.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import QMessageBox, QSize, QIcon
from PyQt5.QtWidgets import QDialog, QListWidgetItem
from main import show_messagebox
from PyQt5.QtGui import QStandardItemModel, QStandardItem


class Ui_Lectures(QDialog):
    def __init__(self, manager):
        super().__init__()
        self.manager = manager
        self.lectures = self.manager.lectures
        self.items = QStandardItemModel()
        self.setFixedSize(QSize(272, 200))
        self.setWindowIcon(QIcon('../resources/breadzip.ico'))
        self.is_clicked_selection = False

    def setupUi(self):
        self.setObjectName("Lectures")
        self.resize(272, 200)
        self.lst_lectures = QtWidgets.QListWidget(self)
        self.lst_lectures.setGeometry(QtCore.QRect(10, 30, 251, 121))
        font = QtGui.QFont()
        font.setFamily("Malgun Gothic")
        font.setPointSize(10)
        self.lst_lectures.setFont(font)
        self.lst_lectures.setObjectName("lst_lectures")
        self.btn_select_subject = QtWidgets.QPushButton(self)
        self.btn_select_subject.setGeometry(QtCore.QRect(180, 160, 81, 31))
        font = QtGui.QFont()
        font.setFamily("Malgun Gothic")
        font.setPointSize(10)
        self.btn_select_subject.setFont(font)
        self.btn_select_subject.setObjectName("btn_start")
        self.label_3 = QtWidgets.QLabel(self)
        self.label_3.setGeometry(QtCore.QRect(10, 10, 251, 16))
        font = QtGui.QFont()
        font.setFamily("Malgun Gothic")
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setText("<html><head/><body><p align=\"justify\">수강할 과목을 선택하십시오.</p></body></html>")
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setWordWrap(True)
        self.label_3.setObjectName("label_3")

        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Lectures", "Dialog"))
        self.btn_select_subject.setText(_translate("Lectures", "과목 선택"))
        self.setWindowTitle(_translate("Login", "수강과목 선택 :: KNUT 빵셔틀"))

        # self.items = QStandardItemModel()
        # for lecture in self.lectures:
        #     self.items.appendRow(QStandardItem(lecture.text))
        # self.lst_lectures.setModel(self.items)

        for lec in self.lectures:
            self.lst_lectures.addItem(lec.text)

        QtCore.QMetaObject.connectSlotsByName(self)

        self.btn_select_subject.clicked.connect(self.select)

    def select(self):
        self.is_clicked_selection = True
        self.close()
