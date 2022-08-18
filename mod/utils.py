from PyQt5 import QtCore, QtGui, QtWidgets


def setMenu(menu:QtWidgets.QMenu, text: str, triggered):
    """设置菜单"""
    action = menu.addAction(text)
    action.triggered.connect(triggered)
