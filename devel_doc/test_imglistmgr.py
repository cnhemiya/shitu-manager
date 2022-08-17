#!/usr/bin/python3
# -*- coding: utf-8 -*-


import os
import sys

__dir__ = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.abspath(os.path.join(__dir__, '../')))

import mod.image_list_manager as imglistmgr


def main():
    label_path = "/home/hmy/drink_dataset_v1.0/gallery/drink_label.txt"
    parser = imglistmgr.ImageListManager(label_path)
    # parser.reset(label_path)
    # print(parser.classifyList)
    # print(parser.labelList[3])
    print(parser.realPathList('百事可乐'))
    print(parser.filePath)
    print(parser.dirName)


def dict_test():
    img_dict = {}
    img_dict["img_path"] = []
    img_dict["img_path"].append("aa")
    img_dict["img_path"].append("bb")
    img_dict["ffff"] = []
    # img_dict.has_key("img_path")
    print("img_pathss" in img_dict.keys())


if __name__ == '__main__':
    main()
    # dict_test()
