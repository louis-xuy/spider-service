# -*- coding: utf-8 -*-

"""
Created on 2018/8/10 下午11:04

@author: xujiang@baixing.com

"""

# -*- coding: utf-8 -*-

from scrapy import Item, Field


class PornArticleItem(Item):
    video_title = Field()
    image_url = Field()
    video_duration = Field()
    quality_480p = Field()
    video_views = Field()
    video_rating = Field()
    link_url = Field()