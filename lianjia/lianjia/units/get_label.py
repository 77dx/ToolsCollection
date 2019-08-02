# -*- coding:utf-8 -*-

import re


url = 'http://imgsrc.baidu.com/forum/w%3D580/sign=52dfc1a83a9b033b2c88fcd225cc3620/4376918fa0ec08fad7c8cf0b57ee3d6d57fbdacc.jpg'
match_url = re.match('http://imgsrc.baidu.com/(.*).jpg', url)
print('==============================')
print(match_url)
print('==============================')


image_path = [x['path'] for ok, x in results if ok]
