#!/usr/bin/python3
# -*- coding: utf-8 -*-


from asyncore import file_dispatcher
import os
import sys

__dir__ = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.abspath(os.path.join(__dir__, '../')))

import mod.image_list_manager as imglistmgr


def main():
    file_path = os.path.join(os.environ["HOME"], "drink_dataset_v1.0/gallery/drink_label_222.txt")
    mgr = imglistmgr.ImageListManager(file_path)
    print(mgr.findLikeClassify("伊利"))
    # mgr.renameClassify("红牛", "红牛_222")
    # mgr.writeFile()

if __name__ == '__main__':
    main()
