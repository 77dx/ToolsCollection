# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy import Request
from lianjia.items import QingsongItem

class QingsongjiajiaoSpider(scrapy.Spider):
    name = 'qingsongjiajiao'
    allowed_domains = ['www.changingedu.com']
    start_urls = ['https://www.changingedu.com/shenzhen/r-/p1']

    def parse(self, response):

        all_urls = response.css("a::attr(href)").extract()

        for url in all_urls:
            match_url = re.match("(/teacher/\d+.html)",url)
            if match_url:
                request_url = "https://www.changingedu.com" + match_url.group(1)
                #print(request_url)
                yield Request(request_url,callback=self.parse_detail)

        next_url ="https://www.changingedu.com" + response.css(".page_next::attr(href)").extract_first("")
        if next_url:
            yield Request(url=next_url,callback=self.parse)

        pass


    def parse_detail(self,response):


        # names = response.xpath("/html/body/div[2]/span[2]/p[1]/text()").extract()
        # name = ''.join(names).strip()
        # labels = response.xpath('//p[@class="f8-section-p3"]/span/text()').extract()
        # label = ','.join(labels)
        # certifications = response.xpath('//p[@class="f8-section-p4"]/span/text()').extract()
        # certification = ','.join(certifications)
        stu_comment = response.xpath("//div[@class='hot-tags']/ul/li/text()").extract()
        if len(stu_comment)>0:
            del stu_comment[0]

        comment_count = response.xpath('//span[@class="mlR10"]/text()').extract()
        if len(comment_count)>0:
            del comment_count[0]


        # bad_praises = response.xpath('//*[@id="abt"]/div[1]/div[1]/div[2]/p/span[3]/text()').extract()
        # bad_praise = ','.join(bad_praises)
        # teach_years = response.xpath("/html/body/div[2]/span[2]/p[2]/span[1]/label/text()").extract()
        # teach_year = ''.join(teach_years)
        # teach_hours = response.xpath("/html/body/div[2]/span[2]/p[2]/span[2]/label/text()").extract()
        # teach_hour = ''.join(teach_hours)
        # salarys_1 = response.xpath('//label[@class="fs28"]/text()').extract()
        # salary_1 = ''.join(salarys_1)
        # salarys_2 = response.xpath('//label[@class="fs18"]/text()').extract()
        # salary_2 = ''.join(salarys_2)
        # presents = response.xpath('//p[@class="percent"]/text()').extract()
        # present = ''.join(presents)
        # url = response.url

        list = []

        if len(stu_comment)>0:
            for i in range(0,len(stu_comment)):
                x = stu_comment[i] + comment_count[i]
                list.append(x)

        comment_list = ','.join(list)

        qingsong_item = QingsongItem()
        # qingsong_item["name"] = name
        # qingsong_item["label"] = label
        # qingsong_item["certification"] = certification
        qingsong_item["stu_comments"] = comment_list
        # qingsong_item["bad_praise"] = bad_praise
        # qingsong_item["teach_year"] = teach_year
        # qingsong_item["teach_hour"] = teach_hour
        # qingsong_item["salary"] = salary_1 + salary_2
        # qingsong_item["present"] = present
        # qingsong_item["url"] = url


        yield qingsong_item




        pass