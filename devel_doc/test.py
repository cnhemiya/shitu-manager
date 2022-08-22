#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys

__dir__ = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.abspath(os.path.join(__dir__, '../')))

import hashlib
import shutil


def fileMD5(file_path: str):
    md5 = hashlib.md5()
    with open(file_path, 'rb') as f:
        md5.update(f.read())
    return md5.hexdigest()

def copyFile(from_path: str, to_path: str):
    shutil.copyfile(from_path, to_path)
    return os.path.exists(to_path)

def removeFile(file_path: str):
    if os.path.exists(file_path):
        os.remove(file_path)
    return not os.path.exists(file_path)

def fileExtension(file_path: str):
    return os.path.splitext(file_path)[1]

def newFile(file_path: str):
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

def main():
    print(initLibrary("/home/hmy/zz_st_img/test"))

if __name__ == '__main__':
    main()