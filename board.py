from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from os import path
from mylabel import MyLabel


class Board(QGridLayout):
    def __init__(self):
        super(Board, self).__init__()
        self.setObjectName("gridLayout")
        self.setHorizontalSpacing(0)
        self.setVerticalSpacing(0)
        self.tile = []
        self.dir = path.dirname(__file__)
        alt = 1;
        for i in range(0, 8):
            if alt > 0:
                alt -= 1
            else:
                alt += 1
            self.tile.append([])
            for j in range(0, 8):
                self.tile[i].append(MyLabel())
                self.tile[i][j].setGeometry(QtCore.QRect(0, 0, 200, 200))
                self.tile[i][j].i=i
                self.tile[i][j].j=j
                if alt > 0:
                    self.tile[i][j].setStyleSheet(
                        "QLabel{background-color :qlineargradient(spread:pad, x1:0.489, y1:1, x2:0.512, y2:0, stop:0 rgba(40, 40, 40, 246), stop:1 rgba(145, 145, 145, 255));border: 1px solid black;}QLabel:hover { border: 2px solid qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(255, 176, 176, 167), stop:0.0909091 rgba(255, 125, 125, 51), stop:0.1 rgba(255, 0, 0, 255), stop:0.409091 rgba(255, 151, 151, 92), stop:0.6 rgba(255, 180, 180, 84), stop:1 rgba(255, 76, 76, 205))}")
                    alt -= 1
                else:
                    self.tile[i][j].setStyleSheet(
                        "QLabel{background-color :qlineargradient(spread:pad, x1:0.506, y1:0.977273, x2:0.512, y2:0, stop:0 rgba(214, 214, 214, 246), stop:1 rgba(255, 255, 255, 255));border: 1px solid black}QLabel:hover { border: 2px solid qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(255, 176, 176, 167), stop:0.0909091 rgba(255, 125, 125, 51), stop:0.1 rgba(255, 0, 0, 255), stop:0.409091 rgba(255, 151, 151, 92), stop:0.6 rgba(255, 180, 180, 84), stop:1 rgba(255, 76, 76, 205))}")
                    alt += 1
                self.addWidget(self.tile[i][j], i, j, 1, 1)
        self.setGeometry(QtCore.QRect(0,0,800,800))

    def set_piece(self, code, col, x, y):
        if code == 0:  # king
            if col == 0:
                self.tile[x][y].change_pixmap(path.join(self.dir,"images\BK.png"))
                self.tile[x][y].piece=0
            else:
                self.tile[x][y].change_pixmap(path.join(self.dir,"images\WK.png"))
                self.tile[x][y].piece=10
        elif code == 1:  # queen
            if col == 0:
                self.tile[x][y].change_pixmap(path.join(self.dir,"images\BQ.png"))
                self.tile[x][y].piece=1
            else:
                self.tile[x][y].change_pixmap(path.join(self.dir,"images\WQ.png"))
                self.tile[x][y].piece=11
        elif code == 2:  # bishop
            if col == 0:
                self.tile[x][y].change_pixmap(path.join(self.dir,"images\BB.png"))
                self.tile[x][y].piece=2
            else:
                self.tile[x][y].change_pixmap(path.join(self.dir,"images\WB.png"))
                self.tile[x][y].piece=12
        elif code == 3:  # knight
            if col == 0:
                self.tile[x][y].change_pixmap(path.join(self.dir,"images\BT.png"))
                self.tile[x][y].piece=3
            else:
                self.tile[x][y].change_pixmap(path.join(self.dir,"images\WT.png"))
                self.tile[x][y].piece=13
        elif code == 4:  # rook
            if col == 0:
                self.tile[x][y].change_pixmap(path.join(self.dir,"images\BR.png"))
                self.tile[x][y].piece=4
            else:
                self.tile[x][y].change_pixmap(path.join(self.dir,"images\WR.png"))
                self.tile[x][y].piece=14
        elif code == 5:  # pawn
            if col == 0:
                self.tile[x][y].change_pixmap(path.join(self.dir,"images\BP.png"))
                self.tile[x][y].piece=5
            else:
                self.tile[x][y].change_pixmap(path.join(self.dir,"images\WP.png"))
                self.tile[x][y].piece=15

    def remove_piece(self,x,y):
        self.tile[x][y].pixmap = None
        self.tile[x][y].repaint()
        self.tile[x][y].piece = -1