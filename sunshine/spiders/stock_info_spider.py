
import scrapy
import time
import json
from sunshine.items.stockItems import StockInfoItem
from scrapy import Request, Spider
from urllib.parse import urlencode


class StockInfoSpider(Spider):
    """
    交易所股票基本信息获取
    """
    name = 'stock_info'
    
    def __init__(self, *args, **kwargs):
        super(StockInfoSpider, self).__init__(*args, **kwargs)
        # self.client = MongodbClient('localhost', '27017', db='stock_db')
    
    custom_settings = {
        'ITEM_PIPELINES': {
            'sunshine.pipelines.json.JsonPipeline': 800
        },
        'FilePath': "/data/stock_db/stock_info.json",
    }

    def start_requests(self):
        url = 'http://www.szse.cn/api/report/ShowReport/data?'
        indicator_map = {"A股列表": "tab1", "B股列表": "tab2", "CDR列表": "tab3", "AB股列表": "tab4"}
        for name, indicator in indicator_map.items():
            for pageno in range(1, 130, 1):
                params = {
                        "SHOWTYPE": "JSON",
                        "CATALOGID": "1110",
                        "PAGENO": str(pageno),
                        "TABKEY": indicator,
                        "random": "0.013838108061339227",
                    }
                yield Request(url+urlencode(params), meta={'type': name}, callback=self.parse_sz)

        ## 上海交易所
        indicator_map = {"主板A股": "1", "主板B股": "2", "科创板": "8"}
        url = "http://query.sse.com.cn/security/stock/getStockListData2.do"
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
                    "pageHelp.pageSize": "5000",
                    "pageHelp.pageNo": "1",
                    "pageHelp.endPage": "11",
                    "_": int(round(time.time() * 1000))
            }
            yield Request(url+urlencode(params), callback=self.parse, meta={'type': name}, headers=headers)
        
        
        
            
    def parse(self, response):
        # 股票信息
        # 股票tick数据
        _type = response.meta['type']
        text_data = response.text
        json_data = json.loads(text_data[text_data.find("{"):-1])
        data = json_data.get('result')
        if data:
            for element in data:
                symbol = element.get('COMPANY_CODE')
                listed_date = element.get('LISTING_DATE')
                url = 'http://query.sse.com.cn/commonQuery.do?jsonCallBack=jsonpCallback4159&isPagination=false&sqlId=COMMON_SSE_ZQPZ_GP_GPLB_C&productid={}&_={}'
                yield Request(url.format(symbol, int(round(time.time() * 1000))), meta={'listed_date':listed_date, 'type':_type}, callback=self.parse_info_sh)
                
            
    def parse_sz(self, response):
        _type = response.meta['type']
        text_data = response.text
        j_list = json.loads(text_data)
        for e in j_list:
            for stock_info in e.get('data',[]):
                stock_code = stock_info.get('agdm')
                url = 'http://www.szse.cn/api/report/index/companyGeneralization?random=0.046565225009869815&secCode={}'.format(stock_code)
                yield Request(url, meta={'type':_type}, callback=self.parse_info_sz)

    
    def parse_info_sh(self, response):
        _type = response.meta['type']
        listed_date = response.meta['listed_date']
        text_data = response.text
        j_list = json.loads(text_data[text_data.find("{"):-1])
        data = j_list.get('result')
        if data:
            stock_info = StockInfoItem()
            stock_info['code'] = data['SECURITY_CODE_A'] + '.XSHG'
            stock_info['fullname'] = data['FULLNAME']
            stock_info['enname'] = data['FULL_NAME_IN_ENGLISH']
            stock_info['symbol'] = data['COMPANY_ABBR']
            stock_info['address'] = data['COMPANY_ADDRESS']
            stock_info['listed_date'] = listed_date
            stock_info['de_listed_date'] = '0000-00-00'
            stock_info['sector_code_name'] = data['SSE_CODE_DESC']
            stock_info['industry_name'] = data['CSRC_GREAT_CODE_DESC']
            stock_info['board_type'] = _type
            stock_info['status'] = data['STATE_CODE_A_DESC']
            stock_info['province'] = data['AREA_NAME_DESC']
            stock_info['exchange'] = 'XSHG'
            stock_info['type'] = 'CS'
            stock_info['trading_hours'] = '09:31-11:30,13:00-15:00'
            #stock_info['created_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            yield stock_info
    
    def parse_info_sz(self, response):
        _type = response.meta['type']
        data = json.loads(response.text).get('data', None)
        if data:
            stock_info = StockInfoItem()
            stock_info['code'] = data['agdm']+'.XSHE'
            stock_info['fullname'] = data['gsqc']
            stock_info['enname'] = data['ywqc']
            stock_info['symbol'] = data['agjc']
            stock_info['address'] = data['zcdz']
            stock_info['listed_date'] = data['agssrq']
            stock_info['de_listed_date'] = '0000-00-00'
            stock_info['sector_code_name'] = data['sshymc']
            stock_info['industry_name'] = ''
            stock_info['board_type'] = _type
            stock_info['status'] = ''
            stock_info['area'] = data['dldq']
            stock_info['province'] = data['sheng']
            stock_info['city'] = data['shi']
            stock_info['exchange'] = 'XSHE'
            stock_info['type'] = 'CS'
            stock_info['round_lot'] = 100
            stock_info['trading_hours'] = '09:31-11:30,13:00-15:00'
            # stock_info['created_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            yield stock_info


class IndexInfoSpider(Spider):
    name = 'index_info'

    def __init__(self, *args, **kwargs):
        super(IndexInfoSpider, self).__init__(*args, **kwargs)

    custom_settings = {
        'ITEM_PIPELINES': {
            'sunshine.pipelines.json.JsonPipeline': 800
        },
        'FilePath': "/data/stock_db/stock_info.json",
    }

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


# TODO 指数成分数据
