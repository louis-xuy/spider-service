#!/usr/bin/python
# -*-coding:utf-8-*-

# Scrapy settings for woaidu_crawler project
import os

PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))

BOT_NAME = 'sunshine'

SPIDER_MODULES = ['sunshine.spiders']
NEWSPIDER_MODULE = 'sunshine.spiders'

DOWNLOAD_DELAY = 1
CONCURRENT_ITEMS = 100
CONCURRENT_REQUESTS = 16
#The maximum number of concurrent (ie. simultaneous) requests that will be performed to any single domain.
CONCURRENT_REQUESTS_PER_DOMAIN = 8
CONCURRENT_REQUESTS_PER_IP = 0
DEPTH_LIMIT = 0
DEPTH_PRIORITY = 0
DNSCACHE_ENABLED = True
# DUPEFILTER_CLASS = 'scrapy.dupefilter.RFPDupeFilter'
# SCHEDULER = 'scrapy.core.scheduler.Scheduler'

# AutoThrottle extension
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 3.0
AUTOTHROTTLE_CONCURRENCY_CHECK_PERIOD = 10#How many responses should pass to perform concurrency adjustments.

# XXX:scrapy's item pipelines have orders!!!!!,it will go through all the pipelines by the order of the list;
# So if you change the item and return it,the new item will transfer to the next pipeline.
# XXX:notice:
# if you want to use shard mongodb,you need MongodbWoaiduBookFile and ShardMongodbPipeline
# if you want to use single mongodb,you need WoaiduBookFile and SingleMongodbPipeline
ITEM_PIPELINES = {
    'sunshine.pipelines.mongodb.SingleMongodbPipeline': 800
    # 'sunshine.pipelines.final_test.FinalTestPipeline':800
}

COOKIES_ENABLED = False


DOWNLOADER_MIDDLEWARES = {
    # 'article_spider.contrib.downloadmiddleware.google_cache.GoogleCacheMiddleware':50,
    # 'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
    # 'sunshine.contrib.downloadmiddleware.rotate_useragent.RotateUserAgentMiddleware':400,
}

#To make RotateUserAgentMiddleware enable.
USER_AGENT = ''

DEFAULT_REQUEST_HEADERS = {
    # 'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
}

LOG_FILE = "logs/scrapy.log"

# STATS_CLASS = 'sunshine.statscol.graphite.RedisGraphiteStatsCollector'

# GRAPHITE_HOST = '127.0.0.1'
# GRAPHITE_PORT = 2003
# GRAPHITE_IGNOREKEYS = []

# SingleMONGODB_SERVER = "localhost"
# SingleMONGODB_PORT = 27017
# SingleMONGODB_DB = "article_fs"
#
# GridFs_Collection = "article_file"

# SCHEDULER = "sunshine.redis.scheduler.Scheduler"
# SCHEDULER_PERSIST = False
# SCHEDULER_QUEUE_CLASS = 'sunshine.redis.queue.SpiderPriorityQueue'
