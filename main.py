#!/usr/bin/env python3
import sys

from PyQt5.QtWidgets import QMainWindow,QMessageBox,QApplication

from mainwindow import MainWindow
from onlinewindow import OnlineWindow
from mygame import MyGame


__author__ = "Kushagra Surana"


class Window(QMainWindow):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.mainWidget = MainWindow()
        self.mainWidget.ui.start.clicked.connect(self.change_central_widget)
        self.mainWidget.ui.load_game2.clicked.connect(self.showLoadGameWindow)
        self.mainWidget.ui.onlineGameButton.clicked.connect(self.show_online_game_window)
        self.setCentralWidget(self.mainWidget)

    def show_online_game_window(self):
        self.onlineWindow = OnlineWindow()
        self.setCentralWidget(self.onlineWindow)

    def change_central_widget(self):
        f = 1
        if not ((self.mainWidget.ui.rb1.isChecked() or self.mainWidget.ui.rb2.isChecked()) and (
                    self.mainWidget.ui.rb3.isChecked() or self.mainWidget.ui.rb4.isChecked())):
            QMessageBox.about(None, "", "Select Players")
        else:
            if self.mainWidget.ui.rb1.isChecked():
                if self.mainWidget.ui.rb3.isChecked():  # bot vs bot
                    if self.mainWidget.ui.bot_path1.text() == "" or self.mainWidget.ui.bot_path2.text() == "":
                        QMessageBox.about(None, "error", "no bot file")
                        f = 0  # dialog for null
                    self.gameWidget = MyGame(1, "", self.mainWidget.ui.bot_path1.text(),
                                             self.mainWidget.ui.bot_path2.text())
                else:
                    if self.mainWidget.ui.bot_path1.text() == "":
                        QMessageBox.about(None, "error", "no bot file")
                        f = 0
                    else:
                        self.gameWidget = MyGame(1, "", self.mainWidget.ui.bot_path1.text())  # bot vs human
            else:
                if self.mainWidget.ui.rb3.isChecked():
                    if self.mainWidget.ui.bot_path2.text() == "":
                        QMessageBox.about(None, "error", "no bot file")
                        f = 0
                    else:
                        self.gameWidget = MyGame(1, "", "", self.mainWidget.ui.bot_path2.text())  # human vs bot
                else:
                    self.gameWidget = MyGame()  # human vs human
            if f:
                self.setCentralWidget(self.gameWidget)
                self.gameWidget.back.clicked.connect(self.change_central_widget2)

    def change_central_widget2(self):
        self.mainWidget = MainWindow()
        self.mainWidget.ui.start.clicked.connect(self.change_central_widget)
        self.mainWidget.ui.load_game2.clicked.connect(self.showLoadGameWindow)
        self.setCentralWidget(self.mainWidget)

    def showLoadGameWindow(self):
        new_game = 0
        print("loading")
        file_path = self.mainWidget.ui.load_path.text()
        if (file_path == ""):
            pass
        else:
            self.gameWidget = MyGame(new_game, file_path)
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