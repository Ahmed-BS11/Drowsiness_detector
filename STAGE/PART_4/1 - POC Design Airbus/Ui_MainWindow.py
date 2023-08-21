from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QImage,QPixmap
from PyQt5.QtCore import Qt,QThread,pyqtSignal,QTimer
import random
from Worker1 import Worker1

# ### IF RADAR
# import serial
# import time
# cfgCOM = serial.Serial('/dev/ttyUSB0', 115200,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,timeout=0.3)
# dataCOM = serial.Serial('/dev/ttyUSB1', 921600,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,timeout=0.3)
# dataCOM.flushInput()
# cfgCOM.flushOutput()
# confFile = open(r"RadarCFG.cfg", 'r')
# Lines = confFile.readlines()
# for line in Lines:
#     time.sleep(.03)
#     cfgCOM.write(line.encode())
#     ack = cfgCOM.readline()
#     ack = cfgCOM.readline()
# time.sleep(5)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(960, 540)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame_radar = QtWidgets.QFrame(self.centralwidget)
        self.frame_radar.setMinimumSize(QtCore.QSize(400, 500))
        self.frame_radar.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_radar.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_radar.setObjectName("frame_radar")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame_radar)
        self.verticalLayout.setObjectName("verticalLayout")
        self.heart_rate = QtWidgets.QFrame(self.frame_radar)
        self.heart_rate.setStyleSheet("background-color: rgb(255, 217, 228);")
        self.heart_rate.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.heart_rate.setFrameShadow(QtWidgets.QFrame.Raised)
        self.heart_rate.setObjectName("heart_rate")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.heart_rate)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.logo_heart = QtWidgets.QLabel(self.heart_rate)
        self.logo_heart.setMinimumSize(QtCore.QSize(150, 0))
        self.logo_heart.setStyleSheet("image: url(:/newPrefix/heart.png);")
        self.logo_heart.setText("")
        self.logo_heart.setObjectName("logo_heart")
        self.verticalLayout_2.addWidget(self.logo_heart)
        self.label = QtWidgets.QLabel(self.heart_rate)
        self.label.setStyleSheet("color: rgb(161, 119, 131);\n"
"font: 50pt \"Arial\";")
        self.label.setObjectName("label")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.verticalLayout_2.addWidget(self.label)
        self.verticalLayout.addWidget(self.heart_rate)
        self.lung_rate = QtWidgets.QFrame(self.frame_radar)
        self.lung_rate.setStyleSheet("background-color: rgb(178, 232, 233);")
        self.lung_rate.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.lung_rate.setFrameShadow(QtWidgets.QFrame.Raised)
        self.lung_rate.setObjectName("lung_rate")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.lung_rate)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_2 = QtWidgets.QLabel(self.lung_rate)
        self.label_2.setStyleSheet("image: url(:/newPrefix/lungs.png);")
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.verticalLayout_3.addWidget(self.label_2)
        self.label_3 = QtWidgets.QLabel(self.lung_rate)
        self.label_3.setStyleSheet("\n"
"color : rgb(108, 160, 161);\n"
"\n"
"font: 50pt \"Arial\";")
        self.label_3.setObjectName("label_3")
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.verticalLayout_3.addWidget(self.label_3)
        self.verticalLayout.addWidget(self.lung_rate)
        self.horizontalLayout.addWidget(self.frame_radar)
        self.frame_camera = QtWidgets.QFrame(self.centralwidget)
        self.frame_camera.setMinimumSize(QtCore.QSize(560, 500))
        self.frame_camera.setMaximumSize(QtCore.QSize(5454112, 16777215))
        self.frame_camera.setStyleSheet("background-color: rgb(221, 221, 221);")
        self.frame_camera.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_camera.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_camera.setObjectName("frame_camera")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.frame_camera)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.logo = QtWidgets.QLabel(self.frame_camera)
        self.logo.setMinimumSize(QtCore.QSize(421, 0))
        self.logo.setMaximumSize(QtCore.QSize(421, 252))
        self.logo.setText("")
        self.logo.setObjectName("logo")
        PixMapLogo = QPixmap(r"C:\Users\moham\Desktop\PFE\Clean_PoC_Airbus\Logos\LogoActia.png")
        PixMapLogo = PixMapLogo.scaled(int(self.logo.width()*1.5),int(self.logo.height()*3),Qt.IgnoreAspectRatio, Qt.FastTransformation)
        self.logo.setPixmap(PixMapLogo)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.logo)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_6.addWidget(self.logo)
        self.label_camera = QtWidgets.QLabel(self.frame_camera)
        self.label_camera.setMinimumSize(QtCore.QSize(540, 384))
        self.label_camera.setMaximumSize(QtCore.QSize(540, 384))
        self.label_camera.setText("")
        self.label_camera.setObjectName("label_camera")
        self.verticalLayout_6.addWidget(self.label_camera)
        self.horizontalLayout.addWidget(self.frame_camera)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 960, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        self.Worker1 = Worker1()
        self.Worker1.start()
        self.Worker1.ImageUpdate.connect(self.ImageUpdateSlot)
        MainWindow.setStatusBar(self.statusbar)
        self.timer = QTimer(MainWindow)
        self.timer.timeout.connect(self.update_values)
        # self.timer.timeout.connect(self.radar) ### IF RADAR
        self.timer.start(100)  # Update values every second

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def update_values(self):
        bpm_mean = 80  # Mean BPM for adults
        bpm_stddev = 2  # Standard deviation of BPM for adults
        brpm_mean = 15  # Mean BRPM for adults
        brpm_stddev = 1  # Standard deviation of BRPM for adults

        bpm = random.gauss(bpm_mean, bpm_stddev)  # Generate random BPM from normal distribution
        brpm = random.gauss(brpm_mean, brpm_stddev)  # Generate random BRPM from normal distribution

        self.label.setText(f"{bpm:.0f} BPM")
        self.label_3.setText(f"{brpm:.0f} BRPM")

    def ImageUpdateSlot(self, Image):
        self.label_camera.setPixmap(QPixmap.fromImage(Image))

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "110 BPM"))
        self.label_3.setText(_translate("MainWindow", "96 BRPM"))
        self.frame_camera.setToolTip(_translate("MainWindow", "<html><head/><body><p>fdsgsf</p></body></html>"))

    ### RADAR PART ###
    # def radar(self):
    #     ack=dataCOM.read_until(b'\x02\x01\x04\x03\x06\x05\x08\x07')
    #     try:
    #         HR_=str(ack[40])
    #         BR_=str(ack[42])
    #         self.label.setText(f"{HR_} BPM")
    #         self.label_3.setText(f"{BR_} BRPM")
    #     except:
    #         pass
if __name__ == "__main__":
    import sys
    from Worker1 import Worker1  # Import here, at the end of the module
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())