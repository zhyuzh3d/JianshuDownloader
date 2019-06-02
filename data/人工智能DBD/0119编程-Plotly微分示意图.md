>[点击这里进入**人工智能嘚吧嘚**目录，观看全部文章](https://www.jianshu.com/p/ff37dbc75edb)
---

前两篇文章[**微分**](https://www.jianshu.com/p/04ee6b3c927a)、[**微分2**](https://www.jianshu.com/p/fdb2d0f86be9)解说了关于微分的几个基本概念，比如导数、切线、斜率什么的。这些是学习人工智能和机器学习技术的必要基础知识，你可以参照下面y=x<sup>3</sup>/1000函数图像进行回顾和理解。

![](imgs/4324074-c0c8c5c4e2b9d952.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

当然，最好的办法是用代码把它实现一遍，下面的代码利用plotly实现的代码，可以参照理解这张图的原理。

```
#生成微分示意图

import plotly.offline as py
import plotly.graph_objs as go
import random
import math
py.init_notebook_mode()


#原函数
def func(n):
    res = math.pow(n, 3) * 0.0001  
    #y=x^3*0.0001，0.0001仅用来缩小竖向值,控制显示区域
    return res


#计算某x值对应点的斜率，即dy/dx
def slope(x):
    res = 3 * math.pow(x, 2) * 0.0001
    #y=2x^2,从常见导数公式推导f(x)=x^n则f'(x)=(n-1)x^(n-1)
    return res


#计算切线上点的位置
def tangent(x, n):
    k = slope(x)
    return k * n - (k * x - func(x))


#-----------------------------------
#生成曲线数据
def curve(start, end):  #f(x)
    data = go.Scatter(
        x=[n for n in range(start, end)],
        y=[func(n) for n in range(start, end)],
        name='curve')
    return data


#生成切线数据
NoTanLegend = True #只显示第一条线的图例


def tangentLine(x, ran=10):  
    global NoTanLegend
    data = go.Scatter(
        x=[n for n in range(x - ran, x + ran)],
        y=[tangent(x, n) for n in range(x - ran, x + ran)],
        showlegend=NoTanLegend,
        name='tangent',
        mode='lines',
        line={
            'color': 'red',
            'width': 4
        })
    NoTanLegend = False
    return data


#生成横线斜率短线数据
NoSlopeLegend = True


def slopeLine(x, scale):
    global NoSlopeLegend
    k = slope(x)
    data = go.Scatter(
        x=[n for n in range(x, x + int(k * scale))],
        y=[func(x) for n in range(x, x + int(k * scale))],
        showlegend=NoSlopeLegend,
        name='slope',
        mode='lines',
        line={
            'color': 'green',
            'width': 5
        })
    NoSlopeLegend = False
    return data


#生成点数据
def points(li):  #f(x)
    data = go.Scatter(
        x=[n for n in li],
        y=[func(n) for n in li],
        name='points',
        mode='markers',
        marker={
            'size': 8,
            'color': 'black'
        })
    return data


#准备数据
pli = [20, 40, 60, 80] #数据点列表
datas = []
datas += [curve(0, 100)]
datas += [tangentLine(p, 8) for p in pli]
datas += [points(pli)]
datas += [slopeLine(p, 10) for p in pli]

#----------------------------------------
#绘图
layout = go.Layout(  #layout 网格坐标布局
    autosize=False,
    width=800,
    height=600,
    xaxis=dict(range=(0, 100),title='x Axis'),
    yaxis=dict(range=(0, 100),title='y Axis'),
)
fig = go.FigureWidget(datas, layout)
py.iplot(fig)
```
后面的文章会从这些数学知识的基础上继续介绍偏微分和梯度下降等基础概念。


---
>[点击这里进入**人工智能DBD嘚吧嘚**目录，观看全部文章](https://www.jianshu.com/p/ff37dbc75edb)
---
###每个人的智能新时代
如果您发现文章错误，请不吝留言指正；
如果您觉得有用，请点喜欢；
如果您觉得很有用，欢迎转载~
---
END