# 编号 英雄 列表 url=https://game.gtimg.cn/images/lol/act/img/js/heroList/hero_list.js
import  requests
import  os
from  PIL  import  Image
import  time

def getjosn():
    url0="https://game.gtimg.cn/images/lol/act/img/js/heroList/hero_list.js"
    try:
        r=requests.get(url0)
        r.raise_for_status()
        r.encoding=r.apparent_encoding
        herolist=r.json()  #转换为josn格式
    except:
       print("爬取失败:")
    print(herolist)
    herolists=herolist["hero"]    #获得hero对应的字典类型
    heronumber=list(map(lambda x:x["heroId"],herolists))  #获得英雄的编号列表
    heroname=list(map(lambda x:x["name"],herolists))   #获得英雄的名称列表
    return heroname,heronumber
def strs(k):
    if k>=0 and k<10:
        return "00"+str(k)
    else:
        return "0"+str(k)
def down():
    name,number=getjosn()   #获得name 和 编号   第一个黑暗之女   001    第二个狂战士 002
    i=0   #计数
    if not os.path.exists("D://英雄联盟壁纸//"):   #判断英雄联盟壁纸这个目录是否存在
        os.mkdir("D://英雄联盟壁纸//")    #创建这个目录
    for j in number:  #遍历每个编号
        if not os.path.exists("D://英雄联盟壁纸//"+name[i]):   #判断这个英雄文件夹是否存在
            os.mkdir("D://英雄联盟壁纸//"+name[i])   #创建这个英雄文件夹
        os.chdir("D://英雄联盟壁纸//"+name[i])  #进入这个文件夹
        i+=1
        for k in range(20):  #假设有20个皮肤
            path="https://game.gtimg.cn/images/lol/act/img/skin/big"+str(j)+str(strs(k))+".jpg"
            print(path)
            rr=requests.get(path)
            if rr.status_code==200: #请求正常
                with open(str(k)+".jpg","wb") as f:  #写入文件
                    f.write(rr.content)
                    f.close()
            print("{}的原壁纸已经下载了{}张\r".format(name[i-1],k))
def look():
    hero=input("欢迎查询英雄皮肤,请选择你要查询的英雄:")
    m="D://英雄联盟壁纸//"+str(hero)
    if not os.path.exists(m):   #判断改英雄皮肤是否已经下载
        ys=input("很抱歉,这个英雄的壁纸暂时未下载，是否调入下载功能yes/no:")
        if ys=="yes":
            print("正在全部下载中:")
            down()
        else:
            print("请重新输入英雄：")
            look()
    for i in range(20):  #查看此英雄的所有皮肤壁画
        image=Image.open(m+"//"+str(i)+".jpg")
        image.show()
        time.sleep(1)

def main():
    print("该程序已经下载了部分英雄原壁纸(下载全部壁纸耗时且占用内存)")
    n=input("1、继续下载:/2、选择浏览:")
    if n=="1":
        down()
    else:
        look()
main()