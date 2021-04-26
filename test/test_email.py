#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: jaxon
@Time: 2021-01-29 10:37
"""
from pandas.tests.io.excel.test_xlsxwriter import xlsxwriter

try:
    from io import BytesIO
except ImportError:
    from cStringIO import StringIO as BytesIO
from io import StringIO
import smtplib
import pytest
import xlsxwriter



import pandas as pd
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart


def export_csv(df):
    with StringIO() as buffer:
        df.to_csv(buffer)
        return buffer.getvalue()



def export_excel(df):
    with BytesIO() as bio:
        writer = pd.ExcelWriter(bio, engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Sheet1')
        writer.save()
        bio.seek(0)
        return bio.getvalue()



class test_email():
    
    def test_send_dataframe(self):
        print('test')
        df = pd.DataFrame({'a':[1,2,3], 'b':[4,5,6]})
        SEND_FROM = 'xu8888jiang@126.com'
        EXPORTERS = {'dataframe.csv': export_csv, 'dataframe.xlsx': export_excel}
        multipart = MIMEMultipart()
        multipart['From'] = "xu8888jiang@126.com"
        multipart['To'] = "360138359@qq.com"
        multipart['Subject'] = '导出数据'
        for filename in EXPORTERS:
            print(EXPORTERS[filename](df))
            attachment = MIMEApplication(EXPORTERS[filename](df))
            #attachment['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
            attachment.add_header('Content-Disposition', 'attachment', filename=('utf8','',filename))
            multipart.attach(attachment)
        s = smtplib.SMTP_SSL(host='smtp.126.com', port='465')
        s.login('xu8888jiang@126.com','ZYCFWACYWJIYLZHI')
        s.sendmail(SEND_FROM, '360138359@qq.com', multipart.as_string())
        s.quit()

test_email().test_send_dataframe()
