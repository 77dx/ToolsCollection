# -*- coding: utf-8 -*-
'''

这是微信公众号的一篇文章，获取的是阅读量和点赞数

'''
import requests
import json
from time import sleep
import os
def get_read_num():

    url = "https://mp.weixin.qq.com/mp/getappmsgext?f=json&uin=NzQ1MjM1ODgw&key=dc7082fadb9eea529ad53004aaa27ed00470479f95458f871cd419a014693b78a1e2c22c56ef3e6e33c2b56231862cfe949110fa59a7ae2f4afdb2386d3f4184cb7ec2f77315eccce8ab2e1d9f754834&pass_ticket=n7rgWxFhbGKf3UFjPD8CbZdNCVYoGsQohhzlshtTJ6qT0Ar4ydYjkH9g83MbmAys&wxtoken=777&devicetype=Windows%26nbsp%3B7&clientversion=62060028&appmsg_token=954_FMkGIrZ0Ah%252FHKtEG07kQRf408gN54FvO_7f4Cclq5Tl4scp5ntlfWco2PyPNjGUR-KshooKirG_-RCRv&x5=0&f=json"
    headers = {
        "Host": "mp.weixin.qq.com",
        "Connection": "keep - alive",
        "Content - Type": "application/x-www-form-urlencoded;charset=UTF-8",
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 MicroMessenger/6.5.2.501 NetType/WIFI WindowsWechat QBCore/3.43.691.400 QQBrowser/9.0.2524.400",
        "Referer":"https://mp.weixin.qq.com/s?__biz=MjM5OTE3Nzg4MA==&mid=2651725046&idx=1&sn=b36aa345cad6afc159c85a90e566b3b5&chksm=bcc5c7018bb24e174c7e9fad1c140d22aa44ae80648d958ed4f8d1e2872e1493e4f8ebebf960&scene=0&key=c6043a089a40b0a3698e3c9fb0ae8470c8a46711c7c9e5c0107f57325153a876b1ff6c3b17a747ccfa3643178f3278965b1fbdb811e02d3a9bdc32e7d96bde088f57cceb6227431dcc4608ce77f5e11e&ascene=1&uin=NzQ1MjM1ODgw&devicetype=Windows+7&version=62060028&lang=zh_CN&pass_ticket=n7rgWxFhbGKf3UFjPD8CbZdNCVYoGsQohhzlshtTJ6qT0Ar4ydYjkH9g83MbmAys&winzoom=1"
    }
    cookies = {
        "rewardsn" : "",
        "wxtokenkey" : "777",

        
        "wxuin" : "745235880",
        "devicetype" : "Windows7",
        "version" : "62060028",
        "lang" : "zh_CN",
        "pass_ticket" : "n7rgWxFhbGKf3UFjPD8CbZdNCVYoGsQohhzlshtTJ6qT0Ar4ydYjkH9g83MbmAys",
        "wap_sid2" : "CKjLreMCElxXdWVfZk9fenBvMkI3QUhGT1JoMWdKMVhZRjN6cE55blZTNHZ2M2IxQmJmMWU4ZXF4TExKMVowcVgxQ2NFZ0Q2eGNld1lsMTducXdkc2hIcG1RdXZxcm9EQUFBfjDGn4XXBTgNQAE ="
    }

    parms = {
        "r":"9451514314860106",
        "__biz":"MjM5OTE3Nzg4MA==",
        "appmsg_type":"9",
        "mid":"2651725046",
        "sn":"b36aa345cad6afc159c85a90e566b3b5",
        "idx":"1",
        "scene": "0",
        "title": "周四早，来听8点1氪",
        "ct": "1524724358",
        "abtest_cookie": "",
        "devicetype": "Windows 7",
        "version": "/mmbizwap/zh_CN/htmledition/js/appmsg/index3d3efa.js",
        "is_need_ticket": "1",
        "is_need_ad": "0",
        "comment_id":"253874301844078593",
        "is_need_reward":"0",
        "both_ad":"0",
        "reward_uin_count": "0",
        "send_time": "",
        "msg_daily_idx": "1",
        "is_original": "0",
        "is_only_read": "1",
        "req_id": "2615hEBMxv3rpr7lrYEzCHZj",
        "pass_ticket": "n7rgWxFhbGKf3UFjPD8CbZdNCVYoGsQohhzlshtTJ6qT0Ar4ydYjkH9g83MbmAys",
        "is_temp_url": "0"
    }

    response = requests.post(url,headers=headers,data=parms,cookies=cookies)

    json_res = json.loads(response.text)
    print("阅读数量")
    print(json_res)
    print(json_res["appmsgstat"]["read_num"])
    print("点赞数量")
    print(json_res["appmsgstat"]["like_num"])



if __name__ == '__main__':

    while True:
        print("最新数据")
        print("***************************************")
        get_read_num()
        print("***************************************")
        print("\n")
        print("\n")
        print("\n")
        sleep(10)