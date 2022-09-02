import os
import sys

__dir__ = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.abspath(os.path.join(__dir__, '../')))

from PyQt5 import QtCore, QtGui, QtWidgets
import hashlib
import shutil
import mod.image_list_manager


def setMenu(menu:QtWidgets.QMenu, text: str, triggered):
    """设置菜单"""
    action = menu.addAction(text)
    action.triggered.connect(triggered)

def fileMD5(file_path: str):
    """计算文件的MD5值"""
    md5 = hashlib.md5()
    with open(file_path, 'rb') as f:
        md5.update(f.read())
    return md5.hexdigest().lower()

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

def copyImageToDir(self, from_image_path: str, to_dir_path: str):
    """复制图像文件到目标目录"""
    if not os.path.exists(from_image_path) and not os.path.exists(to_dir_path):
        return None
    md5 = fileMD5(from_image_path)
    file_ext = fileExtension(from_image_path)
    new_path = os.path.join(to_dir_path, md5 + file_ext)
    copyFile(from_image_path, new_path)
    return new_path

def oneKeyImportFromFile(from_path: str, to_path: str):
    """从其它图像库 from_path {image_list.txt} 导入到图像库 to_path {image_list.txt}"""
    if not os.path.exists(from_path) or not os.path.exists(to_path):
        return None
    if from_path == to_path:
        return None
    from_mgr = mod.image_list_manager.ImageListManager(file_path=from_path)
    to_mgr = mod.image_list_manager.ImageListManager(file_path=to_path)
    count = 0
    for classify in from_mgr.classifyList:
        img_list = from_mgr.realPathList(classify)
        to_mgr.addClassify(classify)
        to_img_list = to_mgr.imageList(classify)
        new_img_list = []
        for img in img_list:
            from_image_path = img
            to_dir_path = os.path.join(to_mgr.dirName, "images")
            md5 = fileMD5(from_image_path)
            file_ext = fileExtension(from_image_path)
            new_path = os.path.join(to_dir_path, md5 + file_ext)
            if os.path.exists(new_path):
                # 如果新文件 MD5 重复跳过后面的复制文件操作
                continue
            copyFile(from_image_path, new_path)
            new_img_list.append("images/" + md5 + file_ext)
            count += 1
        to_img_list += new_img_list
        to_mgr.resetImageList(classify, to_img_list)
    to_mgr.writeFile()
    return count

def oneKeyImportFromDirs(from_dirs: str, to_image_list_path: str):
    if not os.path.exists(from_dirs) or not os.path.exists(to_image_list_path):
        return None
    if from_dirs == os.path.dirname(to_image_list_path):
        return None

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
