import os
import sys

from devel_doc.test import isEmptyDir

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
        self.__initUI()

    def __initUI(self):
        """初始化界面"""
        # 初始化分割窗口
        self.ui.splitter.setStretchFactor(0, 20)
        self.ui.splitter.setStretchFactor(1, 80)

        # 初始化图像缩放
        self.ui.imageScaleSlider.setValue(4)


    def __initToolBtn(self):
        """初始化工具按钮"""
        self.__setToolButton(self.ui.appMenuBtn, "应用菜单",
                             "./resource/app_menu.png", TOOL_BTN_ICON_SIZE)

        self.__setToolButton(self.ui.saveImageLibraryBtn, "保存图像库",
                             "./resource/save_image_Library.png", TOOL_BTN_ICON_SIZE)
        self.ui.saveImageLibraryBtn.clicked.connect(self.saveImageLibrary)

        self.__setToolButton(self.ui.addClassifyBtn, "添加分类",
                             "./resource/add_classify.png", TOOL_BTN_ICON_SIZE)
        self.ui.addClassifyBtn.clicked.connect(self.__classifyUiContext.addClassify)

        self.__setToolButton(self.ui.removeClassifyBtn, "移除分类",
                             "./resource/remove_classify.png", TOOL_BTN_ICON_SIZE)
        self.ui.removeClassifyBtn.clicked.connect(self.__classifyUiContext.removeClassify)

        self.__setToolButton(self.ui.searchClassifyBtn, "查找分类",
                             "./resource/search_classify.png", TOOL_BTN_ICON_SIZE)
        self.ui.searchClassifyBtn.clicked.connect(self.__classifyUiContext.searchClassify)

        self.__setToolButton(self.ui.addImageBtn, "添加图片",
                             "./resource/add_image.png", TOOL_BTN_ICON_SIZE)
        self.ui.addImageBtn.clicked.connect(self.__imageListUiContext.addImage)

        self.__setToolButton(self.ui.removeImageBtn, "移除图片",
                             "./resource/remove_image.png", TOOL_BTN_ICON_SIZE)
        self.ui.removeImageBtn.clicked.connect(self.__imageListUiContext.removeImage)

        self.ui.searchClassifyHistoryCmb.setToolTip("查找分类历史")
        self.ui.imageScaleSlider.setToolTip("图片缩放")

    def __setToolButton(self, button, tool_tip: str, icon_path: str, icon_size: int):
        """设置工具按钮"""
        button.setToolTip(tool_tip)
        button.setIcon(QtGui.QIcon(icon_path))
        button.setIconSize(QtCore.QSize(icon_size, icon_size))

    def __initAppMenu(self):
        """初始化应用菜单"""
        mod.utils.setMenu(self.__appMenu, "新建图像库", self.newImageLibrary)
        mod.utils.setMenu(self.__appMenu, "打开图像库", self.openImageLibrary)
        mod.utils.setMenu(self.__appMenu, "保存图像库", self.saveImageLibrary)
        self.__appMenu.addSeparator()
        mod.utils.setMenu(self.__appMenu, "新建索引库", self.newIndexLibrary)
        mod.utils.setMenu(self.__appMenu, "打开索引库", self.openIndexLibrary)
        mod.utils.setMenu(self.__appMenu, "更新索引库", self.updateIndexLibrary)
        self.__appMenu.addSeparator()
        mod.utils.setMenu(self.__appMenu, "退出", self.exitApp)

        self.ui.appMenuBtn.setMenu(self.__appMenu)
        self.ui.appMenuBtn.setPopupMode(QtWidgets.QToolButton.InstantPopup)

    def __connectSignal(self):
        """连接信号与槽"""
        self.__classifyUiContext.selected.connect(self.__imageListUiContext.setImageList)
        self.ui.searchClassifyBtn.clicked.connect(self.searchClassify)
        self.ui.imageScaleSlider.valueChanged.connect(self.__imageListUiContext.setImageScale)

    def newImageLibrary(self):
        """新建图像库"""
        dir_path = self.__openDirDialog("新建图像库")
        if dir_path != None:
            if not mod.utils.isEmptyDir(dir_path):
                QtWidgets.QMessageBox.warning(self, "警告", "该目录不为空，请选择空目录")
                return
            if not mod.utils.initLibrary(dir_path):
                QtWidgets.QMessageBox.warning(self, "警告", "新建图像库失败")
                return
            self.__imageListMgr.readFile(os.path.join(dir_path, "image_list.txt"))

    def __openDirDialog(self, title: str):
        """打开目录对话框"""
        dlg = QtWidgets.QFileDialog(self)
        dlg.setWindowTitle(title)
        dlg.setOption(QtWidgets.QFileDialog.ShowDirsOnly, True)
        dlg.setFileMode(QtWidgets.QFileDialog.Directory)
        dlg.setAcceptMode(QtWidgets.QFileDialog.AcceptOpen)
        if dlg.exec_() == QtWidgets.QDialog.Accepted:
            dir_path = dlg.selectedFiles()[0]
            return dir_path
        return None

    def openImageLibrary(self):
        """打开图像库"""
        dir_path = self.__openDirDialog("打开图像库")
        image_list_file = os.path.join(dir_path, "image_list.txt")
        if dir_path != None:
            if os.path.exists(image_list_file) \
                and os.path.exists(os.path.join(dir_path, "images")):
                self.__imageListMgr.readFile(image_list_file)
                self.__classifyUiContext.setClassifyList(self.__imageListMgr.classifyList)
                self.__setStatusBar(image_list_file)

    def saveImageLibrary(self):
        """保存图像库"""
        if os.path.exists(self.__imageListMgr.filePath):
            self.__imageListMgr.writeFile()
            self.__setStatusBar(self.__imageListMgr.filePath)

    def newIndexLibrary(self):
        print("newIndexLibraryAction.clicked")

    def openIndexLibrary(self):
        print("openIndexLibraryAction.clicked")

    def updateIndexLibrary(self):
        print("updateIndexLibraryAction.clicked")

    def searchClassify(self):
        """查找分类"""
        cmb = self.ui.searchClassifyHistoryCmb
        txt = cmb.currentText()
        is_has = False
        if txt != "":
            for i in range(cmb.count()):
                if cmb.itemText(i) == txt:
                    is_has = True
                    break
            if not is_has:
                cmb.addItem(txt)
        self.__classifyUiContext.searchClassify(txt)

    def exitApp(self):
        """退出应用"""
        os._exit(0)
        
    def __setStatusBar(self, msg: str):
        """设置状态栏信息"""
        self.ui.statusbar.showMessage("文件路径：{}".format(msg))
