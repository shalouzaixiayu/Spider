# -*- coding :  utf-8 -*-
# @Time      :  2020/4/27  18:57
# @author    :  沙漏在下雨
# @Software  :  PyCharm
# @CSDN      :  https://me.csdn.net/qq_45906219
import requests
from lxml import etree
import re
import os

count = 2


def get_page_url(urls, headers):  # 给定目录网址，获得每个章节的网址

    r = requests.get(urls, headers=headers)
    html = etree.HTML(r.text)  # 形成xpath对象
    html = etree.tostring(html)  # 修改代码
    html = etree.fromstring(html)  # 转换格式 不加就会出错
    result = html.xpath(
        '//div[@class = "volume"][2]//ul[@class = "cf"]//li/a/@href')  # 目前先确定第二个div标签 获得改标签下网址
    result = ['http:' + i for i in result]  # 拼接网址
    name = html.xpath('//div[@class = "volume"][2]//ul[@class = "cf"]//li/a/text()')  # 确定第二个div标签的文章标题

    return result, name


def get_page_text(urls, headers):  # 根据每一页的网址 获得其中的文本信息 然后返回给主函数
    text = []  # 文本
    for i in urls:  # 遍历这个列表
        r = requests.get(i, headers=headers)
        if r.status_code == 200:  # 如果请求正常
            s = re.sub(r':', '', r.text)
            page_html = etree.HTML(s)  # 形成xpath对象
            page_html = etree.tostring(page_html)  # 修改代码规格
            # print(page_html.decode('utf-8'))
            page_html = etree.fromstring(page_html)  # 转换格式
            page_text = page_html.xpath(
                '//div[@class="read-content j_readContent"]/p/text()')  # 寻找真实网址

            text.append(page_text)
    print(text)
    return text  # 该文本还需要修改


def write_page_text(text, title):  # 根据获得的文本 和 标题 然后写入文件夹中
    path = 'D://庆余年//'
    if not os.path.exists(path):  # 如果目录不存在的话
        os.mkdir(path)  # 创建这个目录
        os.chdir(path)  # 进入这个目录
    else:
        os.chdir(path)  # 进入这个目录

    for i in zip(title, text):  # 形成拉链
        s = ''.join(i[1])
        with open('第' + str(count - 1) + '卷. ' + i[0] + '.txt', 'a+', encoding='utf-8') as fw:
            fw.write(i[0] + '\n')
            fw.write(s)
        print(f'{i[0]}: 已经下载完成！')


if __name__ == '__main__':
    menu_url = 'https://book.qidian.com/info/114559#Catalog'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/81.0.4044.122 Safari/537.36 Edg/81.0.416.64'
    }
    page_url, page_title = get_page_url(menu_url, headers)
    text = get_page_text(page_url, headers)  # 获取一个div标签里面的所有章节信息
    write_page_text(text, page_title)
