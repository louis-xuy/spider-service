#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Time    : 2018/8/11 0:27

__author__ = 'xujiang@baixing.com'

from scrapy.spiders import CrawlSpider, Rule
from sunshine.items import GaoxiaoJobItem
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.linkextractors import LinkExtractor


class ArticleSpider(CrawlSpider):
    name = "gaoxiaojob"
    allowed_domains = ['gaoxiaojob.com']
    start_urls = [
        'http://www.gaoxiaojob.com/zhaopin/yanjiujigou/index_1.html',
    ]
    rules = (
        # LxmlLinkExtractor提取链接列表
        Rule(LxmlLinkExtractor(allow=(r'/news/\d{4}/\d{2}/\d{2}/\d+\.html',
                                        r'/news/hyyw/news/index\d+\.html'),
                                restrict_xpaths=('//div[@class="list"]', 
                                                    '//div[@class="page"]')),
                callback='parse_links', follow=False),
    )
    

    def parse_links(self, response):
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

        article = GaoxiaoJobItem()
        article["url"] = response.url

        title = response.xpath(self.rule.title_xpath).extract()
        article["title"] = parse_text(title, self.rule.name, 'title')

        body = response.xpath(self.rule.body_xpath).extract()
        article["body"] = parse_text(body, self.rule.name, 'body')

        publish_time = response.xpath(self.rule.publish_time_xpath).extract()
        article["publish_time"] = parse_text(publish_time, self.rule.name,
                                            'publish_time')

        article["source_site"] = self.rule.source_site

        return article