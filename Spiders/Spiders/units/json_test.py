# -*- coding:utf-8 -*-

import json
import re

labels = open("../../stu_comments.json",encoding="utf-8")

labels_json = json.load(labels)


label_xls = open("stu_comments.txt","w")

list = []

#把json字典的值取出来
for label_all in labels_json:
    label_list = label_all.get("stu_comments")
    list.append(label_list.split(","))


all_label = []
for label_list in list:
    for label in filter(None, label_list):
        all_label.append(label)

'''
all_label是所有的标签了
1.先找出有重复的文字
2.用正则提取出文字相同的元素

'''

#1.提取出所有标签的文字
name_list = []
for label in all_label:
    match_obj = re.match("([\u4E00-\u9FA5]+).*",label)
    if match_obj:
        name_list.append(match_obj.group(1))



#2.把文字相同的拿出来
A_list = []
B_list = []

for name in name_list:
    # print(name)
    if name not in A_list:
        A_list.append(name)
    elif name in A_list:
        B_list.append(name)

# print(A_list)
# print(B_list)

#3.B_list就是相同元素
#4.all_label是所有的标签
print(len(all_label))
print(len(B_list))
#5.把相同的元素排序
all_list = []



# for i in range(0,len(all_label)):
#     match_i = re.match("([\u4E00-\u9FA5]+).*", all_label[i])
#     if match_i:
#         ii = match_i.group(1)
#     for j in range(i+1,len(all_label)):
#         match_j = re.match("([\u4E00-\u9FA5]+).*",all_label[j])
#         if match_j:
#             jj = match_j.group(1)
#         if ii== jj:
#             all_label[i], all_label[j] = all_label[j], all_label[i]












#按照字符串长度排序
count = len(all_label)


print(all_label)



# for i in range(0,count):
#     match_i = re.match("([\u4E00-\u9FA5]+).*", all_label[i])
#     if match_i:
#         ii = match_i.group(1)
#     for j in range(i+1,count):
#         match_j = re.match("([\u4E00-\u9FA5]+).*", all_label[j])
#         if match_j:
#             jj = match_j.group(1)
#         if ii == jj:
#             all_label[i + 1], all_label[j] = all_label[j], all_label[i + 1]


all_label.sort()

for i in range(0,count):

    for j in range(i+1,count):

        if len(all_label[i]) > len(all_label[j]):
            all_label[i],all_label[j] = all_label[j],all_label[i]


print(all_label)


print(len(all_label))









    # for label in label_list:
    #     # print(label)
    #
    #     print(label)
    #     list.append(label)
    # list.append(label_list)

# list_i = []
#
# for i in list:
#     # print(i.split(","))
#     list_i.append(i)
#
# # print(list_i)
# comments = []
# for j in list_i:
#     for x in j.split(","):
#         comments.append(x.strip())
#
#
#
#
# list_2 = []
# for label in comments:
#     # print(label)
#     if label not in list_2:
#         # print(label)
#         list_2.append(label)
#
# # print(list_2)
#

#
#
#
for element in all_label:
    label_xls.write(element+"\n")

