# -*- coding: utf-8 -*-
"""
    :author: XieJava
    :url: http://ishareread.com
    :copyright: © 2019 XieJava <xiejava@ishareread.com>
    :license: MIT, see LICENSE for more details.
"""
import scrapy
import json
from scrapy import Request

class XiciSpider(scrapy.Spider):
    name="xici_proxy"
    allowed_domains=["www.xicidaili.com"]

    def start_requests(self):
        start_urls = 'https://www.xicidaili.com/nn/%s'
        for i in range(1,4):
            yield Request(start_urls % i)


    #书籍标签页的解析函数
    def parse(self, response):
        for sel in response.xpath('//table[@id="ip_list"]/tr[position()>1]'):
            ip=sel.css('td:nth-child(2)::text').extract_first()
            port=sel.css('td:nth-child(3)::text').extract_first()
            scheme= sel.css('td:nth-child(6)::text').extract_first()
            url = '%s://httpbin.org/ip' % scheme
            proxy = '%s://%s:%s' % (scheme, ip, port)
            meta = {'proxy': proxy,
                    'dont_retry': True,
                    'download_timeout': 10,
                    '_proxy_scheme': scheme,
                    '_proxy_ip': ip,}
            print(meta)
            yield scrapy.Request(url,callback=self.check_available,meta=meta,dont_filter=True)

    def check_available(self, response):
        proxy_ip = response.meta['_proxy_ip']  # 判断代理是否具有隐藏IP 功能
        print(proxy_ip+'----------'+json.loads(response.text)['origin'])
        if proxy_ip in json.loads(response.text)['origin']:
            print('-----XX----'+json.loads(response.text)['origin'])
            yield {'proxy_scheme': response.meta['_proxy_scheme'],
                   'proxy': response.meta['proxy'],}

