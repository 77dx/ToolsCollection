#-*-coding:utf-8-*-

'''
正在测试裘学活动报名，想要做并发接口测试，需要将一部分请求参数做
参数化，因为有汉字和数字，所以，用python批量生成数据。
很简单，但是实现了目的。
'''


#生成1-100的姓名
def name_add(nums):

    i = 1
    while i<=nums:
        result = "张"+str(i)+"鸣"
        i = i+1
        write_file(result+"\n")


#将姓名保存进txt文件
def write_file(value):
    fo = open("names.txt","a")
    fo.seek(0,2)
    fo.write(value)
    fo.close()








if __name__ == '__main__':
    name_add(100)