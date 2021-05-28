#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: jaxon
@Time: 2021-04-30 09:15
"""

from io import BytesIO
import pandas as pd
from scrapy import Request, Spider
from sunshine.models import loadSession
from sunshine.models.stock_model import StockInfo


def get_security_list():
    session = loadSession()
    d = session.query(StockInfo).filter(StockInfo.type=='CS').all()
    return d


class ProfitFlowSpider(Spider):
    """
    新浪财经-财务报表-利润表
    http://money.finance.sina.com.cn/corp/go.php/vDOWN_BalanceSheet/displaytype/4/stockid/{stock}/ctrl/all.phtml
    """

    name = 'profit_flow'

    custom_settings = {
        'ITEM_PIPELINES': {
            'sunshine.spiders.stock.pipelines.StockInfoPipeline': 800
        },
        'SQLITE_PATH': "stock_db",
        'SQLITE_DBNAME': 'stock_info'
    }
    
    def __init__(self, *args, **kwargs):
        super(ProfitFlowSpider, self).__init__(*args, **kwargs)
        
    def start_requests(self):
        url = 'http://money.finance.sina.com.cn/corp/go.php/vDOWN_BalanceSheet/displaytype/4/stockid/{}/ctrl/all.phtml'
        secu_list = get_security_list()
        for d in secu_list:
            yield Request(url.format(d.code.split('.')[0]), callback=self.parse)
        
    def parse(self, response, **kwargs):
        df = pd.read_table(BytesIO(response.body), encoding="gb2312", header=None).iloc[:, :-2]
        df = df.T
        df.columns = df.iloc[0, :]
        df = df.iloc[1:, :]
        print(df.head(3))