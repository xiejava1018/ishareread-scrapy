# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo as pymongo
from scrapy.exceptions import DropItem
from scrapy.item import Item


class PriceConverterPipeline(object):

    exchange_rate=8.5309

    def process_item(self, item, spider):
        price = float(item['price'][1:]) * self.exchange_rate
        item['price']='¥%.2f'%price
        return item


class DuplicatesPipeline(object):
    def __init__(self):
        self.book_set=set()

    def process_item(self,item,spider):
        name=item['name']
        if name in self.book_set:
            raise DropItem("Duplicate book found:%s"%item)
        self.book_set.add(name)
        return item


class MongoDBPipeline(object):
    DB_URI='mongodb://127.0.0.1:27017'
    DB_NAME='bookdb'

    def open_spider(self,spider):
        self.client=pymongo.MongoClient(self.DB_URI)
        self.db=self.client[self.DB_NAME]
        self.db.authenticate('book', 'book@123')

    def close_spider(self,spider):
        self.client.close()

    def process_item(self,item,spider):
        collection=self.db[spider.name]
        post=dict(item) if isinstance(item,Item) else item
        collection.insert_one(post)
        return item
