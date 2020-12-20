# !/usr/bin/python3
# -*- coding: utf-8 -*-


def array2string(arr, sepitem=',', sepstring='\n'):
    text = ''
    for i in arr:
        col = ''
        for j in i:
            if col == '':
                col = str(j)
            else:
                col += sepitem + str(j)
        if text == '':
            text = col
        else:
            text += sepstring + col
    return text


def linear_array2string(arr, sepitem=','):
    text = ''
    for i in arr:
        if text == '':
            text = str(i)
        else:
            text += sepitem + str(i)
    return text
