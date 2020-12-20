# !/usr/bin/python3
# -*- coding: utf-8 -*-

import random
import os

def get_random_file(_config):
    numbers_dirs = os.listdir(_config.collections_dir)
    random.shuffle(numbers_dirs)
    number_path = _config.collections_dir + '/' + numbers_dirs[0]
    captcha_dirs = os.listdir(number_path)
    random.shuffle(captcha_dirs)
    captcha_name = captcha_dirs[0]
    return str(number_path + '/' + captcha_name)