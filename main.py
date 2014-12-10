import sys
from mainwindow import MainWindow
from mygame import MyGame
from PyQt5.QtWidgets import *


class Window(QMainWindow):

    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.mainWidget = MainWindow()
        self.mainWidget.ui.start.clicked.connect(self.change_central_widget)
        self.setCentralWidget(self.mainWidget)

    def change_central_widget(self):
        self.gameWidget = MyGame()
        self.setCentralWidget(self.gameWidget)


def main():
    app = QApplication(sys.argv)
    my_app = Window()
    my_app.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()