import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from ui.login import Ui_Login
from ui.main import Ui_Main


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    Main = QtWidgets.QMainWindow()
    main = Ui_Main()
    main.setupUi(Main)
    Main.show()
    app.exec_()
