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

    def start_requests(self):
        for i in range(100):
            yield Request('http://httpbin.org/ip', dont_filter=True)
            yield Request('http://httpbin.org/ip', dont_filter=True)

    def parse(self, response):
        print(json.loads(response.text))