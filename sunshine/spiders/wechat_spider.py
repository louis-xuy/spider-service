#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: jaxon
@Time: 2020-12-22 17:59
"""

import html
import json
from sunshine.utils import timestamp_to_date, get_param,get_current_date
from scrapy import Request, Spider
from sunshine.items.items import wechatItem


class WechatSpider(Spider):
    name = 'wechat'
    #allowed_domains = ['mp.weixin.qq.com']
    # custom_settings = {
    #     'DOWNLOADER_MIDDLEWARES': {
    #         'sunshine.contrib.downloadmiddleware.wechat_useragent.WechatUserAgentMiddleware'
    #     }
    # }
    
    def __init__(self, *args, **kwargs):
        super(WechatSpider, self).__init__(*args, **kwargs)
        
        biz = 'MzU3MzQ3NTkzNw=='
        # 微信登录后的一些标识参数
        pass_ticket = 'FP36imPXsuUvTMHPJC2T6/1Atatado42RpIR2/X1ydWIE0MmZK4SDLRgofm4xt22'
        appmsg_token = '1101_rnYUOvCwC%2BIMtnEnI53HqnBuEENlV_nGTfwWTw~~'
        uin = 'MjA1NTkxNDA0MA=='
        key = '2be38213874af320b582ca000825872e3360d77c022988401c1ffe2630b98eae6e1677bb47869c1536c4bcd7564c859069d75b6009c5ac98412f0f477e3daf9e68eb156ae48eb257a7fbb32545b4c673884a0d638acfd2dee7542b9ba699c7f1a8c75cf492afd4aefc0a5b762708fe5ee574a4da8f60d550e71d9800acc83b43'

        
        self.headers = {
                        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) MicroMessenger/6.8.0(0x16080000) MacWechat/2.6.1(0x12060110) Chrome/39.0.2171.95 Safari/537.36 NetType/WIFI WindowsWechat',
                        'Accept-Language':'zh-cn',
                        'X-Requested-With': 'XMLHttpRequest'
                }
        self.cookies = {
            'wxtokenkey': '777',
            "wxuin": "2055914040",
            "devicetype": "iPhoneiOS14.3",
            "version": "1800022d",
            "lang": "zh_CN",
            'wap_sid2': 'CLiEq9QHEooBeV9IRExEVjlWQ0ZUbkxEdWNsLXBNb2dlZlpFMzR0WXN4UldfTFNXN2RYUk52QU82MUxoMURsZjZ4M3ByTktMNi1Hc1JBQjZxdzY5SWRsUFJVbHNLV0pRcWpxTmp4azlZbXctOVpnS1FFLXppTzRvTDFSbG9iZTFORFkyNEwycm1HcnhTb1NBQUF + MPTcwYEGOA1AlU4 =',
            "pass_ticket": pass_ticket,
            'pgv_pvid': '7172348791',
            'tvfe_boss_uuid': '635902e301547d2d',
            'pac_uid':'0_5d2d2e360cbc7'
        }
    
        
        self.url = "https://mp.weixin.qq.com/mp/profile_ext?"
        # 重要参数
        self.params = {
            'action': 'getmsg',
            '__biz': biz,
            'f': 'json',
            'offset': '10',  # 若需要多页爬取， 构造 : str(self.offset)
            'count': '10',
            'is_ok': '1',
            'scene': '124',
            'uin': uin,
            'key': key,  # 这个好像二十分钟就会失效， 需要隔段时间更换
            'pass_ticket': pass_ticket,
            'wxtoken': '',
            'appmsg_token': appmsg_token,
            'x5': '0',
        }
        
    def start_requests(self):
        # self.url += (urlencode(self.params) + '&f=json HTTP/1.1')
        # self.url = self.url.replace('%3D%3D&f=json', '==&f=json', 1)
        url = 'https://mp.weixin.qq.com/s?__biz=MzU3MzQ3NTkzNw==&mid=2247513979&idx=1&sn=a8f273ca38e6400adc3e26a7f4e7104c&chksm=fcc3ea75cbb463639c3e4dbf16415b801f11d99a1cba16b88a8b6cdcf8aa95bb19a128bd47ae&scene=27#wechat_redirect'
        #yield Request(self.url, cookies=self.cookies, headers=self.headers, callback=self.parse)
        yield Request(url, cookies=self.cookies, headers=self.headers, callback=self.parse_item)
        
    def _parse_article_info(self, article_info, comm_msg_info):
        if not article_info:
            return
        
        title = article_info.get("title")
        digest = article_info.get("digest")
        url = article_info.get("content_url").replace("\\", "").replace("amp;", "")
        source_url = article_info.get("source_url").replace("\\", "")  # 引用的文章链接
        cover = article_info.get("cover").replace("\\", "")
        subtype = article_info.get("subtype")
        is_multi = article_info.get("is_multi")
        author = article_info.get("author")
        copyright_stat = article_info.get("copyright_stat")
        duration = article_info.get("duration")
        del_flag = article_info.get("del_flag")
        type = comm_msg_info.get("type")
        publish_time = timestamp_to_date(comm_msg_info.get("datetime"))
        sn = get_param(url, "sn")

        if sn:
            # 缓存文章信息
            article_data = {
                "title": title,
                "digest": digest,
                "url": url,
                "source_url": source_url,
                "cover": cover,
                "subtype": subtype,
                "is_multi": is_multi,
                "author": author,
                "copyright_stat": copyright_stat,
                "duration": duration,
                "del_flag": del_flag,
                "type": type,
                "publish_time": publish_time,
                "sn": sn,
                #"__biz": __biz,
                "spider_time": get_current_date(),
            }
    
            return article_data

    def parse(self, response, *args):
        resp = response.json()
        print(resp)
        ret, status = resp.get('ret'), resp.get('errmsg')
        if ret == 0 or status == 'ok':
            # 控制下一个抓取的offset
            offset = resp.get('next_offset')
            # 将包含主要内容的list转为json格式
            general_msg_list = resp.get('general_msg_list')
            # 一个msg_list中含有10个msg
            msg_list = json.loads(general_msg_list)['list']
            for msg in msg_list:
                # msg是该推送的信息，包含了comm_msg_info以及app_msg_ext_info两个信息，注意某一个推送中可能含有多个文章。
                comm_msg_info = msg.get('comm_msg_info')
                app_msg_ext_info = msg.get('app_msg_ext_info')

                # # 该推送的id
                # msg_id = comm_msg_info.get('id')
                # # 该推送的发布时间，例如1579965567需要转化为datetime，datetime.fromtimestamp(1579965567)
                # post_time = datetime.fromtimestamp(comm_msg_info['datetime'])
                # # 该推送的类型
                # msg_type = comm_msg_info.get('type')

                if app_msg_ext_info:
                    # 推送的第一篇文章
                    article_info = self._parse_article_info(app_msg_ext_info, comm_msg_info)
                    print(article_info)
                    url = article_info.get('url').replace("\\", "").replace("http", "https")
                    url = html.unescape(url)
                    print('url:', url)
                    print('=' * 50)
                    yield Request(url, headers=self.headers, meta=article_info, callback=self.parse_item)
                    # 判断是不是多篇文章
                    is_multi = app_msg_ext_info.get("is_multi")
                    # 如果是1，继续爬取；如果是0，单条推送=只有一篇文章
                    if is_multi:
                        multi_app_msg_item_list = app_msg_ext_info.get('multi_app_msg_item_list')
                        for information in multi_app_msg_item_list:
                            article_info = self._parse_article_info(information, comm_msg_info)
                            url = article_info.get('url').replace("\\", "").replace("http", "https")
                            url = html.unescape(url)
                            print(article_info)
                            print('url', url)
                            print('='*50)
                            yield Request(url, headers=self.headers, meta=article_info, callback=self.parse_item)
                        
            ## TODO 下一页
            
    def parse_item(self, response):
        print(response.request.url)
        item = wechatItem()
        item.sn = get_param(response.request.url, "sn")
        print(item.sn)
        content = response.xpath(
            '//div[@class="rich_media_content "]|//div[@class="rich_media_content"]|//div[@class="share_media"]'
        )
        print(content)
        title = response.xpath('//h2[@class="rich_media_title"]/text()').extract_first(default="").strip()
        print(title)
        item.account = (
            response.xpath('//a[@id="js_name"]/text()')
                .extract_first(default="")
                .strip()
        )
        item.author = (
            response.xpath(
                '//span[@class="rich_media_meta rich_media_meta_text"]//text()'
            )
                .extract_first(default="")
                .strip()
        )

        publish_timestamp = response.re_first('n="(\d{10})"')
        publish_timestamp = int(publish_timestamp) if publish_timestamp else None
        item.publish_time = (
            timestamp_to_date(publish_timestamp) if publish_timestamp else None
        )

        item.pics_url = content.xpath(".//img/@src|.//img/@data-src").extract()
        item.__biz = get_param(response.request.url, "__biz")

        item.digest = response.re_first('var msg_desc = "(.*?)"')
        item.cover = response.re_first('var cover = "(.*?)";') or response.re_first(
            'msg_cdn_url = "(.*?)"'
        )
        item.source_url = response.re_first("var msg_source_url = '(.*?)';")

        item.content_html = content.extract_first(default="")
        item.comment_id = response.re_first('var comment_id = "(\d+)"')
        yield item
