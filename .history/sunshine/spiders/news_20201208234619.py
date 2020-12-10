#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Time    : 2018/8/11 0:27

__author__ = 'xujiang@baixing.com'

import re
import time
import hashlib
import json
import requests
import scrapy
from html.parser import HTMLParser

from sunshine.items import NewsItem
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor

from scrapy import Request
from scrapy.selector import Selector


def ListCombiner(lst):
    string = ""
    for e in lst:
        string += e
    return string.replace(' ','').replace('\n','').replace('\t','')\
        .replace('\xa0','').replace('\u3000','').replace('\r','')\
        .replace('[]','')


def get_as_cp():
    zz ={}
    now = round(time.time())
    # print now  #获取计算机时间
    e = hex(int(now)).upper()[2:]  #hex()转换一个整数对象为十六进制的字符串表示
    # print e
    i = hashlib.md5(str(int(now))).hexdigest().upper() #hashlib.md5().hexdigest()创建hash对象并返回16进制结果
    if len(e)!=8:
        zz = {'as': "479BB4B7254C150",
            'cp': "7E0AC8874BB0985"}
        return zz
    n=i[:5]
    a=i[-5:]
    r = ""
    s = ""
    for i in range(5):
        s = s+n[i]+e[i]
    for j in range(5):
        r = r+e[j+3]+a[j]
    zz = {
            'as': "A1" + s + e[-3:],
            'cp': e[0:3] + r + "E1"
        }
    return zz


def get_article_list(user_id=None, hot_time=None):
    url = "http://it.snssdk.com/pgc/ma/"

    ap = get_as_cp()
    querystring = {"page_type": "1", "max_behot_time": hot_time, "uid": user_id,
                   "media_id": user_id, "output": "json", "is_json": "1", "count": "20", "page": 1,
                   "from": "user_profile_app", "version": "2", "as": ap['as'], "cp": ap['cp']}

    headers = {
        'user-agent': "Mozilla/5.0 (Linux; Android 4.4.4; MuMu Build/V417IR) \
            AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/33.0.0.0 Mobile Safari/537.36 JsSdk/2 NewsArticle/6.3.1 NetType/wifi",
        'cache-control': "no-cache"
    }

    response = requests.request(
        "GET", url, headers=headers, params=querystring)

    # print (response.text)
    jj = json.loads(response.text)
    has_more = jj['has_more']
    next_hot_time = 0
    if has_more:
        next_hot_time = jj['next']['max_behot_time']

    list = jj['data']
    print (len(list), has_more, next_hot_time)
    b_should_hold = False
    if len(list) == 0:
        print (response.text)
        b_should_hold = True

    # ss = []
    # for t in list:
    # print t['title']
    # pri
    # ss.append( [t['item_id'], t['publish_time'], t['has_video'], t['article_url'], t['title'], t['source'],  t['tag'], ' | '.join(t['categories'])])

    return list, has_more, next_hot_time, b_should_hold


def get_detail(group_id):
    url = "https://www.toutiao.com/a{}/".format(group_id)

    headers = {
        'upgrade-insecure-requests': "1",
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36",
        'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        'accept-encoding': "gzip, deflate, br",
        'accept-language': "en,zh-CN;q=0.9,zh;q=0.8,zh-TW;q=0.7,la;q=0.6",
        # 'cookie': "tt_webid=6547538660773250573; UM_distinctid=162e3be903dff6-0449f153325ada-33627106-1fa400-162e3be903fbe2; tt_webid=6547538660773250573; _ga=GA1.2.1193771552.1524469973; uuid=\"w:6b278e6d93e24b489d64fc1429314f78\"; login_flag=6e02465e870d2a82323af50ced7a3485; sid_tt=5a14e60aa368844ab5a74397a83fd330; sid_guard=\"5a14e60aa368844ab5a74397a83fd330|1524547131|15552000|Sun\054 21-Oct-2018 05:18:51 GMT\"; __tea_sdk__ssid=b011223f-64ee-4cc5-bbc2-e127f6df85a2; tt_webid=6547538660773250573; WEATHER_CITY=%E5%8C%97%E4%BA%AC; __tea_sdk__user_unique_id=97539191906; __tasessionId=97ajmgt551527917229150; sso_login_status=0; _gid=GA1.2.350819017.1527920525; CNZZDATA1259612802=1144703413-1524465903-https%253A%252F%252Fwww.google.com%252F%7C1527920669",
        'cache-control': "no-cache",
        'postman-token': "879dd0f8-5db8-147c-3a3b-279ea713eb2d"
    }

    response = requests.request("GET", url, headers=headers)
    # print(response.text)
    text = response.text
    content = text[text.find("content: '") + len("content: '"):text.find("groupId: '")]
    # html_parser = HTMLParser.HTMLParser()
    content = HTMLParser.HTMLParser().unescape(content)

def get_user_ids():
    # users = SES.query(db.User).all()
    # return users
    pass

def next_time_seg():
    with open('last_time.txt', 'r+') as fp:
        last_time = int(fp.readline())
        if last_time == 0:
            last_time = int(time.time() - 60*60 -5)
        now_time = int(time.time()-5)
        fp.seek(0)
        fp.write(str(now_time))
        fp.truncate()
        return (last_time, now_time)

