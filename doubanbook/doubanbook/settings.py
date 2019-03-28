# -*- coding: utf-8 -*-

# Scrapy settings for doubanbook project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'doubanbook'

SPIDER_MODULES = ['doubanbook.spiders']
NEWSPIDER_MODULE = 'doubanbook.spiders'


# 修改编码为utf-8
FEED_EXPORT_ENCODING = 'utf-8'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'doubanbook (+http://www.yourdomain.com)'
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 0.5

RANDOM_DELAY=5

RANDOM_UA_TYPE='random'
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'doubanbook.middlewares.DoubanbookSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'doubanbook.middlewares.DoubanbookDownloaderMiddleware': 543,
#}
DOWNLOADER_MIDDLEWARES = {
    'doubanbook.middlewares.ProxyMiddleware': 543,
    #'doubanbook.middlewares.RandomHttpProxyMiddleware': 543,
#    'doubanbook.middlewares.DoubanbookDownloaderMiddleware': 543,
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
    'doubanbook.middlewares.RandomUserAgentMiddleware': 400,
    'doubanbook.middlewares.RandomDelayMiddleware': 999,
}
HTTPPROXY_PROXY_LIST_FILE='E:\pythonproject\ishareread-scrapy\doubanbook\doubanbook\proxy_list.json'
# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'doubanbook.pipelines.DoubanbookPipeline': 300,
#}
ITEM_PIPELINES = {
    'doubanbook.pipelines.DoubanbookPipeline': 300,
    'doubanbook.pipelines.MySQLPipeline': 350,
}

PROXIES = ['http://61.176.223.7:58822','http://116.209.58.157:9999', 'http://116.209.55.69:9999']

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

#mysql数据库配置
MYSQL_HOST = '127.0.0.1'
MYSQL_DB_NAME = 'isharedb'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'mnbvvbnm'