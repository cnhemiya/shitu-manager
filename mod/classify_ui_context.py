import os
import sys

__dir__ = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.abspath(os.path.join(__dir__, '../')))

from PyQt5 import QtCore, QtWidgets
import mod.image_list_manager as imglistmgr
import mod.utils
import mod.ui_addclassifydialog
import mod.ui_renameclassifydialog


class ClassifyUiContext(QtCore.QObject):
    # 分类界面相关业务
    selected = QtCore.pyqtSignal(str) # 选择分类信号
    
    def __init__(self, ui:QtWidgets.QListView, parent:QtWidgets.QMainWindow, 
                image_list_mgr:imglistmgr.ImageListManager):
        super(ClassifyUiContext, self).__init__()
        self.__ui = ui
        self.__parent = parent
        self.__imageListMgr = image_list_mgr
        self.__menu = QtWidgets.QMenu()
        self.__initMenu()
        self.__initUi()
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

    def __initUi(self):
        """初始化分类界面"""
        self.__ui.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

    def __connectSignal(self):
        """连接信号"""
        self.__ui.clicked.connect(self.uiClicked)
        self.__ui.doubleClicked.connect(self.uiDoubleClicked)

    def __initMenu(self):
        """初始化分类界面菜单"""
        mod.utils.setMenu(self.__menu, "添加分类", self.addClassify)
        mod.utils.setMenu(self.__menu, "移除分类", self.removeClassify)
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
        if not self.__ui.currentIndex().isValid():
            return
        txt = index.data()
        self.selected.emit(txt)

    def uiDoubleClicked(self, index):
        """分类列表双击"""
        if not self.__ui.currentIndex().isValid():
            return
        ole_name = index.data()
        dlg = QtWidgets.QDialog(parent=self.parent)
        ui = mod.ui_renameclassifydialog.Ui_RenameClassifyDialog()
        ui.setupUi(dlg)
        ui.oldNameLineEdit.setText(ole_name)
        result = dlg.exec_()
        new_name = ui.newNameLineEdit.text()
        if result == QtWidgets.QDialog.Accepted:
            mgr_result = self.__imageListMgr.renameClassify(ole_name, new_name)
            if not mgr_result:
                QtWidgets.QMessageBox.warning(self.parent, "重命名分类", "重命名分类错误")
            else:
                self.setClassifyList(self.__imageListMgr.classifyList)

    def addClassify(self):
        """添加分类"""
        dlg = QtWidgets.QDialog(parent=self.parent)
        ui = mod.ui_addclassifydialog.Ui_AddClassifyDialog()
        ui.setupUi(dlg)
        result = dlg.exec_()
        txt = ui.lineEdit.text()
        if result == QtWidgets.QDialog.Accepted:
            mgr_result = self.__imageListMgr.addClassify(txt)
            if not mgr_result:
                QtWidgets.QMessageBox.warning(self.parent, "添加分类", "添加分类错误")
            else:
                self.setClassifyList(self.__imageListMgr.classifyList)

    def removeClassify(self):
        """移除分类"""
        if not self.__ui.currentIndex().isValid():
            return
        classify = self.__ui.currentIndex().data()
        result = QtWidgets.QMessageBox.information(self.parent, "移除分类", 
                "确定移除分类: {}".format(classify),
                buttons=QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel,
                defaultButton=QtWidgets.QMessageBox.Cancel)
        if result == QtWidgets.QMessageBox.Ok:
            if len(self.__imageListMgr.imageList(classify)) > 0:
                QtWidgets.QMessageBox.warning(self.parent, "移除分类", "分类下存在图片，请先移除图片")
            else:
                self.__imageListMgr.removeClassify(classify)
                self.setClassifyList(self.__imageListMgr.classifyList())

    def renemeClassify(self):
        """重命名分类"""
        idx = self.__ui.currentIndex()
        if idx.isValid():
            self.uiDoubleClicked(idx)

    def searchClassify(self, classify):
        """查找分类"""
        self.setClassifyList(self.__imageListMgr.findLikeClassify(classify))
