from PyQt5.QtWidgets import *
from board import Board


class MyGame(QWidget):
    def __init__(self, new_game=1):
        super(MyGame, self).__init__()
        self.whites_move = 1
        self.selected_i = None
        self.selected_j = None
        self.score_white=0
        self.score_black=0
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
            if (i, j) in self.possible_moves(self.selected_i, self.selected_j,self.game_board.tile[self.selected_i][self.selected_j].piece):
                print(i, j, "in move list")  # working
                piece = self.game_board.tile[self.selected_i][self.selected_j].piece
                code = self.get_code(piece)
                col = self.get_col(piece)
                self.game_board.remove_piece(self.selected_i, self.selected_j)
                self.game_board.set_piece(code, col, i, j)
                self.selected_i = None
                self.selected_j = None
                if self.whites_move == 1:
                    self.whites_move = 0
                else:
                    self.whites_move = 1
                if(code==5 and i==0 and col==1):
                    self.score_white+=1
                    print("white increase")
                    self.game_board.remove_piece(i,j)
                if(code==5 and i==7 and col==0):
                    self.score_black+=1
                    print("black increase")
                    self.game_board.remove_piece(i,j)

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
        move_list = [(1, 1), (2, 2)]
        return move_list

    def get_code(self,piece):
        return piece % 10

    def get_col(self,piece):
        if piece == -1:
            return -1
        if piece > 5:
            return 1
        else:
            return 0

    def pawn_movelist(self,i, j, col):
        movelist = []
        if col == 1:
            if self.game_board.tile[i-1][j].piece == -1:
                movelist.append((i-1,j))
                if(i==6 and self.game_board.tile[i-2][j].piece == -1):
                    movelist.append((i-2,j))
            if(j>0):
                if self.get_col(self.game_board.tile[i-1][j-1].piece) == 0:
                    movelist.append((i-1,j-1))
            if(j<7):
                if self.get_col(self.game_board.tile[i-1][j+1].piece) == 0:
                    movelist.append((i-1,j+1))
        else:
            if self.game_board.tile[i+1][j].piece == -1:
                movelist.append((i+1,j))
                if(i==1 and self.game_board.tile[i+2][j].piece == -1):
                    movelist.append((i+2,j))
            if(j>0):
                if self.get_col(self.game_board.tile[i+1][j-1].piece) == 1:
                    movelist.append((i+1,j-1))
            if(j<7):
                if self.get_col(self.game_board.tile[i+1][j+1].piece) == 1:
                    movelist.append((i+1,j+1))
        print (movelist)
        return movelist

    def rook_movelist(self,i, j, col):
        movelist = []
        if col == 1:
            # first for left direction
            tempj=j-1
            while(tempj>=0 and self.game_board.tile[i][tempj].piece==-1):
                movelist.append((i,tempj))
                tempj-=1
            if(tempj>=0 and self.get_col(self.game_board.tile[i][tempj].piece)==0 ): #kill
                movelist.append((i,tempj))
            # for right direction
            tempj=j+1
            while(tempj<8 and self.game_board.tile[i][tempj].piece==-1):
                movelist.append((i,tempj))
                tempj+=1
            if(tempj<8 and self.get_col(self.game_board.tile[i][tempj].piece)==0 ): #kill
                movelist.append((i,tempj))
            # for down
            tempi=i+1
            while tempi<8 and self.game_board.tile[tempi][j].piece==-1:
                movelist.append((tempi,j))
                tempi+=1
            if(tempi<8 and self.get_col(self.game_board.tile[tempi][j].piece)==0 ): #kill
                movelist.append((tempi,j))
            # for up
            tempi=i-1
            while tempi>=0 and self.game_board.tile[tempi][j].piece==-1:
                movelist.append((tempi,j))
                tempi-=1
            if(tempi>=0 and self.get_col(self.game_board.tile[tempi][j].piece)==0 ): #kill
                movelist.append((tempi,j))
        else:
            # first for left direction
            tempj=j-1
            while(tempj>=0 and self.game_board.tile[i][tempj].piece==-1):
                movelist.append((i,tempj))
                tempj-=1
            if(tempj>=0 and self.get_col(self.game_board.tile[i][tempj].piece)==1 ): #kill
                movelist.append((i,tempj))
            # for right direction
            tempj=j+1
            while(tempj<8 and self.game_board.tile[i][tempj].piece==-1):
                movelist.append((i,tempj))
                tempj+=1
            if(tempj<8 and self.get_col(self.game_board.tile[i][tempj].piece)==1 ): #kill
                movelist.append((i,tempj))
            # for down
            tempi=i+1
            while tempi<8 and self.game_board.tile[tempi][j].piece==-1:
                movelist.append((tempi,j))
                tempi+=1
            if(tempi<8 and self.get_col(self.game_board.tile[tempi][j].piece)==1 ): #kill
                movelist.append((tempi,j))
            # for up
            tempi=i-1
            while tempi>=0 and self.game_board.tile[tempi][j].piece==-1:
                movelist.append((tempi,j))
                tempi-=1
            if(tempi>=0 and self.get_col(self.game_board.tile[tempi][j].piece)==1 ): #kill
                movelist.append((tempi,j))
        print(movelist)
        return movelist

    def knight_movelist(self,i, j, col):
        if col == 1:
            pass
        else:
            pass

    def bishop_movelist(self,i, j, col):
        if col == 1:
            pass
        else:
            pass

    def queen_movelist(self,i, j, col):
        if col == 1:
            pass
        else:
            pass

    def king_movelist(self,i, j, col):
        if col == 1:
            pass
        else:
            pass