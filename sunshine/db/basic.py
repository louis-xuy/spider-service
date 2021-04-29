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

settings = get_project_settings()

Base = declarative_base()

def get_engine():
    # pymysql utf8mb4/mysqlconnector utf8
    connect_str = "sqlite:////data/stock_db/stock.db"
    engine = create_engine(connect_str)
    return engine


def create_forum_table(engine):
    Base.metadata.create_all(engine)
    


__all__ = ['get_engine', 'create_forum_table', 'Base', 'settings']