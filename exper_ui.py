# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'G:\Coding\Python\3Knights\exper_ui.ui'
#
# Created: Fri Dec 12 23:43:10 2014
#      by: PyQt5 UI code generator 5.3.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(476, 300)
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(60, 80, 343, 25))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.p1_score = QtWidgets.QLabel(self.widget)
        self.p1_score.setObjectName("p1_score")
        self.horizontalLayout.addWidget(self.p1_score)
        self.undo = QtWidgets.QPushButton(self.widget)
        self.undo.setObjectName("undo")
        self.horizontalLayout.addWidget(self.undo)
        self.save = QtWidgets.QPushButton(self.widget)
        self.save.setObjectName("save")
        self.horizontalLayout.addWidget(self.save)
        self.back = QtWidgets.QPushButton(self.widget)
        self.back.setObjectName("back")
        self.horizontalLayout.addWidget(self.back)
        self.p2_score = QtWidgets.QLabel(self.widget)
        self.p2_score.setObjectName("p2_score")
        self.horizontalLayout.addWidget(self.p2_score)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.p1_score.setText(_translate("Form", "Player1-0"))
        self.undo.setText(_translate("Form", "Undo"))
        self.save.setText(_translate("Form", "Save"))
        self.back.setText(_translate("Form", "Back"))
        self.p2_score.setText(_translate("Form", "Player2-0"))

