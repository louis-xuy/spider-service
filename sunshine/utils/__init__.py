#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Time    : 2018/7/26 0:06

<<<<<<< HEAD
__author__ = 'xujiang@baixing.com'

import time
import datetime
from sunshine import settings

def get_global_settings():
    """
    :return:从crapy的全局设置脚本settings.py中获取所有的设置文件
    """
    custom_settings = {}
    keys = [item for item in dir(settings) if not item.startswith("__")]
    for key in keys:
        custom_settings[key] = getattr(settings, key)
    return custom_settings

def timestamp_to_date(timestamp, time_format='%Y-%m-%d %H:%M:%S'):
    '''
    @summary:
    ---------
    @param timestamp: 将时间戳转化为日期
    @param format: 日期格式
    ---------
    @result: 返回日期
    '''

    date = time.localtime(timestamp)
    return time.strftime(time_format, date)

def get_param(url, key):
    params = url.split('?')[-1].split('&')
    for param in params:
        key_value = param.split('=', 1)
        if key == key_value[0]:
            return key_value[1]
    return None

def get_current_timestamp():
    return int(time.time())


def get_current_date(date_format='%Y-%m-%d %H:%M:%S'):
    return datetime.datetime.now().strftime(date_format)
    # return time.strftime(date_format, time.localtime(time.time()))

def str_to_dict(s, join_symbol="\n", split_symbol=":"):
    s_list = s.split(join_symbol)
    data = dict()
    for item in s_list:
        item = item.strip()
        if item:
            k, v = item.split(split_symbol, 1)
            data[k] = v.strip()
    return data
=======
__author__ = 'xujiang@baixing.com'
>>>>>>> 1ea7eb54248b7973704616ac1cbad7693a523428
