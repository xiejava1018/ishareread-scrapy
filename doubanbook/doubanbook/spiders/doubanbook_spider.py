import scrapy

from scrapy.linkextractors import LinkExtractor
from ..items import DoubanbookItem

class DoubanBookSpider(scrapy.Spider):
    name="doubanbooks"
    allowed_domains=["book.douban.com"]
    start_urls=['https://book.douban.com/tag/?view=type']

    #书籍标签页的解析函数
    def parse(self, response):
        for tags_table in response.css('table.tagCol'):
            tag_cells=tags_table.css('td')
            for tag in tag_cells:
                taglab=tag.xpath('./a/text()').extract_first()
                taburl=tag.xpath('./a/@href').extract_first()
                taburl = response.urljoin(taburl)
                print(taglab,taburl)
                yield scrapy.Request(taburl,callback=self.parse_booklist)


    #列表页的解析函数
    def parse_booklist(self,response):
        bookurls=response.css('.info h2 a::attr(href)').extract()
        for bookurl in bookurls:
            yield scrapy.Request(bookurl,meta={'bookdoubanurl': bookurl}, callback=self.parse_bookdetail)
        next_url = response.css('span.next a::attr(href)').extract_first()
        if next_url:
            next_url = response.urljoin(next_url)
            yield scrapy.Request(next_url, callback=self.parse_booklist)

    #书籍详情页的解析函数
    def parse_bookdetail(self,response):
        bookdoubanurl=response.meta['bookdoubanurl']
        book = DoubanbookItem()
        bookdoubanid = bookdoubanurl.split("/")[-2]
        book['bookdoubanid']=bookdoubanid
        book['bookdoubanurl'] = bookdoubanurl
        book['bookname']=response.css('div#wrapper h1 span::text').extract_first()
        book['bookimageurl'] = response.css('div#mainpic a::attr(href)').extract_first()
        book['bookauthor'] = response.css('div#info').xpath('./span[contains(text(),"作者")]/following-sibling::a/text()').extract_first()
        book['bookpress'] = response.css('div#info').xpath('./span[contains(text(),"出版社")]/following-sibling::text()').extract_first()
        book['bookpressdate'] = response.css('div#info').xpath('./span[contains(text(),"出版年")]/following-sibling::text()').extract_first()
        book['bookpage'] = response.css('div#info').xpath('./span[contains(text(),"页数")]/following-sibling::text()').extract_first()
        book['bookprice'] = response.css('div#info').xpath('./span[contains(text(),"定价")]/following-sibling::text()').extract_first()
        book['bookisbn'] = response.css('div#info').xpath('./span[contains(text(),"ISBN")]/following-sibling::text()').extract_first()
        bookcontent_extract_info=response.css('div.related_info h2').xpath('./span[contains(text(),"内容简介")]/../following-sibling::div').css('.all .intro').extract()
        if bookcontent_extract_info:
            book['bookcontent']=bookcontent_extract_info
        else:
            book['bookcontent']=response.css('div.related_info h2').xpath('./span[contains(text(),"内容简介")]/../following-sibling::div').css('.intro').xpath('./*').extract()
        bookauthordesc_extact_info=response.css('div.related_info h2').xpath('./span[contains(text(),"作者简介")]/../following-sibling::div').css('.all .intro').extract()
        if bookauthordesc_extact_info:
            book['bookauthordesc']=bookauthordesc_extact_info
        else:
            book['bookauthordesc'] = response.css('div.related_info h2').xpath('./span[contains(text(),"作者简介")]/../following-sibling::div').css('.intro').xpath('./*').extract()
        book['bookcatalog'] = response.css('div.related_info h2').xpath('./span[contains(text(),"目录")]/../following-sibling::div[contains(@id,"full")]/text()').extract()
        yield book