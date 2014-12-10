from PyQt5.QtWidgets import *
from board import Board


class MyGame(QWidget):
    def __init__(self,new_game=1):
        super(MyGame, self).__init__()
        if new_game == 1:
            self.initUI()
        else:
            pass

    def initUI(self):
        self.game_board = Board()
        for i in range(0,8):
            self.game_board.set_piece(5, 0, 1, i)
            self.game_board.set_piece(5, 1, 6, i)
        self.game_board.set_piece(4, 0, 0, 1)
        self.game_board.set_piece(4, 1, 7, 6)
        self.game_board.set_piece(2, 0, 0, 6)
        self.game_board.set_piece(2, 1, 7, 1)
        self.setLayout(self.game_board)