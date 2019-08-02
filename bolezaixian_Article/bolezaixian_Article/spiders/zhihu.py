# -*- coding: utf-8 -*-
import scrapy
from scrapy import Spider
from scrapy import Request
from scrapy.loader import ItemLoader
from bolezaixian_Article.utils.until_my.zhihu_login import zhihu_getCookies
from selenium import webdriver
from time import sleep
import pickle
import re
import json
import datetime
from bolezaixian_Article.items import ZhihuQuestionItem
from bolezaixian_Article.items import ZhihuAnswerItem
#兼容python2和python3
try:
    import urlparse as parse
except:
    from urllib import parse

class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['https://www.zhihu.com/']
    start_answer_url = "https://www.zhihu.com/api/v4/questions/{0}/answers?include=data[*].is_normal,admin_closed_comment,reward_info,is_collapsed,annotation_action,annotation_detail,collapse_reason,is_sticky,collapsed_by,suggest_edit,comment_count,can_comment,content,editable_content,voteup_count,reshipment_settings,comment_permission,created_time,updated_time,review_info,relevant_info,question,excerpt,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp;data[*].mark_infos[*].url;data[*].author.follower_count,badge[?(type=best_answerer)].topics&offset={1}&limit={2}&sort_by=default"

    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0",
        "Connection":"keep-alive"
    }

    def parse(self, response):
        '''
        这里和伯乐在线不一样，没有提供所有问题的url，所以
        就必须实时在页面里面去抓取url

        提取页面所有的url,筛选出question的url
        '''

        #取页面a标签的href属性
        all_urls = response.css("a::attr(href)").extract()
        #href的url只有后半段，需要把前半段拼接起来，才是完整的url
        all_urls = [parse.urljoin(response.url,url) for url in all_urls]
        #筛选出https的url
        all_urls = filter(lambda x:True if x.startswith("https") else False,all_urls)
        #用正则筛选出符合question的url
        for url in all_urls:
            match_obj = re.match("(.*zhihu.com/question/(\d+))(/|$).*",url)
            if match_obj:
                request_url = match_obj.group(1)
                yield Request(request_url,headers=self.headers,callback=self.parse_question)
            # else:
            #     yield Request(url,headers=self.headers,callback=self.parse)


    def parse_question(self,response):

        match_obj = re.match("(.*zhihu.com/question/(\d+))(/|$).*", response.url)
        if match_obj:
            question_id = int(match_obj.group(2))

        item_loader = ItemLoader(item=ZhihuQuestionItem(),response=response)
        item_loader.add_css("title","h1.QuestionHeader-title::text")
        item_loader.add_css("content",".QuestionHeader-detail span::text")
        item_loader.add_value("url",response.url)
        item_loader.add_value("zhihu_id",question_id)
        item_loader.add_css("answer_num", ".List-headerText span::text")
        item_loader.add_css("comments_num",".QuestionHeader-Comment button::text")
        item_loader.add_css("foucus_num",'.NumberBoard-itemValue::text')
        item_loader.add_css("views_user_num",'.NumberBoard-itemValue::text')
        item_loader.add_css("topics",".QuestionHeader-topics .Popover div::text")

        question_item = item_loader.load_item()
        yield Request(self.start_answer_url.format(question_id,5,10),headers=self.headers,callback=self.parse_answer)
        yield question_item


    def parse_answer(self,response):

        answer_json = json.loads(response.text)
        is_end = answer_json["paging"]["is_end"]
        next_url = answer_json["paging"]["next"]

        for answer in answer_json["data"]:
            answer_item = ZhihuAnswerItem()

            answer_item["zhihu_id"] = answer["id"]
            answer_item["url"] = answer["url"]
            answer_item["question_id"] = answer["question"]["id"]
            answer_item["anthor_id"] = answer["author"]["id"] if "id" in answer["author"] else None
            answer_item["content"] = answer["content"] if "content" in answer else None
            answer_item["praise_num"] = answer["voteup_count"]
            answer_item["comments_num"] = answer["comment_count"]
            answer_item["create_time"] = answer["created_time"]
            answer_item["update_time"] = answer["updated_time"]
            answer_item["crawl_time"] = datetime.datetime.now()

            yield answer_item

        if not is_end:
            yield Request(next_url,headers=self.headers,callback=self.parse_answer)

    def start_requests(self):

        #登录知乎

        # 用selenium打开知乎页面
        driver = webdriver.Firefox()
        driver.get("https://www.zhihu.com/")

        # 先清空浏览器的cookie
        driver.delete_all_cookies()
        print('cookies is all delete')

        # 登录
        driver.find_element_by_xpath('//div[@id="root"]/div/main/div/div/div/div[2]/div[2]/span').click()
        sleep(1)
        driver.find_element_by_xpath(
            '//*[@id="root"]/div/main/div/div/div/div[2]/div[1]/form/div[1]/div[2]/div[1]/input').send_keys(
            "396321556@qq.com")
        driver.find_element_by_xpath(
            '//*[@id="root"]/div/main/div/div/div/div[2]/div[1]/form/div[2]/div/div[1]/input').send_keys("dx396321556")
        driver.find_element_by_xpath('//*[@id="root"]/div/main/div/div/div/div[2]/div[1]/form/button').click()
        print("登录成功")
        sleep(10)

        # 获取cookies
        cookies = driver.get_cookies()
        cookie_dict = {}
        for cookie in cookies:
            # print(cookie['name'])
            f = open('D:/scrapy/ArticleSpider/cookies/zhihu/' + cookie['name'] + '.zhihu', 'wb')
            pickle.dump(cookie, f)
            f.close()
            cookie_dict[cookie['name']] = cookie['value']

        # 关闭浏览器
        driver.close()

        yield Request(self.start_urls[0],callback=self.parse,cookies=cookie_dict,headers=self.headers)


