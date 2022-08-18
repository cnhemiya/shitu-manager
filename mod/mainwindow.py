import os
import sys

__dir__ = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.abspath(os.path.join(__dir__, '../')))

from PyQt5 import QtCore, QtGui, QtWidgets
import mod.ui_mainwindow
import mod.image_list_manager
import mod.classify_ui_context
import mod.image_list_ui_context
import mod.utils


TOOL_BTN_ICON_SIZE = 64


class MainWindow(QtWidgets.QMainWindow):
    """主窗口"""

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = mod.ui_mainwindow.Ui_MainWindow()
        self.ui.setupUi(self)  # 初始化主窗口界面
        self.resize(1280, 720)

        self.__imageListMgr = mod.image_list_manager.ImageListManager()

        self.__appMenu = QtWidgets.QMenu()
        self.__initAppMenu()  # 初始化应用菜单

        # 分类界面相关业务
        self.__classifyUiContext = mod.classify_ui_context.ClassifyUiContext(
                ui=self.ui.classifyListView, parent=self, image_list_mgr=self.__imageListMgr)

        # 图片列表界面相关业务
        self.__imageListUiContext = mod.image_list_ui_context.ImageListUiContext(
                ui=self.ui.imageListWidget, parent=self, image_list_mgr=self.__imageListMgr)

        self.__initToolBtn()
        self.__connectSignal()
        

    def __initToolBtn(self):
        """初始化工具按钮"""
        self.__setToolButton(self.ui.appMenuBtn, "应用菜单",
                             "./resource/app_menu.png", TOOL_BTN_ICON_SIZE)

        self.__setToolButton(self.ui.saveImageListBtn, "保存图片列表",
                             "./resource/save_image_list.png", TOOL_BTN_ICON_SIZE)
        self.ui.saveImageListBtn.clicked.connect(self.saveImageList)

        self.__setToolButton(self.ui.addClassifyBtn, "添加分类",
                             "./resource/add_classify.png", TOOL_BTN_ICON_SIZE)
        self.ui.addClassifyBtn.clicked.connect(self.__classifyUiContext.addClassify)

        self.__setToolButton(self.ui.removeClassifyBtn, "删除分类",
                             "./resource/remove_classify.png", TOOL_BTN_ICON_SIZE)
        self.ui.removeClassifyBtn.clicked.connect(self.__classifyUiContext.removeClassify)

        self.__setToolButton(self.ui.searchClassifyBtn, "查找分类",
                             "./resource/search_classify.png", TOOL_BTN_ICON_SIZE)
        self.ui.searchClassifyBtn.clicked.connect(self.__classifyUiContext.searchClassify)

        self.__setToolButton(self.ui.addImageBtn, "添加图片",
                             "./resource/add_image.png", TOOL_BTN_ICON_SIZE)
        self.ui.addImageBtn.clicked.connect(self.__imageListUiContext.addImage)

        self.__setToolButton(self.ui.removeImageBtn, "删除图片",
                             "./resource/remove_image.png", TOOL_BTN_ICON_SIZE)
        self.ui.removeImageBtn.clicked.connect(self.__imageListUiContext.removeImage)

        self.ui.searchClassifyHistoryCmb.setToolTip("查找分类历史")
        self.ui.imageZoomOutInHSlider.setToolTip("图片缩放")

    def __setToolButton(self, button, tool_tip: str, icon_path: str, icon_size: int):
        """设置工具按钮"""
        button.setToolTip(tool_tip)
        button.setIcon(QtGui.QIcon(icon_path))
        button.setIconSize(QtCore.QSize(icon_size, icon_size))

    def __initAppMenu(self):
        """初始化应用菜单"""
        mod.utils.setMenu(self.__appMenu, "打开图片列表", self.openImageList)
        mod.utils.setMenu(self.__appMenu, "保存图片列表", self.saveImageList)
        self.__appMenu.addSeparator()
        mod.utils.setMenu(self.__appMenu, "新建索引库", self.newIndexLibrary)
        mod.utils.setMenu(self.__appMenu, "打开索引库", self.openIndexLibrary)
        mod.utils.setMenu(self.__appMenu, "更新索引库", self.updateIndexLibrary)

        self.ui.appMenuBtn.setMenu(self.__appMenu)
        self.ui.appMenuBtn.setPopupMode(QtWidgets.QToolButton.InstantPopup)

    def __connectSignal(self):
        """连接信号与槽"""
        self.ui.classifyListView.clicked.connect(self.classifyListViewClicked)

    def openImageList(self):
        """打开图像列表"""
        file_path = QtWidgets.QFileDialog.getOpenFileName()
        print(file_path)
        label_path = file_path[0]
        self.__imageListMgr.readFile(label_path)
        self.setClassifyListView(self.__imageListMgr.classifyList)
        self.__setStatusBar(label_path)

    def newIndexLibrary(self):
        print("newIndexLibraryAction.clicked")

    def openIndexLibrary(self):
        print("openIndexLibraryAction.clicked")

    def updateIndexLibrary(self):
        print("updateIndexLibraryAction.clicked")

    def saveImageList(self):
        """保存图片列表"""
        print("saveImageListBtn.clicked")

    def setClassifyListView(self, classify_list):
        """设置分类列表"""
        list_model = QtCore.QStringListModel(classify_list)
        self.ui.classifyListView.setModel(list_model)

    def setImageListView(self, image_list):
        """设置图片列表"""
        self.ui.imageListWidget.clear()
        for i in image_list:
            item = QtWidgets.QListWidgetItem(self.ui.imageListWidget)
            item.setIcon(QtGui.QIcon(i))
            item.setText(i)
            self.ui.imageListWidget.addItem(item)

    def classifyListViewClicked(self, index):
        """分类列表点击事件"""
        txt = index.data()
        self.setImageListView(self.__imageListMgr.realPathList(txt))

    def __setStatusBar(self, msg: str):
        """设置状态栏信息"""
        self.ui.statusbar.showMessage("文件路径：{}".format(msg))
