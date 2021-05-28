import time
import json
from io import BytesIO
import pandas as pd
from sunshine.models import loadSession
from sunshine.models.stock_model import StockInfo
from sunshine.items.stockItems import StockInfoItem
from scrapy import Request, Spider
from urllib.parse import urlencode

from loguru import logger

class StockInfoSZSpider(Spider):
    """
    交易所股票基本信息获取
    """
    name = 'stock_info_sz'

    custom_settings = {
        'ITEM_PIPELINES': {
            'sunshine.pipelines.stock_pipeline.StockInfoPipeline': 800
        },
        'SQLITE_PATH': "stock",
        'SQLITE_DBNAME': 'stock_info'
    }
    
    def __init__(self, *args, **kwargs):
        super(StockInfoSZSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        """
            深圳证券交易所-股票列表
            http://www.szse.cn/market/product/stock/list/index.html
            :param indicator: choice of {"A股列表", "B股列表", "CDR列表", "AB股列表"}
            :type indicator: str
            :return: 指定 indicator 的数据
            :rtype: pandas.DataFrame
            """
        url = "http://www.szse.cn/api/report/ShowReport?"
        indicator_map = {"MainBoard": "tab1"}
        for name, indicator in indicator_map.items():
            params = {
                "SHOWTYPE": "xlsx",
                "CATALOGID": "1110",
                "TABKEY": indicator,
                "random": "0.6935816432433362",
            }
            yield Request(url+urlencode(params), callback=self.parse_item, meta={'type': name})
    
    def parse_item(self, response):
        _type = response.meta['type']
        df = pd.read_excel(BytesIO(response.body), engine="openpyxl")
        if df.shape[0] > 0:
            for index, data in df.iterrows():
                stock_info = StockInfoItem()
                stock_info['code'] = str(data['A股代码']).rjust(6, '0')+'.XSHE'
                stock_info['fullname'] = data['公司全称']
                stock_info['symbol'] = data['A股简称']
                stock_info['listed_date'] = data['A股上市日期']
                stock_info['de_listed_date'] = '0000-00-00'
                stock_info['industry_name'] = ''
                stock_info['board_type'] = _type
                stock_info['status'] = ''
                stock_info['exchange'] = 'XSHE'
                stock_info['type'] = 'CS'
                stock_info['round_lot'] = 100
                stock_info['trading_hours'] = '09:31-11:30,13:00-15:00'
                # stock_info['created_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                yield stock_info


class StockInfoSHSpider(Spider):
    """
        上海证券交易所-股票列表
        http://www.sse.com.cn/assortment/stock/list/share/
        :param indicator: choice of {"主板A股": "1", "主板B股": "2", "科创板": "8"}
        :type indicator: str
        :return: 指定 indicator 的数据
        """
    name = 'stock_info_sh'
    
    custom_settings = {
        'ITEM_PIPELINES': {
            'sunshine.pipelines.stock_pipeline.StockInfoPipeline': 800
        },
        'SQLITE_PATH': "stock_db",
        'SQLITE_DBNAME': 'stock_info'
    }
    
    def __init__(self, *args, **kwargs):
        super(StockInfoSHSpider, self).__init__(*args, **kwargs)
    
    def start_requests(self):
        
        indicator_map = {"MainBoard": "1", "GEM": "8"}
        url = "http://query.sse.com.cn/security/stock/getStockListData2.do?"
        headers = {
            "Host": "query.sse.com.cn",
            "Pragma": "no-cache",
            "Referer": "http://www.sse.com.cn/assortment/stock/list/share/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
        }
        for name, indicator in indicator_map.items():
            params = {
                "jsonCallBack": "jsonpCallback61921",
                "isPagination": "true",
                "stockCode": "",
                "csrcCode": "",
                "areaName": "",
                "stockType": indicator,
                "pageHelp.cacheSize": "1",
                "pageHelp.beginPage": "1",
                "pageHelp.pageSize": "2000",
                "pageHelp.pageNo": "1",
                "pageHelp.endPage": "11",
                "_": int(round(time.time() * 1000))
            }
            yield Request(url + urlencode(params), callback=self.parse_item, meta={'type': name}, headers=headers)
        
    def parse_item(self, response):
        _type = response.meta['type']
        text_data = response.text
        j_list = json.loads(text_data[text_data.find("{"):-1])
        datas = j_list.get('result')
        if datas:
            for data in datas:
                stock_info = StockInfoItem()
                stock_info['code'] = data['SECURITY_CODE_A'] + '.XSHG'
                stock_info['symbol'] = data['COMPANY_ABBR']
                stock_info['listed_date'] = data['LISTING_DATE']
                stock_info['de_listed_date'] = '0000-00-00'
                #stock_info['sector_code_name'] = data['SSE_CODE_DESC']
                #stock_info['industry_name'] = data['CSRC_GREAT_CODE_DESC']
                stock_info['board_type'] = _type
                #stock_info['status'] = data['STATE_CODE_A_DESC']
                #stock_info['province'] = data['AREA_NAME_DESC']
                stock_info['exchange'] = 'XSHG'
                stock_info['type'] = 'CS'
                stock_info['trading_hours'] = '09:31-11:30,13:00-15:00'
                # stock_info['created_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                yield stock_info
    

class IndexInfoSpider(Spider):
    
    name = 'index_info'

    custom_settings = {
        'ITEM_PIPELINES': {
            'sunshine.pipelines.stock_pipeline.StockInfoPipeline': 800
        },
        'SQLITE_PATH': "stock_db",
        'SQLITE_DBNAME': 'stock_info'
    }

    def __init__(self, *args, **kwargs):
        super(IndexInfoSpider, self).__init__(*args, **kwargs)


    def start_requests(self):
        url = 'https://www.ricequant.com/doc/rqdata/python/indices-dictionary.html'
        yield Request(url, callback=self.parse)
    
    def parse(self, response, **kwargs):
        links = response.xpath('//div/table/tbody/tr')
        for link in links:
            index_info = StockInfoItem()
            index_info['code'] = code = link.xpath("./td[1]//text()").get()
            index_info['symbol'] = link.xpath("./td[2]//text()").get()
            index_info['fullname'] = link.xpath("./td[3]//text()").get()
            index_info['listed_date'] = link.xpath("./td[4]//text()").get()
            index_info['de_listed_date'] = link.xpath("./td[5]//text()").get()
            index_info['trading_hours'] = '09:31-11:30,13:01-15:00'
            index_info['exchange'] = index_info['code'].split('.')[1]
            index_info['type'] = 'INDX'
            index_info['round_lot'] = 1.0
            yield index_info


# TODO 股票行业获取
class StockIndustrySpider(Spider):
    
    name = 'update_industry_name'
    
    custom_settings = {
        'ITEM_PIPELINES': {
            'sunshine.pipelines.stock_pipeline.StockIndustryNamePipeline': 800
        },
    }
    
    def __init__(self, *args, **kwargs):
        super(StockIndustrySpider, self).__init__(*args, **kwargs)
    
    def start_requests(self):
        ## 获取基本信息
        url = 'http://f10.eastmoney.com/CompanySurvey/CompanySurveyAjax?code={}{}'
        session = loadSession()
        stock_info_list = session.query(StockInfo).filter(StockInfo.type=='CS').all()
        for stock_info_item in stock_info_list:
            if not stock_info_item.industry_name or stock_info_item.industry_name:
                _type ={'XSHG':'SH', 'XSHE':'SZ'}.get(stock_info_item.exchange)
                code = stock_info_item.code.split('.')[0]
                yield Request(url.format(_type, code),meta={'code': stock_info_item.code}, callback=self.parse)

    def parse(self, response, **kwargs):
        res = response.text
        data = json.loads(res)
        if data:
            basic = data.get('jbzl',{}).get('sszjhhy',None)
            industry_name = basic.split('-')[-1]
            code = response.meta['code']
            yield {'code': code, 'industry_name': industry_name}
            

# TODO 股票板块


# TODO 股票概念

# TODO 股票交易日期获取


# TODO 指数成分数据
class IndexComponentsSpider(Spider):
    name = 'index_components'
    
    custom_settings = {
        'ITEM_PIPELINES': {
            'sunshine.spiders.stock.pipelines.StockInfoPipeline': 800
        },
    }
    
    def __init__(self, *args, **kwargs):
        super(IndexComponentsSpider, self).__init__(*args, **kwargs)
    
    def start_requests(self):
        pass