# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import Request
from Spiders.items import LianjiaItem
class LianjiaSpiderSpider(scrapy.Spider):
    name = 'lianjia_spider'
    allowed_domains = ['sz.fang.lianjia.com']
    start_urls = ['https://sz.fang.lianjia.com/loupan/pg1']

    def parse(self, response):
        base_url = "https://sz.fang.lianjia.com/loupan/pg"
        i = 1
        while i<=89:
            next_url = base_url + str(i)
            i = i + 1
            yield Request(url=next_url, callback=self.parse_details)




    def parse_details(self,response):

        i = 0
        while i<10:
            name = response.xpath('//div[@class="resblock-name"]/a/text()').extract()[i]
            type = response.xpath('//span[@class="resblock-type"]/text()').extract()[i]
            status= response.xpath('//span[@class="sale-status"]/text()').extract()[i]
            address = response.xpath('//div[@class="resblock-location"]/a/text()').extract()[i]
            average_price = response.xpath('//span[@class="number"]/text()').extract()[i]
            url = response.url

            lianjia_item = LianjiaItem()

            lianjia_item["name"] = name
            lianjia_item["type"] = type
            lianjia_item["status"] = status
            lianjia_item["address"] = address
            lianjia_item["average_price"] = average_price
            lianjia_item["url"] = url

            i = i+1
            yield lianjia_item