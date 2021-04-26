#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: jaxon
@Time: 2020-12-29 10:55
"""
import logging
import smtplib
import pandas as pd
from io import BytesIO
from datetime import date

from scrapy import signals
from pymongo import MongoClient

from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
logger = logging.getLogger(__name__)


def export_excel(df):
    with BytesIO() as bio:
        writer = pd.ExcelWriter(bio, engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Sheet1')
        writer.save()
        bio.seek(0)
        return bio.getvalue()


class MailSender(object):
    def __init__(self, crawler):
        crawler.signals.connect(self.spider_idle, signal=signals.spider_idle)
        crawler.signals.connect(self.spider_closed, signal=signals.spider_closed)
        client = MongoClient(self.MONGODB_SERVER, self.MONGODB_PORT)
        self.db = client[self.MONGODB_DB]
        
    @classmethod
    def from_crawler(cls, crawler):
        # if not crawler.settings.getbool('MYEXT_ENABLED'):
        #     print('---')
        #     raise NotConfigured

        cls.MONGODB_SERVER = crawler.settings.get('SingleMONGODB_SERVER',
                                                  'localhost')
        cls.MONGODB_PORT = crawler.settings.getint('SingleMONGODB_PORT', 27017)
        cls.MONGODB_DB = crawler.settings.get('SingleMONGODB_DB', 'books_fs')
        cls.MONGODB_TB = crawler.settings.get('SingleMONGODB_TB', 'article_detail')
        instance = cls(crawler)
        return instance

    def spider_idle(self, spider):
        logger.info('idle spider %s' % spider.name)

    # def spider_closed(self, spider):
    #     print("closed spider %s" %spider.name)
    #     today = date.today().strftime('%Y-%m-%d')
    #     cursor = self.db[self.MONGODB_TB].find({"update": today})
    #     df = pd.DataFrame(list(cursor))
    #     print(df)
    #     multipart = MIMEMultipart()
    #     multipart['From'] = 'xu8888jiang@126.com'
    #     multipart['To'] = ', '.join(['xueting221314@126.com', 'xu8888jiang@126.com'])
    #     multipart['Subject'] = '岗位信息汇总'
    #     attachment = MIMEApplication(export_excel(df))
    #     attachment.add_header('Content-Disposition', 'attachment', filename=('gbk', '', '工作岗位.xlsx'))
    #     multipart.attach(attachment)
    #     s = smtplib.SMTP_SSL(host='smtp.126.com', port='465')
    #     s.login('xu8888jiang@126.com', 'ZYCFWACYWJIYLZHI')
    #     s.sendmail('xu8888jiang@126.com', ['xueting221314@126.com', 'xu8888jiang@126.com'], multipart.as_string())
    #     s.quit()
    
    def spider_closed(self, spider):
        import yagmail
        yag = yagmail.SMTP(user="xu8888jiang@126.com", password='', host="smtp.126.com", port='465')
        content = ["1,2,3"]
        attachment = ['gaoxiaojob.xlsx']
        subject = "高校job"
        yag.send(['360138359@qq.com', 'xueting221314@126.com'], subject, content, attachment)
        yag.close()
        print("发送成功")