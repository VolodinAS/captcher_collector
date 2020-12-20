# !/usr/bin/python3
# -*- coding: utf-8 -*-


import pickle
import os
import requests.cookies


def save_cookies(requests_cookiejar, filename):
    with open(filename, 'wb') as f:
        pickle.dump(requests_cookiejar, f)


def load_cookies(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)


def save_cookies2(session, filename):
    if not os.path.isdir(os.path.dirname(filename)):
        return False
    with open(filename, 'wb') as f:
        f.truncate()
        pickle.dump(session.cookies._cookies, f)
    print('IMHEREWRITE')


def load_cookies2(session, filename):
    if not os.path.isfile(filename):
        return False

    with open(filename, 'rb') as f:
        cookies = pickle.load(f)
        if cookies:
            jar = requests.cookies.RequestsCookieJar()
            jar._cookies = cookies
            session.cookies = jar
        else:
            return False
