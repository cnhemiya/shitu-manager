import os
import sys

from PyQt5 import QtCore, QtGui, QtWidgets
import hashlib
import shutil


def setMenu(menu:QtWidgets.QMenu, text: str, triggered):
    """设置菜单"""
    action = menu.addAction(text)
    action.triggered.connect(triggered)

def fileMD5(file_path: str):
    """计算文件的MD5值"""
    md5 = hashlib.md5()
    with open(file_path, 'rb') as f:
        md5.update(f.read())
    return md5.hexdigest()

def copyFile(from_path: str, to_path: str):
    """复制文件"""
    shutil.copyfile(from_path, to_path)
    return os.path.exists(to_path)

def removeFile(file_path: str):
    """删除文件"""
    if os.path.exists(file_path):
        os.remove(file_path)
    return not os.path.exists(file_path)

def fileExtension(file_path: str):
    """获取文件的扩展名"""
    return os.path.splitext(file_path)[1]

def newFile(file_path: str):
    """创建文件"""
    if os.path.exists(file_path):
        return False
    else:
        with open(file_path, 'w') as f:
            pass
        return True

def isEmptyDir(dir_path: str):
    """判断目录是否为空"""
    return not os.listdir(dir_path)

def initLibrary(dir_path: str):
    """初始化库"""
    images_dir = os.path.join(dir_path, "images")
    if not os.path.exists(images_dir):
        os.makedirs(images_dir)
    image_list_path = os.path.join(dir_path, "image_list.txt")
    newFile(image_list_path)
    return os.path.exists(dir_path)
