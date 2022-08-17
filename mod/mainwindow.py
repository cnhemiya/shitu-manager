import os
import sys

__dir__ = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.abspath(os.path.join(__dir__, '../')))

from PyQt5 import QtCore, QtGui, QtWidgets
import mod.ui_mainwindow
import mod.image_list_manager


TOOL_BTN_ICON_SIZE = 64


class MainWindow(QtWidgets.QMainWindow):
    """主窗口"""

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = mod.ui_mainwindow.Ui_MainWindow()
        self.ui.setupUi(self)  # 初始化主窗口界面
        self.resize(1280, 720)

        self.__appMenu = QtWidgets.QMenu()
        self.__initAppMenu()  # 初始化应用菜单

        self.__initToolBtn()
        self.__connectSignal()
        self.__initImageListViewStyle()
        self.__imageListMgr = mod.image_list_manager.ImageListManager()

    def __initToolBtn(self):
        """初始化工具按钮"""
        self.__setToolButton(self.ui.appMenuBtn, "应用菜单",
                             "./resource/app_menu.png", TOOL_BTN_ICON_SIZE)

        self.__setToolButton(self.ui.saveImageListBtn, "保存图片列表",
                             "./resource/save_image_list.png", TOOL_BTN_ICON_SIZE)
        self.ui.saveImageListBtn.clicked.connect(self.saveImageList)

        self.__setToolButton(self.ui.addClassifyBtn, "添加分类",
                             "./resource/add_classify.png", TOOL_BTN_ICON_SIZE)
        self.ui.addClassifyBtn.clicked.connect(self.addClassify)

        self.__setToolButton(self.ui.removeClassifyBtn, "删除分类",
                             "./resource/remove_classify.png", TOOL_BTN_ICON_SIZE)
        self.ui.removeClassifyBtn.clicked.connect(self.removeClassify)

        self.__setToolButton(self.ui.searchClassifyBtn, "查找分类",
                             "./resource/search_classify.png", TOOL_BTN_ICON_SIZE)
        self.ui.searchClassifyBtn.clicked.connect(self.searchClassify)

        self.__setToolButton(self.ui.addImageBtn, "添加图片",
                             "./resource/add_image.png", TOOL_BTN_ICON_SIZE)
        self.ui.addImageBtn.clicked.connect(self.addImage)

        self.__setToolButton(self.ui.removeImageBtn, "删除图片",
                             "./resource/remove_image.png", TOOL_BTN_ICON_SIZE)
        self.ui.removeImageBtn.clicked.connect(self.removeImage)

        self.__setToolButton(self.ui.zoomOutBtn, "缩小",
                             "./resource/zoom_out.png", TOOL_BTN_ICON_SIZE)
        self.ui.zoomOutBtn.clicked.connect(self.zoomOut)

        self.__setToolButton(self.ui.zoomInBtn, "放大",
                             "./resource/zoom_in.png", TOOL_BTN_ICON_SIZE)
        self.ui.zoomInBtn.clicked.connect(self.zoomIn)

        self.ui.searchClassifyHistoryCmb.setToolTip("查找分类历史")
        self.ui.imageZoomOutInHSlider.setToolTip("图片缩放")

    def __setToolButton(self, button, tool_tip: str, icon_path: str, icon_size: int):
        """设置工具按钮"""
        button.setToolTip(tool_tip)
        button.setIcon(QtGui.QIcon(icon_path))
        button.setIconSize(QtCore.QSize(icon_size, icon_size))

    def saveImageList(self):
        """保存图片列表"""
        print("saveImageListBtn.clicked")

    def addClassify(self):
        """添加分类"""
        print("addClassifyBtn.clicked")

    def removeClassify(self):
        """删除分类"""
        print("removeClassifyBtn.clicked")

    def searchClassify(self):
        """查找分类"""
        print("searchClassifyBtn.clicked")

    def addImage(self):
        """添加图片"""
        print("addImageBtn.clicked")

    def removeImage(self):
        """删除图片"""
        print("removeImageBtn.clicked")

    def zoomOut(self):
        """缩小"""
        print("zoomOutBtn.clicked")

    def zoomIn(self):
        """放大"""
        print("zoomInBtn.clicked")

    def __initAppMenu(self):
        """初始化应用菜单"""
        self.__setAppMenu("打开图片列表", self.openImageList)
        self.__setAppMenu("保存图片列表", self.saveImageList)
        self.__appMenu.addSeparator()
        self.__setAppMenu("新建索引库", self.newIndexLibrary)
        self.__setAppMenu("打开索引库", self.openIndexLibrary)
        self.__setAppMenu("更新索引库", self.updateIndexLibrary)

        self.ui.appMenuBtn.setMenu(self.__appMenu)
        self.ui.appMenuBtn.setPopupMode(QtWidgets.QToolButton.InstantPopup)

    def __setAppMenu(self, text: str, triggered):
        """设置应用菜单"""
        action = self.__appMenu.addAction(text)
        action.triggered.connect(triggered)

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

    def setClassifyListView(self, classify_list):
        """设置分类列表"""
        list_model = QtCore.QStringListModel(classify_list)
        self.ui.classifyListView.setModel(list_model)

    def __initImageListViewStyle(self):
        """初始化图片列表样式"""
        self.ui.imageListWidget.setViewMode(QtWidgets.QListView.IconMode)
        self.ui.imageListWidget.setIconSize(QtCore.QSize(320, 320))
        self.ui.imageListWidget.setSpacing(15)
        self.ui.imageListWidget.setMovement(QtWidgets.QListView.Static)

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
