# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/main.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from utils import *


def show_messagebox(message, title, icon=QMessageBox.Information):
    msg_box = QMessageBox()
    msg_box.setIcon(icon)
    msg_box.setText(message)
    # msg_box.setInformativeText(message)
    msg_box.setWindowTitle(title)
    # msg_box.setDetailedText("The details are as follows:")
    msg_box.setStandardButtons(QMessageBox.Ok)
    retval = msg_box.exec_()
    # print("value of pressed message box button:", retval)


class Ui_Main(object):
    def __init__(self):
        self.id = None
        self.pw = None

    def setupUi(self, _wnd_main):
        _wnd_main.setObjectName("Main")
        _wnd_main.resize(531, 332)
        self.centralwidget = QtWidgets.QWidget(_wnd_main)
        self.centralwidget.setObjectName("centralwidget")
        _wnd_main.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(_wnd_main)
        self.statusbar.setObjectName("statusbar")
        _wnd_main.setStatusBar(self.statusbar)

        _translate = QtCore.QCoreApplication.translate
        _wnd_main.setWindowTitle(_translate("Main", "MainWindow"))
        QtCore.QMetaObject.connectSlotsByName(_wnd_main)

        # Open login dialog first
        from sources.login import Ui_Login
        dlg_login = Ui_Login()
        dlg_login.setupUi()
        dlg_login.exec()

        # Get account information
        self.id = dlg_login.edit_id.text()
        self.pw = dlg_login.edit_pw.text()

        self.login(self.id, self.pw)

    @staticmethod
    def login(id, pw):
        driver = load_webdriver(debug=True)
        driver.implicitly_wait(3)
        h_web_page = open_page(driver, 'https://ecampus.ut.ac.kr')
        login(driver, h_web_page, '20029701', 'Qkrwotjr4$')
        lectures = get_lectures(driver, h_web_page, year=2020)
        lecture_range = range(len(lectures))

        choice = int(input("Select the number you want >> "))
        while choice not in lecture_range:
            print("[WARN] Please Enter a number from {}~{}".format(0, len(lectures) - 1))
            print()
            choice = int(input("Select the number you want >> "))
        lec = lectures[choice]


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    wnd_main = QtWidgets.QMainWindow()
    Ui_Main().setupUi(wnd_main)
    wnd_main.show()
    app.exec_()
