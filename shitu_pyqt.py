#!/usr/bin/python3
# -*- coding: utf-8 -*-


import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import mod.mainwindow


def main():
    app = QtWidgets.QApplication(sys.argv)
    main_window = mod.mainwindow.MainWindow()
    # main_window.show()
    main_window.showMaximized()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()