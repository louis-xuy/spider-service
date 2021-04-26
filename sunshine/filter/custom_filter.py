#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: jaxon
@Time: 2020-12-11 13:05
"""

import os

from scrapy.dupefilters import RFPDupeFilter


class CustomFilter(RFPDupeFilter):
    """A dupe filter that considers specific ids in the url"""

    def __getid(self, url):
        mm = url.split("&refer")[0]  # or something like that
        return mm

    def request_seen(self, request):
        fp = self.__getid(request.url)
        if fp in self.fingerprints:
            return True
        self.fingerprints.add(fp)
        if self.file:
            self.file.write(fp + os.linesep)