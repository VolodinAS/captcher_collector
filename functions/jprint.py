# !/usr/bin/python3
# -*- coding: utf-8 -*-
import json


def jprint(arr, name=''):
    print('---------------------- <json ' + name + '> ----------------------')
    print(json.dumps(arr, indent=4))
    print('---------------------- </json ' + name + '> ----------------------')
    print(' ')
