#!/usr/bin/python3
# -*- coding: utf-8 -*-


import os


class ImageListManager:
    def __init__(self, file_path="", encoding="utf-8"):
        self.__filePath = ""
        self.__dataList = {}
        if file_path != "":
            self.readFile(file_path, encoding)

    @property
    def filePath(self):
        return self.__filePath

    @property
    def dirName(self):
        return os.path.dirname(self.__filePath)

    @property
    def dataList(self):
        return self.__dataList

    @property
    def classifyList(self):
        return self.__dataList.keys()

    def readFile(self, file_path: str, encoding="utf-8"):
        if not os.path.exists(file_path):
            raise Exception("文件不存在：{}".format(file_path))
        self.__filePath = file_path
        self.__readParse(file_path, encoding)

    def __readParse(self, file_path: str, encoding="utf-8"):
        with open(file_path, "r", encoding=encoding) as f:
            for line in f:
                line = line.rstrip("\n")
                data = line.split("\t")
                self.__appendData(data)

    def __appendData(self, data: list):
        if data[1] not in self.__dataList:
            self.__dataList[data[1]] = []
        self.__dataList[data[1]].append(data[0])

    def realPathList(self, classify:str):
        if classify not in self.classifyList:
            return []
        paths = self.__dataList[classify]
        if len(paths) == 0:
            return []
        for i in range(len(paths)):
            paths[i] = os.path.join(self.dirName, paths[i])
        return paths
