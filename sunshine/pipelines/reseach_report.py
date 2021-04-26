#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: jaxon
@Time: 2021-02-17 02:21
"""

from scrapy import Request
from scrapy.pipelines.files import FilesPipeline



class StockReseachReportFile(FilesPipeline):

    def get_media_requests(self, items, info):
        industryName = items['industryName']
        for pdf_url in items['file_urls']:
            yield Request(pdf_url, meta={'industryName': industryName})  # 继续传递分类、标题

    def file_path(self, request, response=None, info=None):
        # 按照full\分类\标题\图片合集命名
        filename = r'full/%s/%s' % (request.meta['industryName'], request.url.split('/')[-1])
        return filename