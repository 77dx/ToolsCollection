# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy import Request
from lianjia.items import DoubanItem
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

class DoubanSpider(scrapy.Spider):
    name = 'DoubanSpider'
    allowed_domains = ['https://movie.douban.com']
    start_urls = ['https://movie.douban.com/subject/30183817/comments?start=0&limit=20&sort=new_score&status=P']

    def parse(self, response):
        # 制定爬取rules
        page_link = LinkExtractor(allow=(r'https://movie\.douban\.com/subject/30183817/comments.*'),
                                  restrict_xpaths=('//div[@id="paginator"]/a[3]/@href'),
                                  )
        rules = (Rule(page_link, callback='parse_page', follow=True),)



        # all_urls = response.css("a::attr(href)").extract()   #获取页面所的链接地址
        # for url in all_urls:
        #     match_url = re.match("(/start=\d+)", url)
        #     if match_url:
        #         request_url = "https://movie.douban.com/subject/30183817/comments?" + match_url.group(1) + '&limit=20&sort=new_score&status=P'
        #         yield Request(request_url, callback=self.parse_detail)
        #
        # next_url = 'https://movie.douban.com/subject/30183817/comments'+ response.css('#paginator a::attr(href)').extract_first("")
        #
        # if next_url:
        #     yield Request(url=next_url, callback=self.parse)
        #
        # pass

    def parse_detail(self, response):
        item = DoubanItem
        selector = Selector(text=response.body)
        information_list = selector.xpath('//*[@id="comments"]')
        for information in information_list:
            vote = information.xpath('//div[@class="comment"]/h3/span[1]/span/text')  # vote 代表评论点赞数量
            time = information.xpath('//div[@class="comment"]/h3/span[2]/span[3]/@title').extract()  # time 是评论发表时间
            goal = information.xpath('//div[@class="comment"]/h3/span[2]/span[2]/@title').extract()  # 影片得分
            comment = information.xpath('//div[@class="comment"]/p/text()')  # 评论的文本
            if goal:
                goal = goal[0].strip()
            else:
                goal = '0'
            item['vote'] = vote
            item['time'] = time
            item['goal'] = goal
            item['comment'] = comment
            yield item






