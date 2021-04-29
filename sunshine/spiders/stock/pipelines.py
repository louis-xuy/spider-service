#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: jaxon
@Time: 2021-04-27 16:06
"""

import logging

from sunshine.pipelines.sqlitepipeline import SqlitePipeline
from sunshine.spiders.stock.model import StockInfo
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger(__name__)

class StockInfoPipeline(SqlitePipeline):
    
    def __init__(self, *args, **kwargs):
        super(StockInfoPipeline, self).__init__(*args, **kwargs)
        
    
    def process_item(self, item, spider):
        item_exists = self.session.query(StockInfo).filter_by(code=item['code']).first()
        if item_exists:
            logger.info('item {} is exists in DB.'.format(item['code']))
        else:
            new_item = StockInfo(**item)
            self.session.add(new_item)
            logger.info('New item {} added to DB.'.format(item['code']))


class StockDailyDataPipeline(SqlitePipeline):
    
    def __init__(self, *args, **kwargs):
        super(StockDailyDataPipeline, self).__init__(*args, **kwargs)
    
    def process_item(self, item, spider):
        item_exists = self.session.query(StockDailyDataPipeline).filter_by(code=item['code']).first()
        if item_exists:
            logger.info('item {} is exists in DB.'.format(item['code']))
        else:
            new_item = StockInfo(**item)
            self.session.add(new_item)
            logger.info('New item {} added to DB.'.format(item['code']))