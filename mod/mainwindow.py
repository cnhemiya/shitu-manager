from PyQt5 import QtCore, QtGui, QtWidgets
import mod.ui_mainwindow
import mod.labelparse


TOOL_BTN_ICON_SIZE = 64


class MainWindow(QtWidgets.QMainWindow):
    """主窗口"""
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = mod.ui_mainwindow.Ui_MainWindow()
        self.ui.setupUi(self) # 初始化主窗口界面
        self.resize(1280, 720)
        # self.__setIcon()
        self.__connectSignal()
        self.__initImageListViewStyle()
        self.__labelParser = mod.labelparse.LabelParse()

    def __setIcon(self):
        """设置工具按钮图标"""
        # self.ui.addBtn.setIcon(QtGui.QIcon("./resource/add.png"))
        # self.ui.addBtn.setIconSize(QtCore.QSize(
        #     TOOL_BTN_ICON_SIZE, TOOL_BTN_ICON_SIZE))
        # self.ui.openBtn.setIcon(QtGui.QIcon("./resource/open.png"))
        # self.ui.openBtn.setIconSize(QtCore.QSize(
        #     TOOL_BTN_ICON_SIZE, TOOL_BTN_ICON_SIZE))
        # self.ui.searchBtn.setIcon(QtGui.QIcon("./resource/search.png"))
        # self.ui.searchBtn.setIconSize(QtCore.QSize(
        #     TOOL_BTN_ICON_SIZE, TOOL_BTN_ICON_SIZE))
        # self.ui.setBtn.setIcon(QtGui.QIcon("./resource/setting.png"))
        # self.ui.setBtn.setIconSize(QtCore.QSize(
        #     TOOL_BTN_ICON_SIZE, TOOL_BTN_ICON_SIZE))

    def __connectSignal(self):
        """连接信号与槽"""
        # self.ui.addBtn.clicked.connect(self.addClassify)
        # self.ui.openBtn.clicked.connect(self.openLibrary)
        # self.ui.searchBtn.clicked.connect(self.searchClassify)
        # self.ui.setBtn.clicked.connect(self.setDialog)
        self.ui.classifyListView.clicked.connect(self.classifyListViewClicked)

    def addClassify(self):
        print("addBtn.clicked")

    def openLibrary(self):
        """打开库文件"""
        file_path = QtWidgets.QFileDialog.getOpenFileName()
        print(file_path)
        label_path = file_path[0]
        self.__labelParser.readFile(label_path)
        self.setClassifyListView(self.__labelParser.classifyList)
        self.__setStatusBar(label_path)

    def searchClassify(self):
        print("searchBtn.clicked")

    def setDialog(self):
        print("setBtn.clicked")

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
        self.setImageListView(self.__labelParser.realPathList(txt))

    def __setStatusBar(self, msg:str):
        """设置状态栏信息"""
        self.ui.statusbar.showMessage("文件路径：{}".format(msg))
