from PyQt5.QtWidgets import *

from mainwindow_ui import Ui_Form


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.init_ui()

    def init_ui(self):
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setWindowTitle("3Knights")
        # hide widgets
        self.ui.lab2.hide()
        self.ui.lab3.hide()
        self.ui.rb1.hide()
        self.ui.rb2.hide()
        self.ui.rb3.hide()
        self.ui.rb4.hide()
        self.ui.bot_path1.hide()
        self.ui.bot_path2.hide()
        self.ui.browse1.hide()
        self.ui.browse2.hide()
        self.ui.start.hide()
        self.ui.load_game2.hide()
        self.ui.browse3.hide()
        self.ui.load_path.hide()
        self.ui.back1.hide()
        self.ui.back2.hide()
        self.ui.start.hide()
        self.ui.groupBox.hide()
        self.ui.groupBox_2.hide()
        # connects
        self.ui.new_game.clicked.connect(self.new_game_clicked)
        self.ui.browse1.clicked.connect(self.browse1_clicked)
        self.ui.browse2.clicked.connect(self.browse2_clicked)
        self.ui.start.clicked.connect(self.start_clicked)
        self.ui.load_game.clicked.connect(self.load_game_clicked)
        self.ui.load_game2.clicked.connect(self.load_game2_clicked)
        self.ui.browse3.clicked.connect(self.browse3_clicked)
        self.ui.rules.clicked.connect(self.rules_clicked)
        self.ui.back1.clicked.connect(self.back1_clicked)
        self.ui.back2.clicked.connect(self.back2_clicked)

    def new_game_clicked(self):
        self.ui.lab2.show()
        self.ui.lab3.show()
        self.ui.rb1.show()
        self.ui.rb2.show()
        self.ui.rb3.show()
        self.ui.rb4.show()
        self.ui.bot_path1.show()
        self.ui.bot_path2.show()
        self.ui.browse1.show()
        self.ui.browse2.show()
        self.ui.back1.show()
        self.ui.start.show()
        self.ui.groupBox_2.show()
        self.ui.groupBox.show()
        self.back2_clicked()
        self.ui.new_game.hide()

    def browse1_clicked(self):
        self.ui.bot_path1.setText(QFileDialog.getOpenFileName()[0])

    def browse2_clicked(self):
        self.ui.bot_path2.setText(QFileDialog.getOpenFileName()[0])

    def start_clicked(self):
        pass

    def load_game_clicked(self):
        self.back1_clicked()
        self.ui.load_path.show()
        self.ui.browse3.show()
        self.ui.back2.show()
        self.ui.load_game2.show()
        self.ui.load_game.hide()

    def load_game2_clicked(self):
        pass

    def browse3_clicked(self):
        self.ui.load_path.setText(QFileDialog.getOpenFileName()[0])

    def rules_clicked(self):
        pass

    def back1_clicked(self):
        self.ui.lab2.hide()
        self.ui.lab3.hide()
        self.ui.rb1.hide()
        self.ui.rb2.hide()
        self.ui.rb3.hide()
        self.ui.rb4.hide()
        self.ui.bot_path1.hide()
        self.ui.bot_path2.hide()
        self.ui.browse1.hide()
        self.ui.browse2.hide()
        self.ui.back1.hide()
        self.ui.start.hide()
        self.ui.groupBox_2.hide()
        self.ui.groupBox.hide()
        self.ui.new_game.show()

    def back2_clicked(self):
        self.ui.back2.hide()
        self.ui.load_path.hide()
        self.ui.browse3.hide()
        self.ui.load_game.show()
        self.ui.load_game2.hide()