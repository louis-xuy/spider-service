#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: jaxon
@Time: 2021-04-29 13:25
"""

from sunshine.db.basic import get_session


class SqlitePipeline(object):
    
    def __init__(self, *args, **kwargs):
        self.session = get_session()


    def open_spider(self, spider):
        """
        spider开启时调用
        """
        print("### spdier open {}".format(spider.name))
        return 0
    
    
    def process_item(self, item, spider):
        pass
    
    def close_spider(self, spider):
        # We commit and save all items to DB when spider finished scraping.
        try:
            self.session.commit()
        except:
            self.session.rollback()
            raise
        finally:
            self.session.close()

    