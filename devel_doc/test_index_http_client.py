#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys

__dir__ = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.abspath(os.path.join(__dir__, '../')))

import mod.index_http_client


def main():
    client = mod.index_http_client.IndexHttpClient("127.0.0.1", 8000)
    # print(client.url())
    client.updateImages("qq.txt", "/home/hmy/11")

if __name__ == '__main__':
    main()