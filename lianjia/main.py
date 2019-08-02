# -*- coding:utf-8 -*-

#调用命令行，调试

from scrapy.cmdline import execute

import sys
import os


#切换到main文件所在的目录
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# execute(["scrapy","crawl","lianjia_spider"])
# execute(["scrapy","crawl","lagou_spider"])
# execute(["scrapy","crawl","qingsongjiajiao"])
execute(["scrapy","crawl","ThyroidBar"])



