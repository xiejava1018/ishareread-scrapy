# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanbookItem(scrapy.Item):
    # 书籍信息
    bookdoubanid = scrapy.Field()
    bookdoubanurl=scrapy.Field()
    bookname = scrapy.Field()
    bookauthor=scrapy.Field()
    bookauthordesc=scrapy.Field()
    bookpress=scrapy.Field()
    bookpressdate=scrapy.Field()
    bookisbn=scrapy.Field()
    bookcatalog=scrapy.Field()
    bookcontent=scrapy.Field()
    bookimageurl=scrapy.Field()
    bookprice=scrapy.Field()
    bookpage=scrapy.Field()

