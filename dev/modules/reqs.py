
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
    imglist = re.findall(r"[^`]\!\[[^\]]*\]\((.+?)\)", cont, re.S)
    for iu in imglist:
        imgUrl = iu.split('?')[0]
        global curImg
        curImg = os.path.basename(imgUrl)
        print('GETTING IMAGE:', curImg)
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
            'https://upload-images.jianshu.io/upload_images', 'imgs')
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

    n = 0
    for d in getlist:
        global curArt
        curArt = str(n)+':' + d['title']
        n += 1
        print('GETTING ARTICLE:', curArt)
        time.sleep(1)
        getArticle(d, vol, opt)
        afini += 1  # 计数加1
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
    n = 0  # 序号
    for d in getlist:
        global curVol
        curVol = str(n)+':'+d['name']
        n += 1
        print('GETTING VOLUMN:', curVol)
        time.sleep(1)
        getArticlesList(d, opt, artnarr)

    print("DOWNLOAD FINI!", atotal, afini)
    global state
    state = '已完成'
    print(state)
    return 'getVolums OK!'

#...