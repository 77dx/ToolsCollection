# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy import Request
from lianjia.items import ThyroidBarItem


class ThyroidbarSpider(scrapy.Spider):
    name = 'ThyroidBar'
    allowed_domains = ['http://tieba.baidu.com']
    kw = "周星驰"
    start_urls = ['http://tieba.baidu.com/f?kw='+kw+'&ie=utf-8&tab=main/']

    def parse(self, response):
        i = 1
        all_urls = response.css("a::attr(href)").extract()

        for url in all_urls:
            match_url = re.match("(/p/\d+)", url)
            if match_url:
                request_url = "http://tieba.baidu.com" + match_url.group(1)
                # print(request_url)
                yield Request(request_url, callback=self.parse_detail)


        next_url = "http://tieba.baidu.com/f?kw=%E5%91%A8%E6%98%9F%E9%A9%B0&ie=utf-8" + response.xpath('//a[contains(text(),"下一页")]/@href').extract_first("")

        if next_url:
            yield Request(url=next_url, callback=self.parse)

        pass

    def parse_detail(self, response):

        image_urls = response.xpath("//img[@class='BDE_Image']/@src").extract()

        if image_urls:
            thyroid_item = ThyroidBarItem()
            thyroid_item['image_urls'] = image_urls
            yield thyroid_item

        # for url in image_urls:
        #     thyroid_item = ThyroidBarItem()
        #     thyroid_item['url'] = url
        #     yield thyroid_item





