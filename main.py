import sys
from mainwindow import MainWindow
from mygame import MyGame
from PyQt5.QtWidgets import *


class Window(QMainWindow):

    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.mainWidget = MainWindow()
        self.mainWidget.ui.start.clicked.connect(self.change_central_widget)
        self.mainWidget.ui.load_game2.clicked.connect(self.change_central_widget3)
        self.setCentralWidget(self.mainWidget)

    def change_central_widget(self):
        self.gameWidget = MyGame()
        self.setCentralWidget(self.gameWidget)
        self.gameWidget.back.clicked.connect(self.change_central_widget2)

    def change_central_widget2(self):
        self.mainWidget = MainWindow()
        self.mainWidget.ui.start.clicked.connect(self.change_central_widget)
        self.setCentralWidget(self.mainWidget)

    def change_central_widget3(self):
        new_game = 0
        file_path = self.mainWidget.ui.load_path.text()
        self.gameWidget = MyGame(new_game,file_path)
        self.setCentralWidget(self.gameWidget)
        self.gameWidget.back.clicked.connect(self.change_central_widget2)

def main():
    app = QApplication(sys.argv)
    my_app = Window()
    my_app.show()
    my_app.setWindowTitle("3Knights")
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()