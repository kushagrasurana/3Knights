import socket
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow,QMessageBox, QFileDialog
from onlinewindow_ui import Ui_MainWindow
from urllib.request import urlopen
import _thread
import threading

from mygame import MyGame

# the game connects on port 12574
game_port = 12574

class OnlineWindow(QMainWindow):
    connectionEstablished = pyqtSignal(socket.socket, int)
    def __init__(self):
        super(OnlineWindow, self).__init__()
        self.host_private_ip = ""
        self.host_public_ip = ""
        self.has_connected = 0
        self.lock = threading.Lock()
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        self.connectionEstablished.connect(self.openGame)
        _thread.start_new_thread(self.create_server, ())

        self.init_ui()

    def get_private_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("gmail.com",80))
        ip = s.getsockname()[0]
        s.close()
        return ip

    def get_public_ip(self):
        return (urlopen('http://ip.42.pl/raw').read()).decode("ascii")


    def init_ui(self):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("3Knights")

        self.host_private_ip = self.get_private_ip()
        self.ui.selfPrivateIp.setText(self.host_private_ip)
        self.host_public_ip = self.get_public_ip()
        self.ui.selfPublicIp.setText(self.host_public_ip)

        self.ui.connectButton.clicked.connect(self.connect_to_opponent)
        self.ui.browseButton.clicked.connect(self.browse_clicked)

    def create_server(self):
        global game_port
        host = socket.gethostname()
        port = game_port
        print("server is up")
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        self.server_socket.bind((host, port))
        self.server_socket.listen(1)
        self.connection_socket, address = self.server_socket.accept()

        self.lock.acquire()
        if not self.has_connected:
            self.has_connected = 1
            self.client_socket.close()
            self.connectionEstablished.emit(self.connection_socket, 1)



    def connect_to_opponent(self):
        global game_port
        remote_ip = self.ui.oponnentIp.text()
        try:
            self.client_socket.connect((remote_ip, game_port))
            self.ui.connectButton.setDisabled(True)

            self.lock.acquire()
            if not self.has_connected:
                self.has_connected = 1
                self.server_socket.close()
                self.connectionEstablished.emit(self.client_socket, 0)
        except Exception as e:
            QMessageBox.about(None, "Connection Problem", "Error : %s" % e)
            self.ui.connectButton.setEnabled(True)

    def openGame(self, socket, i_am_white):
        if i_am_white:
            self.gameWidget = MyGame(1, "", self.ui.botPath.text(), "", 1, socket, i_am_white)
        else:
            self.gameWidget = MyGame(1, "", "", self.ui.botPath.text(), 1, socket, i_am_white)
        self.setCentralWidget(self.gameWidget)

    def browse_clicked(self):
        self.ui.botPath.setText(QFileDialog.getOpenFileName()[0])