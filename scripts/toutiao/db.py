#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Time    : 2018/8/12 12:29

__author__ = 'xujiang@baixing.com'

#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

from mongoengine import *

connect('article_fs',host='localhost',port=27017)

class User(Document):
    ID = LongField(primary_key=True)
    AREA = StringField()
    FOLLOWERS_COUNT = IntField()
    MEDIA_TYPE = StringField()
    MEDIA_ID = IntField()
    DESCRIPTION = StringField()
    VERIFIED_CONTENT = StringField()
    SCREEN_NAME = StringField()
    VISIT_COUNT_RECENT = IntField()
    USER_AUTH_INFO = StringField()
    NAME = StringField()
    BIG_AVATAR_URL = StringField()
    GENDER = IntField()
    UGC_PUBLISH_MEDIA_ID = StringField()
    FOLLOWINGS_COUNT = IntField()
    ST = IntField() #0 inited 1 filled 2 mlc data

class Article(Document):
    ID = LongField(primary_key=True)
    PUBLISH_TIME = IntField()
    CREATOR_UID = IntField()
    MEDIA_ID = IntField()
    SOURCE = StringField()
    TITLE = StringField()
    CITY = StringField()
    IMAGE_LIST = StringField()
    KEYWORDS = StringField()
    LABEL = StringField()
    CATEGORIES = StringField()
    TAG = StringField()
    URL = StringField()
    ST = IntField()
    CONTENT = StringField()

print (User.objects(ID=  101244377789).count())