# -*- coding: utf-8 -*-
import scrapy
import datetime
import re
from scrapy.http import Request
from urllib import parse
import xlwt
from bolezaixian_Article.items import JobboleArticleItem,ArticleItemLoader
from bolezaixian_Article.utils.common import get_md5
#from scrapy.loader import ItemLoader
class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        '''
        1.获取本页文章的url,交给scrapy下载并解析
        2.获取下一页的文章的所有url，交给scrapy下载，结果返回给parse
       '''
        post_nodes = response.css("#archive .floated-thumb .post-thumb a")

        for post_node in post_nodes:
            post_url = post_node.css("::attr(href)").extract_first("")
            front_image_url = post_node.css("img::attr(src)").extract_first("")
            yield Request(url=parse.urljoin(response.url,post_url), meta={"front_image_url":front_image_url}, callback=self.parse_detail)

        next_url = response.css(".next.page-numbers::attr(href)").extract_first("")
        if next_url:
            yield Request(url=parse.urljoin(response.url,next_url), callback=self.parse)

        pass

    def parse_detail(self,response):
        '''
        #用xpath和css提取具体的页面元素---是回调函数
        #re_selector1 = response.xpath("/html/body/div[1]/div[3]/div[1]/div[1]/h1")
        #re_selector2 = response.xpath('//*[@id="post-113782"]/div[1]/h1/text()')

        # 实例化item
        article_item = JobboleArticleItem()

        #文章标题
        #title = response.xpath("//div[@class='entry-header']/h1/text()").extract_first()
        title = response.css(".entry-header h1::text").extract()[0]

        #文章封面图
        front_image_url= response.meta.get("front_image_url","")

        #创建时间
        #create_date = response.xpath("//p[@class='entry-meta-hide-on-mobile']/text()").extract()[0].strip()
        create_date = response.css("p.entry-meta-hide-on-mobile::text").extract()[0].strip().replace("·","").strip()


        #点赞数
        #praise_num  = response.xpath("//div[@class='post-adds']/span[1]/h10/text()").extract()[0]
        praise_num = int(response.css(".vote-post-up h10::text").extract()[0])

        #收藏数
        #collect = response.xpath("//span[contains(@class,'bookmark-btn')]/text()").extract()[0]
        collect = response.css(".bookmark-btn::text").extract()[0]
        if re.match(".*?(\d+).*",collect):
            collect = int(re.match(".*?(\d+).*",collect).group(1))
        else:
            collect = 0

        #评论数
        comment = response.xpath("//a[@href='#article-comment']/span/text()").extract()[0]
        if re.match(".*?(\d+).*",comment):
            comment = int(re.match(".*?(\d+).*",comment).group(1))
        else:
            comment = 0

        #正文
        content = response.xpath("//div[@class='entry']").extract()[0]


        #把提取出来的数据存到item里面去

        article_item["title"] = title
        article_item["create_date"] = create_date
        try:
            create_date = datetime.datetime.strftime(create_date,'%Y/%m/%d').date()
        except Exception as e:
            create_date = datetime.datetime.now().date()
        article_item["url"] = response.url
        article_item["front_image_url"] = [front_image_url]
        article_item["praise_num"] = praise_num
        article_item["comment"] = comment
        article_item["collect"] = collect
        article_item["content"] = content
        article_item["url_object_id"] = get_md5(response.url)
        '''

        #通过item loader加载item
        front_image_url = response.meta.get("front_image_url", "")
        item_loader = ArticleItemLoader(item=JobboleArticleItem(),response=response)
        item_loader.add_css("title",".entry-header h1::text")
        item_loader.add_value("url",response.url)
        item_loader.add_value("url_object_id", get_md5(response.url))
        item_loader.add_css("create_date", "p.entry-meta-hide-on-mobile::text")
        item_loader.add_value("front_image_url", [front_image_url])
        item_loader.add_css("praise_num", ".vote-post-up h10::text")
        item_loader.add_css("collect", ".bookmark-btn::text")
        item_loader.add_xpath("comment","//a[@href='#article-comment']/span/text()")
        item_loader.add_xpath("content", "//div[@class='entry']")

        article_item = item_loader.load_item()

        yield article_item

        pass