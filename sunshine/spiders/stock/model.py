#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: jaxon
@Time: 2021-04-27 11:14
"""


from sqlalchemy import Column, Integer, String, Float
from sunshine.db.basic import Base



# 股票基本信息
class StockInfo(dict, Base):
    __tablename__ = 'stock_info'

    # 表的结构:
    id = Column(Integer, primary_key=True)
    code = Column(String(16))
    industry_code = Column(String(10))
    market_tplus = Column(Integer)
    symbol = Column(String(16))
    special_type = Column(String(16))
    exchange = Column(String(16))
    status = Column(String(16))
    type = Column(String(16))
    listed_date = Column(String(16))
    de_listed_date = Column(String(16))
    sector_code_name = Column(String(16))
    abbrev_symbol = Column(String(16))
    sector_code = Column(String(50))
    round_lot = Column(Integer)
    trading_hours = Column(String(50))
    board_type = Column(String(50))
    industry_name = Column(String(16))
    trading_code = Column(String(5))
    fullname = Column(String(64))
    area = Column(String(16))
    total_capital = Column(Integer)
    current_capital = Column(Integer)

    def __init__(self, **items):
        for key in items:
            if hasattr(self, key):
                setattr(self, key, items[key])


class TradeDays(Base):
    __tablename__ = 'trade_days'
    
    id = Column(Integer, primary_key=True)
    exchange = Column(String(16))
    cal_date = Column(String(16))
    is_open = Column(String(16))


class DailyStockData(dict, Base):
    __tablename__ = 'daily_stock'
    
    id = Column(Integer, primary_key=True)
    code = Column(String(16))
    datetime = Column(String(16))
    open = Column(Float)
    close = Column(Float)
    low = Column(Float)
    high = Column(Float)
    pre_close = Column(Float)
    volume = Column(Float)
    money = Column(Float)
    turnover = Column(Float)
    
    def __init__(self, **items):
        for key in items:
            if hasattr(self, key):
                setattr(self, key, items[key])


class SuspendedDays(dict, Base):
    """停牌信息"""
    __tablename__ = 'suspended_days'
    
    id = Column(Integer, primary_key=True)
    code = Column(String(16))
    suspend_date = Column(String(16))
    suspend_timing = Column(String(16))
    suspend_type = Column(String(16))
    
    def __init__(self, **items):
        for key in items:
            if hasattr(self, key):
                setattr(self, key, items[key])
    

