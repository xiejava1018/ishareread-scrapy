# -*- coding: utf-8 -*-
"""
    :author: XieJava
    :url: http://ishareread.com
    :copyright: © 2019 XieJava <xiejava@ishareread.com>
    :license: MIT, see LICENSE for more details.
"""

import scrapy
from ..items import BookItem

class KgBookSpider(scrapy.Spider):
    name="kgbook"
    allowed_domains=["www.kgbook.com"]
    start_urls=['https://www.kgbook.com']

    #书籍标签页的解析函数
    def parse(self, response):
        for categoryitem in response.css('#category .row ul li'):
            category=categoryitem.xpath('./a/text()').extract_first()
            categoryurl=categoryitem.xpath('./a/@href').extract_first()
            categoryurl = response.urljoin(categoryurl)
            print(category,categoryurl)
            yield scrapy.Request(categoryurl,meta={'category': category},callback=self.parse_booklist)


    #列表页的解析函数
    def parse_booklist(self,response):
        category=response.meta['category']
        bookurls=response.css('.channel-item h3 a::attr(href)').extract()
        for bookurl in bookurls:
            yield scrapy.Request(bookurl,meta={'category': category}, callback=self.parse_bookdetail)
        next_url = response.css('.pagenavi').xpath('./a[contains(text(),"下一页")]/@href').extract_first()
        if next_url:
            next_url = response.urljoin(next_url)
            yield scrapy.Request(next_url, callback=self.parse_booklist)

    #书籍详情页的解析函数
    def parse_bookdetail(self,response):
        category=response.meta['category']
        book = BookItem()
        book['bookcategory'] =category
        book['bookname'] =response.css('.news_title::text').extract_first()
        bookauthor= response.css('#news_details ul').xpath('./li[contains(text(),"作者")]/text()').extract_first()
        book['bookauthor']=bookauthor.replace('作者：','')
        bookurl = scrapy.Field()
        bookdownloadurl = scrapy.Field()
        # booksavepath = booksavepath
        booksource = scrapy.Field()
        booktype = scrapy.Field()
        yield book