欢迎关注我的专栏( つ•̀ω•́)つ[【人工智能通识】](https://www.jianshu.com/c/e9a7b7b7024d)
[【专题】简书下载器：Python-Tkinter项目编程入门](https://www.jianshu.com/p/0f5011b3d6bb)
---

继续前面的文章。

##改进参数

首先我们在reqs.py中改进getall方法，使它接收传入可变的opt选项设置对象，同时接收volnarr文集列表和artnarr文章列表：
```
#volnarr文集列表，artnarr文章列表，例如volnarr=[0,3,1]表示只获取三个文集，默认为全部
def getAll(opt,volnarr,artnarr):  # 启动线程
    t = Thread(target=getVolums,args=(opt,volnarr,artnarr))  # 多线程，避免锁死界面
    t.start()
    return 'RUNNING!'
```
这样我们可以通过指定`volnarr=[0],artnarr=[0,1,2]`来获取第一个文集的前三篇文章。

然后我们改进一下对应的getVolums函数：
```
def getVolums(opt, volnarr, artnarr):  # 获取文集列表
    print('GETTING VOLS:', opt.urlVolumns)
    res = requests.get(opt.urlVolumns, headers=opt.headers)
    resdata = json.loads(res.text)
    getlist = []  # 指定获取列表
    if len(volnarr) == 0:
        getlist = resdata
    else:
        for i in volnarr:
            if i < len(resdata):
                getlist.append(resdata[i])
    for d in getlist:
        time.sleep(1)
        getArticlesList(d, opt, artnarr)

    print("DOWNLOAD FINI!", atotal, afini)
    return 'getVolums OK!'
```
在中间添加了getlist列表变量，用来列出所需要获取的指定列表，如果设定为空，那么将获取全部resdata。

同时注意`getVolums(opt, volnarr, artnarr)`和`getArticlesList(d, opt, artnarr)`函数的参数变化。

同样我们改进`getArticlesList(vol, opt, artnarr)`:
```
def getArticlesList(vol, opt, artnarr):  # 获取文章列表
    print('GETTING VOL:', vol['name'])
    volId = vol['id']
    urlVol = 'https://www.jianshu.com/author/notebooks/'+str(volId)+'/notes'
    res = requests.get(urlVol, headers=opt.headers)
    resdata = json.loads(res.text)
    getlist = []  # 指定获取列表
    if len(artnarr) == 0:
        getlist = resdata
    else:
        for i in artnarr:
            if i < len(resdata):
                getlist.append(resdata[i])

    for d in getlist:
        time.sleep(1)
        print(d)
        getArticle(d, vol, opt)
    return 'getArticlesList OK!'
```
我们也要改进一下getArticle函数，添加opt传入：
```
def getArticle(art, vol, opt):  # 获取文章内容
```

这些改进完成之后，我们就可以删除顶端的`import options as opt`了,但为了临时测试我们保留它并改为`import options as opts`，我们在底部增加:
```
getAll(opts, [0, 1, 2], [0, 1])
```
然后删除之前抓取数据的data文件夹，运行reqs.py测试，这将只获取前三个文集的第1第2篇文章。

测试成功之后我们再继续改进。

##更新变量

我们来设定在获取数据的同时更新一些信息：
```
atotal = 32  # 总文章数量
afini = 0  # 已读取的文章数量
cookiestr = ''  # cookie全局变量
curVol = '...'  # 正在获取的文集名
curArt = '...'  # 正在获取的文章名
curImg = '...'  # 正在获取的图片名
state='等待中' #当前状态，等待中，获取中，已完成。
```
这三个cur变量将被实时更新，然后显示到界面上。

我们需要在合适的时间更新这些变量，修改后完整的reqs.py如下：
```

import time
from threading import Thread
import requests
import json
import os
import re
import math


atotal = 1  # 总文章数量
afini = 0  # 已读取的文章数量
cookiestr = ''  # cookie全局变量
curVol = '...'  # 正在获取的文集名
curArt = '...'  # 正在获取的文章名
curImg = '...'  # 正在获取的图片名
state = '等待中'  # 当前状态，等待中，获取中，已完成。



def genInfoStr():  # 拼接信息字符串
    global atotal
    global afini
    infoStr = '正在获取('+str(afini)+'/'+str(atotal)+'):'
    per = atotal/15
    fi = math.ceil(afini/per)
    for _ in range(fi):
        infoStr += '■'
    for _ in range(15-fi):
        infoStr += '□'
    return infoStr

# volnarr文集列表，artnarr文章列表，例如volnarr=[0,3,1]表示只获取三个文集，默认为全部


def getAll(opt, volnarr, artnarr):  # 启动线程
    t = Thread(target=getVolums, args=(opt, volnarr, artnarr))  # 多线程，避免锁死界面
    t.start()
    global state
    state = '获取中'
    print(state)
    return 'RUNNING!'


def getArticle(art, vol, opt):  # 获取文章内容
    artId = art['id']
    urlArt = 'https://www.jianshu.com/author/notes/'+str(artId)+'/content'
    res = requests.get(urlArt, headers=opt.headers)
    resdata = json.loads(res.text)
    cont = resdata['content']

   # 文件路径
    dir = os.getcwd()+'/data/' + vol['name'] + '/'
    fname = dir+art['title']
    if not os.path.exists(dir):
        os.makedirs(dir)
        os.makedirs(dir+'/imgs/')

    # 获取图片地址
    imglist = re.findall(r"\!\[[^\]]*\]\((.+?)\)", cont, re.S)
    for iu in imglist:
        imgUrl = iu.split('?')[0]
        global curImg
        curImg = os.path.basename(imgUrl)
        if not os.path.exists(imgUrl):
            res = requests.get(imgUrl)
            img = res.content
            with open(dir+'imgs/'+os.path.basename(imgUrl), 'wb') as f:
                f.write(img)
            time.sleep(1)

    # 保存md文件
    if art['note_type'] == 2:
        fname += '.md'
    else:
        fname += '.html'
    if os.path.exists(fname):
        os.remove(fname)

    with open(fname, 'a') as f:
        newcont = cont.replace(
            'imgs', 'imgs')
        f.write(newcont)
        f.close()

    return 'getArticles OK!'


def getArticlesList(vol, opt, artnarr):  # 获取文章列表
    volId = vol['id']
    urlVol = 'https://www.jianshu.com/author/notebooks/'+str(volId)+'/notes'
    res = requests.get(urlVol, headers=opt.headers)
    resdata = json.loads(res.text)
    getlist = []  # 指定获取列表
    if len(artnarr) == 0:
        getlist = resdata
    else:
        for i in artnarr:
            if i < len(resdata):
                getlist.append(resdata[i])

    # 每个文集计算文章数量
    global atotal
    global afini
    atotal = len(getlist)
    afini = 0
    print("ATOTAL:", atotal, afini)

    print(len(getlist))

    for d in getlist:
        print('>>>',d)
        global curArt
        curArt = d['title']
        print('GETTING ARTICLE:', curArt)
        time.sleep(1)
        getArticle(d, vol, opt)
        afini += 1 #计数加1
    return 'getArticlesList OK!'


def getVolums(opt, volnarr, artnarr):  # 获取文集列表
    res = requests.get(opt.urlVolumns, headers=opt.headers)
    resdata = json.loads(res.text)
    getlist = []  # 指定获取列表
    if len(volnarr) == 0:
        getlist = resdata
    else:
        for i in volnarr:
            if i < len(resdata):
                getlist.append(resdata[i])
    for d in getlist:
        global curVol
        curVol = d['name']
        print('GETTING VOLUMN:', curVol)
        time.sleep(1)
        getArticlesList(d, opt, artnarr)

    print("DOWNLOAD FINI!", atotal, afini)
    global state
    state = '已完成'
    print(state)
    return 'getVolums OK!'
```
注意每次修改都包含三行代码：
```
global state
state = '已完成'
print(state)
```
先声明要修改全局变量，然后修改，然后用一下这个变量（不用的话编辑器会提示语法错误...也是无奈）

注意整个代码中已经去除了options文件的引入，对genInfoStr函数也做了修复。

##点击按钮启动运行

我们终于可以再次返回到main.py文件了。
首先重新引入options和reqs:
```
import modules.reqs as reqs  # 导入reqs请求函数
import modules.options as opts
```
然后修改run运行和refreshInfo刷新两个函数：
```
def run(): # 启动获取动作
    reqs.getAll(opts, [0, 1], [0])

def refreshInfo(): # 信息的自刷新函数
    text=reqs.genInfoStr()
    text+='\nState:'+reqs.state
    text+='\nCurVol:'+reqs.curVol
    text+='\nCurArt:'+reqs.curArt
    text+='\nCurImg:'+reqs.curImg
    info.config(text=text)
    info.after(500, refreshInfo)
```
删除data文件夹，运行main.py，然后点击开始下载按钮，稍后可以得到指定的文章及图片。

>后续我们将获取界面输入内容，实现自定义下载





---
欢迎关注我的专栏( つ•̀ω•́)つ[【人工智能通识】](https://www.jianshu.com/c/e9a7b7b7024d)

---
###每个人的智能新时代
如果您发现文章错误，请不吝留言指正；
如果您觉得有用，请点喜欢；
如果您觉得很有用，欢迎转载~
---
END