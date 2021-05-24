import datetime
import json

from scrapy import Request, Spider
from sunshine.settings import ts_token
from sunshine.items.stockItems import TradeDaysItem
from loguru import logger


class TradeDays(Spider):
    name = 'trade_days'

    custom_settings = {
        'ITEM_PIPELINES': {
            'sunshine.pipelines.stock_pipeline.TradeDaysPipeline': 800
        },
    }

    def __init__(self, *args, **kwargs):
        super(TradeDays, self).__init__(*args, **kwargs)



    def start_requests(self, *args, **kwargs):
        year = datetime.date.today().year
        url = 'http://www.szse.cn/api/report/exchange/onepersistenthour/monthList?month={}-{}&random=0.003920882100288736'
        start_year = int(getattr(self, 'start_year')) if getattr(self, 'start_year') else 2001
        end_year = int(getattr(self, 'end_year')) if getattr(self, 'end_year') else year
        logger.info('crawl calendar between {} and {}'.format(start_year, end_year))
        while start_year < end_year:
            for month in range(1, 13):
                logger.info('request {}-{} calendar'.format(start_year, month))
                yield Request(url.format(start_year, month), callback=self.parse)
            start_year = start_year+1

    def parse(self, response, **kwargs):
        item = dict()
        res_json = json.loads(response.body)
        data = res_json.get('data', {})
        for v in data:
            item['exchange'] = 'SZSE'
            item['cal_date'] = v['jyrq']
            item['is_open'] = v['jybz']
            yield item