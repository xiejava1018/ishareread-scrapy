# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.files import FilesPipeline
from urllib.parse import urlparse
from os.path import basename,dirname,join
from twisted.enterprise import adbapi

class BookspiderPipeline(object):
    def process_item(self, item, spider):
        return item

#保存至MySQL数据库
class MySQLPipeline(object):
    def open_spider(self,spider):
        db = spider.settings.get('MYSQL_DB_NAME', 'isharedb')
        host = spider.settings.get('MYSQL_HOST', '127.0.0.1')
        port = spider.settings.get('MYSQL_PORT', 3306)
        user = spider.settings.get('MYSQL_USER', 'root')
        passwd = spider.settings.get('MYSQL_PASSWORD', 'mnbvvbnm')
        self.dbpool = adbapi.ConnectionPool('MySQLdb', host=host,port=port,db=db,user=user, passwd=passwd, charset='utf8')

    def close_spider(self,spider):
        self.dbpool.close()

    def process_item(self,item,spider):
        self.dbpool.runInteraction(self._getItem, item)
        return item

    def insert_db(self,tx,item):
        bookvalues=(
            item['bookcategory'],
            item['bookname'],
            item['bookauthor'],
            item['bookurl'],
            item['bookdownloadurl'],
            item['booktype'],
            item['booksource'],
        )
        insertbooksql='insert into ishare_collect_book (bookcategory,bookname,bookauthor,bookurl,bookdownloadurl,booktype,booksource) ' \
            'values (%s,%s,%s,%s,%s,%s,%s)'
        print(insertbooksql,bookvalues)
        tx.execute(insertbooksql,bookvalues)

    #判断是否有重复的记录
    def _getItem(self,tx, item):
        # 判断书籍ID是否重复
        selectparam = (item['bookdownloadurl'],)
        selectbooksql = 'select * from ishare_collect_book where bookdownloadurl=%s'
        tx.execute(selectbooksql, selectparam)
        result = tx.fetchall()
        if result:
            print('已经存在记录：'+str(result))
        else:
            self.dbpool.runInteraction(self.insert_db, item)


#下载书籍
class DownLoadBookFilesPipeline(FilesPipeline):
    def file_path(self, request, response=None, info=None):
        path=urlparse(request.url).path
        return join(basename(dirname(path)),basename(path))