#!/usr/bin/python
# -*-coding:utf-8-*-

import datetime
import traceback
from sunshine.utils import color
from scrapy.utils import log
from pymongo import MongoClient


class SingleMongodbPipeline(object):
    """
        save the data to mongodb.
    """

    MONGODB_SERVER = "localhost"
    MONGODB_PORT = 27017
<<<<<<< HEAD
    
=======
    MONGODB_DB = "article_fs"
>>>>>>> 1ea7eb54248b7973704616ac1cbad7693a523428

    def __init__(self):
        """
            The only async framework that PyMongo fully supports is Gevent.
            Currently there is no great way to use PyMongo in conjunction with Tornado or Twisted. PyMongo provides built-in connection pooling, so some of the benefits of those frameworks can be achieved just by writing multi-threaded code that shares a MongoClient.
        """
        self.style = color.color_style()
        try:
            client = MongoClient(self.MONGODB_SERVER, self.MONGODB_PORT)
            self.db = client[self.MONGODB_DB]
        except Exception as e:
            print(
                self.style.ERROR("ERROR(SingleMongodbPipeline): %s" % (
                    str(e), )))
            traceback.print_exc()

    @classmethod
    def from_crawler(cls, crawler):
        cls.MONGODB_SERVER = crawler.settings.get('SingleMONGODB_SERVER',
                    'localhost')
        cls.MONGODB_PORT = crawler.settings.getint('SingleMONGODB_PORT', 27017)
        cls.MONGODB_DB = crawler.settings.get('SingleMONGODB_DB', 'books_fs')
<<<<<<< HEAD
        cls.MONGODB_TB = crawler.settings.get('SingleMONGODB_TB', 'article_detail')
=======
>>>>>>> 1ea7eb54248b7973704616ac1cbad7693a523428
        pipe = cls()
        pipe.crawler = crawler
        return pipe

    def process_item(self, item, spider):
<<<<<<< HEAD
        if self.db[self.MONGODB_TB].find_one({'url': item['url']}):
            return None
        else:
            self.db[self.MONGODB_TB].insert(dict(item))
        # item["mongodb_id"] = str(result)


class T66yMongodbPipeline(SingleMongodbPipeline):
    
    def process_item(self, item, spider):
        if self.db[self.MONGODB_TB].find_one({'url': item['url']}):
            return None
        else:
            self.db[self.MONGODB_TB].insert(dict(item))


class StockInfoMongodbPipeline(SingleMongodbPipeline):
    
    def process_item(self, item, spider):
        table = item._table_name
        if self.db[table].find_one({'secu_code': item['secu_code']}):
            return None
        else:
            self.db[table].insert(dict(item))
            print('insert {} to mongo'.format(item['secu_code']))
=======
        article_detail = {
            'source': item.get('source'),
            'date': item.get('date', []),
            'newsId': item.get('newsId', []),
            'title': item.get('title', ''),
            'contents': item.get('contents', ''),
            'url': item.get('url', ''),
            'comments': item.get('comments', []),
            'time': item.get('time', ''),
            'update_time': datetime.datetime.utcnow()
        }

        result = self.db['article_detail'].insert(article_detail)
        # item["mongodb_id"] = str(result)

        log.msg("Item %s wrote to MongoDB database %s/book_detail" %
                (result, self.MONGODB_DB),
                level=log.DEBUG,
                spider=spider)
        return item
>>>>>>> 1ea7eb54248b7973704616ac1cbad7693a523428
