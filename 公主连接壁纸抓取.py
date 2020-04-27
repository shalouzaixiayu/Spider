# -*- coding :  utf-8 -*-
# @Time      :  2020/4/22  21:48
# @author    :  沙漏在下雨
# @Software  :  PyCharm
# @CSDN      :  https://me.csdn.net/qq_45906219

import requests
import os
from bs4 import BeautifulSoup
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib
import wordcloud
from PIL import  Image

def get_img():  # 获得壁纸
    url = 'http://static.biligame.com/pcr/gw/pc/images/p6/op/'
    girl_url = []
    for i in range(1, 30):  # 假设抓取三十个文件
        s = url + str(i) + '.jpg'
        girl_url.append(s)

    path = 'D://公主连结壁纸//'
    if not os.path.exists(path):
        os.mkdir(path)
        os.chdir(path)
    else:
        os.chdir(path)

    for j, k in enumerate(girl_url):
        r = requests.get(k)
        if r.status_code == 200:
            with open('girl' + str(j) + '.jpg', 'wb') as fw:
                fw.write(r.content)
        else:
            print('壁纸数量不足！')
            break


def get_data(girl_url):  # 获得中文词汇
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36 Edg/81.0.416.62'}
    r = requests.get(girl_url, timeout=100, headers=headers)  # 获得网页
    r.encoding = r.apparent_encoding  # 转码
    soup = BeautifulSoup(r.text, 'lxml')  # 解析库
    d = soup.find_all('d')  # 获得含有d标签
    d_text = [i.text for i in d]  # 获得所有的中文词汇
    d_text = [i.replace(' ', '') for i in d_text]  # 去除空格
    return d_text


def get_draw(counts):  # 绘图
    # 显示中文  
    matplotlib.rcParams['font.family'] = 'SimHei'
    matplotlib.rcParams['font.sans-serif'] = ['SimHei']
    df_girl = pd.DataFrame(counts, index=[i for i in range(30)])
    plt.pie(df_girl)
    plt.title('高频弹幕')
    plt.ylabel('次数')
    plt.grid()
    plt.xticks(rotation=30)
    plt.show()


def get_item(girl_text):  # 统计高频词汇
    counts = {}  # 设置一个字典
    for i in girl_text:
        counts[i] = counts.get(i, 0) + 1  # 存在就给值，不存在就给0，然后加1
    item = list(counts.items())  # 列表
    item.sort(key=lambda x: x[1], reverse=True)  # 正序
    for i in range(10):  # 打印前十个
        girl_data, girl_count = item[i]
        # print(girl_data, girl_count)
    return item[:10]


def make_wordcloud():  # 制作词云
    item = [('啥也干不死', 11), ('散人干不死', 10), ('傻人肝不死', 9),
    ('接头霸王', 7), ('公主焊接', 7), ('妈！', 6), ('日日日', 6),
            ('活动', 5), ('散人肝不死', 5), ('母猪焊接', 4)]
    word = []  # 存放总的词汇
    for i in range(len(item)):  # 长度
        girl_data, girl_count = item[i]
        s = [girl_data for i in range(girl_count)]
        word.append(s)  # 获得总词汇
    # 下面制作词云
    t = sum(word, [])  # 使用sum方式把二维变成一维
    t = ' '.join(t)
    twc = wordcloud.WordCloud(background_color='Tan', width=1500, height=1000, font_path="msyh.ttc")
    twc.generate(t)  # 生成词云
    twc.to_file('girl.png')
    a = Image.open('girl.png')
    a.show()
    return word

if __name__ == '__main__':
    # get_img()
    girl_url = 'https://comwment.bilibili.com/168360624.xml'  # 弹幕的url
    girl_text = get_data(girl_url)  # 获得所有的中文词汇

    # item = get_item(girl_text)
    #girl_text = make_wordcloud()
    girl_text = sum(girl_text, [])
    counts = {}
    for i in girl_text:
        counts[i] = counts.get(i, 0) + 1
    get_draw(counts)

