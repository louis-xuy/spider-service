#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: jaxon
@Time: 2021-04-27 16:06
"""


from sunshine.pipelines.mysqlpipeline import MysqlPipeline
from sunshine.models import Base, engine,loadSession
from sunshine.models.stock_model import StockInfo, TradeDays
from loguru import logger



class TradeDaysPipeline(MysqlPipeline):

    def __init__(self, *args, **kwargs):
        Base.metadata.create_all(engine)
        super(TradeDaysPipeline, self).__init__(*args, **kwargs)

    def process_item(self, item, spider):
        logger.info('add item:{} into db'.format(item))
        if self.session.query(TradeDays).filter_by(cal_date=item['calendar']).first():
            logger.info('item {} is exists in DB.'.format(item['calendar']))
        else:
            new_item = TradeDays(**item)
            self.session.add(new_item)
            self.session.commit()
            logger.info('add {} to db'.format(item['calendar']))


class StockInfoPipeline(MysqlPipeline):
    
    def __init__(self, *args, **kwargs):
        Base.metadata.create_all(engine)
        super(StockInfoPipeline, self).__init__(*args, **kwargs)

        
    
    def process_item(self, item, spider):

        item_exists = self.session.query(StockInfo).filter_by(code=item['code']).first()
        if item_exists:
            logger.info('item {} is exists in DB.'.format(item['code']))
        else:
            new_item = StockInfo(**item)
            self.session.add(new_item)
            logger.info('New item {} added to DB.'.format(item['code']))
            self.session.commit()



class StockDailyDataPipeline(MysqlPipeline):

    def __init__(self, *args, **kwargs):
        super(StockDailyDataPipeline, self).__init__(*args, **kwargs)
    
    def process_item(self, item, spider):
        session = loadSession()
        item_exists = session.query(StockDailyDataPipeline).filter_by(code=item['code']).first()
        if item_exists:
            logger.info('item {} is exists in DB.'.format(item['code']))
        else:
            new_item = StockInfo(**item)
            session.add(new_item)
            logger.info('New item {} added to DB.'.format(item['code']))

class StockIndustryNamePipeline(MysqlPipeline):
    
    def __init__(self, *args, **kwargs):
        super(StockIndustryNamePipeline, self).__init__(*args, **kwargs)
    
    def process_item(self, item, spider):
        session = loadSession()
        try:
            stock_info = session.query(StockInfo).filter(StockInfo.code.like(item['code']))
            stock_info.industry_name = item['industry_name']
        except Exception as e:
            logger.error("insert item {} fail !".format(item['code']))
    
    "P_TYPE['http'] + DOMAINS['oss'] + '/tsdata/%sall%s.csv'" \
    