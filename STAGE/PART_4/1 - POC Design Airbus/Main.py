from PyQt5 import QtWidgets
from Ui_MainWindow import Ui_MainWindow
import sys
import Logos.heart_rc
import Logos.lung_rc

import serial
import time

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
