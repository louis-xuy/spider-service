#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: jaxon
@Time: 2021-04-26 21:31
"""

from scrapy import Request, Spider


class IndexConsSW(Spider):
    """
        申万指数成份信息
        http://www.swsindex.com/idx0210.aspx?swindexcode=801010
        :param index_code: 指数代码
        :type index_code: str
        :return: 申万指数成份信息
        :rtype: pandas.DataFrame
    """
    
    name = 'index_cons_sw'
    
    def start_requests(self):
        
        url = f"http://www.swsindex.com/downfile.aspx?code={index_code}"
    
    