from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from mylabel import MyLabel


class Board(QGridLayout):
    def __init__(self):
        super(Board, self).__init__()
        self.setObjectName("gridLayout")
        self.setHorizontalSpacing(0)
        self.setVerticalSpacing(0)
        self.tile = []
        alt = 1;
        for i in range(0, 8):
            if alt > 0:
                alt -= 1
            else:
                alt += 1
            self.tile.append([])
            for j in range(0, 8):
                self.tile[i].append(MyLabel())
                self.tile[i][j].setGeometry(QtCore.QRect(0, 0, 50, 50))
                self.tile[i][j].setObjectName(str(i) + "," + str(j))
                if alt > 0:
                    self.tile[i][j].setStyleSheet(
                        "background-color :qlineargradient(spread:pad, x1:0.489, y1:1, x2:0.512, y2:0, stop:0 rgba(40, 40, 40, 246), stop:1 rgba(145, 145, 145, 255));border: 1px solid black;")
                    alt -= 1
                else:
                    self.tile[i][j].setStyleSheet(
                        "background-color :qlineargradient(spread:pad, x1:0.506, y1:0.977273, x2:0.512, y2:0, stop:0 rgba(214, 214, 214, 246), stop:1 rgba(255, 255, 255, 255));border: 1px solid black")
                    alt += 1
                self.addWidget(self.tile[i][j], i, j, 1, 1)

    def set_piece(self, code, col, x, y):
        if code == 0:  # king
            if col == 0:
                self.tile[x][y].change_pixmap("/images/BK.png")
            else:
                self.tile[x][y].change_pixmap("/images/WK.png")
        elif code == 1:  # queen
            if col == 0:
                self.tile[x][y].change_pixmap("/images/BQ.png")
            else:
                self.tile[x][y].change_pixmap("/images/WQ.png")
        elif code == 2:  # bishop
            if col == 0:
                self.tile[x][y].change_pixmap("/images/BB.png")
            else:
                self.tile[x][y].change_pixmap("/images/WB.png")
        elif code == 3:  # knight
            if col == 0:
                self.tile[x][y].change_pixmap("/images/BT.png")
            else:
                self.tile[x][y].change_pixmap("/images/WT.png")
        elif code == 4:  # rook
            if col == 0:
                self.tile[x][y].change_pixmap("/images/BR.png")
            else:
                self.tile[x][y].change_pixmap("/images/WR.png")
        elif code == 5:  # pawn
            if col == 0:
                self.tile[x][y].change_pixmap("/images/BP.png")
            else:
                self.tile[x][y].change_pixmap("/images/WP.png")

    def remove_piece(self,x,y):
        self.tile[x][y].pixmap = None