#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: jaxon
@Time: 2021-04-29 14:40
"""

import pandas as ts

from sunshine.spiders.stock.model import TradeDays
from sunshine.db.basic import get_engine
from sqlalchemy.orm import sessionmaker


engine = get_engine()
Session = sessionmaker(bind=engine)
stock_session = Session()

ts.set_token('9e22ca2554f0f7275ba66c9483049a2f2a80be07b5cb9a3e91db8042')
pro = ts.pro_api()


def sync_trade_days(start_date='20100101', end_date='20990101'):
    """ 交易日同步"""
    df = pro.trade_cal(exchange='', start_date=start_date, end_date=end_date)
    for index, row in df.iterrows():
        stock_session.add(TradeDays(
            exchange=row['exchange'],
            cal_date=row['cal_date'],
            is_open=row['is_open']
        ))
        
if __name__ == "__main__":
    sync_trade_days()
