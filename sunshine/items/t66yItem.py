#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: jaxon
@Time: 2021-02-06 15:10
"""

from scrapy.item import Item, Field


class T66y(Item):
    name = Field()
    url = Field() # 视频链接
    page_uri = Field() # 页面url
    update = Field()
    file_urls = Field()
    image_urls=Field()
    
class T66yNovel(Item):
    title = Field()
    content = Field()
    