#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: jaxon
@Time: 2021-04-27 21:13
"""
import io

import numpy
import pandas as pd
from datetime import datetime, time

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
    t = time.strptime(date_string, "%Y-%m-%d")
    y, m, d = t[0:3]
    return numpy.datetime64(datetime(y, m, d))
    

class dailyStock163Spider(Spider):
    """历史行情数据获取"""
    
    name = "stock_daily_163"

    custom_settings = {
        'ITEM_PIPELINES': {
            'sunshine.spiders.stock.pipelines.StockInfoPipeline': 800
        },
        'SQLITE_PATH': "stock_db",
        'SQLITE_DBNAME': 'daily_stock'
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
        try:
            df = pd.read_csv(io.BytesIO(response.body), encoding='GB2312', na_values='None')
            # 股票数据
            for index, row in df.iterrows():
                stock_daily = DailyStockData()
                stock_daily['code'] = item.code
                stock_daily['datetime'] = string2datetime64(row['日期'])
                stock_daily['open'] = row['开盘价']
                stock_daily['high'] = row['最高价']
                stock_daily['low'] = row['最低价']
                stock_daily['close'] = row['收盘价']
                stock_daily['pre_close'] = row['前收盘']
                stock_daily['volume'] = row['成交量']
                stock_daily['money'] = row['成交金额']
                stock_daily['turnover'] = row['换手率']
                yield stock_daily
        except Exception as e:
            self.logger.exception('error when getting k data url={} error={}'.format(response.url, e))
        
        
# TODO 停牌信息




