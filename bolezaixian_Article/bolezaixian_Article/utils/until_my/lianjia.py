#-*-coding:utf-8-*-

from selenium import webdriver
from time import sleep


#打开链家首页
driver = webdriver.Firefox()
driver.get("https://sz.lianjia.com/?utm_source=baidu&utm_medium=pinzhuan&utm_term=biaoti&utm_content=biaotimiaoshu&utm_campaign=sousuo")


#定位页面元素
driver.find_element_by_xpath("/html/body/div[1]/div/div[5]/div[3]/div/div[1]/ul/li[2]/span").click()
driver.find_element_by_xpath('//*[@id="findHouse"]').click()


def get_loupan():
    loupan1 = driver.find_element_by_xpath("/html/body/div[4]/ul[2]/li[1]/div/div[1]/a").text
    loupan2 = driver.find_element_by_xpath("/html/body/div[4]/ul[2]/li[2]/div/div[1]/a").text
    loupan3 = driver.find_element_by_xpath("/html/body/div[4]/ul[2]/li[3]/div/div[1]/a").text
    loupan4 = driver.find_element_by_xpath("/html/body/div[4]/ul[2]/li[4]/div/div[1]/a").text
    loupan5 = driver.find_element_by_xpath("/html/body/div[4]/ul[2]/li[5]/div/div[1]/a").text
    loupan6 = driver.find_element_by_xpath("/html/body/div[4]/ul[2]/li[6]/div/div[1]/a").text
    loupan7 = driver.find_element_by_xpath("/html/body/div[4]/ul[2]/li[7]/div/div[1]/a").text
    loupan8 = driver.find_element_by_xpath("/html/body/div[4]/ul[2]/li[8]/div/div[1]/a").text
    loupan9 = driver.find_element_by_xpath("/html/body/div[4]/ul[2]/li[9]/div/div[1]/a").text
    loupan10= driver.find_element_by_xpath("/html/body/div[4]/ul[2]/li[10]/div/div[1]/a").text
    print(loupan1,loupan2,loupan3,loupan4,loupan5,loupan6,loupan7,loupan8,loupan9,loupan10)

    driver.find_element_by_xpath("/html/body/div[5]/a[5]").click()

while True:
    get_loupan()

sleep(5)
driver.close()