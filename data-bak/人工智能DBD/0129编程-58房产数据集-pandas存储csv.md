>[点击这里进入**人工智能DBD嘚吧嘚**目录，观看全部文章](https://www.jianshu.com/p/ff37dbc75edb)
---

[前面两篇文章介绍了58房产租房信息的爬取和解密](https://www.jianshu.com/p/9975de57b0ce)，这次我们把它整理并做初步分析，再存储为csv备用，并利用[之前的数学知识](https://www.jianshu.com/p/525b016717d0)思考一下如何进行预测。

如果你还没有爬取成功html文件，可以直接从这里下载共99页包含4000多个租房信息的html文件压缩包。
百度网盘链接:https://pan.baidu.com/s/1W86kbqZArLKG7v1PTlufjw  密码:k96p

## 读取原始数据

参考之前文章的代码，这里为了完整，从头来一下，标*表示和前一篇文章一样完全没变，如果看过的可以直接跳过。

####字符批量替换函数*
```
#使用字典批量替换
import re

def multReplace(text, rpdict):
    rx = re.compile('|'.join(map(re.escape, rpdict)))
    return rx.sub(lambda match:rpdict[match.group(0)], text)
```
####58房产专用字体数字解密函数*
```
#解密58房产的字体加密
from fontTools.ttLib import TTFont
import base64
import re
import io

def decode58Fangchan(html,key):
    glyphdict = {
        'glyph00001': '0',
        'glyph00002': '1',
        'glyph00003': '2',
        'glyph00004': '3',
        'glyph00005': '4',
        'glyph00006': '5',
        'glyph00007': '6',
        'glyph00008': '7',
        'glyph00009': '8',
        'glyph00010': '9'
    }    
    data = base64.b64decode(key)  #base64解码
    fonts = TTFont(io.BytesIO(data))  #生成二进制字节
    cmap = fonts.getBestCmap()  #十进制ascii码到字形名的对应{38006:'glyph00002',...}
    chrMapNum = {}  #将变为{‘龥’:'1',...}
    for asc in cmap:
        chrMapNum[chr(asc)] = glyphdict[cmap[asc]]

    return multReplace(html,chrMapNum)
```
####将单个html页面转为租房信息对象列表的函数

这里有一些说明
- 对于`3室2厅1卫        98㎡`这样的字符串要提取室、厅、卫和平米数量，我使用了`re.compile(r'[\d]+室').findall(arealine)[0].replace('室', '')`这样的正则表达式方法，`[\d]+室`中`\d`表示数字，`+`表示数字至少是1个，`室`表示必须包含室字，这样得到的就是`['3室']`，然后再替换掉室字。
- 在`jjr`经纪人这行，后来发现还有`geren`个人或者其他情况，所以就改为提取倒数第二个`contents`来解决。
- 有些地方使用了`multReplace(jjr, {'\xa0': '',  '\n': ''})`方法把冗余内容清理掉。
- `add = re.sub(r'[\s]+', ' ', add).strip()`使用正则表达式把多个空格`[\s]+`替换为单个空格。

```
#读取单个页页面
from bs4 import BeautifulSoup
import html
import re


def getpitem(url):
    with open(url, 'r') as f:
        text = html.unescape(f.read())  #将&#x958f;室变为閏室
        key = re.findall(r"base64,(.*)'\).format", text)[0]  #用正则表达式提取AAE..AAA
        dehtml = decode58Fangchan(text, key)
        soup = BeautifulSoup(dehtml)
        li = soup.find('ul', 'listUl').find_all('li')[:-1]  #最后一个是页码

        pitems = []  #单页的租赁信息列表
        for item in li:
            title = item.find('h2').text
            title = re.sub(r'[\s]+', ' ', title).strip()  #多空格替换为单个空格
            money = item.find('b', 'strongbox').text.strip()
            arealine = item.find('p', 'room strongbox').text
            shi = re.compile(r'[\d]+室').findall(arealine)[0].replace('室', '')
            ting = re.compile(r'[\d]+厅').findall(arealine)[0].replace('厅', '')
            wei = re.compile(r'[\d]+卫').findall(arealine)[0].replace('卫', '')
            area = re.compile(r'[\d\.]{1,5}㎡').findall(arealine)[0].replace(
                '㎡', '')

            add = item.find('p', 'add').text.strip()
            add = multReplace(add, {'\xa0': '', '\n': ''})  #去冗余字符和回车
            add = re.sub(r'[\s]+', ' ', add).strip()  #多空格替换为单个空格

            jjr = item.find('div', 'des').contents[-2:-1][0].text  #经纪人或个人或...
            jjr = multReplace(jjr, {'\xa0': '', '\n': ''})  #多空格替换为单个空格
            jjr = re.sub(r'[\s]+', ' ', jjr).strip()

            info = {
                'title': title,
                'money': money,
                'shi': shi,
                'ting': ting,
                'wei': wei,
                'area': area,
                'add': add,
                'jjr': jjr,
            }

            pitems.append(info)

        return pitems
```
#### 批量读取html文件
```
import os
files = os.listdir(r'./pages/')
file_li = [r'./pages/' + s for s in files]

itemsAll = []

for f in file_li:
    itemsAll = itemsAll + getpitem(f)
print(len(itemsAll))
len(file_li)
```
上面代码正常的话应该输出4596和99。
如果打印`itemsAll`则会得到如下显示：
![](imgs/4324074-82c3c640c776041a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

####用Pandas转换为DataFrame

```
import pandas as pd

col=[k for k in itemsAll[0]]
rows=[[item[k] for k in item] for item in itemsAll]

df=pd.DataFrame(rows,columns=col)
df
```
注意这里`DataFrame()`方法的第一个参数是4596个租房数据对象的列表，而每个数据对象就是8个属性值组成的列表（是`['新未...览中心', '3800', '2'...]`,而不是字典`{'title': '新未来...览中心', 'money': '3800', 'shi': '2', 'ting': '2'...}`)。

它的第二个参数是表头栏的名称,`['title', 'money', 'shi', 'ting', 'wei', 'area', 'add', 'jjr']`共8个列。如果这个列数和rows每个数据的列表长度不一致就会报错。

输出结果如下图：
![](imgs/4324074-7975e76dee66e4ba.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

####保存为csv

```
df.to_csv('58suzhou_zufang_4k.csv')
```
只要这一句就可以了。用下面代码验证是否已经保存成功。
```
df2=pd.read_csv('58suzhou_zufang_4k.csv')
df2[:10]
```
正常的话会输出前10个数据。
![](imgs/4324074-4b4aaeb5f585a0fb.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


####Plotly绘制散点图

```
import plotly.offline as py
import plotly.graph_objs as go
py.init_notebook_mode()
data = go.Scatter(
    x=[m['area'] for m in itemsAll],
    y=[m['money'] for m in itemsAll],
    mode='markers')


layout = go.Layout(  #layout 网格坐标布局
    title='房价与面积',
    autosize=False,
    width=600,
    height=600,
    xaxis=dict(  #axis，x,y
        autorange=False,
        range=(0, 200),
    ),
    yaxis=dict(  #axis，x,y
        autorange=False,
        range=(0, 12000),
    ),
)
fig = go.FigureWidget([data], layout)
fig
```
可以输出得到下图：
![](imgs/4324074-977d492c3b459203.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


##分析思考

我们的问题需求是：**当房东用户在58房产网上录入一个新的房产信息的时候，我们为他提供一个可靠的参考租价**。

假设我们只考虑面积，认为租价money只和房屋的面积area有关，那么我们从上图中可以找到一些规律。

比如横轴100平米的房子，租价都在2k上下，大约都在1.8k到3k这段，只有个别的少量飘到上面6~8k，也许我们给这个房东建议一个1.8+3=2.4比较合理一些。

怎么用算法实现？可以想出很多办法：

- 找出和变量x面积相近的数据，比如找出所有都是100平方左右的数据点，然后把它们的房价相加再平均。如果怕用户是107.3平米找不出横轴一样的数据点，那还可以找一个范围的，比如把102.3~112.3平米之间的都找出再求平均。

- 找到房价和面积之间的线性关系，就是下图这个箭头方向的直线的方程，找出a和b，然后把x面积带进入就能算出y。
![](imgs/4324074-1af40b2ff85b5ed9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

也许还有更多方法，但别忘了，我们需要一种具有通用性的方法，就是这种方法能扩充到房价以外的多个因素才行，因为我们都知道，只靠面积得到的结果并不太靠谱。








---
>[点击这里进入**人工智能DBD嘚吧嘚**目录，观看全部文章](https://www.jianshu.com/p/ff37dbc75edb)
---
###每个人的智能新时代
如果您发现文章错误，请不吝留言指正；
如果您觉得有用，请点喜欢；
如果您觉得很有用，欢迎转载~
---
END