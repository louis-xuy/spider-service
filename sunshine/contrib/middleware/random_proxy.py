#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: jaxon
@Time: 2020-12-20 12:05
"""


import json
import requests


class RandomProxyMiddleware(object):
    def __init__(self, settings):
        self.PROXY_URL = settings.get('PROXY_URL')
        self.chosen_proxy = ''

        if self.PROXY_URL is None:
                raise KeyError('需要先设置获取代理ip接口的地址')
        self.chosen_proxy = self.get_proxy()


    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def get_proxy(self):
        proxy_addr = json.loads(requests.get('{}/{}/'.format(self.PROXY_URL, 'get')).text)['proxy']
        return proxy_addr

    def del_proxy(self, proxy):
        status = requests.get("{}/{}/?proxy={}".format(self.PROXY_URL, 'delete', proxy))
        return status
        
        

    def process_request(self, request, spider):
        if 'proxy' in request.meta:
            if request.meta["exception"] is False:
                return
        request.meta["exception"] = False
        request.meta['proxy'] ="http://" + self.chosen_proxy

    def process_response(self, request, response, spider):

        if response.status in [403, 400, 302] and 'proxy' in request.meta:
            proxy = request.meta['proxy']
            del request.meta['proxy']
            proxy_ip = proxy.split("//")[1]
            try:
                #删除数据库里的ip
                self.del_proxy(proxy_ip)
            except KeyError:
                pass
            self.chosen_proxy = self.get_proxy()  # 这个代理被403,302了 重新获取
            return request
        return response

    def process_exception(self, request, exception, spider):
        if 'proxy' not in request.meta:
            return
        else:
            proxy = request.meta['proxy']
            proxyip = proxy.split("//")[1]
            try:
                # 删除数据库里的ip
                self.del_proxy(proxyip)
            except KeyError:
                pass
            request.meta["exception"] = True
            self.chosen_proxy = self.get_proxy()
            return request

class LocalProxyMiddleware(object):
    
    def process_request(self, request, spider):
        spider.logger.info('t66ysubtitleSpiderMiddlewareprocess_request: request = % s, spider = % s', request, spider)
        request.meta['proxy'] = 'http://127.0.0.1:1087'
        spider.logger.info('request.meta % s', request.meta)
