#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Time    : 2018/7/26 22:15

__author__ = 'xujiang@baixing.com'

import json
import yagmail

msg = ''
with open('/Users/jaxon/WorkSpace/spider-service/gaoxiaojob.json', 'r') as f:
    data = json.load(f)
    for e in data:
        title = e.get('title')
        url = e.get("url")
        category = e.get('category')
        content = e.get('content')
        msg = msg+title+'\n'+url+'\n'+category+'\n'+content+'\n'+'-'*100
yag = yagmail.SMTP(user='xu8888jiang@126.com', password='ZYCFWACYWJIYLZHI', host='smtp.126.com')

yag.send(to='360138359@qq.com', subject='Testing Yagmail', contents=msg)