from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal


class MyLabel(QLabel):
    clickedk = pyqtSignal(int,int)
    def __init__(self, img=None):
        super(MyLabel, self).__init__()
        self.piece=-1 #stores piece number
        self.i=0 #stores x coordinate of this label on grid layout
        self.j=0 #stores y coordinate

        if img is not None:
            self.pixmap = QPixmap(img)
        else:
            self.pixmap = None

    def paintEvent(self, event):
        if self.pixmap is not None:
            size = self.size()
            painter = QtGui.QPainter(self)
            point = QtCore.QPoint(0, 0)
            scaledPix = self.pixmap.scaled(size, Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation)
            # start painting the label from left upper corner
            point.setX((size.width() - scaledPix.width()) / 2)
            point.setY((size.height() - scaledPix.height()) / 2)
            painter.drawPixmap(point, scaledPix)
        else:
            super(MyLabel, self).paintEvent(event)

    def change_pixmap(self, img):
        self.pixmap = QPixmap(img)
        self.repaint()

    def mousePressEvent(self, QMouseEvent):
        self.clickedk.emit(self.i,self.j)
