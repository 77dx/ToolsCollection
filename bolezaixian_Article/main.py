# -*- coding:utf-8 -*-

#调用命令行，调试

from scrapy.cmdline import execute

import sys
import os


#切换到main文件所在的目录
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
#print(os.path.dirname(os.path.abspath(__file__)))

#执行scrapy crawl jobbole命令，启动spider
#execute(["scrapy","crawl","jobbole"])
execute(["scrapy","crawl","zhihu"])
