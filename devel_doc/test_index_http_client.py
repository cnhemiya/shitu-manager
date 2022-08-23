#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys

__dir__ = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.abspath(os.path.join(__dir__, '../')))

import mod.index_http_client


def main():
    client = mod.index_http_client.IndexHttpClient("localhost", 8000)
    # print(client.url())
    # client.update_images("image_list.txt", "/home/user_home/test_lib")
    # client.open_index("/home/user_home/test_lib")
    client.new_index("image_list.txt", "/home/user_home/test_lib", "HNSW32", True)

if __name__ == '__main__':
    main()