import os
import sys
import socket

__dir__ = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.abspath(os.path.join(__dir__, '../')))

from PyQt5 import QtCore, QtGui, QtWidgets
import mod.ui_mainwindow
import mod.image_list_manager
import mod.classify_ui_context
import mod.image_list_ui_context
import mod.ui_newlibrarydialog
import mod.index_http_client
import mod.utils


TOOL_BTN_ICON_SIZE = 64

# try:
#     DEFAULT_HOST = socket.gethostbyname(socket.gethostname())
# except:
#     DEFAULT_HOST = '127.0.0.1'

DEFAULT_HOST = "localhost" 
DEFAULT_PORT = 8000
PADDLECLAS_DOC_URL = "https://gitee.com/paddlepaddle/PaddleClas"


class MainWindow(QtWidgets.QMainWindow):
    """主窗口"""

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = mod.ui_mainwindow.Ui_MainWindow()
        self.ui.setupUi(self)  # 初始化主窗口界面

        self.__imageListMgr = mod.image_list_manager.ImageListManager()

        self.__appMenu = QtWidgets.QMenu() # 应用菜单
        self.__libraryAppendMenu = QtWidgets.QMenu() # 图像库附加功能菜单
        self.__initAppMenu()  # 初始化应用菜单

        self.__pathBar = QtWidgets.QLabel(self) # 路径
        self.__classifyCountBar = QtWidgets.QLabel(self) # 分类数量
        self.__imageCountBar = QtWidgets.QLabel(self) # 图像列表数量
        self.__imageSelectedBar = QtWidgets.QLabel(self) # 图像列表选择数量
        self.__spaceBar1 = QtWidgets.QLabel(self) # 空格间隔栏
        self.__spaceBar2 = QtWidgets.QLabel(self) # 空格间隔栏
        self.__spaceBar3 = QtWidgets.QLabel(self) # 空格间隔栏

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

        # 状态栏界面设置
        space_bar = "                " # 间隔16空格
        self.__spaceBar1.setText(space_bar)
        self.__spaceBar2.setText(space_bar)
        self.__spaceBar3.setText(space_bar)
        self.ui.statusbar.addWidget(self.__pathBar)
        self.ui.statusbar.addWidget(self.__spaceBar1)
        self.ui.statusbar.addWidget(self.__classifyCountBar)
        self.ui.statusbar.addWidget(self.__spaceBar2)
        self.ui.statusbar.addWidget(self.__imageCountBar)
        self.ui.statusbar.addWidget(self.__spaceBar3)
        self.ui.statusbar.addWidget(self.__imageSelectedBar)


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
        
        self.__libraryAppendMenu.setTitle("图像库附加功能")
        mod.utils.setMenu(self.__libraryAppendMenu, "导入到当前图像库", self.importImageLibrary)
        self.__appMenu.addMenu(self.__libraryAppendMenu)

        self.__appMenu.addSeparator()
        mod.utils.setMenu(self.__appMenu, "新建/重建 索引库", self.newIndexLibrary)
        # mod.utils.setMenu(self.__appMenu, "打开索引库", self.openIndexLibrary)
        mod.utils.setMenu(self.__appMenu, "更新索引库", self.updateIndexLibrary)
        self.__appMenu.addSeparator()
        mod.utils.setMenu(self.__appMenu, "帮助", self.showHelp)
        mod.utils.setMenu(self.__appMenu, "关于", self.showAbout)
        mod.utils.setMenu(self.__appMenu, "退出", self.exitApp)

        self.ui.appMenuBtn.setMenu(self.__appMenu)
        self.ui.appMenuBtn.setPopupMode(QtWidgets.QToolButton.InstantPopup)

    def __connectSignal(self):
        """连接信号与槽"""
        self.__classifyUiContext.selected.connect(self.__imageListUiContext.setImageList)
        self.ui.searchClassifyBtn.clicked.connect(self.searchClassify)
        self.ui.imageScaleSlider.valueChanged.connect(self.__imageListUiContext.setImageScale)
        self.__imageListUiContext.listCount.connect(self.__setImageCountBar)
        self.__imageListUiContext.selectedCount.connect(self.__setImageSelectedCountBar)

    def newImageLibrary(self):
        """新建图像库"""
        dir_path = self.__openDirDialog("新建图像库")
        if dir_path != None:
            if not mod.utils.isEmptyDir(dir_path):
                QtWidgets.QMessageBox.warning(self, "错误", "该目录不为空，请选择空目录")
                return
            if not mod.utils.initLibrary(dir_path):
                QtWidgets.QMessageBox.warning(self, "错误", "新建图像库失败")
                return
            self.__reload(os.path.join(dir_path, "image_list.txt"), dir_path)

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
        if dir_path != None:
            image_list_path = os.path.join(dir_path, "image_list.txt")
            if os.path.exists(image_list_path) \
                and os.path.exists(os.path.join(dir_path, "images")):
                self.__reload(image_list_path, dir_path)

    def __reload(self, image_list_path: str, msg: str):
        """重新加载图像库"""
        self.__imageListMgr.readFile(image_list_path)
        self.__imageListUiContext.clear()
        self.__classifyUiContext.setClassifyList(self.__imageListMgr.classifyList)
        self.__setPathBar(msg)
        self.__setClassifyCountBar(len(self.__imageListMgr.classifyList))
        self.__setImageCountBar(0)
        self.__setImageSelectedCountBar(0)

    def saveImageLibrary(self):
        """保存图像库"""
        if not os.path.exists(self.__imageListMgr.filePath):
            QtWidgets.QMessageBox.warning(self, "错误", "请先打开正确的图像库")
            return
        self.__imageListMgr.writeFile()
        self.__reload(self.__imageListMgr.filePath, self.__imageListMgr.dirName)
        hint_str = "为保证图片准确识别，请在修改图片库后更新索引。\n\
如果是新建图像库或者没有索引库，请新建索引。"
        QtWidgets.QMessageBox.information(self, "提示", hint_str)

    def importImageLibrary(self):
        """从其它图像库导入到当前图像库，建议当前库是新建的空库"""
        if not os.path.exists(self.__imageListMgr.filePath):
            QtWidgets.QMessageBox.information(self, "提示", "请先打开正确的图像库")
            return 
        from_path = QtWidgets.QFileDialog.getOpenFileName(caption="导入图像库", filter="txt (*.txt)")[0]
        from_mgr = mod.image_list_manager.ImageListManager(from_path)
        count = mod.utils.oneKeyImport(from_mgr.filePath, self.__imageListMgr.filePath)
        if count == None:
            QtWidgets.QMessageBox.warning(self, "错误", "导入到当前图像库错误")
            return
        QtWidgets.QMessageBox.information(self, "提示", "导入图像库成功，导入图像：{}".format(count))
        self.__reload(self.__imageListMgr.filePath, self.__imageListMgr.dirName)

    def newIndexLibrary(self):
        """新建重建索引库"""
        if not os.path.exists(self.__imageListMgr.filePath):
            QtWidgets.QMessageBox.information(self, "提示", "请先打开正确的图像库")
            return
        dlg = QtWidgets.QDialog(self)
        ui = mod.ui_newlibrarydialog.Ui_NewlibraryDialog()
        ui.setupUi(dlg)
        result = dlg.exec_()
        index_method = ui.indexMethodCmb.currentText()
        force = ui.resetCheckBox.isChecked()
        if result == QtWidgets.QDialog.Accepted:
            try:
                client = mod.index_http_client.IndexHttpClient(DEFAULT_HOST, DEFAULT_PORT)
                err_msg = client.new_index(image_list_path="image_list.txt", 
                        index_root_path=self.__imageListMgr.dirName, 
                        index_method=index_method, 
                        force=force)
                if err_msg == None:
                    QtWidgets.QMessageBox.information(self, "提示", "新建/重建 索引库成功")
                    return
                else:
                    QtWidgets.QMessageBox.warning(self, "错误", err_msg)
                    return
            except Exception as e:
                QtWidgets.QMessageBox.warning(self, "错误", str(e))
                return

    # def openIndexLibrary(self):
    #     """打开索引库"""
    #     if not os.path.exists(self.__imageListMgr.filePath):
    #         QtWidgets.QMessageBox.information(self, "提示", "请先打开正确的图像库")
    #         return
    #     try:
    #         client = mod.index_http_client.IndexHttpClient(DEFAULT_HOST, DEFAULT_PORT)
    #         err_msg = client.open_index(index_root_path=self.__imageListMgr.dirName,
    #                 image_list_path="image_list.txt")
    #         if err_msg == None:
    #             QtWidgets.QMessageBox.information(self, "提示", "打开索引库成功")
    #             return
    #         else:
    #             QtWidgets.QMessageBox.warning(self, "错误", err_msg)
    #             return
    #     except Exception as e:
    #         QtWidgets.QMessageBox.warning(self, "错误", str(e))
    #         return    

    def updateIndexLibrary(self):
        """更新索引库"""
        if not os.path.exists(self.__imageListMgr.filePath):
            QtWidgets.QMessageBox.information(self, "提示", "请先打开正确的图像库")
            return
        try:
            client = mod.index_http_client.IndexHttpClient(DEFAULT_HOST, DEFAULT_PORT)
            err_msg = client.update_index(image_list_path="image_list.txt",
                        index_root_path=self.__imageListMgr.dirName)
            if err_msg == None:
                QtWidgets.QMessageBox.information(self, "提示", "更新索引库成功")
                return
            else:
                QtWidgets.QMessageBox.warning(self, "错误", err_msg)
                return
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "错误", str(e))
            return   

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

    def showHelp(self):
        """显示帮助"""
        QtGui.QDesktopServices.openUrl(QtCore.QUrl(PADDLECLAS_DOC_URL))

    def showAbout(self):
        """显示关于对话框"""
        QtWidgets.QMessageBox.information(self, "关于", "识图图像库管理 V1.0.0")

    def exitApp(self):
        """退出应用"""
        sys.exit(0)
        
    def __setPathBar(self, msg: str):
        """设置路径状态栏信息"""
        self.__pathBar.setText("图像库路径：{}".format(msg))

    def __setClassifyCountBar(self, msg: str):
        self.__classifyCountBar.setText("分类总数量：{}".format(msg))

    def __setImageCountBar(self, count: int):
        """设置图像数量状态栏信息"""
        self.__imageCountBar.setText("当前图像数量：{}".format(count))

    def __setImageSelectedCountBar(self, count: int):
        """设置选择图像数量状态栏信息"""
        self.__imageSelectedBar.setText("选择图像数量：{}".format(count))
