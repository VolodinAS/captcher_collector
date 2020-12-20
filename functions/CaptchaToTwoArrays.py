# !/usr/bin/python3
# -*- coding: utf-8 -*-

from functions.imagelab import image_lab_file
from functions.arrayCutter import arrayCutter
import cv2
import numpy as np
from functions.array2string import array2string, linear_array2string

def CaptchaToTwoArrays(filename):
    complete_array = {
        0: [],
        1: []
    }
    image = image_lab_file(filename=filename)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    se = cv2.getStructuringElement(cv2.MORPH_RECT, (8, 8))
    bg = cv2.morphologyEx(image, cv2.MORPH_DILATE, se)
    out_gray = cv2.divide(image, bg, scale=255)
    out_binary = cv2.threshold(out_gray, 0, 255, cv2.THRESH_OTSU)[1]
    cv2.imwrite('original_captcha_byte.png', out_binary)
    out_binary.tofile('test.txt', ', ')
    Numbers = np.where(out_binary > 1, 0, 1)
    list1 = Numbers.tolist()

    NumbersText = array2string(Numbers)
    f = open('original_captcha_byte.txt', 'w')
    f.write(NumbersText)
    f.close()

    # Транспонирование в одну сторону
    NumbersTransponire = [list(i) for i in zip(*Numbers)]
    NumbersTransponireText = array2string(NumbersTransponire)
    f = open('original_captcha_byte_transponire.txt', 'w')
    f.write(NumbersTransponireText)
    f.close()

    NumberFirst = arrayCutter(NumbersTransponire, good_values=1, in_row=2, summ=2, offset=0)
    text = array2string(NumberFirst['data'])
    f = open('number1_normalize.txt', 'w')
    f.write(text)
    f.close()

    NumberSecond = arrayCutter(NumbersTransponire, good_values=1, in_row=2, summ=2, offset=NumberFirst['index_end'] + 1, debug=1)
    Number_1_Normalize = [list(i) for i in zip(*NumberFirst['data'])]
    # text = array2string(NumberSecond['data'])
    text = array2string(Number_1_Normalize)
    f = open('number2_normalize.txt', 'w')
    f.write(text)
    f.close()

    # Number_1_Normalize = [list(i) for i in zip(*NumberFirst['data'])]
    # NumberFirst = arrayCutter(Number_1_Normalize, good_values=1, in_row=3, summ=3, offset=0)
    # text = array2string(NumberFirst['data'])
    # f = open('number1_normalize.txt', 'w')
    # f.write(text)
    # f.close()

    # Number_2_Normalize = [list(i) for i in zip(*NumberSecond['data'])]
    # NumberSecond = arrayCutter(Number_2_Normalize, good_values=1, in_row=3, summ=3, offset=0)
    # text = array2string(NumberSecond['data'])
    # f = open('number2_normalize.txt', 'w')
    # f.write(text)
    # f.close()

    complete_array[0] = NumberFirst
    complete_array[1] = NumberSecond

    return complete_array