def inter():
    users = get_user_ids()
    print (len(users))
    while True:
        ts = next_time_seg()
        print (ts)
        for u in users:
            print (u['ID'])
            ss = get_article_list(u['ID'])
            for s in ss:
                print (s)
                if s['publish_time'] > ts[0] and s['publish_time'] <= ts[1] and not s['has_video']:
                    #yooo we got an new article!!!!
                    # TODO fix 下面的代码
                    url = s[3]
                    print (s[0], url, s[4], s[5])
                    get_detail(s[0])
                else:
                    pass
        time.sleep(5*60)


class TouTiaoSpider(scrapy.Spider):
    name = 'toutiao'

    def start_requests(self):
        next_hot_time = ""
        b_flag = True
        b_hold_time = 0

    def parse_list(self, response):
        url = "http://it.snssdk.com/pgc/ma/"

        user_id = response.meta['user_id']
        hot_time = response.meta['hot_time']
        ap = get_as_cp()
        querystring = {"page_type": "1", "max_behot_time": hot_time, "uid": user_id,
                       "media_id": user_id, "output": "json", "is_json": "1", "count": "20", "page": 1,
                       "from": "user_profile_app", "version": "2", "as": ap['as'], "cp": ap['cp']}

        headers = {
            'user-agent': "Mozilla/5.0 (Linux; Android 4.4.4; MuMu Build/V417IR) \
                AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/33.0.0.0 Mobile Safari/537.36 JsSdk/2 NewsArticle/6.3.1 NetType/wifi",
            'cache-control': "no-cache"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)





class TencentNewsSpider(CrawlSpider):
    name = 'tencent_news_spider'
    # allowed_domains = ['news.qq.com']
    start_urls = ['http://news.qq.com']
    # http://news.qq.com/a/20170825/026956.htm
    url_pattern = r'(.*)/a/(\d{8})/(\d+)\.htm'
    rules = [
        Rule(LxmlLinkExtractor(allow=[url_pattern]), callback='parse_news', follow=True)
    ]

    def parse_news(self, response):
        sel = Selector(response)
        if sel.xpath('//*[@id="Main-Article-QQ"]/div/div[1]/div[1]/div[1]/h1/text()'):
            title = sel.xpath('//*[@id="Main-Article-QQ"]/div/div[1]/div[1]/div[1]/h1/text()').extract()[0]
        elif sel.xpath('//*[@id="C-Main-Article-QQ"]/div/div[1]/div[1]/div[1]/h1/text()'):
            title = sel.xpath('//*[@id="C-Main-Article-QQ"]/div/div[1]/div[1]/div[1]/h1/text()').extract()[0]
        elif sel.xpath('//*[@id="ArticleTit"]/text()'):
            title = sel.xpath('//*[@id="ArticleTit"]/text()').extract()[0]
        else:
            title = 'unknown'
        pattern = re.match(self.url_pattern, str(response.url))
        source = 'tencent'
        date = pattern.group(2)
        date = date[0:4] + '/' + date[4:6] + '/' + date[6:]
        newsId = pattern.group(3)
        url = response.url
        if sel.xpath('//*[@id="Main-Article-QQ"]/div/div[1]/div[1]/div[1]/div/div[1]/span[3]/text()'):
            time_ = sel.xpath('//*[@id="Main-Article-QQ"]/div/div[1]/div[1]/div[1]/div/div[1]/span[3]/text()').extract()[0]
        else:
            time_ = 'unknown'
        contents = ListCombiner(sel.xpath('//p/text()').extract()[:-8])

        if response.xpath('//*[@id="Main-Article-QQ"]/div/div[1]/div[2]/script[2]/text()'):
            cmt = response.xpath('//*[@id="Main-Article-QQ"]/div/div[1]/div[2]/script[2]/text()').extract()[0]
            if re.findall(r'cmt_id = (\d*);', cmt):
                cmt_id = re.findall(r'cmt_id = (\d*);', cmt)[0]
                comment_url = 'http://coral.qq.com/article/{}/comment?commentid=0&reqnum=1&tag=&callback=mainComment&_=1389623278900'.format(cmt_id)
                yield Request(comment_url, callback=self.parse_comment, meta={'source': source,
                                                                     'date': date,
                                                                     'newsId': newsId,
                                                                     'url': url,
                                                                     'title': title,
                                                                     'contents': contents,
                                                                     'time': time_
                                                                     })
            else:
                item = NewsItem()
                item['source'] = source
                item['time'] = time_
                item['date'] = date
                item['contents'] = contents
                item['title'] = title
                item['url'] = url
                item['newsId'] = newsId
                item['comments'] = 0
                yield item

    def parse_comment(self, response):
        print (response)
        if re.findall(r'"total":(\d*)\,', response.text):
            comments = re.findall(r'"total":(\d*)\,', response.text)[0]
        else:
            comments = 0
        item = NewsItem()
        item['source'] = response.meta['source']
        item['time'] = response.meta['time']
        item['date'] = response.meta['date']
        item['contents'] = response.meta['contents']
        item['title'] = response.meta['title']
        item['url'] = response.meta['url']
        item['newsId'] = response.meta['newsId']
        item['comments'] = comments
        yield item

if __name__ == "__main__":
    inter()
