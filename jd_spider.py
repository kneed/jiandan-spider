# coding:utf-8
import scrapy
from jiandan.items import JiandanItem

from scrapy.crawler import CrawlerProcess


class JiandanSpider(scrapy.Spider):

    name = "jiandan" #唯一的爬虫名字

    #allowed_domains = ["jiandan.net"] #
    start_urls = ['http://jiandan.net/ooxx']

    def parse(self, response):
        item = JiandanItem()
        item['image_urls'] = response.xpath('//p//img//@src').extract()  # 提取图片链接
        # print 'image_urls',item['image_urls']
        yield item #循环抓取图片链接存贮
        new_url = response.xpath('//a[@class="previous-comment-page"]//@href').extract_first()  # 翻页
        # print 'new_url',new_url
        if new_url:
            yield scrapy.Request(response.urljoin(new_url), callback=self.parse) #循环调用Parse