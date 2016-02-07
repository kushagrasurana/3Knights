# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'onlinewindow_ui.ui'
#
# Created: Sun Feb  7 20:30:30 2016
#      by: PyQt5 UI code generator 5.3.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(398, 227)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.oponnentIp = QtWidgets.QLineEdit(self.centralwidget)
        self.oponnentIp.setObjectName("oponnentIp")
        self.horizontalLayout_2.addWidget(self.oponnentIp)
        self.connectButton = QtWidgets.QPushButton(self.centralwidget)
        self.connectButton.setObjectName("connectButton")
        self.horizontalLayout_2.addWidget(self.connectButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_4.addWidget(self.label_4)
        self.yesRadioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.yesRadioButton.setObjectName("yesRadioButton")
        self.buttonGroup = QtWidgets.QButtonGroup(MainWindow)
        self.buttonGroup.setObjectName("buttonGroup")
        self.buttonGroup.addButton(self.yesRadioButton)
        self.horizontalLayout_4.addWidget(self.yesRadioButton)
        self.noRadioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.noRadioButton.setObjectName("noRadioButton")
        self.buttonGroup.addButton(self.noRadioButton)
        self.horizontalLayout_4.addWidget(self.noRadioButton)
        self.botPath = QtWidgets.QLineEdit(self.centralwidget)
        self.botPath.setObjectName("botPath")
        self.horizontalLayout_4.addWidget(self.botPath)
        self.browseButton = QtWidgets.QPushButton(self.centralwidget)
        self.browseButton.setObjectName("browseButton")
        self.horizontalLayout_4.addWidget(self.browseButton)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.selfPrivateIp = QtWidgets.QLabel(self.centralwidget)
        self.selfPrivateIp.setText("")
        self.selfPrivateIp.setObjectName("selfPrivateIp")
        self.horizontalLayout_3.addWidget(self.selfPrivateIp)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.selfPublicIp = QtWidgets.QLabel(self.centralwidget)
        self.selfPublicIp.setText("")
        self.selfPublicIp.setObjectName("selfPublicIp")
        self.horizontalLayout.addWidget(self.selfPublicIp)
        self.verticalLayout.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Enter opponent\'s ip"))
        self.connectButton.setText(_translate("MainWindow", "Connect"))
        self.label_4.setText(_translate("MainWindow", "You are human?"))
        self.yesRadioButton.setText(_translate("MainWindow", "Yes"))
        self.noRadioButton.setText(_translate("MainWindow", "No"))
        self.browseButton.setText(_translate("MainWindow", "Browse"))
        self.label_2.setText(_translate("MainWindow", "Private Ip"))
        self.label_3.setText(_translate("MainWindow", "Public Ip"))

