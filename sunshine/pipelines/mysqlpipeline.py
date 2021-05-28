import datetime
import traceback

import pymysql

from sunshine.models import Base, engine,loadSession
from sunshine.utils import color
from loguru import logger



class MysqlPipeline(object):
    """
        save the data to mongodb.
    """

    def __init__(self):
        """
            The only async framework that PyMongo fully supports is Gevent.
            Currently there is no great way to use PyMongo in conjunction with Tornado or Twisted. PyMongo provides built-in connection pooling, so some of the benefits of those frameworks can be achieved just by writing multi-threaded code that shares a MongoClient.
        """
        self.style = color.color_style()
        self.session = loadSession()

    @classmethod
    def from_crawler(cls, crawler):
        # db = crawler.settings.get('MYSQL_DB_NAME', 'scrapy_db')
        # host = crawler.settings.get('MYSQL_HOST', 'localhost')
        # port = crawler.settings.get('MYSQL_PORT', 3306)
        # user = crawler.settings.get('MYSQL_USER', 'root')
        # passwd = crawler.settings.get('MYSQL_PASSWORD', '123456')
        pipe = cls()
        pipe.crawler = crawler
        return pipe

    # 关闭数据库
    def close_spider(self, spider):
        self.session.close()


    def process_item(self, item, spider):
        pass