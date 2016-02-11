import os
import subprocess
import socket
import pickle
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget,QMessageBox,QFileDialog
from PyQt5.QtCore import QTimer, pyqtSignal
import _thread
from board import Board


class MyGame(QWidget):
    data_received = pyqtSignal(int, int, int, int)

    def __init__(self, new_game=1, file_path="", bot1_path="", bot2_path="", is_online=0, socket=None, i_am_white=0):
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
        self.move_count = 0
        self.bot_max_time = 5  # bot must output its move within bot_max_time
        self.game_speed = 200  # in milliseconds
        self.we_have_bot = 1
        self.is_online = is_online

        if self.bot1_path == "":
            self.white_is_bot = 0
        if self.bot2_path == "":
            self.black_is_bot = 0
        if self.black_is_bot == 0 and self.white_is_bot == 0:
            self.we_have_bot = 0

        self.initUI()
        self.write_board_file()
        if new_game == 0:
            self.load_game()
        if is_online:
            self.online_game_init(socket, i_am_white)
        elif (self.white_is_bot and self.whites_move) or (self.black_is_bot and not self.whites_move):
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
                self.game_board.tile[i][j].clickedk.connect(self.select_tile)
        self.game_board.addLayout(self.horizontalLayout, 8, 0, 1, 8)
        self.setLayout(self.game_board)
        self.undo.clicked.connect(self.undo_move)
        self.save.clicked.connect(self.save_button)


    def online_game_init(self, socket, i_am_white):
        self.socket = socket   # socket has the connection
        self.i_am_white = i_am_white    # only required for online game
        if (i_am_white and self.bot1_path != "") or (not i_am_white and self.bot2_path != ""):
            self.i_am_bot = 1
        else:
            self.i_am_bot = 0
        self.data_received.connect(self.play_received_move)
        if self.is_my_turn():
            if self.i_am_bot:
                self.make_bot_move()
        else:
            _thread.start_new_thread(self.received_move(), ())


    def is_my_turn(self):
        if (self.i_am_white and self.move_count % 2 == 0) or (not self.i_am_white and self.move_count % 2 == 1):
            return True
        return False


    def select_tile(self, i, j):
        if self.is_online and (self.i_am_bot or not self.is_my_turn()):
            return

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
            if self.is_valid_move(self.selected_i, self.selected_j, i, j):
                if self.is_online:
                    self.send_move(self.selected_i, self.selected_j, i, j)
                self.play_move(self.selected_i, self.selected_j, i, j)
            else:
                self.change_style(self.selected_i, self.selected_j, 0)
            self.selected_i = None
            self.selected_j = None


    def play_move(self, previous_i, previous_j, new_i, new_j):  # function which processes move made by a player
        self.move_count += 1
        if self.game_board.tile[new_i][new_j].piece != -1:  # already a piece there
            code = self.get_code(self.game_board.tile[new_i][new_j].piece)
            col = self.get_col(self.game_board.tile[new_i][new_j].piece)
            temp_move = (chr(previous_j + 97) + chr(8 - previous_i + 48) + chr(new_j + 97) + chr(
                8 - new_i + 48) + 'x' + chr(self.game_board.tile[new_i][new_j].piece + 48))
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
        elif (new_i, new_j) in self.en_passant(previous_i, previous_j, self.get_col(
                self.game_board.tile[previous_i][previous_j].piece)):  # check for en_passant
            if self.whites_move:
                self.black_pawn -= 1
                self.game_board.remove_piece(new_i + 1, new_j)
            else:
                self.white_pawn -= 1
                self.game_board.remove_piece(new_i - 1, new_j)
            temp_move = (
                chr(previous_j + 97) + chr(8 - previous_i + 48) + chr(new_j + 97) + chr(
                    8 - new_i + 48) + "xp")
        else:
            temp_move = (
                chr(previous_j + 97) + chr(8 - previous_i + 48) + chr(new_j + 97) + chr(8 - new_i + 48))
        self.move_history.append(temp_move)
        self.undo.setEnabled(True)
        piece = self.game_board.tile[previous_i][previous_j].piece
        code = self.get_code(piece)
        col = self.get_col(piece)
        self.game_board.remove_piece(previous_i, previous_j)
        self.game_board.set_piece(code, col, new_i, new_j)
        self.change_style(previous_i, previous_j, 0)

        if self.whites_move == 1:  # change turn
            self.whites_move = 0
        else:
            self.whites_move = 1
        if code == 5 and new_i == 0 and col == 1:  # check if pawn is promoted
            self.score_white += 1
            self.game_board.remove_piece(new_i, new_j)
            self.p1_score.setText("Player1-" + chr(self.score_white + 48))
            self.white_pawn -= 1
        if code == 5 and new_i == 7 and col == 0:
            self.score_black += 1
            self.game_board.remove_piece(new_i, new_j)
            self.p2_score.setText("Player2-" + chr(self.score_black + 48))
            self.black_pawn -= 1
        if self.game_end():  # check if game is ended
            self.result()
        self.write_board_file()
        if self.is_online:
            if not self.is_my_turn():
                _thread.start_new_thread(self.received_move, ())
            elif self.i_am_bot:
                self.make_bot_move()
        else:
            QTimer.singleShot(self.game_speed, self.make_bot_move)



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
                if j - 1 >= 0 and self.game_board.tile[i][j - 1].piece == 5:
                    if last_move_initial_i == 1 and last_move_final_i == 3 and last_move_final_j == j - 1:  # qualified for en passant
                        en_pass_list.append((i - 1, j - 1))
        else:
            if len(self.move_history) > 0 and i == 4:  # check for En passant
                if j + 1 < 8 and self.game_board.tile[i][j + 1].piece == 15:
                    if last_move_initial_i == 6 and last_move_final_i == 4 and last_move_final_j == j + 1:  # qualified for en passant
                        en_pass_list.append((i + 1, j + 1))
                if j - 1 >= 0 and self.game_board.tile[i][j - 1].piece == 15:
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
        if self.whites_move == 1:       # changes whose turn to play
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
        self.write_board_file()

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
        if len(self.move_history):
            self.undo.setEnabled(True)
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
        self.write_board_file()

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
        if self.white_pawn == 0 and self.black_pawn == 0:
            return 1
        if self.white_pawn == 0 and self.white_bishop == 0 and self.white_rook == 0:
            return 1
        if self.black_pawn == 0 and self.black_bishop == 0 and self.black_rook == 0:
            return 1
        # check if next player is able to make a move
        flag = 1
        for i in range(0, 8):
            if flag:
                for j in range (0, 8):
                    if self.get_col(self.game_board.tile[i][j].piece)==self.whites_move:
                        if len(self.possible_moves(i,j,self.game_board.tile[i][j].piece)) > 0:
                            flag = 0
        if flag:
            return 1


    def result(self,dis=0):  # working
        if dis==1: # white disqualified
            text="white disqualified"
        elif dis==2: # black disqualified
            text="black disqualified"
        else:
            self.score_black += self.black_pawn
            self.score_white += self.white_pawn
            self.p1_score.setText("Player1-" + chr(self.score_white + 48))
            self.p2_score.setText("Player2-" + chr(self.score_black + 48))
            if self.score_white > self.score_black:
                text="white win"
            elif self.score_white == self.score_black:
                text="Stalemate"
            else:
                text="Black Win"
        QMessageBox.about(None,"GG",text)

    # bot part
    def write_board_file(self):
        board_file = open("board_file", 'w')
        board_file.write("%s\n" % self.whites_move)
        for i in range(0, 8):
            for j in range(0, 8):
                piece = self.game_board.tile[i][j].piece
                if piece != -1:
                    pos = chr(j + 97)
                    pos += chr(8 - i + 48)
                    board_file.write("%s %s\n" % (piece, pos))


    def read_move(self,bot_path):
        if bot_path.endswith(".py"):
            proc = subprocess.Popen(["python ", bot_path], stdout=subprocess.PIPE)
        elif bot_path.endswith(".jar"):
            proc = subprocess.Popen(["java -jar ", bot_path], stdout=subprocess.PIPE)
        elif bot_path.endswith(".class"):
            class_name = bot_path.split('/')[-1].split('.')[0]
            pos = bot_path.rfind('/')
            class_path =bot_path[0:pos]
            proc = subprocess.Popen(["java","-classpath",class_path,class_name], stdout=subprocess.PIPE)
        elif bot_path.endswith(".java"):
            proc = subprocess.Popen(["javac",bot_path], stdout=subprocess.PIPE)
            proc.wait()
            class_name = bot_path.split('/')[-1].split('.')[0]
            pos = bot_path.rfind('/')
            class_path =bot_path[0:pos]
            proc = subprocess.Popen(["java","-classpath",class_path,class_name], stdout=subprocess.PIPE)
        elif bot_path.endswith(".cpp"):
            command =  "g++ ",bot_path," -o bot.out"
            proc = subprocess.Popen([command], stdout=subprocess.PIPE)
            bot_path = "bot.out"
            proc.wait()
            proc = subprocess.Popen([bot_path], stdout=subprocess.PIPE)
        elif bot_path.endswith(".c"):
            command =  "gcc ",bot_path," -o bot.out"
            proc = subprocess.Popen([command], stdout=subprocess.PIPE)
            bot_path = "bot.out"
            proc.wait()
            proc = subprocess.Popen([bot_path], stdout=subprocess.PIPE)
        else:
            proc = subprocess.Popen([bot_path], stdout=subprocess.PIPE)
        try:
            stddata = proc.communicate(self.bot_max_time) # accepts output from bot file only if in within the time limits.
        except subprocess.TimeoutExpired:
            proc.kill()
            stddata = ""
        move = stddata[0].decode('ascii')
        if len(move)>=4:
            return move[0:4]
        else:
            return ""

    def validate_move(self, move):
        if len(move) != 4:
            return False
        current_i = 8 - (ord(move[1]) - 48)
        current_j = ord(move[0]) - 97
        final_i = 8 - (ord(move[3]) - 48)
        final_j = ord(move[2]) - 97
        return self.is_valid_move(current_i, current_j, final_i, final_j)

    def is_valid_move(self, current_i, current_j, final_i, final_j):
        piece = self.game_board.tile[current_i][current_j].piece
        if not (8 > current_i >= 0 and 8 > final_i >= 0 and 8 > current_j >= 0 and 0 <= final_j < 8):
            return False
        if self.whites_move:
            if self.get_col(piece) != 1:
                return False
        else:
            if self.get_col(piece) != 0:
                return False
        if (final_i, final_j) in self.possible_moves(current_i, current_j,self.game_board.tile[current_i][current_j].piece):
            return True
        else:
            return False

    def make_bot_move(self):
        if not self.we_have_bot:
            return

        if self.whites_move:
            if self.white_is_bot:  # get move from bot1
                bot1_move = self.read_move(self.bot1_path)
                if self.validate_move(bot1_move):
                    previous_i = 8 - (ord(bot1_move[1]) - 48)
                    previous_j = ord(bot1_move[0]) - 97
                    new_i = 8 - (ord(bot1_move[3]) - 48)
                    new_j = ord(bot1_move[2]) - 97
                    if self.is_online:
                        self.send_move(previous_i, previous_j, new_i, new_j)
                    self.play_move(previous_i, previous_j, new_i, new_j)
                else:
                    self.display_message_box("Invalid move played","Black Wins")
        elif self.black_is_bot:  # get move from bot2
            bot2_move = self.read_move(self.bot2_path)
            if self.validate_move(bot2_move):
                previous_i = 8 - (ord(bot2_move[1]) - 48)
                previous_j = ord(bot2_move[0]) - 97
                new_i = 8 - (ord(bot2_move[3]) - 48)
                new_j = ord(bot2_move[2]) - 97
                if self.is_online:
                        self.send_move(previous_i, previous_j, new_i, new_j)
                self.play_move(previous_i, previous_j, new_i, new_j)
            else:
                self.display_message_box("Invalid move played","White Wins")

    @staticmethod
    def display_message_box(title,message):
        QMessageBox.about(None,title,message)

    def send_move(self, previous_i, previous_j, new_i, new_j):
        move = [previous_i, previous_j, new_i, new_j]
        try:
            self.socket.send(pickle.dumps(move))
        except Exception as e:
            print ("unable to send because %s" % e)

    def received_move(self):
        data = self.socket.recv(1024)
        move = pickle.loads(data)
        print ("Recieved move", move)
        self.data_received.emit(move[0], move[1], move[2], move[3])

    def play_received_move(self, previous_i, previous_j, new_i, new_j):
        self.play_move(previous_i, previous_j, new_i, new_j)