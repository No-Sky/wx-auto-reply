#-*-coding:utf8-*-
import itchat
from pyecharts import Bar,Pie,Geo,Map
import re
import jieba
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator
import numpy as np
import PIL.Image as Image


def get_sex():
    # 获取好友数据
    my_friends = itchat.get_friends(update=True)[0:]
    sex = {"male": 0, "female": 0, "other": 0}
    for item in my_friends[1:]:
        s = item["Sex"]
        if s == 1:
            sex["male"] += 1
        elif s == 2:
            sex["female"] += 1
        else:
            sex["other"] += 1
    total = len(my_friends[1:])

    # 开始画饼
    attr = list(sex.keys())
    v1 = list(sex.values())
    pie = Pie("好友性别比例")
    pie.add("", attr, v1, v1, is_label_show=True)
    pie.render()

def get_data(type):
    result=[]
    my_friends = itchat.get_friends(update=True)[0:]
    for item in my_friends:
        result.append(item[type])
    return result

def friends_province():
    # 获取好友省份
    province= get_data("Province")
    # 分类
    province_distribution = {}
    for item in province:
        #删除英文省份，因为中国地图表中没有
        if bool(re.search('[a-z]',item)):
            continue
        elif not province_distribution.__contains__(item):
            province_distribution[item] = 1
        else:
            province_distribution[item] += 1
    #将省份名为空的删除
    province_distribution.pop('')
    #提取地图接口需要的数据格式
    province_keys=province_distribution.keys()
    province_values=province_distribution.values()

    return province_keys,province_values


def friends_jiangsu():
    # 获取好友城市
    city_distribution={}
    city = get_data("City")
    jiangsu_city=["南通市","常州市","淮安市","连云港市","南京市","苏州市","宿迁市","泰州市","无锡市","徐州市","盐城市","扬州市","镇江市"]
    for item in city:
        item=item+"市"
        if item in jiangsu_city:
            if not city_distribution.__contains__(item):
                city_distribution[item]=1
            else:
                city_distribution[item]+=1
    # 提取地图接口需要的数据格式
    city_keys=city_distribution.keys()
    city_values=city_distribution.values()
    return city_keys,city_values

def friends_signature():
    signature = get_data("Signature")
    wash_signature=[]
    for item in signature:
        #去除emoji表情等非文字
        if "emoji" in item:
            continue
        rep = re.compile("1f\d+\w*|[<>/=【】『』♂ω]")
        item=rep.sub("", item)
        wash_signature.append(item)

    words="".join(wash_signature)
    wordlist = jieba.cut(words, cut_all=True)
    word_space_split = " ".join(wordlist)
    coloring = np.array(Image.open("C:/Users/casua/Desktop/test1.JPG"))
    my_wordcloud = WordCloud(background_color="white", max_words=800,
                             mask=coloring, max_font_size=80, random_state=30, scale=2,font_path="C:/Windows/Fonts/STKAITI.ttf").generate(word_space_split)

    image_colors = ImageColorGenerator(coloring)
    plt.imshow(my_wordcloud.recolor(color_func=image_colors))
    plt.imshow(my_wordcloud)
    plt.axis("off")
    plt.show()

if __name__ == '__main__':
    itchat.auto_login()

    # city=get_data("City")
    # province=get_data("Province")
    # signature=get_data("Signature")
    # nickname=get_data("NickName")

    # 微信好友省份分布
    # attr,value=friends_province()
    # map = Map("我的微信好友分布", "@寒食君",width=1200, height=600)
    # map.add("", attr, value, maptype='china', is_visualmap=True,
    #         visual_text_color='#000')
    # map.render()


    微信江苏好友分布
    attr,value=friends_jiangsu()
    map = Map("江苏好友分布","@寒食君", width=1200, height=600)
    map.add("", attr, value, maptype='江苏', is_visualmap=True,
            visual_text_color='#000')
    map.render()

    # friends_signature()