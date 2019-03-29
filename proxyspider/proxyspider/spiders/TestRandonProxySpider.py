# -*- coding: utf-8 -*-
"""
    :author: XieJava
    :url: http://ishareread.com
    :copyright: © 2019 XieJava <xiejava@ishareread.com>
    :license: MIT, see LICENSE for more details.
"""
import scrapy
from scrapy import Request
import json

class TestRandonProxySpider(scrapy.Spider):
    name="test_random_proxy"
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
            'proxyspider.middlewares.RandomDelayMiddleware': 399,
            'proxyspider.middlewares.RandomUserAgentMiddleware': 400,
            'proxyspider.middlewares.ProxyMiddleware': 543,
            'proxyspider.middlewares.ProcessAllExceptionMiddleware': 544,
        },
        'DOWNLOAD_DELAY': 1,  # 延时最低为2s
        'AUTOTHROTTLE_ENABLED': True,  # 启动[自动限速]
        'AUTOTHROTTLE_DEBUG': True,  # 开启[自动限速]的debug
        'AUTOTHROTTLE_MAX_DELAY': 10,  # 设置最大下载延时
        'DOWNLOAD_TIMEOUT': 15,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 4  # 限制对该网站的并发请求数

    }

    def start_requests(self):
        for i in range(100):
            yield Request('http://httpbin.org/ip', dont_filter=True)
            #yield Request('http://www.ishareread.com/common/disclaimer', dont_filter=True)

    def parse(self, response):
        print('###请求返回的结果###'+response.text)