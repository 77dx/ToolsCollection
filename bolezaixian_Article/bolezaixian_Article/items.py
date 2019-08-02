# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import datetime
import re
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst
from bolezaixian_Article.utils.common import extract_num
from bolezaixian_Article.settings import SQL_DATETIME_FORMAT,SQL_DATE_FORMAT

class BolezaixianArticleItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


def add_Jobbole(value):
    return value+"cathy"


def date_convert(value):
    try:
        create_date = value.strip().replace("·","").strip()
        #create_date = datetime.datetime.strptime(value, '%Y/%m/%d').date()
    except Exception as e:
        create_date = datetime.datetime.now().date()
    return create_date


def get_num(value):
    if re.match(".*?(\d+).*", value):
        nums = int(re.match(".*?(\d+).*", value).group(1))
    else:
        nums = 0
    return nums


class ArticleItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


def return_value(value):
    return value


class JobboleArticleItem(scrapy.Item):
    title = scrapy.Field()
    create_date = scrapy.Field(
        input_processor = MapCompose(date_convert)
    )
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    front_image_url = scrapy.Field(
        output_processor = MapCompose(return_value)
    )
    front_image_path = scrapy.Field()
    praise_num = scrapy.Field(
        input_processor = MapCompose(get_num)
    )
    comment = scrapy.Field(
        input_processor=MapCompose(get_num)
    )
    collect = scrapy.Field(
        input_processor=MapCompose(get_num)
    )
    content = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = "insert into jobbole_article(title,url,url_object_id,comment)VALUES (%s,%s,%s,%s)"

        params = (self["title"], self["url"], self["url_object_id"], self["comment"])
        return insert_sql,params

class ZhihuQuestionItem(scrapy.Item):
    #知乎问题表
    zhihu_id = scrapy.Field()
    topics = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    answer_num = scrapy.Field()
    comments_num = scrapy.Field()
    foucus_num = scrapy.Field()
    views_user_num = scrapy.Field()
    crawl_time = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = "insert into zhihu_question(zhihu_id,topics,url,title,content,answer_num,comments_num,foucus_num,views_num,crawl_time)VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

        zhihu_id = self["zhihu_id"][0]
        topics = ",".join(self["topics"])
        url = self["url"][0]
        title = "".join(self["title"])
        content = "".join(self["content"])
        answer_num = extract_num("".join(self["answer_num"]))
        comments_num = extract_num("".join(self["comments_num"]))
        foucus_num = extract_num("".join(self["foucus_num"]))
        views_user_num = extract_num("".join(self["views_user_num"]))
        crawl_time = datetime.datetime.now().strftime(SQL_DATETIME_FORMAT)

        params =(zhihu_id,topics,url,title,content,answer_num,comments_num,foucus_num,views_user_num,crawl_time)
        return insert_sql,params

class ZhihuAnswerItem(scrapy.Item):
    #知乎回答表
    zhihu_id = scrapy.Field()
    url = scrapy.Field()
    question_id = scrapy.Field()
    anthor_id = scrapy.Field()
    content = scrapy.Field()
    praise_num = scrapy.Field()
    comments_num = scrapy.Field()
    create_time = scrapy.Field()
    update_time = scrapy.Field()
    crawl_time = scrapy.Field()



























