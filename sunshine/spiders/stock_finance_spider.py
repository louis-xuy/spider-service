#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: jaxon
@Time: 2021-04-08 18:50
"""

import pandas as pd
import requests
from io import BytesIO
from scrapy import Request, Spider

class StockFinancialReportSinaSpider(Spider):
    """
    新浪财经-财务报表-三大报表
    https://vip.stock.finance.sina.com.cn/corp/go.php/vFD_BalanceSheet/stockid/600004/ctrl/part/displaytype/4.phtml
    :param stock: 股票代码
    :type stock: str
    :param symbol: choice of {"资产负债表", "利润表", "现金流量表"}
    :type symbol:
    :return: 新浪财经-财务报表-三大报表
    :rtype: pandas.DataFrame
    """
    
    name = 'stock_financial_report_sina'
    
    def __init__(self,*args, **kwargs):
        super(StockFinancialReportSinaSpider, self).__init__(*args, **kwargs)
        # 获取股票列表

    def start_requests(self):
        url = 'http://money.finance.sina.com.cn/corp/go.php/vDOWN_BalanceSheet/displaytype/4/stockid/{}/ctrl/all.phtml'
        r = requests.get(url.format('600004'))
        temp_df = pd.read_table(BytesIO(r.content), encoding="gb2312", header=None).iloc[:, :-2]
        print(temp_df.columns)
        temp_df = temp_df.T
        temp_df.columns = temp_df.iloc[0, :]
        temp_df = temp_df.iloc[1:, :]
        temp_df.index.name = None
        temp_df.columns.name = None