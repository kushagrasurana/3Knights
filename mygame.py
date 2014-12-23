import os
import subprocess
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *

from board import Board


class MyGame(QWidget):
    def __init__(self, new_game=1, file_path="", bot1_path="", bot2_path=""):
        super(MyGame, self).__init__()
        self.whites_move = 1
        self.selected_i = None
        self.selected_j = None
        self.score_white = 0
        self.score_black = 0
        self.white_pawn = 8
        self.white_rook = 1
        self.white_bishop = 1
        self.black_pawn = 8
        self.black_rook = 1
        self.black_bishop = 1
        self.move_history = []
        self.white_is_bot = 1
        self.black_is_bot = 1
        self.last_bot_move = "0"
        self.file_path = file_path
        self.bot1_path = bot1_path
        self.bot2_path = bot2_path
        if self.bot1_path == "":
            self.white_is_bot = 0
        if self.bot2_path == "":
            self.black_is_bot = 0
        self.initUI()
        self.write_board_file()
        if new_game == 0:
            self.load_game()
        self.make_bot_move()

    def initUI(self):
        self.game_board = Board()
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.p1_score = QtWidgets.QLabel()
        self.p1_score.setObjectName("p1_score")
        self.horizontalLayout.addWidget(self.p1_score)
        self.undo = QtWidgets.QPushButton()
        self.undo.setObjectName("undo")
        self.horizontalLayout.addWidget(self.undo)
        self.save = QtWidgets.QPushButton()
        self.save.setObjectName("save")
        self.horizontalLayout.addWidget(self.save)
        self.back = QtWidgets.QPushButton()
        self.back.setObjectName("back")
        self.horizontalLayout.addWidget(self.back)
        self.p2_score = QtWidgets.QLabel()
        self.p2_score.setObjectName("p2_score")
        self.horizontalLayout.addWidget(self.p2_score)
        self.p1_score.setText("Player1-0")
        self.undo.setText("Undo")
        self.undo.setEnabled(False)
        self.save.setText("Save")
        self.back.setText("Back")
        self.p2_score.setText("Player2-0")
        for i in range(0, 8):  # set pawns
            self.game_board.set_piece(5, 0, 1, i)
            self.game_board.set_piece(5, 1, 6, i)
        self.game_board.set_piece(4, 0, 0, 1)
        self.game_board.set_piece(4, 1, 7, 6)
        self.game_board.set_piece(2, 0, 0, 6)
        self.game_board.set_piece(2, 1, 7, 1)
        for i in range(0, 8):
            for j in range(0, 8):
                self.game_board.tile[i][j].clickedk.connect(self.board_clicked)
        self.game_board.addLayout(self.horizontalLayout, 8, 0, 1, 8)
        self.setLayout(self.game_board)
        self.undo.clicked.connect(self.undo_move)
        self.save.clicked.connect(self.save_button)

    def board_clicked(self, i, j):  # when board is clicked
        if self.selected_i is None:  # if no piece was previously selected
            if (self.game_board.tile[i][j].piece > 5 and self.whites_move == 1) or (
                                self.game_board.tile[i][j].piece < 6 and self.game_board.tile[i][
                            j].piece != -1 and self.whites_move == 0):
                self.selected_i = i
                self.selected_j = j
                self.change_style(i, j, 1)  # change border color of selected tile
        elif self.selected_i == i and self.selected_j == j:  # if the same piece is clicked again
            self.selected_i = None
            self.selected_j = None
            self.change_style(i, j, 0)
        else:  # makes the move
            if (i, j) in self.possible_moves(self.selected_i, self.selected_j,
                                             self.game_board.tile[self.selected_i][self.selected_j].piece):
                if self.game_board.tile[i][j].piece != -1:  # already a piece there
                    code = self.get_code(self.game_board.tile[i][j].piece)
                    col = self.get_col(self.game_board.tile[i][j].piece)
                    temp_move = (chr(self.selected_j + 97) + chr(8 - self.selected_i + 48) + chr(j + 97) + chr(
                        8 - i + 48) + 'x' + chr(self.game_board.tile[i][j].piece + 48))
                    if code == 5:  # dead piece is pawn
                        if col == 1:
                            self.white_pawn -= 1
                        else:
                            self.black_pawn -= 1
                    elif code == 4:  # dead piece is rook
                        if col == 1:
                            self.white_rook -= 1
                        else:
                            self.black_rook -= 1
                    else:  # dead piece is bishop
                        if col == 1:
                            self.white_bishop -= 1
                        else:
                            self.black_bishop -= 1
                elif (i, j) in self.en_passant(self.selected_i, self.selected_j, self.get_col(
                        self.game_board.tile[self.selected_i][self.selected_j].piece)):  # check for en_passant
                    if self.whites_move:
                        self.black_pawn -= 1
                        self.game_board.remove_piece(i + 1, j)
                    else:
                        self.white_pawn -= 1
                        self.game_board.remove_piece(i - 1, j)
                    temp_move = (
                        chr(self.selected_j + 97) + chr(8 - self.selected_i + 48) + chr(j + 97) + chr(
                            8 - i + 48) + "xp")
                else:
                    temp_move = (
                        chr(self.selected_j + 97) + chr(8 - self.selected_i + 48) + chr(j + 97) + chr(8 - i + 48))
                self.move_history.append(temp_move)
                self.undo.setEnabled(True)
                piece = self.game_board.tile[self.selected_i][self.selected_j].piece
                code = self.get_code(piece)
                col = self.get_col(piece)
                self.game_board.remove_piece(self.selected_i, self.selected_j)
                self.game_board.set_piece(code, col, i, j)
                self.change_style(self.selected_i, self.selected_j, 0)
                self.selected_i = None
                self.selected_j = None
                if self.whites_move == 1:  # change turn
                    self.whites_move = 0
                else:
                    self.whites_move = 1
                if code == 5 and i == 0 and col == 1:  # check if pawn is promoted
                    self.score_white += 1
                    self.game_board.remove_piece(i, j)
                    current_score1 = ord(self.p1_score.text()[-1])
                    self.p1_score.setText("Player1-" + chr(self.score_white + 48))
                    self.white_pawn -= 1
                if code == 5 and i == 7 and col == 0:
                    self.score_black += 1
                    self.game_board.remove_piece(i, j)
                    self.p2_score.setText("Player2-" + chr(self.score_black + 48))
                    self.black_pawn -= 1
                if self.game_end():  # check if game is ended
                    self.result()
                self.make_bot_move()

    def possible_moves(self, i, j, piece):
        code = self.get_code(piece)
        col = self.get_col(piece)
        if code == 5:  # for pawn
            return self.pawn_movelist(i, j, col)
        elif code == 4:
            return self.rook_movelist(i, j, col)
        elif code == 3:
            return self.knight_movelist(i, j, col)
        elif code == 2:
            return self.bishop_movelist(i, j, col)
        elif code == 1:
            return self.queen_movelist(i, j, col)
        else:
            return self.king_movelist(i, j, col)

    @staticmethod
    def get_code(piece):
        return piece % 10

    @staticmethod
    def get_col(piece):
        if piece == -1:
            return -1
        if piece > 5:
            return 1
        else:
            return 0

    def en_passant(self, i, j, col):
        en_pass_list = []
        if len(self.move_history) > 0:
            last_move = self.move_history[-1]
            last_move_final_i = 8 - (ord(last_move[3]) - 48)
            last_move_final_j = ord(last_move[2]) - 97
            last_move_initial_i = 8 - (ord(last_move[1]) - 48)
            last_move_initial_j = ord(last_move[0]) - 97
        else:
            return []
        if col == 1:
            if len(self.move_history) > 0 and i == 3:  # check for En passant
                if j + 1 < 8 and self.game_board.tile[i][j + 1].piece == 5:
                    if last_move_initial_i == 1 and last_move_final_i == 3 and last_move_final_j == j + 1:  # qualified for en passant
                        en_pass_list.append((i - 1, j + 1))
                elif j - 1 > 0 and self.game_board.tile[i][j - 1].piece == 5:
                    if last_move_initial_i == 1 and last_move_final_i == 3 and last_move_final_j == j - 1:  # qualified for en passant
                        en_pass_list.append((i - 1, j - 1))
        else:
            if len(self.move_history) > 0 and i == 4:  # check for En passant
                if j + 1 < 8 and self.game_board.tile[i][j + 1].piece == 15:
                    if last_move_initial_i == 6 and last_move_final_i == 4 and last_move_final_j == j + 1:  # qualified for en passant
                        en_pass_list.append((i + 1, j + 1))
                elif j - 1 > 0 and self.game_board.tile[i][j - 1].piece == 15:
                    if last_move_initial_i == 6 and last_move_final_i == 4 and last_move_final_j == j - 1:  # qualified for en passant
                        en_pass_list.append((i + 1, j - 1))
        return en_pass_list


    def pawn_movelist(self, i, j, col):
        movelist = []
        en_pass_list = self.en_passant(i, j, col)
        if len(en_pass_list) > 0:
            movelist.append(en_pass_list[0])
        if col == 1:
            if self.game_board.tile[i - 1][j].piece == -1:
                movelist.append((i - 1, j))
                if (i == 6 and self.game_board.tile[i - 2][j].piece == -1):
                    movelist.append((i - 2, j))
            if (j > 0):
                if self.get_col(self.game_board.tile[i - 1][j - 1].piece) == 0:
                    movelist.append((i - 1, j - 1))
            if (j < 7):
                if self.get_col(self.game_board.tile[i - 1][j + 1].piece) == 0:
                    movelist.append((i - 1, j + 1))
        else:
            if self.game_board.tile[i + 1][j].piece == -1:
                movelist.append((i + 1, j))
                if (i == 1 and self.game_board.tile[i + 2][j].piece == -1):
                    movelist.append((i + 2, j))
            if (j > 0):
                if self.get_col(self.game_board.tile[i + 1][j - 1].piece) == 1:
                    movelist.append((i + 1, j - 1))
            if (j < 7):
                if self.get_col(self.game_board.tile[i + 1][j + 1].piece) == 1:
                    movelist.append((i + 1, j + 1))
        print(movelist)
        return movelist

    def rook_movelist(self, i, j, col):
        movelist = []
        temp_j = j - 1
        if col == 1:
            col = 0
        else:
            col = 1
        while (temp_j >= 0 and self.game_board.tile[i][temp_j].piece == -1):
            movelist.append((i, temp_j))
            temp_j -= 1
        if (temp_j >= 0 and self.get_col(self.game_board.tile[i][temp_j].piece) == col ):  # kill
            movelist.append((i, temp_j))
        # for right direction
        temp_j = j + 1
        while (temp_j < 8 and self.game_board.tile[i][temp_j].piece == -1):
            movelist.append((i, temp_j))
            temp_j += 1
        if (temp_j < 8 and self.get_col(self.game_board.tile[i][temp_j].piece) == col ):  # kill
            movelist.append((i, temp_j))
        # for down
        tempi = i + 1
        while tempi < 8 and self.game_board.tile[tempi][j].piece == -1:
            movelist.append((tempi, j))
            tempi += 1
        if (tempi < 8 and self.get_col(self.game_board.tile[tempi][j].piece) == col):  # kill
            movelist.append((tempi, j))
        # for up
        tempi = i - 1
        while tempi >= 0 and self.game_board.tile[tempi][j].piece == -1:
            movelist.append((tempi, j))
            tempi -= 1
        if (tempi >= 0 and self.get_col(self.game_board.tile[tempi][j].piece) == col ):  # kill
            movelist.append((tempi, j))
        print(movelist)
        return movelist

    def knight_movelist(self, i, j, col):
        movelist = []
        # west i.e j+=2
        if col == 1:
            col = 0
        else:
            col = 1
        if j + 2 < 8:
            if i - 1 > 0:
                if self.get_col(self.game_board.tile[i - 1][j + 2].piece) == col or self.game_board.tile[i - 1][
                            j + 2].piece == -1:
                    movelist.append((i - 1, j + 2))
            if i + 1 < 8:
                if self.get_col(self.game_board.tile[i + 1][j + 2].piece) == col or self.game_board.tile[i + 1][
                            j + 2].piece == -1:
                    movelist.append((i - 1, j + 2))
        # east j-=2
        if j - 2 > 0:
            if i - 1 > 0:
                if self.get_col(self.game_board.tile[i - 1][j - 2].piece) == col or self.game_board.tile[i - 1][
                            j - 2].piece == -1:
                    movelist.append((i - 1, j + 2))
            if i + 1 < 8:
                if self.get_col(self.game_board.tile[i + 1][j - 2].piece) == col or self.game_board.tile[i + 1][
                            j - 2].piece == -1:
                    movelist.append((i - 1, j + 2))
        # south i-=2
        if i + 2 < 8:
            if j - 1 > 0:
                if self.get_col(self.game_board.tile[i + 2][j - 1].piece) == col or self.game_board.tile[i + 2][
                            j - 1].piece == -1:
                    movelist.append((i - 1, j + 2))
            if j + 1 < 8:
                if self.get_col(self.game_board.tile[i + 2][j + 1].piece) == col or self.game_board.tile[i + 2][
                            j + 1].piece == -1:
                    movelist.append((i - 1, j + 2))
        # north i-2
        if i - 2 > 0:
            if j - 1 > 0:
                if self.get_col(self.game_board.tile[i - 2][j - 1].piece) == col or self.game_board.tile[i - 2][
                            j - 1].piece == -1:
                    movelist.append((i - 1, j + 2))
            if j + 1 < 8:
                if self.get_col(self.game_board.tile[i - 2][j + 1].piece) == col or self.game_board.tile[i - 2][
                            j + 1].piece == -1:
                    movelist.append((i - 1, j + 2))

    def bishop_movelist(self, i, j, col):
        movelist = []
        if col == 1:
            col = 0
        else:
            col = 1
        # for north east
        tempi = i - 1
        temp_j = j + 1
        while (tempi >= 0 and temp_j < 8 and self.game_board.tile[tempi][temp_j].piece == -1):
            movelist.append((tempi, temp_j))
            tempi -= 1
            temp_j += 1
        if (tempi >= 0 and temp_j < 8 and self.get_col(self.game_board.tile[tempi][temp_j].piece) == col):  # kill
            movelist.append((tempi, temp_j))
        # for north west
        tempi = i - 1
        temp_j = j - 1
        while (tempi >= 0 and temp_j >= 0 and self.game_board.tile[tempi][temp_j].piece == -1):
            movelist.append((tempi, temp_j))
            tempi -= 1
            temp_j -= 1
        if (tempi >= 0 and temp_j >= 0 and self.get_col(self.game_board.tile[tempi][temp_j].piece) == col):  # kill
            movelist.append((tempi, temp_j))
        # south east
        tempi = i + 1
        temp_j = j + 1
        while (tempi < 8 and temp_j < 8 and self.game_board.tile[tempi][temp_j].piece == -1):
            movelist.append((tempi, temp_j))
            tempi += 1
            temp_j += 1
        if (tempi < 8 and temp_j < 8 and self.get_col(self.game_board.tile[tempi][temp_j].piece) == col):  # kill
            movelist.append((tempi, temp_j))
        # south west
        tempi = i + 1
        temp_j = j - 1
        while (tempi < 8 and temp_j >= 0 and self.game_board.tile[tempi][temp_j].piece == -1):
            movelist.append((tempi, temp_j))
            tempi += 1
            temp_j -= 1
        if (tempi < 8 and temp_j >= 0 and self.get_col(self.game_board.tile[tempi][temp_j].piece) == col):  # kill
            movelist.append((tempi, temp_j))
        print(movelist)
        return movelist

    def queen_movelist(self, i, j, col):
        movelist = []
        if col == 1:
            col = 0
        else:
            col = 1
            # Bishop Part
        # for north east
        temp_i = i - 1
        temp_j = j + 1
        while (temp_i >= 0 and temp_j < 8 and self.game_board.tile[temp_i][temp_j].piece == -1):
            movelist.append((temp_i, temp_j))
            temp_i -= 1
            temp_j += 1
        if (temp_i >= 0 and temp_j < 8 and self.get_col(self.game_board.tile[temp_i][temp_j].piece) == col):  # kill
            movelist.append((temp_i, temp_j))
        # for north west
        temp_i = i - 1
        temp_j = j - 1
        while (temp_i >= 0 and temp_j >= 0 and self.game_board.tile[temp_i][temp_j].piece == -1):
            movelist.append((temp_i, temp_j))
            temp_i -= 1
            temp_j -= 1
        if (temp_i >= 0 and temp_j >= 0 and self.get_col(self.game_board.tile[temp_i][temp_j].piece) == col):  # kill
            movelist.append((temp_i, temp_j))
        # south east
        temp_i = i + 1
        temp_j = j + 1
        while (temp_i < 8 and temp_j < 8 and self.game_board.tile[temp_i][temp_j].piece == -1):
            movelist.append((temp_i, temp_j))
            temp_i += 1
            temp_j += 1
        if (temp_i < 8 and temp_j < 8 and self.get_col(self.game_board.tile[temp_i][temp_j].piece) == col):  # kill
            movelist.append((temp_i, temp_j))
        # south west
        temp_i = i + 1
        temp_j = j - 1
        while (temp_i < 8 and temp_j >= 0 and self.game_board.tile[temp_i][temp_j].piece == -1):
            movelist.append((temp_i, temp_j))
            temp_i += 1
            temp_j -= 1
        if (temp_i < 8 and temp_j >= 0 and self.get_col(self.game_board.tile[temp_i][temp_j].piece) == col):  # kill
            movelist.append((temp_i, temp_j))
            # Rook Part
        while (temp_j >= 0 and self.game_board.tile[i][temp_j].piece == -1):
            movelist.append((i, temp_j))
            temp_j -= 1
        if (temp_j >= 0 and self.get_col(self.game_board.tile[i][temp_j].piece) == col ):  # kill
            movelist.append((i, temp_j))
        # for right direction
        temp_j = j + 1
        while (temp_j < 8 and self.game_board.tile[i][temp_j].piece == -1):
            movelist.append((i, temp_j))
            temp_j += 1
        if (temp_j < 8 and self.get_col(self.game_board.tile[i][temp_j].piece) == col ):  # kill
            movelist.append((i, temp_j))
        # for down
        temp_i = i + 1
        while temp_i < 8 and self.game_board.tile[temp_i][j].piece == -1:
            movelist.append((temp_i, j))
            temp_i += 1
        if (temp_i < 8 and self.get_col(self.game_board.tile[temp_i][j].piece) == col):  # kill
            movelist.append((temp_i, j))
        # for up
        temp_i = i - 1
        while temp_i >= 0 and self.game_board.tile[temp_i][j].piece == -1:
            movelist.append((temp_i, j))
            temp_i -= 1
        if (temp_i >= 0 and self.get_col(self.game_board.tile[temp_i][j].piece) == col ):  # kill
            movelist.append((temp_i, j))

    # End

    def king_movelist(self, i, j, col):
        if col == 1:
            pass
        else:
            pass

    # end of movelists
    def change_style(self, i, j, change):  # changes color of tile when a piece is selected
        if ((i + j) % 2 == 0):
            tile_color = 1
        else:
            tile_color = 0  # black
        if change == 1:
            if (tile_color == 0):
                self.game_board.tile[i][j].setStyleSheet(
                    "QLabel{background-color :qlineargradient(spread:pad, x1:0.489, y1:1, x2:0.512, y2:0, stop:0 rgba(40, 40, 40, 246), stop:1 rgba(145, 145, 145, 255));border: 1px solid black;}QLabel { border: 2px solid qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(255, 176, 176, 167), stop:0.0909091 rgba(0, 255, 191, 51), stop:0.1 rgba(0, 255, 234, 255), stop:0.409091 rgba(1, 255, 223, 92), stop:0.6 rgba(180, 255, 240, 84), stop:1 rgba(76, 218, 255, 205))}")
            else:
                self.game_board.tile[i][j].setStyleSheet(
                    "QLabel{background-color :qlineargradient(spread:pad, x1:0.506, y1:0.977273, x2:0.512, y2:0, stop:0 rgba(214, 214, 214, 246), stop:1 rgba(255, 255, 255, 255));border: 1px solid black}QLabel { border: 2px solid qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(255, 176, 176, 167), stop:0.0909091 rgba(0, 255, 191, 51), stop:0.1 rgba(0, 255, 234, 255), stop:0.409091 rgba(1, 255, 223, 92), stop:0.6 rgba(180, 255, 240, 84), stop:1 rgba(76, 218, 255, 205))}")
        else:
            if (tile_color == 0):
                self.game_board.tile[i][j].setStyleSheet(
                    "QLabel{background-color :qlineargradient(spread:pad, x1:0.489, y1:1, x2:0.512, y2:0, stop:0 rgba(40, 40, 40, 246), stop:1 rgba(145, 145, 145, 255));border: 1px solid black;}QLabel:hover { border: 2px solid qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(255, 176, 176, 167), stop:0.0909091 rgba(255, 125, 125, 51), stop:0.1 rgba(255, 0, 0, 255), stop:0.409091 rgba(255, 151, 151, 92), stop:0.6 rgba(255, 180, 180, 84), stop:1 rgba(255, 76, 76, 205))}")
            else:
                self.game_board.tile[i][j].setStyleSheet(
                    "QLabel{background-color :qlineargradient(spread:pad, x1:0.506, y1:0.977273, x2:0.512, y2:0, stop:0 rgba(214, 214, 214, 246), stop:1 rgba(255, 255, 255, 255));border: 1px solid black}QLabel:hover { border: 2px solid qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(255, 176, 176, 167), stop:0.0909091 rgba(255, 125, 125, 51), stop:0.1 rgba(255, 0, 0, 255), stop:0.409091 rgba(255, 151, 151, 92), stop:0.6 rgba(255, 180, 180, 84), stop:1 rgba(255, 76, 76, 205))}")

                # save load and undo

    def undo_move(self):
        if self.whites_move == 1:
            self.whites_move = 0
        else:
            self.whites_move = 1
        if self.selected_i is not None:  # check if a piece is selected, reverts back if selected
            self.change_style(self.selected_i, self.selected_j, 0)
            self.selected_i = None
            self.selected_j = None

        last_move = self.move_history[-1]
        self.move_history.pop()
        current_i = 8 - (ord(last_move[3]) - 48)
        current_j = ord(last_move[2]) - 97
        previous_i = 8 - (ord(last_move[1]) - 48)
        previous_j = ord(last_move[0]) - 97
        piece = self.game_board.tile[current_i][current_j].piece
        if (piece == -1):
            if (current_i == 0):  # white pawn is promoted
                piece = 15
                self.score_white -= 1
                self.white_pawn += 1
                current_score1 = ord(self.p1_score.text()[-1])
                self.p1_score.setText("Player1-" + chr(current_score1 - 1))
            else:
                piece = 5
                self.score_black -= 1
                self.black_pawn += 1
                current_score2 = ord(self.p2_score.text()[-1])
                self.p2_score.setText("Player2-" + chr(current_score2 - 1))
        self.game_board.set_piece(self.get_code(piece), self.get_col(piece), previous_i, previous_j)
        self.game_board.remove_piece(current_i, current_j)
        if 'x' in last_move:
            if 'p' in last_move:  # en_passant
                print("enpassant")
                if self.whites_move:
                    self.game_board.set_piece(5, 0, previous_i, current_j)  # revive black pawn
                    self.black_pawn += 1
                else:
                    self.game_board.set_piece(5, 1, previous_i, current_j)  # revive white pawn
                    self.white_pawn += 1
            else:
                old_piece = ord(last_move[5]) - 48
                old_col = self.get_col(old_piece)
                old_code = self.get_code(old_piece)
                if old_col:  # increase count of pieces as dead pieces are revived
                    if old_code == 5:
                        self.white_pawn += 1
                    elif old_code == 4:
                        self.white_rook += 1
                    elif old_code == 2:
                        self.white_bishop += 1
                else:
                    if old_code == 5:
                        self.black_pawn += 1
                    elif old_code == 4:
                        self.black_rook += 1
                    elif old_code == 2:
                        self.black_bishop += 1
                self.game_board.set_piece(old_code, old_col, current_i, current_j)
        if len(self.move_history) == 0:
            self.undo.setDisabled(True)

    def save_button(self):
        file_name = QFileDialog.getSaveFileName(self, 'Save File', os.getcwd())[0]
        FILE = open(file_name, "w")
        # save who's turn is next
        FILE.write("%s\n" % chr(self.whites_move + 48))
        # save all moves
        for item in self.move_history:
            FILE.write("%s " % item)
        FILE.write("\n")
        # save scores
        FILE.write("%s %s\n" % ( self.p1_score.text(), self.p2_score.text()))
        # save piece information
        FILE.write("%s %s %s\n" % (self.white_pawn, self.white_bishop, self.white_rook))
        FILE.write("%s %s %s\n" % (self.black_pawn, self.black_bishop, self.black_rook))
        # save players
        if self.white_is_bot:
            FILE.write("1 %s \n" % (self.bot1_path))
        else:
            FILE.write("0\n")
        if self.black_is_bot:
            FILE.write("1 %s \n" % (self.bot2_path))
        else:
            FILE.write("0\n")
        FILE.close()

    def load_game(self):
        FILE = open(self.file_path, 'r')
        line = FILE.readline()
        self.whites_move = ord(line[0]) - 48
        line = FILE.readline()
        self.move_history = line.split(' ')
        self.move_history.pop()
        # make moves to current state of game
        for move in self.move_history:
            self.make_move(move)
        line = FILE.readline()
        # set scores
        self.p1_score.setText(line.split(' ')[0])
        self.p2_score.setText(line.split(' ')[1])
        self.score_white = ord(self.p1_score.text()[-1]) - 48
        self.score_black = ord(self.p2_score.text()[-2]) - 48
        # retrieve piece information
        line = FILE.readline()
        self.white_pawn, self.white_bishop, self.white_rook = int(line.split(' ')[0]), int(line.split(' ')[1]), int(
            line.split(' ')[2])
        line = FILE.readline()
        self.black_pawn, self.black_bishop, self.black_rook = int(line.split(' ')[0]), int(line.split(' ')[1]), int(
            line.split(' ')[2])
        # set players
        line = FILE.readline()
        self.white_is_bot = int(line.split(' ')[0])
        if self.white_is_bot:
            self.bot1_path = line.split(' ')[1]
        line = FILE.readline()
        self.black_is_bot = int(line.split(' ')[0])
        if self.black_is_bot:
            self.bot2_path = line.split(' ')[1]
        self.make_bot_move()

    def make_move(self, move):
        current_i = 8 - (ord(move[1]) - 48)
        current_j = ord(move[0]) - 97
        final_i = 8 - (ord(move[3]) - 48)
        final_j = ord(move[2]) - 97
        piece = self.game_board.tile[current_i][current_j].piece
        self.game_board.remove_piece(current_i, current_j)
        if (piece == 5 or piece == 15) and (final_i == 0 or final_i == 7):  # dont set pawn as it is promoted
            pass
        else:
            self.game_board.set_piece(self.get_code(piece), self.get_col(piece), final_i,
                                      final_j)  # set piece to its final position
        if 'p' in move:
            if final_i == 2:  # case for white
                self.game_board.remove_piece(final_i + 1, final_j)
            else:
                self.game_board.remove_piece(final_i - 1, final_j)

    # game ending
    def game_end(
            self):  # game ends when both of the player either of player is unable to move or both player have no pawn remaining
        print("pawn count=", self.white_pawn, self.black_pawn, "bishops=", self.white_bishop, self.black_bishop,
              "rook=", self.white_rook, self.black_rook)
        if self.white_pawn == 0 and self.black_pawn == 0:
            return 1
        if self.white_pawn == 0 and self.white_bishop == 0 and self.white_rook == 0:
            return 1
        if self.black_pawn == 0 and self.black_bishop == 0 and self.black_rook == 0:
            return 1
        if self.white_rook == 0 and self.white_bishop == 0 and self.black_bishop == 0 and self.black_rook == 0:  # check if player is unable to make a move
            pass

    def result(self,dis=0):  # working
        if dis==1: # white disqualified
            pass
        elif dis==2: # black disqualified
            pass
        else:
            self.score_black += self.black_pawn
            self.p1_score.setText("Player1-" + chr(self.score_white + 48))
            self.p2_score.setText("Player2-" + chr(self.score_black + 48))
            if self.score_white > self.score_black:
                print("white win")
            elif self.score_white == self.score_black:
                print("Stalemate")
            else:
                print("Black Win")


    # bot part
    def write_board_file(self):
        board_file = open("self.board_file", 'w')
        board_file.write("%s\n" % self.last_bot_move)
        for i in range(0, 8):
            for j in range(0, 8):
                piece = self.game_board.tile[i][j].piece
                if piece != -1:
                    pos = chr(j + 97)
                    pos += chr(8 - i + 48)
                    board_file.write("%s %s\n" % (piece, pos))

    def read_move(self, bot_path):
        print("reading from")
        print(bot_path)
        proc = subprocess.Popen([bot_path], stdout=subprocess.PIPE)
        stddata = proc.communicate()
        move = stddata[0].decode('ascii')
        print("bot move = ", move[0:4])
        return move

    def validate_move(self, move):
        if len(move) != 4:
            return False
        current_i = 8 - (ord(move[1]) - 48)
        current_j = ord(move[0]) - 97
        final_i = 8 - (ord(move[3]) - 48)
        final_j = ord(move[2]) - 97
        print(current_i, current_j, final_i, final_j)
        piece = self.game_board.tile[current_i][current_j].piece
        print("piece selected=", piece)
        if not (8 > current_i >= 0 and 8 > final_i >= 0 and 8 > current_j >= 0 and 0 <= final_j < 8):
            return False
        print("2")
        if self.whites_move:
            if self.get_col(piece) != 1:
                return False
        else:
            print("3")
            if self.get_col(piece) != 0:
                return False
        if (final_i, final_j) in self.possible_moves(current_i, current_j,self.game_board.tile[current_i][current_j].piece):
            return True
        else:
            return False

    def make_bot_move(self):
        if self.whites_move:
            if self.white_is_bot:  # get move from bot1
                bot1_move = self.read_move(self.bot1_path)
                if self.validate_move(bot1_move):
                    print("validated true")
                    self.selected_i = 8 - (ord(bot1_move[1]) - 48)
                    self.selected_j = ord(bot1_move[0]) - 97
                    final_i = 8 - (ord(bot1_move[3]) - 48)
                    final_j = ord(bot1_move[2]) - 97
                    self.board_clicked(final_i, final_j)
                    self.write_board_file()
                else:
                    print("invalid")
        else:
            if self.black_is_bot:  # get move from bot2
                bot2_move = self.read_move(self.bot2_path)
                if self.validate_move(bot2_move):
                    self.selected_i = 8 - (ord(bot2_move[1]) - 48)
                    self.selected_j = ord(bot2_move[0]) - 97
                    final_i = 8 - (ord(bot2_move[3]) - 48)
                    final_j = ord(bot2_move[2]) - 97
                    self.board_clicked(final_i, final_j)
                    self.write_board_file()
                else:
                    print("invalid")
