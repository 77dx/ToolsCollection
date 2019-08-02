#-*-coding:utf-8-*-

from selenium import webdriver
from time import sleep
import pickle

'''
用selenium登录知乎
由于知乎修改了登录机制，requests请求无法登录了
'''
def zhihu_getCookies():

    #用selenium打开知乎页面
    driver = webdriver.Firefox()
    driver.get("https://www.zhihu.com/")

    #先清空浏览器的cookie
    driver.delete_all_cookies()
    print('cookies is all delete')

    #登录
    driver.find_element_by_xpath('//div[@id="root"]/div/main/div/div/div/div[2]/div[2]/span').click()
    sleep(1)
    driver.find_element_by_xpath('//*[@id="root"]/div/main/div/div/div/div[2]/div[1]/form/div[1]/div[2]/div[1]/input').send_keys("396321556@qq.com")
    driver.find_element_by_xpath('//*[@id="root"]/div/main/div/div/div/div[2]/div[1]/form/div[2]/div/div[1]/input').send_keys("dx396321556")
    driver.find_element_by_xpath('//*[@id="root"]/div/main/div/div/div/div[2]/div[1]/form/button').click()
    print("登录成功")
    sleep(10)

    #获取cookies
    cookies = driver.get_cookies()
    cookie_dict = {}
    for cookie in cookies:
        #print(cookie['name'])
        f = open('D:/scrapy/ArticleSpider/cookies/zhihu/' + cookie['name'] + '.zhihu','wb')
        pickle.dump(cookie,f)
        f.close()
        cookie_dict[cookie['name']] = cookie['value']

    # 关闭浏览器
    driver.close()

    return cookie_dict


