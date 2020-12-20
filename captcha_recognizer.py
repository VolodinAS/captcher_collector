# !/usr/bin/python3
# -*- coding: utf-8 -*-

from Config_recognizer import Config
from functions.jprint import jprint
from functions.get_random_file import get_random_file
from classes.CoolFilePathParser import CFPP
from functions.CaptchaToTwoArrays import CaptchaToTwoArrays
from functions.array2string import array2string, linear_array2string

captcha_path = ''

deffect_captcha = [
    'images/collection/77/captcha94_51.jpg',  # 0
    'images/collection/51/captcha86_32.jpg',  # 1
    'images/collection/10/captcha12_62.jpg',  # 2
    'images/collection/87/captcha22_87.jpg',  # 3
    'images/collection/23/captcha18_235.jpg',  # 4
]

if __name__ == '__main__':

    maxWidth = 0
    maxHeight = 0

    for i in range(2000):
        # captcha_path = get_random_file(Config)
        captcha_path = deffect_captcha[4]
        print(f"path={captcha_path}, MAX_WIDTH={maxWidth}, MAX_HEIGHT={maxHeight}")

        # print('captcha_path:', captcha_path)
        # jprint(captcha_path, 'captcha_path')
        # cfpp = CFPP(captcha_path)
        # CaptchaFileData = cfpp.get_cleanData
        # jprint(CaptchaFileData, 'CaptchaFileData')

        Data = CaptchaToTwoArrays(captcha_path)

        fn = Data[0]['data']
        sn = Data[1]['data']

        # print(fn)
        # print(sn)

        rows = len(fn[0])
        cols = len(fn)

        if rows > maxWidth:
            maxWidth = rows
        if cols > maxHeight:
            maxHeight = cols

        rows = len(sn[0])
        cols = len(sn)

        if rows > maxWidth:
            maxWidth = rows
        if cols > maxHeight:
            maxHeight = cols

        # print(fn)
        # print(sn)

        break

    # NumberFirst = Data[0]
    # text = array2string(NumberFirst['data'], sepitem='')
    # f = open('number1_normalize.txt', 'w')
    # f.write(text)
    # f.close()
    #
    # NumberSecond = Data[1]
    # text = array2string(NumberSecond['data'], sepitem='')
    # f = open('number2_normalize.txt', 'w')
    # f.write(text)
    # f.close()
    #
    # print('IM DONE')
