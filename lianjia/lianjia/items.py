# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LianjiaItem(scrapy.Item):
    name = scrapy.Field()
    type = scrapy.Field()
    status = scrapy.Field()
    address = scrapy.Field()
    average_price = scrapy.Field()
    url = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = "insert into loupan_info(name,type,status,address,average_price,url)VALUES (%s,%s,%s,%s,%s,%s)"

        params = (self["name"], self["type"], self["status"], self["address"], self["average_price"], self["url"])
        return insert_sql,params


class QingsongItem(scrapy.Item):
    name = scrapy.Field()
    label = scrapy.Field()
    certification = scrapy.Field()
    stu_comments = scrapy.Field()
    bad_praise = scrapy.Field()
    teach_year = scrapy.Field()
    teach_hour = scrapy.Field()
    salary = scrapy.Field()
    present = scrapy.Field()
    url = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = "insert into qingsongjiajiao(name,label,certification,stu_comments,bad_praise,teach_year,teach_hour,salary,present,url)VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

        params = (self["name"], self["label"], self["certification"], self["stu_comments"], self["bad_praise"], self["teach_year"], self["teach_hour"], self["salary"], self["present"], self["url"])

        return insert_sql,params


class ThyroidBarItem(scrapy.Item):
    image_urls = scrapy.Field()
    image_path = scrapy.Field()


class DoubanItem(scrapy.Item):
    vote = scrapy.Field()
    time = scrapy.Field()
    goal = scrapy.Field()
    comment = scrapy.Field()

