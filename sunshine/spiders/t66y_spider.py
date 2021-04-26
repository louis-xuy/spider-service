#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: jaxon
@Time: 2021-02-06 15:15
"""

import requests
import re
import time
from scrapy import Request, Spider
from scrapy.selector import Selector
from sunshine.items.t66yItem import T66y, T66yNovel


class T66yVideoSpider(Spider):
    name = 't66y_video'
    allowed_domains = ['http://t66y.com']

    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'sunshine.contrib.middleware.random_proxy.LocalProxyMiddleware': 100,
        },
        
        'ITEM_PIPELINES': {
            #'sunshine.pipelines.mongodb.SingleMongodbPipeline': 800
            'sunshine.pipelines.file.FilePipeline': 800
        },
        'SingleMONGODB_DB': "job",
        'SingleMONGODB_TB': "t66y",
        "FILES_STORE": '~/Documents/logs'
    }
    
    def __init__(self, *args, **kwargs):
        super(T66yVideoSpider, self).__init__(*args, **kwargs)
        self.page = 1
        ## 技术讨论
        #self.url = 'https://t66y.com/thread0806.php?fid=7&search=&page={}'
        # 不骑马的日本人板块
        # self.url = "http://t66y.com/thread0806.php?fid=2&search=&page={}"
        # 骑马的日本人板块
        self.url = "http://t66y.com/thread0806.php?fid=15&search=&page={}"
        # 英语老师板块
        # self.url = "http://t66y.com/thread0806.php?fid=4&search=&page={}"
        
        
    def download_page(self, url):
        '''
                针对草榴的第三级页面的方法，负责下载链接
                '''
        header_data2 = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'rmdown.com',
            'Referer': 'http://www.viidii.info/?http://rmdown______com/link______php?' + url.split("?")[1],
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
        }
        try:
            download_text = requests.get(url, headers=header_data2).text
            p_ref = re.compile("name=\"ref\" value=\"(.+?)\"")  # 点击下载时会有表单提交，几个参数都是页面内hidden属性的值，把他们先提取出来
            p_reff = re.compile("NAME=\"reff\" value=\"(.+?)\"")
            ref = p_ref.findall(download_text)[0]
            reff = p_reff.findall(download_text)[0]
            r = requests.get("http://www.rmdown.com/download.php?ref=" + ref + "&reff=" + reff + "&submit=download")
            with open(ref + ".torrent", "wb") as f:
                f.write(r.content)  # 下载种子到文件
        except:
            print("download page " + url + " failed")

    def start_requests(self):
        print('start t66y crawl ...')
        yield Request(self.url.format(self.page), callback=self.parse)
        #yield Request('http://t66y.com/htm_data/1605/7/1940570.html', callback=self.parse_item)
        
    def parse(self, response):
        print("===================================================")
        print("list page: {}".format(response.request.url))
        # links = response.xpath('//tr[@class="tr3 t_one tac"]/td[@class="tal"]//h3').extract()
        #
        # for li in links:
        #     link = Selector(text=li).xpath(".//h3/a/@href").get()
        #     try:
        #         name = Selector(text=li).xpath(".//h3/a/font/text()").get()
        #     except Exception as e:
        #         name = None
        #     if not name:
        #         name = Selector(text=li).xpath(".//h3/a/text()").get()
        #     print(name, link)
        #     if name and name.find('榴民资讯') >= 0:
        #         yield Request('https://t66y.com/'+link, meta={"name":name}, callback=self.parse_item)
        # if self.page < 110:
        #     self.page = self.page + 1
        #     yield Request(self.url.format(self.page), callback=self.parse_middle)
        node_list = response.xpath("//td[@class='tal']")
        next_page = response.xpath("//a[text()='下一頁']/@href").extract()
        print(next_page)
        # 遍历列表获取种子名称、详情页URL
        for node in node_list:
            print(node)
            if not len(node.xpath('./h3/a/text()').extract()) or not len(node.xpath('./h3/a/@href').extract()):
                 print('...')
                 continue
            title = node.xpath('./h3/a/text()').extract()[0]
            detail_url = node.xpath('./h3/a/@href').extract()[0]
            
            print(title, detail_url)
            # 通过Request meta传递参数
            yield Request(self.allowed_domains[0] + "/" + detail_url, callback=self.parse_detail,
                                meta={'title': title}, dont_filter=True)
        # if next_page not in self.allowed_domains[0]:
        #     yield Request(self.allowed_domains[0] + "/" + next_page, callback=self.parse, dont_filter=True)
    
    def parse_detail(self, response):
        print("-----------------------------------")
        # item = T66y()
        # item['title'] = response.xpath('//div[@class="tpc_content do_not_catch"]/br[0]')
        # item['actor'] = response.xpath('//div[@class="tpc_content do_not_catch"]/br[3]')
        # item['captions'] = response.xpath('//div[@class="tpc_content do_not_catch"]/br[5]')
        # item['format'] = response.xpath('//div[@class="tpc_content do_not_catch"]/br[6]')
        # item['isma'] = response.xpath('//div[@class="tpc_content do_not_catch"]/br[7]')
        # item['bit'] = response.xpath('//div[@class="tpc_content do_not_catch"]/br[8]')
        # item['yanzhengma'] = response.xpath('//div[@class="tpc_content do_not_catch"]/br[9]')
        imgs = response.xpath('//div[@class="tpc_content do_not_catch"]/img/@src').get()
        print(imgs)
        # ## 视频下载链接
        # video_detal_url = response.xpath(
        #     '//div[@class=""]/a[contains(@href, "http://www______rmdown______com/link______php?hash]//text()')
        # yield Request(video_detal_url, meta={'item': item}, callback=self.parse_item)
        title = response.meta['title']
        node_list = response.xpath(
            '//a[@style="cursor:pointer;color:#008000;"]')
        for node in node_list:
            yield Request(node.xpath('./@href').extract()[0], callback=self.parse_item,
                                 meta={'title': title, 'imgs': imgs}, dont_filter=True)
            # 默认获取第一条种子下载地址
            break
            
    
    def parse_item(self, response):
        # item = response.meta['item']
        # print("detail page: {}".format(response.request.url))
        # item['page_uri'] = response.request.url
        # data = response.text
        # #print(data)
        # res = re.findall(r'magnet:[^><\\["]*', data)
        # #res = re.findall(r'magnet:\\?xt=urn:btih:.[^<\s"]*?', data, re.M | re.I)
        # for url in res:
        #     print(url)
        #     item['url'] = url
        #     item['update'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        #     yield item
        
        ## 解析不骑马的日本人板块 and 。。
        title = response.meta['title']
        imgs = response.meta['imgs']
        ref = response.xpath("//input[@type='hidden' and @name='ref']/@value")[0].get()
        reff = response.xpath("//input[@type='hidden' and @name='reff']/@value")[0].get()
        torrent_url = "http://www.rmdown.com/download.php?ref={}&reff={}&submit=download".format(ref, reff)
        item = T66y()
        item['file_urls'] = torrent_url
        item['image_urls'] = imgs
        print(imgs)
        item['name'] = title + ".torrent"
        r = requests.get("http://www.rmdown.com/download.php?ref=" + ref + "&reff=" + reff + "&submit=download")
        with open(ref + ".torrent", "wb") as f:
            f.write(r.content)  # 下载种子到文件
        yield item
        
        

class t66yPicSpider(Spider):
    name = 't66y_pic'
    ## 新时代的我们
    allowed_domains = ['http://t66y.com']
    # start_urls = [# 'http://www.t66y.com/thread0806.php?fid=8&search=&page=1',
    #               'http://www.t66y.com/thread0806.php?fid=16&search=&page=1' # 達蓋爾的旗幟
    # ]
    
    def start_requests(self):
        print('start t66y crawl ...')
        self.url = 'http://www.t66y.com/thread0806.php?fid=16&search=&page={}'
        self.page = 1
        yield Request(self.url.format(self.page), callback=self.parse)
    
    def parse(self, response):
        node_list = response.xpath("//td[@class='tal']")
        next_page = response.xpath("//a[text()='下一頁']/@href").extract()
        for node in node_list:
            print(node)
            if not len(node.xpath('./h3/a/@href').extract()):
                 continue
            title = node.xpath('./h3/[a|a/font]/text()').extract()[0]
            detail_url = node.xpath('./h3/a/@href').extract()[0]
            temp_result = detail_url.split('/')
            if len(temp_result) == 4:
                year_month = temp_result[2]
                post_id = temp_result.split('.')[0]
                print(title, detail_url)
                yield Request(self.allowed_domains[0] + "/" + detail_url, callback=self.parse_item,
                              meta={'post_id': post_id}, dont_filter=True)
    
    def parse_item(self, response):
        title = response.xpath('//h4/text()').extract()[0]
        img_url = response.xpath('//div[@class="image-big"]/img/@src').extract()
        print(title, img_url)
        
        
    

    

class t66yNovelSpider(Spider):
    name = 't66y_novel'

    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'sunshine.contrib.middleware.random_proxy.LocalProxyMiddleware': 100,
        },
    
        'ITEM_PIPELINES': {
            # 'sunshine.pipelines.mongodb.SingleMongodbPipeline': 800
            'sunshine.pipelines.csv.CsvPipeline': 800
        },
        # 'SingleMONGODB_DB': "job",
        # 'SingleMONGODB_TB': "t66y",
        "FILES_STORE": '~/Documents/logs'
    }
    
    allowed_domains = ['http://t66y.com']
    start_urls = ['http://www.t66y.com/thread0806.php?fid=20&search=&page=13']

    def parse(self, response):
        node_list = response.xpath("//td[@class='tal']")
        next_page = response.xpath("//a[text()='下一頁']/@href").extract()
        for node in node_list:
            if not len(node.xpath('./h3/a/text()').extract()) or not len(node.xpath('./h3/a/@href').extract()):
                continue
            title = node.xpath('./h3/a/text()').extract()[0]
            detail_url = node.xpath('./h3/a/@href').extract()[0]
            print(title, detail_url)
            yield Request(self.allowed_domains[0] + "/" + detail_url, callback=self.parse_item,
                          meta={'title': title}, dont_filter=True)
    
    def parse_item(self, response):
        item = T66yNovel()
        item['title'] = response.meta['title']
        item['content'] = '\n'.join(response.xpath('//div[@class="tpc_content do_not_catch"]//text()').extract())
        yield item
