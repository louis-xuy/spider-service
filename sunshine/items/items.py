#!/usr/bin/python
#-*-coding:utf-8-*-

import datetime
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


class GaoxiaoJobItem(Item):
    """gaoxiaojob-Item"""
    crawlkey = Field()          # 关键字
    title = Field()             # 标题
    url = Field()          # 链接
    desc = Field()              # 简述
    pubdate = Field()           # 发布时间
    category = Field()          # 分类
    province = Field()
    headcount = Field()
    location = Field()          # 工作地点
    subject = Field()
    content = Field()           # 内容
    htmlcontent = Field()       # html内容
    update = Field()

class wechatItem(Item):
    account = Field()
    title = Field()
    url = Field()
    author = Field()
    publish_time = Field()
    __biz = Field()
    digest = Field()
    cover = Field()
    pics_url = Field()
    content_html = Field()
    source_url = Field()
    comment_id = Field()
    sn = Field()
    spider_time = Field()
    

    


