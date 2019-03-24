# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

#数据整理，去掉换行及空格
import MySQLdb
import pymongo
from scrapy.item import Item
from twisted.enterprise import adbapi

#去空格回车和其他格式调整
class DoubanbookPipeline(object):
    def process_item(self, item, spider):
        joinstr=''
        for key in item:
            if isinstance(item[key],list):
                if item[key]:
                    #如果是目录，则用<br>连接，并且去掉（）
                    if key=='bookcatalog':
                        joinstr = '<br>'
                        if (len(item[key])>2) and (')' in item[key][-1]):
                            item[key]=item[key][:-2]
                    item[key]=joinstr.join(item[key])
                else:
                    item[key] = ''
            if item[key] is not None:
                item[key]=item[key].replace(' ','').replace('\n','')
            else:
                item[key]=''
        return item


#数据整理，去掉重复记录
class DuplicatesPipeline(object):
    def process_item(self, item, spider):
        pass


class MySQLPipeline(object):
    def open_spider(self,spider):
        db = spider.settings.get('MYSQL_DB_NAME', 'isharedb')
        host = spider.settings.get('MYSQL_HOST', '127.0.0.1')
        port = spider.settings.get('MYSQL_PORT', 3306)
        user = spider.settings.get('MYSQL_USER', 'root')
        passwd = spider.settings.get('MYSQL_PASSWORD', 'mnbvvbnm')
        self.dbpool = adbapi.ConnectionPool('MySQLdb', host=host, db=db,user=user, passwd=passwd, charset='utf8')
        #self.db_conn = MySQLdb.connect(host=host, port=port, db=db,user=user, passwd=passwd, charset='utf8')
        #self.db_cur = self.dbpool.cursor()

    def close_spider(self,spider):
        self.dbpool.close()

    def process_item(self,item,spider):
        self.dbpool.runInteraction(self.insert_db, item)
        return item

    def insert_db(self,tx,item):
        bookvalues=(
            item['bookname'],
            item['bookauthor'],
            item['bookpress'],
            item['bookpressdate'],
            item['bookisbn'],
            item['bookcontent'],
            item['bookauthordesc'],
            item['bookcatalog'],
            item['bookimageurl'],
            item['bookprice'],
            item['bookpage'],
            item['bookdoubanid'],
            item['bookdoubanurl'],
        )
        if self.checknoexistbook(tx,item):
            insertbooksql='insert into ishare_book (book_name,book_author,book_press,book_pressdate,book_isbn,book_content_desc,book_author_desc,book_catalog,book_image,book_price,book_pages,book_douban_id,book_douban_url) ' \
                'values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            tx.execute(insertbooksql,bookvalues)

    #判断是否有重复的记录
    def checknoexistbook(self,tx,item):
        #判断书籍ID是否重复
        selectparam=(item['bookdoubanid'])
        selectbooksql='select book_douban_id from ishare_book where book_douban_id=%s'
        self.db_cur=tx.execute(selectbooksql, selectparam)
        values = self.db_cur.fetchall()
        if len(values) > 0:
            print("已经存在记录：" + str(values))
            return False
        else:
            return True
