#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: jaxon
@Time: 2021-04-27 21:13
"""
import io

import numpy
import pandas as pd
from datetime import datetime
import time

from scrapy import Spider, Request

from sunshine.models import loadSession
from sunshine.models.stock_model import StockInfo, DailyStockData


def get_security_list():
    session = loadSession()
    d = session.query(StockInfo).all()
    return d


def string2datetime64(date_string):
    """
    :param date_string: y-m-d
    :return:
    """
    t = datetime.strptime(date_string, "%Y-%m-%d")
    return t.strftime('%Y%m%d')+'000000'

class dailyStock163Spider(Spider):
    """历史行情数据获取"""
    
    name = "stock_daily_163"

    custom_settings = {
        'ITEM_PIPELINES': {
            'sunshine.pipelines.stock_pipeline.StockDailyDataPipeline': 800
        },
    }
    
    def __init__(self, *args, **kwargs):
        super(dailyStock163Spider, self).__init__(*args, **kwargs)
        
    def start_requests(self):
        start_date = getattr(self, "start_date", None)
        end_date = getattr(self, "end_date", None)
        for item in get_security_list():
            if not start_date:
                start_date = item.listed_date.replace('-', '')
            if not end_date:
                end_date = datetime.today().strftime('%Y%m%d')
            if item.exchange == 'XSHG':
                exchange_flag = 0
            else:
                exchange_flag = 1

            url = 'http://quotes.money.163.com/service/chddata.html?code={}{}&start={}&end={}'.format(
                exchange_flag, item.code.split('.')[0], start_date, end_date
            )
            yield Request(url=url, meta={'item': item},
                              callback=self.parse_item)
    
    def parse_item(self, response):
        item = response.meta['item']
        code = item.code
        try:
            df = pd.read_csv(io.BytesIO(response.body), encoding='GB2312', na_values='None')
            # 股票数据
            for index, row in df.iterrows():
                yield {
                    'code': code,
                    'datetime': string2datetime64(row['日期']),
                    'open': row['开盘价'],
                    'high': row['最高价'],
                    'low': row['最低价'],
                    'close': row['收盘价'],
                    'pre_close': row['前收盘'],
                    'volume': row['成交量'],
                    'money': row['成交金额'],
                    'turnover': row['换手率']
                }

        except Exception as e:
            self.logger.exception('error when getting k data url={} error={}'.format(response.url, e))
        
        
# TODO 停牌信息




