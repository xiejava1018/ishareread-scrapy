# -*- coding: utf-8 -*-
"""
    :author: XieJava
    :url: http://ishareread.com
    :copyright: © 2019 XieJava <xiejava@ishareread.com>
    :license: MIT, see LICENSE for more details.
"""

import scrapy

from scrapy.linkextractors import LinkExtractor
from .doubanbook_spider import DoubanBookSpider
from ..items import DoubanbookItem

class GetDoubanBookSpider(scrapy.Spider):
    name="doubanbook"
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
            'doubanbook.middlewares.RandomUserAgentMiddleware': 400,
            'doubanbook.middlewares.RandomDelayMiddleware': 999,
        },
        'ITEM_PIPELINES':{
            'doubanbook.pipelines.DoubanbookPipeline': 300,
            'doubanbook.pipelines.MySQLPipeline': 350,
        },
        'DOWNLOAD_DELAY': 1,  # 延时最低为2s
        'AUTOTHROTTLE_ENABLED': True,  # 启动[自动限速]
        'AUTOTHROTTLE_DEBUG': True,  # 开启[自动限速]的debug
        'AUTOTHROTTLE_MAX_DELAY': 10,  # 设置最大下载延时
        'DOWNLOAD_TIMEOUT': 15,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 4  # 限制对该网站的并发请求数
    }
    allowed_domains=["book.douban.com"]
    start_urls=['https://book.douban.com/subject/4913064/']

    #书籍标签页的解析函数
    def parse(self, response):
        for url in self.start_urls:
            print('url:=='+url)
            yield scrapy.Request(url=url,meta={'bookdoubanurl': url},callback=self.parse_bookdetail)

    #书籍详情页的解析函数
    def parse_bookdetail(self,response):
        book=DoubanBookSpider.parse_book(response)
        yield book