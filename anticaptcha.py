# !/usr/bin/python3
# -*- coding: utf-8 -*-

from Config_recognizer import Config
from functions.get_random_file import get_random_file
from python_anticaptcha import AnticaptchaClient, ImageToTextTask

api_key = 'baab6d29c827e366193de6983585757f'

captcha_path = get_random_file(Config)

print(captcha_path)
# exit()
#
captcha_fp = open(captcha_path, 'rb')
client = AnticaptchaClient(api_key)
task = ImageToTextTask(fp=captcha_fp, numeric=1)
job = client.createTask(task)
job.join()
SOLUTION = job.get_captcha_text()
print(f"SOLUTION: |{SOLUTION}|")

