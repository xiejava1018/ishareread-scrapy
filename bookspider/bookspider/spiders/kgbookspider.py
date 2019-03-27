# -*- coding: utf-8 -*-
"""
    :author: XieJava
    :url: http://ishareread.com
    :copyright: © 2019 XieJava <xiejava@ishareread.com>
    :license: MIT, see LICENSE for more details.
"""

import scrapy
import re
from ..items import BookItem

class KgBookSpider(scrapy.Spider):
    name="kgbook"
    allowed_domains=["www.kgbook.com","kgbook.com"]
    start_urls=['https://www.kgbook.com']
    booktypes=['mobi','epub','azw3','pdf']
    downloadtypes=['mobi','epub','azw3']
    booksource='kgbook'

    #书籍标签页的解析函数
    def parse(self, response):
        excludecategorys=['工具书','电子书制作']
        for categoryitem in response.css('#category .row ul li'):
            category=categoryitem.xpath('./a/text()').extract_first()
            categoryurl=categoryitem.xpath('./a/@href').extract_first()
            categoryurl = response.urljoin(categoryurl)
            print(category,categoryurl)
            if category not in excludecategorys:
                yield scrapy.Request(categoryurl,meta={'category': category},callback=self.parse_booklist,dont_filter = True)


    #列表页的解析函数
    def parse_booklist(self,response):
        category=response.meta['category']
        bookurls=response.css('.channel-item h3').xpath('./a/@href').extract()
        for bookurl in bookurls:
            bookurl = response.urljoin(bookurl)
            print('parse_booklist--bookurl====' + bookurl)
            yield scrapy.Request(bookurl,meta={'category': category,'bookurl':bookurl}, callback=self.parse_bookdetail,dont_filter = True)
        next_url = response.css('.pagenavi').xpath('./a[contains(text(),"下一页")]/@href').extract_first()
        if next_url:
            next_url = response.urljoin(next_url)
            print('next_url=====' + next_url)
            yield scrapy.Request(next_url,meta={'category': category},callback=self.parse_booklist,dont_filter = True)

    #书籍详情页的解析函数
    def parse_bookdetail(self,response):
        category=response.meta['category']
        bookurl=response.meta['bookurl']
        print('bookurl==XX==' + bookurl)
        bookcategory =category
        bookname =response.css('.news_title::text').extract_first()
        bookauthor= response.css('#news_details ul').xpath('./li[contains(text(),"作者")]/text()').extract_first()
        bookauthor = bookauthor.replace('作者：', '')
        book_restype =response.css('#news_details ul').xpath('./li[contains(text(),"格式")]/text()').extract_first()
        book_restype = book_restype.replace('格式：', '')
        sels=response.css('#introduction a.button')
        for sel in sels:
            bookrestypestr = sel.xpath('./text()').extract_first()
            bookrestype=self.getbookrestype(bookrestypestr)
            book = BookItem()
            book['bookcategory'] = bookcategory
            book['bookname'] = bookname
            book['bookauthor'] = bookauthor
            book['bookurl'] = bookurl
            book['booksource']=self.booksource
            book['booksavepath'] =''
            book['file_urls']=[]
            if '下载' in bookrestypestr:
                bookrestype=book_restype
            if bookrestype in self.booktypes:
                bookresurl=sel.xpath('./@href').extract_first()
                book['bookdownloadurl']= bookresurl
                book['booktype']=bookrestype
                if bookrestype in self.downloadtypes:
                    book['file_urls'].append(bookresurl)
                yield book


    def getbookrestype(self,bookrestypestr):
        for booktype in self.booktypes:
            if re.search(booktype,bookrestypestr, re.I):
                return booktype