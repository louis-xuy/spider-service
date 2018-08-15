#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Time    : 2018/7/26 22:15

__author__ = 'xujiang@baixing.com'

import os
import re
import chardet

def parse_data():
    cates = {}
    f_item = None
    with open('C:/Users/Administrator/Desktop/news_tensite_xml.dat', 'rb') as f:
        for line in f:
            print(line)


def detect_file_encoding(file_path):
    ''' 返回文件的编码 '''
    f = open(file_path, 'rb')
    data = f.read()
    predict = chardet.detect(data)
    f.close()
    return predict['encoding']


if __name__ == '__main__':
    # detect file encode type
    file_path = 'C:/Users/Administrator/Desktop/news_tensite_xml.dat'
    print(detect_file_encoding(file_path))

    # read file
    f2 = open(file_path, encoding='GB2312', errors="ignore")
    content2 = f2.read()
    print (content2)
    f2.close()

    # write to text file
    f = open('C:/Users/Administrator/Desktop\news_tensite_xml.txt', 'w', encoding='utf8')

    # exact the text between <content> and  </content>
    c = re.findall('<content>.*</content>', content2)
    print("Length of list: %d" % len(c))
    i = 0
    for item in c:
        b = item.replace('<content>', '')
        b = b.replace('</content>', '')
        f.write(str(b) + '\n')
        i = i + 1
        if i % 1000 == 0:
            print("index: %d / %d" % (i, len(c)))

    f.close()