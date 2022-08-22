import os
import sys

__dir__ = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.abspath(os.path.join(__dir__, '../')))

from PyQt5 import QtCore, QtGui, QtWidgets
import requests


class IndexHttpClient(QtCore.QObject):
    def __init__(self, host: str, port: int):
        super(IndexHttpClient, self).__init__()
        self.__host = host
        self.__port = port

    def url(self):
        return "http://{}:{}".format(self.__host, self.__port)

    def updateImages(self, image_list_path: str, index_root_path: str):
        params = {"image_list_path":image_list_path, \
            "index_root_path":index_root_path}
        req = requests.get(self.url(), params=params)