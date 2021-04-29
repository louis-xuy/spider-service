#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Time    : 2018/8/11 1:14

__author__ = 'xujiang@baixing.com'

#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import sqlalchemy
from sqlalchemy import *
from sqlalchemy.orm import *
import sqlalchemy.types
import logging
import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String


Base = declarative_base()

# 股票基本信息
class ListedStockInfo(Base):
    __tablename__ = 'listed_stock_info'

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
    

class MyDB(object):
    def __init__(self):
        logging.info("database init")
        self.engine = create_engine("sqlite:///toutiao.db", pool_recycle=3600, echo=False)
        self.make_session = sessionmaker(bind=self.engine)
        self.metadata = MetaData(self.engine)

    def create_tables(self):
        Base.metadata.create_all(self.engine)
        logging.info("create database tables")


mydb = MyDB()
mydb.create_tables()