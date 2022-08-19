import os
import sys

__dir__ = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.abspath(os.path.join(__dir__, '../')))

from PyQt5 import QtCore, QtGui, QtWidgets
import mod.image_list_manager as imglistmgr
import mod.utils


class ImageListUiContext(QtCore.QObject):
    # 图片列表界面相关业务
    def __init__(self, ui:QtWidgets.QListWidget, parent:QtWidgets.QMainWindow, 
                image_list_mgr:imglistmgr.ImageListManager):
        super(ImageListUiContext, self).__init__()
        self.__ui = ui
        self.__parent = parent
        self.__imageListMgr = image_list_mgr
        self.__initUi()
        self.__menu = QtWidgets.QMenu()
        self.__initMenu()
        self.__selectedClassify = ""

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

    def __initUi(self):
        """初始化图片列表样式"""
        self.__ui.setViewMode(QtWidgets.QListView.IconMode)
        self.__ui.setIconSize(QtCore.QSize(320, 320))
        self.__ui.setSpacing(15)
        self.__ui.setMovement(QtWidgets.QListView.Static)
        self.__ui.setSelectionMode(QtWidgets.QAbstractItemView.ContiguousSelection)

    def __initMenu(self):
        """初始化图片列表界面菜单"""
        mod.utils.setMenu(self.__menu, "添加图片", self.addImage)
        mod.utils.setMenu(self.__menu, "移除图片", self.removeImage)
        mod.utils.setMenu(self.__menu, "编辑图片分类", self.editImageClassify)
        self.__menu.addSeparator()
        mod.utils.setMenu(self.__menu, "选择全部图片", self.selectAllImage)
        mod.utils.setMenu(self.__menu, "取消选择图片", self.cancelSelectImage)

        self.__ui.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.__ui.customContextMenuRequested.connect(self.__showMenu)

    def __showMenu(self, pos):
        """显示图片列表界面菜单"""
        self.__menu.exec_(self.__ui.mapToGlobal(pos))

    def setImageList(self, classify:str):
        """设置图片列表"""
        self.__selectedClassify = classify
        image_list = self.__imageListMgr.imageList(classify)
        self.__ui.clear()
        for i in image_list:
            item = QtWidgets.QListWidgetItem(self.__ui)
            item.setIcon(QtGui.QIcon(self.__imageListMgr.realPath(i)))
            item.setData(QtCore.Qt.UserRole, i)
            self.__ui.addItem(item)

    def addImage(self):
        """添加图片"""
        print("addImage.clicked")

    def removeImage(self):
        """移除图片"""
        path_list = []
        image_list = self.__ui.selectedItems()
        if len(image_list) == 0:
            return
        for i in range(self.__ui.count()):
            item = self.__ui.item(i)
            if not item.isSelected():
                path_list.append(item.data(QtCore.Qt.UserRole))
        self.__imageListMgr.resetImageList(self.__selectedClassify, path_list)
        self.setImageList(self.__selectedClassify)

    def editImageClassify(self):
        """编辑图片分类"""
        print("editImageClassify.called")

    def selectAllImage(self):
        """选择所有图片"""
        self.__ui.selectAll()

    def cancelSelectImage(self):
        """取消选择图片"""
        self.__ui.clearSelection()
