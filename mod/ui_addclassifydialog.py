# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/AddClassifyDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.5
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AddClassifyDialog(object):
    def setupUi(self, AddClassifyDialog):
        AddClassifyDialog.setObjectName("AddClassifyDialog")
        AddClassifyDialog.resize(286, 127)
        AddClassifyDialog.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(AddClassifyDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(AddClassifyDialog)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.lineEdit = QtWidgets.QLineEdit(AddClassifyDialog)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout.addWidget(self.lineEdit)
        spacerItem = QtWidgets.QSpacerItem(20, 11, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.buttonBox = QtWidgets.QDialogButtonBox(AddClassifyDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(AddClassifyDialog)
        self.buttonBox.accepted.connect(AddClassifyDialog.accept)
        self.buttonBox.rejected.connect(AddClassifyDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(AddClassifyDialog)

    def retranslateUi(self, AddClassifyDialog):
        _translate = QtCore.QCoreApplication.translate
        AddClassifyDialog.setWindowTitle(_translate("AddClassifyDialog", "添加分类"))
        self.label.setText(_translate("AddClassifyDialog", "分类名称"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    AddClassifyDialog = QtWidgets.QDialog()
    ui = Ui_AddClassifyDialog()
    ui.setupUi(AddClassifyDialog)
    AddClassifyDialog.show()
    sys.exit(app.exec_())