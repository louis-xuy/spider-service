#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: jaxon
@Time: 2021-04-28 17:04
"""


from scrapy import Request, Spider


class SuspendedDays(Spider):
    """
    停牌信息获取
    """
    name = 'suspended_days'
    
    custom_settings = {
        'ITEM_PIPELINES': {
            'sunshine.spiders.stock.pipelines.StockInfoPipeline': 800
        },
        'SQLITE_PATH': "stock_db",
        'SQLITE_DBNAME': 'suspended_days'
    }
    
    def __init__(self, *args, **kwargs):
        super(SuspendedDays, self).__init__(*args, **kwargs)

    