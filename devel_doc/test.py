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

def main():
    print(newFile("/home/hmy/999.txt"))

if __name__ == '__main__':
    main()