# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
#from bolezaixian_Article.pipelines import BolezaixianArticlePipeline
import codecs
import json
import MySQLdb
import MySQLdb.cursors
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter
from twisted.enterprise import adbapi
from bolezaixian_Article import items

class BolezaixianArticlePipeline(object):
    def process_item(self, item, spider):
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

#Mysql同步写入数据（写完一条数据才能写第二条），但是数据量很大时候，同步写入的效率就很低了，
#所以引入异步写入数据库，多条数据同时写。
class MysqlPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect('39.108.67.203','root','123456','article_spider',charset="utf8",use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self,item,spider):
        insert_sql ="insert into jobbole_article(title,create_date,url,url_object_id,front_image_url,praise_num,comment,collect,content)VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"

        self.cursor.execute(insert_sql,(item["title"],item["create_date"],item["url"],item["url_object_id"],item["front_image_url"],item["praise_num"],item["comment"],item["collect"],item["content"]))
        self.conn.commit()


#Mysql异步化操作
class MysqlTwistedPipeline(object):

    def __init__(self,dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls,settings):

        dbparms = dict(
            host = settings["MYSQL_HOST"],
            db = settings["MYSQL_DBNAME"],
            user = settings["MYSQL_USER"],
            password = settings["MYSQL_PASSWORD"],
            charset='utf8',
            #游标设置
            cursorclass = MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)

        return cls(dbpool)

    def process_item(self,item,spider):
        #使用twisted将mysql插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert,item)
        #处理异步执行出现的异常
        query.addErrback(self.handle_error,item,spider)

    def handle_error(self,failure,item,spider):
        #处理异步插入的异常

        print(failure)

    def do_insert(self,cursor,item):
        #执行具体的插入
        insert_sql,params = item.get_insert_sql()
        cursor.execute(insert_sql, params)


class JsonExporterPipleline(object):
    def __init__(self):
        self.file = open('article_export.json','wb')
        self.exporter = JsonItemExporter(self.file,encoding='utf-8',ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self,spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self,item,spider):
        self.exporter.export_item(item)

        return item

class ArticleImagePipeline(BolezaixianArticlePipeline):
    def item_completed(self,results,item,info):
        if "front_image_url" in item:
            for ok,value in results:
                image_file_path = value["path"]
            item["front_image_path"] = image_file_path

        return item

        pass