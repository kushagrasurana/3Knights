import sys
from mainwindow import MainWindow
from PyQt5.QtWidgets import *


def main():
    app = QApplication(sys.argv)
    my_app = MainWindow()
    my_app.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()