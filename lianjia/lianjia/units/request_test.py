# -*- coding: utf-8 -*-

import requests


# url = "https://www.lagou.com/jobs/2751893.html"
# params = {
#     "city_id":"440300"
# }
# response = requests.get(url)
#
# print(response.text)


list = ['新概念', '听力', '小升初', '中考', '国际学校经验', '提升解题技巧', '机构经验']

print(''.join(list,",").strip())