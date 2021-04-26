#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: jaxon
@Time: 2020-12-09 20:24
"""

from scrapy.exporters import JsonItemExporter


class JsonPipeline(object):

<<<<<<< HEAD
    def __init__(self, file_path):
        self.file = open("{}.json".format(file_path), 'wb')
        self.exporter = JsonItemExporter(self.file, encoding ='utf-8', ensure_ascii=False)
        self.exporter.start_exporting()

    @classmethod
    def from_crawler(cls, crawler):
        """
        获取spider的settings参数,返回Pipeline实例对象
        """
        store_file = crawler.settings.get("FilePath")
        print("### pipeline get spider_data: {}".format(store_file))
    
        return cls(store_file)


    def close_spider(self, spider):
        """
        spider关闭时调用
        """
        print("### spdier close {}".format(spider.name))
=======
    def __init__(self):
        self.file = open("gaoxiaojob.json", 'wb')
        self.exporter = JsonItemExporter(self.file, encoding ='utf-8', ensure_ascii = False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
>>>>>>> 1ea7eb54248b7973704616ac1cbad7693a523428
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
<<<<<<< HEAD
        return item

    def open_spider(self, spider):
        """
        spider开启时调用
        """
        print("### spdier open {}".format(spider.name))
=======
        return item
>>>>>>> 1ea7eb54248b7973704616ac1cbad7693a523428
