#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: jaxon
@Time: 2021-04-10 22:04
"""

from pymongo import MongoClient


class MongodbClient(object):
    def __init__(self, host, port, **kwargs):
        self.name = ""
        self._db_name = kwargs.pop('db')
        self.client = MongoClient(host, port, **kwargs)
        self.db = self.client[self._db_name]

    def changeTable(self, name):
        self.name = name

    def get(self):
        data = self.db[self.name].find_one()
        return data

    def put(self, data):
        if self.db[self.name].find_one({'stock_code': data['stock_code'], 'datetime': data['datetime']}):
            return None
        else:
            self.db[self.name].insert(data)

    def pop(self):
        data = list(self.db[self.name].aggregate([{'$sample': {'size': 1}}]))
        if data:
            data = data[0]
            value = data['proxy']
            self.delete(value)
            return {'proxy': value, 'value': data['num']}
        return None

    def delete(self, obj):
        """dict"""
        self.db[self.name].remove(obj)

    def getAll(self):
        return {p['proxy'] for p in self.db[self.name].find()}

    def clean(self):
        self.client.drop_database(self._db_name)

    def delete_all(self):
        self.db[self.name].remove()

    def update(self, key, value):
        self.db[self.name].update({'proxy': key}, {'$inc': {'num': value}})

    def exists(self, obj):
        return True if self.db[self.name].find_one(obj) != None else False

    def getNumber(self):
        return self.db[self.name].count()