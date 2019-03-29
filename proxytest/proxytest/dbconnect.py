# -*- coding: utf-8 -*-
"""
    :author: XieJava
    :url: http://ishareread.com
    :copyright: © 2019 XieJava <xiejava@ishareread.com>
    :license: MIT, see LICENSE for more details.
"""
import redis

class RedisDB(object):
    @classmethod
    def getConnect(self,crawler):
        db_host = crawler.settings.get('REDIS_HOST', '127.0.0.1')
        db_port = crawler.settings.get('REDIS_PORT', 6379)
        db_password = crawler.settings.get('REDIS_DB_PASSWORD', '123456')
        db_index = crawler.settings.get('REDIS_DB_INDEX', 0)
        db_conn = redis.StrictRedis(host=db_host, port=db_port, db=db_index, password=db_password,
                                    decode_responses=True)
        return db_conn