# -*- coding: utf-8 -*-

from wxpy import *
import jieba
import numpy


#登录微信
def wx_login():
    bot = Bot()
    my_friends = bot.friends()
    return my_friends

#统计微信好友男女比例
def sex_friends(my_friends):
    sex_dict = {'male':0,'female':0}

    for friend in my_friends:
        if friend.sex == 1:
            sex_dict['male'] +=1
        elif friend.sex == 2:
            sex_dict['female'] +=1
    print(sex_dict)

#好友签名统计
def show_signature(my_friends):

    for friend in my_friends:
        pattern = re.compile(r'[\u4E00- \u9FA5]+')
        filterdata = re.findall(pattern,friend.signature)
        write_text_file('signatures.txt',''.join(filterdata))

    content = read_txt_file('signatures.txt')
    segment = jieba.lcut(content)
    words_df = pd.DateFrame({'segment':segment})

    stopwords = pd.read_csv("stopwords.txt",index_col=False,quoting=3,sep="",names=['stopword'],encoding='utf-8')
    words_df = words_df[~words_df.segment.isin(stopwords,stopword)]
    print(words_df)

    words_stat = words_df.groupby(by=['segment'])['segment'].agg({"计数":numpy.size})
    words_stat = words_stat.reset_index().sort_value(by=["计数"],ascending=False)

    color_mask = imread("Documents/61a7c58071305ef271373a6681d7aacc.jfif")
    wordcloud = WordCloud(font_path="",
                          background_color="white",
                          max_word=100,
                          mask=color_mask,
                          max_font_size=100,
                          random_state=42,
                          width=1000,height=860,margin=2,
                          )

    word_frequence = {x:[0]:x[1]for x in words_stat.head(100).values}
    print(word_frequence)
    word_frequence_dict={}
    for key in word_frequence:
        word_frequence_dict[key] = word_frequence[key]

        wordcloud.geneerate_from_frequencies(word_frequence_dict)
        image_colors = ImageColorGenrator(color_mask)
        wordcloud.recolor(color_func=image_colors)
        wordcloud.to_file("output.png")
        plt.imshow(wordcloud)
        plt.axis("off")
        plt.show()





if __name__ == '__main__':
    my_friends = wx_login()
    sex_friends(my_friends)
    write_text(my_friends)
    show_signature(my_friends)