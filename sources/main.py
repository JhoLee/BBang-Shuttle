# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/main.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!

APP_VERSION = 0.1

import sys
from PyQt5.Qt import QSize, QIcon, QTimer
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QMessageBox, QMainWindow
from PyQt5.QtWidgets import QWidget

from sources.manager import EcampusManager


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


class Ui_Main(QMainWindow):
    def __init__(self):
        super().__init__()
        # super().__init__()
        self.id = None
        self.pw = None
        self.manager = None
        self.selected_lecture_index = None
        self.dlg_login = None
        self.lecture_selected = None
        self.setupUi()

    def setupUi(self):

        self.setObjectName("Main")
        self.resize(531, 312)
        self.setFixedSize(QSize(531, 312))
        self.setWindowIcon(QIcon('../resources/main.ico'))
        self.centralwidget = QtWidgets.QWidget()
        self.centralwidget.setObjectName("centralwidget")

        self.statusbar = QtWidgets.QStatusBar()
        self.statusbar.setObjectName("statusbar")
        # _wnd_main.setStatusBar(self.statusbar)

        self.lst_logs = QtWidgets.QListWidget(self.centralwidget)
        self.lst_logs.setGeometry(QtCore.QRect(10, 10, 511, 251))
        self.lst_logs.setObjectName("lst_lectures")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(10, 270, 271, 41))
        font = QtGui.QFont()
        font.setFamily("Malgun Gothic")
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setText("<html><head/><body><p align=\"center\"><span style=\" font-size:8pt;\">Version: {} Powered by ChromeDriver<br/>ⓒ 2020 @JhoLee, @cr3ux53c. All rights reserved.</span></p></body></html>".format(str(APP_VERSION)))
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setWordWrap(True)
        self.label_4.setObjectName("label_4")
        # self.btn_close = QtWidgets.QPushButton(self.centralwidget)
        # self.btn_close.setGeometry(QtCore.QRect(380, 270, 141, 31))
        font = QtGui.QFont()
        font.setFamily("Malgun Gothic")
        font.setPointSize(10)
        # self.btn_close.setFont(font)
        # self.btn_close.setObjectName("btn_close")
        self.btn_start = QtWidgets.QPushButton(self.centralwidget)
        self.btn_start.setText("수강 시작")
        self.btn_start.clicked.connect(self.start)
        self.btn_start.setGeometry(QtCore.QRect(290, 270, 71, 31))
        font = QtGui.QFont()
        font.setFamily("Malgun Gothic")
        font.setPointSize(10)
        self.btn_start.setFont(font)

        _translate = QtCore.QCoreApplication.translate
        # _wnd_main.setWindowTitle(_translate("Main", "MainWindow"))
        # self.btn_close.setText("수강 중지 및 로그아웃")
        # self.btn_close.clicked.connect(self.close)
        self.setCentralWidget(self.centralwidget)
        QtCore.QMetaObject.connectSlotsByName(self)

        self.manager = EcampusManager()

        # Open login dialog first
        from sources.login import Ui_Login
        dlg_login = Ui_Login(manager=self.manager)
        dlg_login.setupUi()
        dlg_login.exec()
        self.manager = dlg_login.manager

        # Get lecture information
        import time
        try:
            self.manager.get_lectures(year=time.gmtime().tm_year)

            # driver = dlg_login.driver
            # h_web_page = dlg_login.h_web_page
            lectures = self.manager.lectures
            if lectures is None:
                exit(-3)

            from sources.lectures import Ui_Lectures
            dlg_lectures = Ui_Lectures(manager=self.manager)
            dlg_lectures.setupUi()
            dlg_lectures.exec()

            self.selected_lecture_index = None
            for index in range(dlg_lectures.lst_lectures.count()):
                if dlg_lectures.lst_lectures.item(index).isSelected():
                    self.selected_lecture_index = index
                    break
            if self.selected_lecture_index is None:
                exit(-1)

            if not dlg_lectures.is_clicked_selection:
                exit(-2)

            self.lecture_selected = lectures[self.selected_lecture_index]

            self.manager.get_attendable_courses(self.selected_lecture_index)
            for log in self.manager.logs:
                self.lst_logs.addItem(log)

            # Todo: Generate manager instance in main.py not in login.py
            # self.manager = dlg_login.manager
            # self.manager.get_attendable_courses(selected_lecture_index)
            # # self.manager.courses == courses
            # for course in self.manager.courses:
            #     self.manager.attend_course(course)
            #
            # self.manager.log("Finish", 'info')
            #
            # # while len(self.manager.logs) > 0:
            # #     print_to_gui(self.manager.logs.pop(0))
            #
            # self.manager.driver.close()
        except:
            exit(-4)

    def start(self):
        self.btn_start.setEnabled(False)
        courses = self.manager.courses

        # for course in courses:
        # log_dump = "[INFO] Opening the course '{}' for {} min {} sec.".format(
        #     course['title'],
        #     course['time_left'] // 60,
        #     course['time_left'] % 60)
        # self.lst_logs.addItem(log_dump)
        from PyQt5.QtCore import QEventLoop
        loop = QEventLoop()
        QTimer.singleShot(3000, loop.quit)
        loop.exec_()
        self.manager.attend_all_courses()
        self.manager.driver.close()
        for log in self.manager.logs:
            self.lst_logs.addItem(log)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    wnd_main = Ui_Main()
    wnd_main.show()
    sys.exit(app.exec_())
