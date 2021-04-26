#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: jaxon
@Time: 2020-12-10 00:23
"""
<<<<<<< HEAD

import yagmail
from scrapy.exporters import CsvItemExporter
from scrapy.mail import MailSender
=======
from scrapy.exporters import CsvItemExporter
>>>>>>> 1ea7eb54248b7973704616ac1cbad7693a523428


class CsvPipeline(object):

    def __init__(self):
<<<<<<< HEAD
        self.file = open("stock_list.csv", 'wb')
        self.exporter = CsvItemExporter(self.file)
=======
        self.file = open("booksdata.csv", 'wb')
        self.exporter = CsvItemExporter(self.file, unicode)
>>>>>>> 1ea7eb54248b7973704616ac1cbad7693a523428
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
<<<<<<< HEAD
        return item

=======
        return item
>>>>>>> 1ea7eb54248b7973704616ac1cbad7693a523428
