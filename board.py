from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets

class Board(QWidget):
    def __init__(self):
        super(Board, self).__init__()
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(220, 0, 41, 16))
        self.label.setObjectName("label1")
        self.label.setText("kk")
        self.widget = QtWidgets.QWidget(self)
        self.widget.setGeometry(QtCore.QRect(200, 300, 158, 83))
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.tile = []
        for i in range(0, 8):
            self.tile.append([])
            for j in range(0, 8):
                self.tile[i].append(QtWidgets.QLabel(self))
                self.tile[i][j].setGeometry(QtCore.QRect(220, 0, 41, 16))
                self.tile[i][j].setObjectName(str(i) + "," + str(j))
                self.tile[i][j].setText(str(i) + "," + str(j))
                self.gridLayout.addWidget(self.tile[i][j], i, j, 1, 1)