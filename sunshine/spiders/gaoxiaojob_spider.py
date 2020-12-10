#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Time    : 2018/8/11 0:27

__author__ = 'xujiang@baixing.com'

import logging
from pyquery import PyQuery
from scrapy import Request
from scrapy.spiders import CrawlSpider, Rule
from sunshine.items import GaoxiaoJobItem
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.linkextractors import LinkExtractor
from sunshine.utils.html_parse import parse_text


class ArticleSpider(CrawlSpider):
    name = "gaoxiaojob"
    allowed_domains = ['gaoxiaojob.com']
    start_urls = [
        'http://www.gaoxiaojob.com/zhaopin/yanjiujigou/index_1.html',
    ]
    rules = (
        # LxmlLinkExtractor提取链接列表
        Rule(LxmlLinkExtractor(allow=(r'zhaopin/yanjiujigou/\d{8}/\d{6}\.html')), callback='parse_item'),
                                        Rule(LxmlLinkExtractor(allow=(r'zhaopin/yanjiujigou/index_\d+\.html')))
    )

    def parse(self, response):
        self.log('-------------------> link_list url=%s' % response.url, logging.INFO)
        links = response.xpath('//div[starts-with(@class, "listbox")]/ul/li')
        for link in links:
            url = link.xpath('span[1]/a/@href').extract()[0]
            date_str = link.xpath('span[2]/text()').extract()[0]
            date_str = date_str.split(' ')[1] + ':00'
            self.log('+++++++++++' + date_str, logging.INFO)
            yield Request(url=url, meta={'ds': date_str}, callback=self.parse_item_page)

    def parse_item(self, response):
        self.log('Hi, this is an job page! %s' % response.url)
        item = GaoxiaoJobItem()
        item['crawlkey'] = self.name
        item["url"] = response.url
        item['title'] = response.xpath('//h1[@class="title-a"]//text()').extract()
        item['category'] = response.xpath('//ul[@class="article_fenlei"]').extract()[0]
        item['content'] = response.xpath('//div[@class="article_body"]').extract()[0]
        
        #item['content'] = response.xpath('//div[@class="article_body"]/p//text()').extract()
        #item['pubdate'] = doc('b'):contains("发布时间")')[0].tail
        #item['pubdate'] = response.xpath('//ul[@class="article_fenlei"]/li/b[contains(./text(), "发布时间")]/following::text()[1]').extract()[0]
        #item['need_person'] = response.xpath(
        #    '//ul[@class="article_fenlei"]/li/b[contains(./text(), "招聘人数")]/following::text()[1]').extract()[0]

        yield item
