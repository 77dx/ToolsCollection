# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
import MySQLdb.cursors
from scrapy.exceptions import DropItem
from twisted.enterprise import adbapi
from lianjia import items
from scrapy.exporters import JsonItemExporter
import codecs
import json
from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request

class LianjiaPipeline(object):
    def process_item(self, item, spider):
        return item


class JsonExporterPipleline(object):
    def __init__(self):
        self.file = open('douban.json','wb')
        self.exporter = JsonItemExporter(self.file,encoding='utf-8',ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self,spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self,item,spider):
        self.exporter.export_item(item)

        return item
from openpyxl import Workbook

class DoubanMoivePipeline(object):

    def __int__(self):
        self.wb = Workbook()
        self.ws = self.wb.active
        self.ws .append(['对评论的支持数量', '时间', '影片得分', '评论'])  # 设置表头

    def process_item(self, item, spider):
        # 将数据写入表格当中
        line = [item['vote'], item['time'], item['goal'], item['comment']]
        self.ws.apend(line)
        self.wb.save('douban_movie_comment.xlsx', as_template=False)
        return item


class JsonWithEncodingPipline(object):
    #自定义Json文件的导出
    def __init__(self):
        self.file = codecs.open('labels.json','w',encoding='utf-8')
    def process_item(self,item,spider):
        lines = json.dumps(dict(item),ensure_ascii=False)+'\n'
        self.file.write(lines)
        return item
    def spider_closed(self,spider):
        self.file.close()



class MysqlTwistedPipeline(object):
    def __init__(self,dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls,settings):
        dbparms = dict(
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            password=settings["MYSQL_PASSWORD"],
            charset='utf8',
            # 游标设置
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)

        return cls(dbpool)

    def process_item(self, item, spider):
        # 使用twisted将mysql插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
        # 处理异步执行出现的异常
        query.addErrback(self.handle_error, item, spider)

    def handle_error(self, failure, item, spider):
        # 处理异步插入的异常

        print(failure)


    def do_insert(self, cursor, item):
        # 执行具体的插入
        insert_sql, params = item.get_insert_sql()
        cursor.execute(insert_sql, params)


class ImageDownloadPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield Request(image_url)


    def item_completed(self, results, item, info):
        image_path = [x['path'] for ok, x in results if ok]
        if not image_path:
            raise DropItem("Item contains no images")
        item['image_path'] = image_path
        return item
