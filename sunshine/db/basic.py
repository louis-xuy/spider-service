#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: jaxon
@Time: 2021-04-27 10:33
"""

# basic.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from scrapy.utils.project import get_project_settings
from sqlalchemy.orm import sessionmaker

settings = get_project_settings()

Base = declarative_base()

def get_session():
    # pymysql utf8mb4/mysqlconnector utf8
    connect_str = "sqlite:////data/stock_db/stock.db"
    engine = create_engine(connect_str)
    create_forum_table(engine)
    session = sessionmaker(bind=engine)
    return session()

def create_forum_table(engine):
    Base.metadata.create_all(engine)
    


__all__ = ['get_session', 'create_forum_table', 'Base', 'settings']