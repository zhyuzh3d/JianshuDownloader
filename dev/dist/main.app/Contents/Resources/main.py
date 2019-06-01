from tkinter import *
from tkinter import ttk
import time
import random
import modules.reqs as reqs  # 导入reqs请求函数
import modules.options as opts
from tkinter.scrolledtext import ScrolledText
import os

# 创建窗体
root = Tk()
root.title('简书文章下载器')
root.resizable(width=False, height=False)
root.config(background='#EEE')


def run():  # 启动获取动作
    hdrs = iptHeader.get("1.0", END)
    vols = iptVol.get("1.0", END)
    arts = iptArt.get("1.0", END)

    opts.headers = opts.str2obj(hdrs, '\n', ': ')

    volnarr = []
    vols=vols.replace('\n', '')
    volsarr = vols.split(',')
    volnarr = map(lambda x: int(x), volsarr)
    volnarr = list(set(volnarr))

    artnarr = []
    artsarr = arts.split(',')
    map(lambda x: int(x), artsarr)
    artnarr = list(set(artnarr))

    writeHeaders()  # 保存设置

    reqs.getAll(opts, volnarr, artnarr)


def refreshInfo():  # 信息的自刷新函数
    text = reqs.genInfoStr()
    text += '\nState:'+reqs.state
    text += '\nCurVol:'+reqs.curVol
    text += '\nCurArt:'+reqs.curArt
    text += '\nCurImg:'+reqs.curImg
    info.config(text=text)
    info.after(500, refreshInfo)


# 创建界面
rown = 0  # 占位符
ttk.Frame(root, height=10).grid()

rown += 1  # header输入框
iptHeader = ScrolledText(root, height=1, width=50)
iptHeader.grid(row=rown, padx=10, pady=0, sticky=W)

rown += 1  # header输入框说明
text1 = '''
请从浏览器右击检查打开控制台
切换到Network部分
从XHR类型中找到notebooks请求
复制它的Request Headers部分
注意不要包含:打头的部分，并去除if-none-match行'
'''
label1 = ttk.Label(root, text=text1)
label1.grid(row=rown, pady=0, padx=10, sticky=W)

rown += 1  # 占位符
ttk.Frame(root, height=20).grid(row=rown)

rown += 1  # 文集序号输入框
iptVol = Text(root, height=1, width=50)
iptVol.grid(row=rown, padx=10, pady=0, sticky=W)

rown += 1  # vol输入框说明
label2 = ttk.Label(root, text='文集列表，请用英文逗号分隔，如0,1,2')
label2.grid(row=rown, pady=0, padx=10, sticky=W)

rown += 1  # 占位符
ttk.Frame(root, height=20).grid(row=rown)

rown += 1  # 文集序号输入框
iptArt = Text(root, height=1, width=50)
iptArt.grid(row=rown, padx=10, pady=0, sticky=W)

rown += 1  # vol输入框说明
label3 = ttk.Label(root, text='文章列表，请用英文逗号分隔，如0,1,2')
label3.grid(row=rown, pady=0, padx=10, sticky=W)

rown += 1  # 占位符
ttk.Frame(root, height=30).grid(row=rown)

# 运行按钮
rown += 1
bt = ttk.Button(root, text='开始下载', width=30, command=run)
bt.grid(row=rown, padx=10, ipady=10, pady=0, sticky='WE')

# 信息标签
rown += 1
info = ttk.Label(root, text='?/?')
info.grid(row=rown,  padx=10, ipady=10, ipadx=10, sticky=W)
info.after(500, refreshInfo)  # 自动循环更新


def writeHeaders():  # 将header写入到临时文件
    hdrs = iptHeader.get("1.0", END)
    with open(os.getcwd()+'/config.txt', 'a') as f:
        f.write(hdrs)


def readHeaders():  # 读取设置文件并填充到界面
    fpath = os.getcwd()+'/config.txt'
    if os.path.exists(fpath):
        f = open(fpath, 'r')
        hdrs = f.read()
        iptHeader.insert(INSERT, hdrs)


readHeaders()

root.mainloop()

#...