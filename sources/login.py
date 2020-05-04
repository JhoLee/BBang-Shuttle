# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/login.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!

APP_VERSION = 0.1

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import QMessageBox, QSize, QIcon
from PyQt5.QtWidgets import QDialog
from main import show_messagebox
from utils import *

class Ui_Login(QDialog):
    def __init__(self):
        super().__init__()
        self.lectures = None
        self.driver = None
        self.h_web_page = None
        self.setWindowIcon(QIcon('../resources/login.ico'))

    def setupUi(self):
        self.setObjectName("self")
        self.resize(273, 300)
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(20, 20, 91, 16))
        font = QtGui.QFont()
        font.setFamily("Malgun Gothic")
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.setGeometry(QtCore.QRect(20, 60, 91, 16))
        font = QtGui.QFont()
        font.setFamily("Malgun Gothic")
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.btn_login = QtWidgets.QPushButton(self)
        self.btn_login.setGeometry(QtCore.QRect(180, 220, 81, 31))
        font = QtGui.QFont()
        font.setFamily("Malgun Gothic")
        font.setPointSize(10)
        self.btn_login.setFont(font)
        # self.btn_login.setObjectName("btn_login")
        self.chk_license = QtWidgets.QCheckBox(self)
        self.chk_license.setGeometry(QtCore.QRect(20, 220, 141, 31))
        font = QtGui.QFont()
        font.setFamily("Malgun Gothic")
        font.setPointSize(10)
        self.chk_license.setFont(font)
        self.chk_license.setChecked(False)
        self.chk_license.setAutoRepeat(False)
        self.chk_license.setObjectName("chk_license")
        self.edit_id = QtWidgets.QLineEdit(self)
        self.edit_id.setGeometry(QtCore.QRect(120, 20, 131, 21))
        font = QtGui.QFont()
        font.setFamily("Malgun Gothic")
        font.setPointSize(10)
        self.edit_id.setFont(font)
        self.edit_id.setObjectName("edit_id")
        self.edit_pw = QtWidgets.QLineEdit(self)
        self.edit_pw.setGeometry(QtCore.QRect(120, 60, 131, 21))
        font = QtGui.QFont()
        font.setFamily("Malgun Gothic")
        font.setPointSize(10)
        self.edit_pw.setFont(font)
        self.edit_pw.setEchoMode(QtWidgets.QLineEdit.Password)
        self.edit_pw.setObjectName("edit_pw")
        self.label_3 = QtWidgets.QLabel(self)
        self.label_3.setGeometry(QtCore.QRect(10, 90, 251, 121))
        font = QtGui.QFont()
        font.setFamily("Malgun Gothic")
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setText("<html><head/><body><p align=\"justify\">&nbsp;본 프로그램의 사용으로 야기되는 어떠한 긍정적, 부정적 결과에 대해서도 제작자는 그 책임을 지지 않습니다.</p><p align=\"justify\">&nbsp;본 프로그램은 사용자 입력 정보에 대한 어떠한 정보도 학교 서버외의 원격지로 전송하거나 수집하지 않습니다.</p></body></html>")
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setWordWrap(True)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self)
        self.label_4.setGeometry(QtCore.QRect(10, 255, 251, 41))
        font = QtGui.QFont()
        font.setFamily("Malgun Gothic")
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setText("<html><head/><body><p align=\"center\"><span style=\" font-size:8pt;\">Version: {} Powered by ChromeDriver<br/>ⓒ 2020 @JhoLee, @cr3ux53c. All rights reserved.</span></p></body></html>".format(str(APP_VERSION)))
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setWordWrap(True)
        self.label_4.setObjectName("label_4")

        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self, Login):
        _translate = QtCore.QCoreApplication.translate
        Login.setWindowTitle(_translate("Login", "로그인 :: 한국교통대학교 e-Campus 출석체크"))
        self.label.setText(_translate("Login", "학     번 : "))
        self.label_2.setText(_translate("Login", "비밀번호 : "))
        self.btn_login.setText(_translate("Login", "로그인"))
        self.chk_license.setText(_translate("Login", "위 라이선스에 동의"))
        self.btn_login.clicked.connect(self.check_validation)
        self.setFixedSize(QSize(273, 300))

    def check_validation(self):
        self.btn_login.setText("로그인 중...")
        if self.chk_license.isChecked():
            if self.edit_id.text() == '' or self.edit_pw.text() == '':
                show_messagebox('로그인 정보를 입력하십시오.', '경고', QMessageBox.Warning)
            else:
                self.driver, self.h_web_page, self.lectures = self.login()
                self.close()
        else:
            self.show_messagebox('계속 진행하려면 라이선스에 동의해야합니다.', '경고', QMessageBox.Warning)

    def login(self):
        driver = load_webdriver(debug=False)
        driver.implicitly_wait(3)
        h_web_page = open_page(driver, 'https://ecampus.ut.ac.kr')
        login(driver, h_web_page, self.edit_id, self.edit_pw)
        lectures = get_lectures(driver, h_web_page, year=2020)
        return driver, h_web_page, lectures

    @staticmethod
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