import os
from stat import filemode
import sys

__dir__ = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.abspath(os.path.join(__dir__, '../')))

from PyQt5 import QtCore, QtGui, QtWidgets
import mod.image_list_manager as imglistmgr
import mod.utils
import mod.ui_renameclassifydialog
import mod.imageeditclassifydialog

# 图像缩放基数
BASE_IMAGE_SIZE = 64


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
        self.__imageScale = 1

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
        if len(self.__imageListMgr.filePath) > 0:
            self.__menu.exec_(self.__ui.mapToGlobal(pos))

    def setImageScale(self, scale:int):
        """设置图片大小"""
        self.__imageScale = scale
        size = QtCore.QSize(scale * BASE_IMAGE_SIZE, scale * BASE_IMAGE_SIZE)
        self.__ui.setIconSize(size)
        for i in range(self.__ui.count()):
            item = self.__ui.item(i)
            item.setSizeHint(size)

    def setImageList(self, classify:str):
        """设置图片列表"""
        size = QtCore.QSize(self.__imageScale * BASE_IMAGE_SIZE, self.__imageScale * BASE_IMAGE_SIZE)
        self.__selectedClassify = classify
        image_list = self.__imageListMgr.imageList(classify)
        self.__ui.clear()
        for i in image_list:
            item = QtWidgets.QListWidgetItem(self.__ui)
            item.setIcon(QtGui.QIcon(self.__imageListMgr.realPath(i)))
            item.setData(QtCore.Qt.UserRole, i)
            item.setSizeHint(size)
            self.__ui.addItem(item)

    def addImage(self):
        """添加图片"""
        filter = "图片 (*.png *.jpg *.jpeg *.PNG *.JPG *.JPEG);;所有文件(*.*)"
        dlg = QtWidgets.QFileDialog(self.__parent)
        dlg.setFileMode(QtWidgets.QFileDialog.ExistingFiles) # 多选文件
        dlg.setViewMode(QtWidgets.QFileDialog.Detail) # 详细模式
        file_paths = dlg.getOpenFileNames(filter=filter)[0]
        if len(file_paths) == 0:
            return
        image_list_dir = self.__imageListMgr.dirName
        file_list = []
        for path in file_paths:
            if not os.path.exists(path):
                continue
            if image_list_dir in path:
                # 去掉 image_list_dir 的路径和斜杠
                begin = len(image_list_dir) + 1
                file_list.append(path[begin:])
        if len(file_list) > 0:
            new_list = self.__imageListMgr.imageList(self.__selectedClassify) + file_list
            self.__imageListMgr.resetImageList(self.__selectedClassify, new_list)
            self.setImageList(self.__selectedClassify)

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
        old_classify = self.__selectedClassify
        dlg = mod.imageeditclassifydialog.ImageEditClassifyDialog(parent=self.__parent,
                        old_classify=old_classify,
                        classify_list=self.__imageListMgr.classifyList)
        result = dlg.exec_()
        new_classify = dlg.newClassify
        if result == QtWidgets.QDialog.Accepted \
                and new_classify != old_classify \
                and new_classify != "":
            self.__moveImage(old_classify, new_classify)

    def __moveImage(self, old_classify, new_classify):
        """移动图片"""
        keep_list = []
        is_selected = False
        move_list = self.__imageListMgr.imageList(new_classify)
        for i in range(self.__ui.count()):
            item = self.__ui.item(i)
            txt = item.data(QtCore.Qt.UserRole)
            if item.isSelected():
                move_list.append(txt)
                is_selected = True
            else:
                keep_list.append(txt)
        if is_selected:
            self.__imageListMgr.resetImageList(new_classify, move_list)
            self.__imageListMgr.resetImageList(old_classify, keep_list)
            self.setImageList(old_classify)

    def selectAllImage(self):
        """选择所有图片"""
        self.__ui.selectAll()

    def cancelSelectImage(self):
        """取消选择图片"""
        self.__ui.clearSelection()
