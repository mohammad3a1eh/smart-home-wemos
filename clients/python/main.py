from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import requests
import threading
import json
import webbrowser

red = None
green = None
blue = None
alpha = None
        

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setAutoFillBackground(True)
        MainWindow.setStyleSheet("")
        MainWindow.setAnimated(False)
        MainWindow.setDocumentMode(False)
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        MainWindow.setDockNestingEnabled(False)
        MainWindow.setUnifiedTitleAndToolBarOnMac(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.channel_box = QtWidgets.QGroupBox(self.centralwidget)
        self.channel_box.setGeometry(QtCore.QRect(10, 190, 311, 261))
        self.channel_box.setObjectName("channel_box")
        self.channel_1 = QtWidgets.QPushButton(self.channel_box)
        self.channel_1.setGeometry(QtCore.QRect(10, 20, 291, 51))
        self.channel_1.setCheckable(True)
        self.channel_1.setAutoDefault(False)
        self.channel_1.setDefault(False)
        self.channel_1.setObjectName("channel_1")
        self.channel_2 = QtWidgets.QPushButton(self.channel_box)
        self.channel_2.setGeometry(QtCore.QRect(10, 80, 291, 51))
        self.channel_2.setCheckable(True)
        self.channel_2.setChecked(False)
        self.channel_2.setDefault(False)
        self.channel_2.setObjectName("channel_2")
        self.channel_3 = QtWidgets.QPushButton(self.channel_box)
        self.channel_3.setGeometry(QtCore.QRect(10, 140, 291, 51))
        self.channel_3.setCheckable(True)
        self.channel_3.setObjectName("channel_3")
        self.channel_4 = QtWidgets.QPushButton(self.channel_box)
        self.channel_4.setGeometry(QtCore.QRect(10, 200, 291, 51))
        self.channel_4.setCheckable(True)
        self.channel_4.setObjectName("channel_4")
        self.option_box = QtWidgets.QGroupBox(self.centralwidget)
        self.option_box.setGeometry(QtCore.QRect(10, 10, 411, 171))
        self.option_box.setObjectName("option_box")
        self.ip = QtWidgets.QLineEdit(self.option_box)
        self.ip.setGeometry(QtCore.QRect(10, 20, 391, 51))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.ip.setFont(font)
        self.ip.setInputMask("")
        self.ip.setAlignment(QtCore.Qt.AlignCenter)
        self.ip.setClearButtonEnabled(True)
        self.ip.setObjectName("ip")
        self.auto_refresh = QtWidgets.QCheckBox(self.option_box)
        self.auto_refresh.setGeometry(QtCore.QRect(10, 80, 121, 31))
        self.auto_refresh.setObjectName("auto_refresh")
        self.delay = QtWidgets.QLineEdit(self.option_box)
        self.delay.setGeometry(QtCore.QRect(130, 80, 91, 31))
        self.delay.setInputMask("")
        self.delay.setAlignment(QtCore.Qt.AlignCenter)
        self.delay.setClearButtonEnabled(True)
        self.delay.setObjectName("delay")
        self.label = QtWidgets.QLabel(self.option_box)
        self.label.setGeometry(QtCore.QRect(230, 80, 51, 31))
        self.label.setObjectName("label")
        self.refresh = QtWidgets.QPushButton(self.option_box)
        self.refresh.setGeometry(QtCore.QRect(270, 120, 131, 41))
        self.refresh.setObjectName("refresh")
        self.status_icon = QtWidgets.QPushButton(self.option_box)
        self.status_icon.setEnabled(True)
        self.status_icon.setGeometry(QtCore.QRect(10, 120, 61, 41))
        self.status_icon.setAutoFillBackground(True)
        self.status_icon.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(".\\assets/sync.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.status_icon.setIcon(icon)
        self.status_icon.setIconSize(QtCore.QSize(50, 50))
        self.status_icon.setFlat(True)
        self.status_icon.setObjectName("status_icon")
        self.webpanel = QtWidgets.QPushButton(self.option_box)
        self.webpanel.setGeometry(QtCore.QRect(130, 120, 131, 41))
        self.webpanel.setObjectName("webpanel")
        self.log_box = QtWidgets.QGroupBox(self.centralwidget)
        self.log_box.setGeometry(QtCore.QRect(330, 190, 461, 341))
        self.log_box.setObjectName("log_box")
        self.log = QtWidgets.QPlainTextEdit(self.log_box)
        self.log.setGeometry(QtCore.QRect(10, 20, 441, 311))
        self.log.setDocumentTitle("")
        self.log.setReadOnly(True)
        self.log.setTabStopWidth(20)
        self.log.setObjectName("log")
        self.tip_box = QtWidgets.QGroupBox(self.centralwidget)
        self.tip_box.setGeometry(QtCore.QRect(430, 10, 361, 171))
        self.tip_box.setObjectName("tip_box")
        self.tips = QtWidgets.QLabel(self.tip_box)
        self.tips.setGeometry(QtCore.QRect(10, 20, 341, 141))
        self.tips.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.tips.setWordWrap(True)
        self.tips.setIndent(1)
        self.tips.setObjectName("tips")
        self.rgb_box = QtWidgets.QGroupBox(self.centralwidget)
        self.rgb_box.setGeometry(QtCore.QRect(10, 460, 311, 131))
        self.rgb_box.setObjectName("rgb_box")
        self.set_color = QtWidgets.QPushButton(self.rgb_box)
        self.set_color.setGeometry(QtCore.QRect(160, 20, 141, 41))
        self.set_color.setObjectName("set_color")
        self.select_color = QtWidgets.QPushButton(self.rgb_box)
        self.select_color.setGeometry(QtCore.QRect(10, 20, 141, 41))
        self.select_color.setObjectName("select_color")
        self.preview_color = QtWidgets.QLabel(self.rgb_box)
        self.preview_color.setGeometry(QtCore.QRect(10, 70, 291, 51))
        self.preview_color.setStyleSheet("background-color: rgb(67, 255, 57);")
        self.preview_color.setAlignment(QtCore.Qt.AlignCenter)
        self.preview_color.setWordWrap(True)
        self.preview_color.setIndent(1)
        self.preview_color.setObjectName("preview_color")
        self.temp_box = QtWidgets.QGroupBox(self.centralwidget)
        self.temp_box.setGeometry(QtCore.QRect(330, 540, 461, 51))
        self.temp_box.setObjectName("temp_box")
        self.temp = QtWidgets.QLabel(self.temp_box)
        self.temp.setGeometry(QtCore.QRect(10, 19, 441, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.temp.setFont(font)
        self.temp.setAlignment(QtCore.Qt.AlignCenter)
        self.temp.setObjectName("temp")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle("MainWindow")
        self.channel_box.setTitle("Channel manager")
        self.channel_1.setText("Channel One")
        self.channel_2.setText("Channel Two")
        self.channel_3.setText("Channel Three")
        self.channel_4.setText("Channel Four")
        self.option_box.setTitle("Device options")
        self.ip.setText("192.168.4.1")
        self.ip.setPlaceholderText("Device ip")
        self.auto_refresh.setText("Auto refresh every ")
        self.delay.setText("5")
        self.delay.setPlaceholderText("0")
        self.label.setText("seconds")
        self.refresh.setText("Manual refresh")
        self.webpanel.setText("Open web-panel")
        self.log_box.setTitle("Log")
        self.log.setPlainText("")
        self.tip_box.setTitle("Tips")
        self.tips.setText("Connect to the board and enter the iPanel.\n"
"In the next section, you can turn on the automatic update or update manually.\n"
"If the connection was established, you can do the control (:")
        self.rgb_box.setTitle("RGB controller")
        self.set_color.setText("Set color")
        self.select_color.setText("Select color")
        self.preview_color.setText("preview")
        self.temp_box.setTitle("temperature")
        self.temp.setText("0℃")


    def open_color_dialog(self):
        global red, green, blue, alpha
        color = QtWidgets.QColorDialog.getColor()
        # print(color.name())
        print(color.getRgb())
            
        red, green, blue, alpha = color.getRgb()        
            
        # if color.isValid():
        #     self.preview_color.setStyleSheet(f"background-color: {color.name()};")
                
    def updateTimer(self):
        try:
            if self.auto_refresh.isChecked():
                delay_value = int(self.delay.text()) * 1000
                self.timer.timeout.connect(self.runPingThread)
                self.timer.start(delay_value)
            else:
                self.timer.stop()
        except ValueError:
            self.timer.stop()
            
    def runPingThread(self):
        threading.Thread(target=self.ping).start()
            
    def ping(self):
        url = f"http://{self.ip.text()}/read"
        icon = QtGui.QIcon()  
        try:
            response = requests.get(url, timeout=2)
            
        
            if response.status_code == 200:
                icon.addPixmap(QtGui.QPixmap(".\\assets/ok.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                log = str(json.dumps(response.json(), sort_keys=True, indent=2, separators=(',', ': ')))
                
                pins = ["pin_1", "pin_2", "pin_3", "pin_4"]
                keys = [self.channel_1, self.channel_2, self.channel_3, self.channel_4]
                
                for i in pins:
                    if response.json()[i] == "Low":
                        keys[pins.index(i)].setChecked(False)
                    else:
                        keys[pins.index(i)].setChecked(True)
                        
                self.temp.setText("{:.2f}".format(response.json()['temp'])+"℃")
                self.preview_color.setStyleSheet(f"background-color: rgb({response.json()['red']},{response.json()['green']},{response.json()['blue']});")
                        
            else:
                icon.addPixmap(QtGui.QPixmap(".\\assets/nok.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                log = str(response.status_code)
        except Exception as e:
            icon.addPixmap(QtGui.QPixmap(".\\assets/nok.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            log = str(e)
        
        QtCore.QMetaObject.invokeMethod(self.log, "setPlainText", QtCore.Qt.QueuedConnection, QtCore.Q_ARG(str, log))
        self.status_icon.setIcon(icon)
        
    def openpanel(self):
        if self.ip.text() != "":
            webbrowser.open(f"http://{self.ip.text()}", new=0, autoraise=True)

    def keyaction(self, pin):
        url = f"http://{self.ip.text()}/light"
        d = {"baseNumber": pin}
        
        try:
            response = requests.post(url, timeout=2, data=d)
        except:
            pass
        
    def rgbaction(self, red, green, blue):
        url = f"http://{self.ip.text()}/rgb"
        d = {
            "red" : red,
            "green" : green,
            "blue" : blue
            }
        
        try:
            response = requests.post(url, timeout=2, data=d)
        except:
            pass
        
    def changecolor(self):
        global red, green, blue
        print(red, green, blue)
        self.rgbaction(red, green, blue)
        
        
        
        
        
        

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.timer = QtCore.QTimer(self)
        self.select_color.clicked.connect(self.open_color_dialog)
        self.auto_refresh.stateChanged.connect(self.updateTimer)
        self.refresh.clicked.connect(self.runPingThread)
        self.webpanel.clicked.connect(self.openpanel)
        self.set_color.clicked.connect(self.changecolor)
        self.channel_1.clicked.connect(lambda: self.keyaction(1))
        self.channel_2.clicked.connect(lambda: self.keyaction(2))
        self.channel_3.clicked.connect(lambda: self.keyaction(3))
        self.channel_4.clicked.connect(lambda: self.keyaction(4))
        

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())