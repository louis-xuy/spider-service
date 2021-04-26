#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: jaxon
@Time: 2021-02-17 14:00
"""

import io
import os
import re
import json
import time
import math

import h5py
import pandas as pd
from datetime import datetime
from urllib.parse import urlencode

import requests
from scrapy import Request, Spider
from sunshine.items.stockItems import StockDailyTrade,StockNewsItem


def convert_date_to_int(dt):
    t = dt.year * 10000 + dt.month * 100 + dt.day
    t *= 1000000
    return t

def new_round(_float, _len):
    if isinstance(_float, float):
        if str(_float)[::-1].find('.') <= _len:
            return _float
        if str(_float)[-1] == '5':
            return round(float(str(_float)[:-1]+'6'), _len)
        else:
            return round(_float, _len)
    else:
        return round(_float, _len)
    
class GenerateDayBarTask():
    def __call__(self, df, path, fields, **kwargs):
        order_book_ids = set(df.order_book_id)
        with h5py.File(path, 'w') as h5:
            if not (df is None or df.empty):
                df.reset_index(inplace=True)
                df['datetime'] = [convert_date_to_int(d) for d in df['date']]
                del df['date']
                df.set_index(['order_book_id', 'datetime'], inplace=True)
                df.sort_index(inplace=True)
                for order_book_id in order_book_ids:
                    print(order_book_id)
                    print(df.loc[order_book_id].to_records()[:3])
                    h5.create_dataset(order_book_id, data=df.loc[order_book_id].to_records(), **kwargs)


def get_security_list():
    import pickle
    
    with open('/Users/jaxon/.rqalpha/bundle/instruments.pk', 'rb') as f:
        datas = pickle.load(f)
        return [d for d in datas if d['type']=='CS' and d['status']== 'Active']



class MoneySpider(Spider):
    """
    东方财富网新闻数据爬取
    """
    
    name = 'research_report_money'
    allowed_domains = ['finance.eastmoney.com']
    start_urls = []
    base_url = 'http://finance.eastmoney.com/news/cgsxw_{}.html'
    for i in range(1, 50):
        start_urls.append(base_url.format(i))
    
    def parse(self, response):
        article_list = response.xpath('//ul[@id="newsListContent"]/li')
        for article in article_list:
            detail_url = article.xpath('.//a/@href').extract_first()
            item = StockNewsItem()
            abstract1 = article.xpath('.//p[@class="info"]/@title')
            abstract2 = article.xpath('.//p[@class="info"]/text()')
            item['abstract'] = abstract1.extract_first().strip() if len(
                abstract1) else abstract2.extract_first().strip()
            yield Request(detail_url, callback=self.parse1, meta={'item': item})
    
    def parse1(self, response):
        item = response.meta['item']
        item['website'] = '东方财富网'
        item['url'] = response.url
        item['title'] = response.xpath('//div[@class="newsContent"]/h1/text()').extract_first()
        soup = bs(response.text, 'lxml')
        p_list = soup.select('div#ContentBody p')
        item['content'] = '\n'.join([p.text.strip() for p in p_list]).strip()
        item['datetime'] = response.xpath('//div[@class="time-source"]/div[@class="time"]/text()').extract_first()
        item['original'] = response.xpath('//div[@class="source data-source"]/@data-source').extract_first()
        item['author'] = response.xpath('//p[@class="res-edit"]/text()').extract_first().strip()
        yield item


class MoneyIndustryReseachReportSpider(Spider):
    """
    东方财富网 行研下载
    """
    name = 'stock_money_reseach_report'
    custom_settings = {
        'ITEM_PIPELINES': {
            'sunshine.pipelines.reseach_report.StockReseachReportFile': 800
        },
        'FILES_STORE': '/Users/jaxon/Documents/stock/ReseachReport'
    }
    
    def start_requests(self):
        ## 行业研究数据
        self.url = 'http://reportapi.eastmoney.com/report/list?cb=datatable3646054&industryCode=*&pageSize=50&industry=*&rating=*&ratingChange=*&beginTime=2019-02-17&endTime=2021-02-17&pageNo={0}&fields=&qType=1&orgCode=&rcode=&p={0}&pageNum={0}&_=1613491568500'
        self.page = 1
        yield Request(self.url.format(self.page), callback=self.parse)
    
    def parse(self, response, **kwargs):
        ret = response.text
        ret = re.findall("datatable\d{7}\((.*)\)", ret)[0]
        datas = json.loads(ret)
        _size = datas.get("size")
        _data = datas.get("data")
        if _data:
            for i in _data:
                infoCode = i['infoCode']
                industryName = i['industryName']
                yield Request('http://data.eastmoney.com/report/zw_industry.jshtml?infocode={}'.format(infoCode),
                              meta={'industryName': industryName}, callback=self.parse_item)
            self.page = self.page+1
            yield Request(self.url.format(self.page), callback=self.parse)
    
    def parse_item(self, response, **kwargs):
        industryName = response.meta['industryName']
        pdf_url = response.xpath('//a[@class="pdf-link"]/@href').get(0)
        item = StockNewsItem()
        item['file_urls'] = [pdf_url]
        item['industryName'] = industryName
        yield item

class TencentIndustryReseachReportSpider(Spider):
    name = 'stock_tencent_reseach_report'
    custom_settings = {
        'ITEM_PIPELINES': {
            'sunshine.pipelines.reseach_report.StockReseachReportFile': 800
        },
        'FILES_STORE': '/Users/jaxon/Documents/stock/ReseachReport'
    }
    
    def start_requests(self):
        ## 行业研究数据
        self.url = 'http://reportapi.eastmoney.com/report/list?cb=datatable3646054&industryCode=*&pageSize=50&industry=*&rating=*&ratingChange=*&beginTime=2019-02-17&endTime=2021-02-17&pageNo={0}&fields=&qType=1&orgCode=&rcode=&p={0}&pageNum={0}&_=1613491568500'
        yield Request(self.url.format(1), callback=self.parse)



class wangyiStockSpider(Spider):
    """
    网易财经k线数据获取
    """
    name = "stock_daily_trade_wangyi"
    
    def __init__(self, *args, **kwargs):
        super(wangyiStockSpider, self).__init__(*args, **kwargs)
        self.headers = {
            'Referer': 'http://quotes.money.163.com/',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36'
        }
        self.stock_list = pd.read_csv("stock_list.csv")
    
    def start_requests(self):
        
        for index, row in self.stock_list.iterrows():
            stock_url = 'http://quotes.money.163.com/trade/lsjysj_{}.html'.format(row.code.split('.')[0])
            print("stock url :{}".format(stock_url))
            respones = requests.get(stock_url, headers=self.headers).text
            soup = bs(respones, 'lxml')
            start_time = soup.find('input', {'name': 'date_start_type'}).get('value').replace('-', '')  # 获取起始时间
            # start_time = '20200101'
            end_time = soup.find('input', {'name': 'date_end_type'}).get('value').replace('-', '')  # 获取结束时间
            time.sleep(math.random.choice([1, 2]))
            
            download_url = "{}&start={}&end={}&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP".format(
                row.download_url, start_time, end_time)
            data = requests.get(download_url, headers=self.headers)
            with open('/data/db/stock_daily/{}.csv'.format(row.code), 'wb') as f:  # 保存数据
                for chunk in data.iter_content(chunk_size=10000):
                    if chunk:
                        f.write(chunk)
                print("{}数据已经下载完成".format(row.code))


class EastMoneyStockSpider(Spider):
    """
    东方财富获取最新股票日线数据

    """
    name = 'stock_daily_trade_money'
    custom_settings = {
        'ITEM_PIPELINES': {
            'sunshine.pipelines.csv.CsvPipeline': 800
        }
    }
    
    def __init__(self, *args, **kwargs):
        super(EastMoneyStockSpider, self).__init__(*args, **kwargs)
        self._today = datetime.date.today()
        self.page = 1
    
    def start_requests(self):
        ## 上海A股
        self.SH_URL = 'http://4.push2.eastmoney.com/api/qt/clist/get?cb=jQuery11240355804879697194_1613125162111&pn={}&pz=20000&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:1+t:2,m:1+t:23&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152&_=1613125162165'
        yield Request(self.SH_URL.format(self.page), meta={'type': '.XSHG'}, callback=self.parse_item)
        ## 深圳A股
        self.SZ_URL = 'http://4.push2.eastmoney.com/api/qt/clist/get?cb=jQuery11240355804879697194_1613125162111&pn={}&pz=20000&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:0+t:6,m:0+t:13,m:0+t:80&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152&_=1613125162125'
        print('start request...')
        yield Request(self.SZ_URL.format(self.page), meta={'type': '.XSHE'}, callback=self.parse_item)
    
    def parse_item(self, response):
        item = StockDailyTrade()
        content = response.text
        type = response.meta['type']
        print(content)
        ret = re.findall("jQuery\d{20}_\d{13}\((.*)\)", content)[0]
        print(ret)
        datas = json.loads(ret)
        if datas.get('data'):
            _total = datas.get('data').get('total')
            _list = datas.get("data").get('diff')
            for i in _list:
                item['SecuCode'] = i.get('f12') + '.' + type
                item['SecuAbbr'] = i.get('f14')
                item['Open'] = i.get('f17')
                item['High'] = i.get('f15')
                item['Low'] = i.get('f16')
                item['Last'] = i.get('f2')
                item['ChgRate'] = i.get('f3')  # 涨跌幅 chg_rate(%)
                item['Volume'] = i.get('f5')
                item['Amount'] = i.get('f6')
                item['TradingDay'] = str(self._today)
                yield item
            # if response.meta['type'] == 'sh':
            #     self.sh_page = self.sh_page + 1
            #     yield Request(self.SH_URL.format(self.sh_page), meta={'type': 'sh'}, callback=self.parse_item)
            # else:
            #     self.sz_page = self.sz_page + 1
            #     yield Request(self.SZ_URL.format(self.sz_page), meta={'type': 'sz'}, callback=self.parse_item)



class dailyStock163Spider1(Spider):
    
    
    """历史行情数据获取"""

    name = "stock_daily_163"
    
    def __init__(self, *args, **kwargs):
        super(dailyStock163Spider1, self).__init__(*args, **kwargs)
        
        self.path = '/Users/jaxon/.rqalpha/bundle'
        
        self.genDayBar = GenerateDayBarTask()

    def get_k_data_url(self, exchange, code, start, end):
        return 'http://quotes.money.163.com/service/chddata.html?code={}{}&start={}&end={}'.format(
            exchange, code, start, end)
    
    # 指定日期的话，是用来抓增量数据的
    # 如果需要代理请打开
    # @random_proxy
    def yield_request(self, item, start_date=None, end_date=None):
        data_path = self.path + '/stocks.csv'
        if start_date:
            start = start_date
        else:
            start = item['listed_date'].replace('-', '')

        if end_date:
            end = end_date
        else:
            end = datetime.today().strftime('%Y%m%d')

        if item['exchange'] == 'XSHG':
            exchange_flag = 0
        else:
            exchange_flag = 1
        url = self.get_k_data_url(exchange_flag, item['order_book_id'].split('.')[0], start, end)
        yield Request(url=url, meta={'path': data_path, 'item': item},
                          callback=self.download_day_k_data)
    
    def start_requests(self):
        item = getattr(self, "security_item", '')
        start_date = getattr(self, "start_date")
        end_date = getattr(self, "end_date")
        
        for item in get_security_list():
            for request in self.yield_request(item):
                yield request

    def download_day_k_data(self, response):
        print(response.url)
        path = response.meta['path']
        item = response.meta['item']
        try:
            # 已经保存的csv数据
            if os.path.exists(path):
                saved_df = pd.read_csv(path, dtype=str)
            else:
                saved_df = pd.DataFrame()
            df = pd.read_csv(io.BytesIO(response.body), encoding='GB2312', na_values='None')
            df['order_book_id'] = item['order_book_id']
            # 指数数据
            if item['type'] == 'index':
                INDEX_FIELDS = ['order_book_id', 'date', 'low', 'open', 'close', 'preClose', 'high', 'volume', 'amount']
                df = df.loc[:,
                     ['order_book_id', '日期', '最低价', '开盘价', '收盘价', '前收盘', '最高价', '成交量', '成交金额']]
                df.columns = INDEX_FIELDS
            # 股票数据
            else:
                STOCK_FIELDS = ['order_book_id', 'date', 'open', 'close', 'high', 'low', 'pre_close', 'volume', 'amount', 'turnover']
                
                df = df.loc[:,['order_book_id', '日期', '开盘价', '收盘价', '最高价', '最低价', '前收盘', '成交量', '成交金额', '换手率']]
                df.columns = STOCK_FIELDS
                data_types_dict = {'open': float, 'close': float, 'high': float, 'low': float,'pre_close':float, 'volume': int,
                                   'amount': float, 'turnover': float}
                df = df.astype(data_types_dict)
            
            # 合并到当前csv中
            saved_df = saved_df.append(df, ignore_index=True)
            saved_df = saved_df.drop_duplicates(subset='date', keep='last')
            saved_df.date = pd.to_datetime(saved_df.date)
            self.genDayBar(saved_df, self.path+'/stock1.h5', [])
        except Exception as e:
            self.logger.exception('error when getting k data url={} error={}'.format(response.url, e))


class dailyIndexEM(Spider):
    """
        东方财富股票指数数据
        http://quote.eastmoney.com/center/hszs.html
        :param symbol: 带市场标识的指数代码
        :type symbol: str
        :return: 指数数据
        :rtype: pandas.DataFrame
    """
    
    def start_requests(self):
        # 获取指数代码：
        stocks = sorted(list(rqdatac.all_instruments().order_book_id))
        
        market_map = {"XSHE": "0", "XSHG": "1"}
        url = "http://push2his.eastmoney.com/api/qt/stock/kline/get"
        for stock in stocks:
            params = {
                "cb": "jQuery1124033485574041163946_1596700547000",
                "secid": f"{market_map[stock[-4:]]}.{stock[:6]}",
                "ut": "fa5fd1943c7b386f172d6893dbfba10b",
                "fields1": "f1,f2,f3,f4,f5",
                "fields2": "f51,f52,f53,f54,f55,f56,f57,f58",
                "klt": "101",  # 日频率
                "fqt": "0",
                "beg": "20100101",
                "end": "20220101",
                "_": "1596700547039",
            }
            yield Request()
