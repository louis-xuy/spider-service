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




class JanshuItem(Item):
    mongodb_id = Field()
    title = Field()
    content = Field()
    article_id = Field()
    origin_url = Field()
    author = Field()
    avatar = Field()
    publish_time = Field()
    readers = Field()
    likes = Field()
    words = Field()
    comments = Field()
    rewards = Field()

