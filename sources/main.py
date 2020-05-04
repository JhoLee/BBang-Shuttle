# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/main.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt5.Qt import QSize, QIcon
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
        _wnd_main.setFixedSize(QSize(531, 332))
        _wnd_main.setWindowIcon(QIcon('../resources/main.ico'))
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

        driver = dlg_login.driver
        h_web_page = dlg_login.h_web_page
        # Get lecture information
        lectures = dlg_login.lectures
        if lectures is None:
            exit()

        from sources.lectures import Ui_Lectures
        dlg_lectures = Ui_Lectures(lectures)
        dlg_lectures.setupUi()
        dlg_lectures.exec()

        selected_lecture_index = None
        for index in range(dlg_lectures.lst_lectures.count()):
            if dlg_lectures.lst_lectures.item(index).isSelected():
                selected_lecture_index = index
                break
        if selected_lecture_index is None:
            exit(-1)

        if not dlg_lectures.is_clicked_start:
            exit(-2)

        # Todo: Generate manager instance in main.py not in login.py
        self.manager = dlg_login.manager
        self.manager.get_attendable_courses(selected_lecture_index)
        # self.manager.courses == courses
        for course in self.manager.courses:
            self.manager.attend_course(course)

        self.manager.log("Finish", 'info')

#
        # while len(self.manager.logs) > 0:
        #     print_to_gui(self.manager.logs.pop(0))
#


        self.manager.driver.close()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    wnd_main = QtWidgets.QMainWindow()
    Ui_Main().setupUi(wnd_main)
    wnd_main.show()
    sys.exit(app.exec_())
