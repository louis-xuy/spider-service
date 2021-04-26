#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: jaxon
@Time: 2020-12-24 11:08
"""

from gongshangguanli.ts_scrawer import NewsunshineClient

client = NewsunshineClient()

client.login("18502150276", "xj19880512")

session = client.getSession()
