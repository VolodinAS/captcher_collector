# !/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import json


class CFPP(object):

    def __init__(self, path_string):
        """
        Инициализация класса
        :param path_string: Путь до файла
        :type path_string: str
        :return: Массив с данными
        :rtype: dict
        """
        self.ps = path_string

        # print('self.ps:', self.ps)
        self.arr = str(self.ps).split('/')
        # print('self.arr:', self.arr)
        self.pathFile = os.path.dirname(self.ps)
        # print('self.pathFile:', self.pathFile)
        self.fullname = self.arr[-1]
        # print('self.fullname:', self.fullname)
        self.ext_arr = str(self.fullname).split('.')
        # print('self.ext_arr:', self.ext_arr)
        self.filename = self.ext_arr[0]
        # print('self.filename:', self.filename)
        self.ext = self.ext_arr[1]
        # print('self.ext:', self.ext)

        self.cleanData = {
            'path_string': self.ps,
            'pathFile': self.pathFile,
            'fullName': self.fullname,
            'fileName': self.filename,
            'fileExt': self.ext,
        }

    def __str__(self):
        return json.dumps(self.cleanData, indent=4)

    @property
    def get_pathFile(self):
        return self.path_file

    @property
    def get_simpleData(self):
        return self.arr

    @property
    def get_fullname(self):
        return self.fullname

    @property
    def get_filename(self):
        return self.filename

    @property
    def get_fileExt(self):
        return self.ext

    @property
    def get_cleanData(self):
        return self.cleanData
