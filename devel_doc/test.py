#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys

__dir__ = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.abspath(os.path.join(__dir__, '../')))

import urllib.parse
import mod.utils
import mod.image_list_manager

def url_decode():
    # url 转码
    ss = """image_list_path=image_list.txt&index_root_path=%2Fhome%2Fuser_home%2Ftest_lib&index_method=HNSW32&force=True"""
    print(urllib.parse.parse_qs(ss))

def main():
    url_decode()

if __name__ == '__main__':
    main()