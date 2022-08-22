# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/ImageEditClassifyDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.5
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(414, 415)
        Dialog.setMinimumSize(QtCore.QSize(0, 0))
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.oldLineEdit = QtWidgets.QLineEdit(Dialog)
        self.oldLineEdit.setEnabled(False)
        self.oldLineEdit.setObjectName("oldLineEdit")
        self.verticalLayout.addWidget(self.oldLineEdit)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.newLineEdit = QtWidgets.QLineEdit(Dialog)
        self.newLineEdit.setEnabled(False)
        self.newLineEdit.setObjectName("newLineEdit")
        self.verticalLayout.addWidget(self.newLineEdit)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.searchWordLineEdit = QtWidgets.QLineEdit(Dialog)
        self.searchWordLineEdit.setObjectName("searchWordLineEdit")
        self.horizontalLayout.addWidget(self.searchWordLineEdit)
        self.searchButton = QtWidgets.QPushButton(Dialog)
        self.searchButton.setObjectName("searchButton")
        self.horizontalLayout.addWidget(self.searchButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.classifyListView = QtWidgets.QListView(Dialog)
        self.classifyListView.setEnabled(True)
        self.classifyListView.setMinimumSize(QtCore.QSize(400, 200))
        self.classifyListView.setObjectName("classifyListView")
        self.verticalLayout.addWidget(self.classifyListView)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "编辑图像分类"))
        self.label.setText(_translate("Dialog", "原分类"))
        self.label_2.setText(_translate("Dialog", "新分类"))
        self.searchButton.setText(_translate("Dialog", "查找"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())