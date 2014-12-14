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
        if self.mainWidget.ui.rb1.isChecked():
            if self.mainWidget.ui.rb3.isChecked(): # bot vs bot
                if (self.mainWidget.ui.bot_path1.text()=="" or self.mainWidget.ui.bot_path2.text()==""):
                    pass # dialog for null
                self.gameWidget = MyGame(1,"",self.mainWidget.ui.bot_path1.text(),self.mainWidget.ui.bot_path2.text())
            else:
                self.gameWidget = MyGame(1,"",self.mainWidget.ui.bot_path1.text()) # bot vs human
        else:
            if self.mainWidget.ui.rb3.isChecked():
                self.gameWidget = MyGame(1,"","",self.mainWidget.ui.bot_path2.text()) # human vs bot
            else:
                self.gameWidget = MyGame() # human vs human

        self.setCentralWidget(self.gameWidget)
        self.gameWidget.back.clicked.connect(self.change_central_widget2)

    def change_central_widget2(self):
        self.mainWidget = MainWindow()
        self.mainWidget.ui.start.clicked.connect(self.change_central_widget)
        self.mainWidget.ui.load_game2.clicked.connect(self.change_central_widget3)
        self.setCentralWidget(self.mainWidget)

    def change_central_widget3(self):
        new_game = 0
        print("loading")
        file_path = self.mainWidget.ui.load_path.text()
        if (file_path == ""):
            pass
        else:
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