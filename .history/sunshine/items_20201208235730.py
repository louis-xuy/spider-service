#!/usr/bin/python
#-*-coding:utf-8-*-

from scrapy.item import Item, Field
class NewsItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    id = Field()
    categories = Field()
    city = Field()
    image_list = Field()
    keywords = Field()
    label = Field()
    tag = Field()
    st = Field()
    source = Field()
    newsId = Field()
    title = Field()
    contents = Field()
    url = Field()
    comments = Field()
    publish_time = Field()


class NewsItem(scrapy.Item):
    """gaoxiaojob-Item"""
    crawlkey = scrapy.Field()      # 关键字
    title = scrapy.Field()         # 标题
    link = scrapy.Field()          # 链接
    desc = scrapy.Field()          # 简述
    pubdate = scrapy.Field()       # 发布时间
    category = scrapy.Field()      # 分类
    location = scrapy.Field()      # 来源
    content = scrapy.Field()       # 内容
    htmlcontent = scrapy.Field()   # html内容
