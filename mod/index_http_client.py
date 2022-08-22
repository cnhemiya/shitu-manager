import os
import sys

__dir__ = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.abspath(os.path.join(__dir__, '../')))

from PyQt5 import QtCore, QtGui, QtWidgets
import requests
import http.client

class IndexHttpClient():
    def __init__(self, host: str, port: int):
        # super(IndexHttpClient, self).__init__()
        self.__host = host
        self.__port = port

    def url(self):
        return "http://{}:{}".format(self.__host, self.__port)

    def new_index(self, image_list_path: str, index_root_path: str, index_method = "HNSW32", force = False):
        """新建库"""
        params = {"image_list_path":image_list_path, \
            "index_root_path":index_root_path, \
            "index_method":index_method, \
            "force":force}
        req = requests.get(self.url() + "/new_index", params=params)
        result = req.json()
        msg = result["error_message"]
        return msg

    def open_index(self, index_root_path: str):
        """打开库"""
        params = {"index_root_path":index_root_path}
        req = requests.get(self.url() + "/open_index", params=params)
        result = req.json()
        msg = result["error_message"]
        return msg

    def update_images(self, image_list_path: str, index_root_path: str):
        """更新库图片"""
        params = {"image_list_path":image_list_path, \
            "index_root_path":index_root_path}
        req = requests.get(self.url() + "/update_images", params=params)
        result = req.json()
        msg = result["error_message"]
        return msg
