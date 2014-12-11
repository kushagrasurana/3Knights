from PyQt5.QtWidgets import *
from board import Board


class MyGame(QWidget):
    def __init__(self, new_game=1):
        super(MyGame, self).__init__()
        self.whites_move = 1
        self.selected_i = None
        self.selected_j = None
        if new_game == 1:
            self.initUI()
        else:
            pass

    def initUI(self):
        self.game_board = Board()
        for i in range(0, 8):
            self.game_board.set_piece(5, 0, 1, i)
            self.game_board.set_piece(5, 1, 6, i)
        self.game_board.set_piece(4, 0, 0, 1)
        self.game_board.set_piece(4, 1, 7, 6)
        self.game_board.set_piece(2, 0, 0, 6)
        self.game_board.set_piece(2, 1, 7, 1)
        for i in range(0, 8):
            for j in range(0, 8):
                self.game_board.tile[i][j].clickedk.connect(self.board_clicked)
        self.setLayout(self.game_board)

    def board_clicked(self, i, j):
        if self.selected_i is None:
            if (self.game_board.tile[i][j].piece > 5 and self.whites_move == 1) or (self.game_board.tile[i][j].piece < 6 and self.game_board.tile[i][j].piece != -1 and self.whites_move == 0):
                self.selected_i = i
                self.selected_j = j
        elif self.selected_i == i and self.selected_j == j:
            self.selected_i = None
            self.selected_j = None
        else:
            if (i,j) in self.possible_moves(i,j):
                print (i,j,"in move list") # working
                piece = self.game_board.tile[self.selected_i][self.selected_j].piece
                code = self.get_code(piece)
                col = self.get_col(piece)
                self.game_board.remove_piece(self.selected_i,self.selected_j)
                self.game_board.set_piece(code,col,i,j)
                self.selected_i = None
                self.selected_j = None

    def possible_moves(self,i,j):
        move_list=[(1,1),(2,2)]
        return move_list

    def get_code(self,piece):
        return piece%10

    def get_col(self,piece):
        if piece > 5:
            return 1
        else:
            return 0
