#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: jaxon
@Time: 2020-12-29 10:35
"""


from openpyxl import Workbook


class ExcelPipeline(object):
    def __init__(self):
        self.wb = Workbook()
        self.ws = self.wb.active
        self.ws.append(['crawlkey', 'pubdate', 'province', 'location',
                        'category', 'subject', 'headcount', 'url', 'title', 'content'])

    def process_item(self, item, spider):  # 工序具体内容
        line = [item['crawlkey'], item['pubdate'], item['province'], item['location'], item['category'], item['subject'],
                item['headcount'], item['url'], item['title'], item['content']]  # 把数据中每一项整理出来
        self.ws.append(line)  # 将数据以行的形式添加到xlsx中
        self.wb.save('{}.xlsx'.format(spider.name))
        return item
