# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BookItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    bookcategory = scrapy.Field()
    bookname = scrapy.Field()
    bookauthor = scrapy.Field()
    bookurl = scrapy.Field()
    bookdownloadurl = scrapy.Field()
    booktype = scrapy.Field()
    bookstatusdesc=scrapy.Field()
