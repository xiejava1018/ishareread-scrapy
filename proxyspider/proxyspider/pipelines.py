# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import redis
from scrapy import Item

class ProxyspiderPipeline(object):
    def process_item(self, item, spider):
        return item


class RedisPipeline:
    def open_spider(self,spider):
        db_host = spider.settings.get('REDIS_HOST', '127.0.0.1')
        db_port = spider.settings.get('REDIS_PORT', 6379)
        db_password = spider.settings.get('REDIS_DB_PASSWORD', '123456')
        db_index = spider.settings.get('REDIS_DB_INDEX', 0)
        self.db_conn = redis.StrictRedis(host=db_host, port=db_port,db=db_index,password=db_password)

    def process_item(self,item,spider):
        self.insert_db(item)
        return item

    def insert_db(self,item):
        if isinstance(item,Item):
            item=dict(item)
        print('ggg='+item['proxy']+'item:'+str(item))
        self.db_conn.set(item['proxy'],str(item))

