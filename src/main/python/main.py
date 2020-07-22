
import sys
import os
from by_socket import Receiver
from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QPushButton,
                             QMessageBox, QLineEdit, QHBoxLayout, QVBoxLayout, QWidget)

import qss
def import_styles(qss_name):
    styleFile = os.path.join(
                    os.path.dirname(__file__),
                    f'qss/{qss_name}'
                    )
    print(styleFile)
    style = ""
    with open(styleFile, 'r') as f:
        style = f.read()

    return style


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'i2Gadget Server'
        self.left = 20

        self.right =20
        self.top = 50
        self.width = 400
        self.height = 200
        self.setWindowTitle(self.title)
        self.setFixedSize(300,100)
        #self.setFixedSIze(400,200)#Geometry(self.left, self.right, self.width, self.height)
        self.main_widget = MainWidget() 
        self.setCentralWidget(self.main_widget) 
        # self.show()

class MainWidget(QWidget):#QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'i2Gadget Server'
        self.width = 400
        self.height = 200
        self.setWindowTitle(self.title)
        # self.setGeometry(self.left, self.right, self.width, self.height)
        self.initUI()
        # self.show()
    
    def initUI(self):
        self.receiver = Receiver(port=40000, ipaddr = None, set_daemon=True, log_function=lambda x :self.status_text.setText(x) )
        self.receiver.start_loop()
        self.ipaddr = self.receiver.ipaddr
        self.port = self.receiver.port

        self.startButton = QPushButton("start", self)
        self.startButton.clicked.connect(self.startButtonClicked)
        
        self.status_text = QLabel("start server")
        self.status_text.setText(f"ip:{self.ipaddr} port:{self.port}")
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(self.startButton)
        vbox.addWidget(self.status_text)
        self.setLayout(vbox)

       

        

        self.setWindowTitle('Button01')
        self.show()

    def startButtonClicked(self):
        sender = self.sender()
        # self.statusBar().showMessage(sender.text() + ' Push Button01')
        self.receiver.start_loop()
        self.startButton.setEnabled(False)

        
        self.status_text.setText(f"ip:{self.ipaddr} port:{self.port}")

    def closeEvent(self, event):
        self.receiver.stop_loop()
        self.receiver.close_sock()
        QMainWindow.closeEvent(self, event)
if __name__ == '__main__':
    appctxt = ApplicationContext()       # 1. Instantiate ApplicationContext
    
    style_string = qss.style# import_styles("style.qss")#pyqtcss.get_style("dark_orange")
    appctxt.app.setStyleSheet(style_string)
    window = MainWindow()
    window.resize(250, 150)
    window.show()
    exit_code = appctxt.app.exec_()      # 2. Invoke appctxt.app.exec_()
    sys.exit(exit_code)
