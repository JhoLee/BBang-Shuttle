import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from ui.login import Ui_Login
from ui.main import Ui_Main


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Login()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
