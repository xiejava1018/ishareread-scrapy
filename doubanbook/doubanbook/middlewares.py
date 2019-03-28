# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware
from scrapy.exceptions import NotConfigured
from collections import defaultdict
import json
import random
import redis
import logging
import time
from scrapy import signals
from fake_useragent import UserAgent

#随机访问时间间隔
class RandomDelayMiddleware(object):
    def __init__(self, crawler):
        super(RandomDelayMiddleware,self).__init__()
        self.delay = crawler.settings.get("RANDOM_DELAY", 10)

    def __init__(self, delay):
        self.delay = delay

    @classmethod
    def from_crawler(cls, crawler):
        delay = crawler.settings.get("RANDOM_DELAY", 10)
        if not isinstance(delay, int):
            raise ValueError("RANDOM_DELAY need a int")
        return cls(delay)

    def process_request(self, request, spider):
        delay = random.randint(0, self.delay)
        logging.debug("### random delay: %s s ###" % delay)
        time.sleep(delay)

#随机请求头
class RandomUserAgentMiddleware(object):
    def __init__(self,crawler):
        super(RandomUserAgentMiddleware, self).__init__()
        self.ua = UserAgent()
        # 从配置文件settings中读取RANDOM_UA_TYPE值，默认为random，可以在settings中自定义
        self.ua_type = crawler.settings.get("RANDOM_UA_TYPE", "random")
    @classmethod
    def from_crawler(cls,crawler):
        return cls(crawler)

    def process_request(self,request,spider):
        def get_ua():
            return getattr(self.ua,self.ua_type)
        request.headers.setdefault('User-Agent',get_ua())


class RandomHttpProxyMiddleware(HttpProxyMiddleware):

    def __init__(self,auth_encoding='latin-1', proxy_list_file=None):
        if not proxy_list_file:
            raise NotConfigured
        self.auth_encoding=auth_encoding
        self.proxies=defaultdict(list)

        with open(proxy_list_file) as f:
            proxy_list=json.load(f)
            for proxy in proxy_list:
                scheme=proxy['proxy_scheme']
                url=proxy['proxy']
            self.proxies[scheme].append(self._get_proxy(url, scheme))

    @classmethod
    def from_crawler(cls, crawler):
        auth_encoding = crawler.settings.get('HTTPPROXY_AUTH_ENCODING', 'latain-1')
        # 从配置文件中读取代理服务器列表文件（json）的路径
        proxy_list_file = crawler.settings.get('HTTPPROXY_PROXY_LIST_FILE')
        return cls(auth_encoding,proxy_list_file)

    def _set_proxy(self, request, scheme):
        #随机选择一个代理
        creds,proxy=random.choice(self.proxies[scheme])
        print(creds,proxy)
        request.meta['proxy']=proxy
        if creds:
            request.headers['Proxy-Authorization'] = b'Basic ' + creds

class ProxyMiddleware(object):
    '''
    设置Proxy
    '''
    def __init__(self, ip):
        self.ip = ip

    @classmethod
    def from_crawler(cls, crawler):
        db_host = crawler.settings.get('REDIS_HOST', '127.0.0.1')
        db_port = crawler.settings.get('REDIS_PORT', 6379)
        db_password = crawler.settings.get('REDIS_DB_PASSWORD', '123456')
        db_index = crawler.settings.get('REDIS_DB_INDEX', 0)
        db_conn = redis.StrictRedis(host=db_host, port=db_port, db=db_index, password=db_password,decode_responses=True)
        proxys=db_conn.keys()
        return cls(ip=proxys)

    def process_request(self, request, spider):
        proxyip = random.choice(self.ip)
        print('####用到的代理IP###--'+proxyip)
        request.meta['proxy'] = proxyip


class DoubanbookSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class DoubanbookDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
