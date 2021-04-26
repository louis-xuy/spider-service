#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Time    : 2018/8/11 0:27

__author__ = 'xujiang@baixing.com'

<<<<<<< HEAD
import re
import logging
import datetime
from scrapy import Request, Spider
from sunshine.items.items import GaoxiaoJobItem


class ArticleSpider(Spider):

    name = "gaoxiaojob"
    allowed_domains = ['gaoxiaojob.com']
    today = datetime.date.today().strftime('%Y-%m-%d')

    custom_settings = {
        'ITEM_PIPELINES': {
            'sunshine.pipelines.excel.ExcelPipeline': 500
            # 'sunshine.pipelines.mongodb.SingleMongodbPipeline': 800
            # 'sunshine.pipelines.final_test.FinalTestPipeline':800
        },
        # 发送邮件
        'EXTENSIONS': {
                'sunshine.extensions.mail_sender.MailSender': 300
        },
        'SingleMONGODB_DB': 'job',
        'SingleMONGODB_TB': "research_job"
    }

    start_urls = [
        'http://www.gaoxiaojob.com/zhaopin/yanjiujigou/index_1.html',
    ]

    def parse(self, response):
        next_url = response.xpath('//div[contains(@class,"Page")]/a[@class="next"]/@href').get()
        next_url = f"http://www.gaoxiaojob.com/zhaopin/yanjiujigou/{next_url}"
        yield Request(url=next_url, callback=self.parse)
        links = response.xpath('//span[@class="ltitle"]/a/@href').getall()
        for link in links:
            try:
                mo = re.match(r'http://www\.gaoxiaojob\.com/zhaopin/.*/(\d{8})/\d{6}\.html', link, re.M | re.I)
                pubdate = mo.group(1)
                if pubdate > (datetime.datetime.now() - datetime.timedelta(days=2)).strftime('%Y%m%d'):
                    yield Request(url=link, callback=self.parse_item)
            except Exception as e:
                continue
=======
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
>>>>>>> 1ea7eb54248b7973704616ac1cbad7693a523428

    def parse_item(self, response):
        self.log('Hi, this is an job page! %s' % response.url)
        item = GaoxiaoJobItem()
        item['crawlkey'] = self.name
        item["url"] = response.url
<<<<<<< HEAD
        item['title'] = response.xpath('//h1[@class="title-a"]//text()').get()
        pubdate = response.xpath('//ul[@class="article_fenlei"]/li/b[contains(./text(), "发布时间")]/following::text()[1]').get()
        item['pubdate'] = pubdate.replace('：', '').strip()
        item['province'] = response.xpath('//a[contains(@href, "http://www.gaoxiaojob.com/zhaopin/diqu/")]//text()').get()
        item['location'] = response.xpath('//a[contains(@href, "http://www.gaoxiaojob.com/zhaopin/chengshi")]//text()').get()
        item['category'] = response.xpath('//a[contains(@href, "http://www.gaoxiaojob.com/zhaopin/keyanrencai")]//text()').get()
        item['headcount'] = response.xpath('//ul[@class="article_fenlei"]/li/b[contains(./text(), "招聘人数")]/following::text()[1]').get().replace('：','')
        texts = response.xpath("//div[@class='article_body']//p")
        lines = []
        for test in texts:
            line = ''.join(test.xpath('//p//span//text()').getall())
            lines.append(line.strip())
        item['content'] = '\n'.join(lines)
        item['htmlcontent'] = response.xpath('//div[@class="article_body"]').get()
        item['subject'] = ','.join(response.xpath('//a[contains(@href, "http://www.gaoxiaojob.com/zhaopin/xuqiuxueke")]//text()').getall())
        item['update'] = self.today
=======
        item['title'] = response.xpath('//h1[@class="title-a"]//text()').extract()
        item['category'] = response.xpath('//ul[@class="article_fenlei"]').extract()[0]
        item['content'] = response.xpath('//div[@class="article_body"]').extract()[0]
        
        #item['content'] = response.xpath('//div[@class="article_body"]/p//text()').extract()
        #item['pubdate'] = doc('b'):contains("发布时间")')[0].tail
        #item['pubdate'] = response.xpath('//ul[@class="article_fenlei"]/li/b[contains(./text(), "发布时间")]/following::text()[1]').extract()[0]
        #item['need_person'] = response.xpath(
        #    '//ul[@class="article_fenlei"]/li/b[contains(./text(), "招聘人数")]/following::text()[1]').extract()[0]

>>>>>>> 1ea7eb54248b7973704616ac1cbad7693a523428
        yield item
