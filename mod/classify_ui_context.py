import os
import sys

__dir__ = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.abspath(os.path.join(__dir__, '../')))

from PyQt5 import QtCore, QtWidgets
import mod.image_list_manager as imglistmgr
import mod.utils


class ClassifyUiContext(QtCore.QObject):
    selected = QtCore.pyqtSignal(str) # 选择分类信号
    
    def __init__(self, ui:QtWidgets.QListView, parent:QtWidgets.QMainWindow, 
                image_list_mgr:imglistmgr.ImageListManager):
        super(ClassifyUiContext, self).__init__()
        self.__ui = ui
        self.__parent = parent
        self.__imageListMgr = image_list_mgr
        self.__menu = QtWidgets.QMenu()
        self.__initMenu()
        self.__connectSignal()

    @property
    def ui(self):
        return self.__ui

    @property
    def parent(self):
        return self.__parent

    @property
    def imageListManager(self):
        return self.__imageListMgr

    @property
    def menu(self):
        return self.__menu

    def __connectSignal(self):
        """连接信号"""
        self.__ui.clicked.connect(self.uiClicked)

    def __initMenu(self):
        """初始化分类界面菜单"""
        mod.utils.setMenu(self.__menu, "添加分类", self.addClassify)
        mod.utils.setMenu(self.__menu, "删除分类", self.removeClassify)
        mod.utils.setMenu(self.__menu, "重命名分类", self.renemeClassify)

        self.__ui.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.__ui.customContextMenuRequested.connect(self.__showMenu)

    def __showMenu(self, pos):
        """显示分类界面菜单"""
        self.__menu.exec_(self.__ui.mapToGlobal(pos))

    def setClassifyList(self, classify_list):
        """设置分类列表"""
        list_model = QtCore.QStringListModel(classify_list)
        self.__ui.setModel(list_model)

    def uiClicked(self, index):
        """分类列表点击"""
        txt = index.data()
        self.selected.emit(txt)

    def addClassify(self):
        """添加分类"""
        print("addClassifyBtn.called")

    def removeClassify(self):
        """删除分类"""
        print("removeClassifyBtn.called")

    def renemeClassify(self):
        """重命名分类"""
        print("renemeClassify.called")

    def searchClassify(self):
        """查找分类"""
        print("searchClassify.called")