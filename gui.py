import sys
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(274, 300)
        self.text_id = QtWidgets.QPlainTextEdit(Dialog)
        self.text_id.setGeometry(QtCore.QRect(130, 10, 131, 31))
        self.text_id.setObjectName("text_id")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 20, 101, 16))
        font = QtGui.QFont()
        font.setFamily("Malgun Gothic")
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(20, 60, 101, 16))
        font = QtGui.QFont()
        font.setFamily("Malgun Gothic")
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.text_pw = QtWidgets.QPlainTextEdit(Dialog)
        self.text_pw.setGeometry(QtCore.QRect(130, 50, 131, 31))
        self.text_pw.setObjectName("text_pw")
        self.btn_login = QtWidgets.QPushButton(Dialog)
        self.btn_login.setGeometry(QtCore.QRect(170, 250, 91, 31))
        font = QtGui.QFont()
        font.setFamily("Malgun Gothic")
        font.setPointSize(12)
        self.btn_login.setFont(font)
        self.btn_login.setObjectName("btn_login")
        self.checkBox = QtWidgets.QCheckBox(Dialog)
        self.checkBox.setGeometry(QtCore.QRect(20, 100, 241, 61))
        font = QtGui.QFont()
        font.setFamily("Malgun Gothic")
        font.setPointSize(10)
        self.checkBox.setFont(font)
        self.checkBox.setChecked(False)
        self.checkBox.setAutoRepeat(False)
        self.checkBox.setObjectName("checkBox")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "한국교통대학교 e-Campus 출석체크"))
        self.label.setText(_translate("Dialog", "학     번 : "))
        self.label_2.setText(_translate("Dialog", "비밀번호 : "))
        self.btn_login.setText(_translate("Dialog", "로그인"))
        self.checkBox.setText(_translate("Dialog", "이용약관\n"
"제작자는 어떠한 결과에 대해서도 책임을 지지 않음"))




if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
