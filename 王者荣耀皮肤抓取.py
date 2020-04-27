# 图片 编号  josn格式 含有 所有信息：https://pvp.qq.com/web201605/js/herolist.json
import requests
import os
from PIL import Image


def getjson():
    url0 = "https://pvp.qq.com/web201605/js/herolist.json"
    herolist = requests.get(url0)
    herolist_josn = herolist.json()  # 转换为josn 格式
    hero_name = list(map(lambda x: x["cname"], herolist_josn))
    # 获得json中英雄的名字
    hero_number = list(map(lambda x: x["ename"], herolist_josn))
    # 获得josn中英雄的序号
    return hero_name, hero_number


def downhero():
    name, number = getjson()
    i = 0
    if not os.path.exists("D://王者荣耀//"):  # 如果这个总目录不存在 就创建
        os.mkdir("D://王者荣耀//")
    for j in number:  # 遍历每一个英雄的编号
        if not os.path.exists("D://王者荣耀//" + name[i]):
            os.mkdir("D://王者荣耀//" + name[i])  # 创建每个英雄的文件夹
        os.chdir("D://王者荣耀//" + name[i])
        i += 1  # 计数  下一次创建下一个英雄的文件夹
        for k in range(10):  # 假设每个英雄最大化皮肤就是10
            path = "http://game.gtimg.cn/images/yxzj/img201606/skin/hero-info/" + str(j) + "/" + str(
                j) + "-bigskin-" + str(k) + ".jpg"
            r = requests.get(path)
            if r.status_code == 200:
                with open(str(k) + ".jpg", "wb") as f:
                    f.write(r.content)  # 写入二进制文件 保存图片
                    f.close()
            print("{}已经保存{}张:\r".format(name[i], k))  # 进度显示


downhero()
