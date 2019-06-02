>[点击这里进入**人工智能嘚吧嘚**目录，观看全部文章](https://www.jianshu.com/p/ff37dbc75edb)
---

结合[上一篇文章](https://www.jianshu.com/p/525b016717d0)理解下图中标出的偏导数（斜率）和梯度示意。

![](imgs/4324074-5a0a9080712f11ca.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

注意图中两个红色箭头指示出曲面两端的高低不同，所以沿y方向的斜率更大。图中紫色线条指示为负梯度方向，即梯度下降方向。

这个图形的Ploly代码如下:
```
#二元函数
import plotly.offline as py
import plotly.graph_objs as go
import random
import math
py.init_notebook_mode()


#原函数
def func(x, y):
    res = math.pow(x, 3) + math.pow(y, 3) + 2 * x + 400 * y
    return res


#求x方向偏导
def slopex(x, y):
    res = 3 * math.pow(x, 2) + math.pow(y, 3) + 400 * y
    return res


#求y方向偏导
def slopey(x, y):
    res = math.pow(x, 3) + 3 * math.pow(y, 2) + 2 * x
    return res


#------------------------------------数据
#绘制表面
surf = go.Surface(
    z=[[func(x, y) for x in range(0, 20)] for y in range(0, 20)],
    opacity=0.85,
    colorscale='Hot',
    showscale=False,
)

#点位置
point = dict(x=15, y=15, z=func(15, 15))

#绘制蓝色的y方向走向的细线
liney = go.Scatter3d(
    x=[n for n in range(0, 21)],
    y=[point['y'] for n in range(0, 20)],
    z=[func(n, point['y']) for n in range(0, 21)],
    line=dict(width=2, color='blue'),
    mode='lines')

#绘制蓝色的x方向走向的细线
linex = go.Scatter3d(
    y=[n for n in range(0, 21)],
    x=[point['x'] for n in range(0, 21)],
    z=[func(point['x'], n) for n in range(0, 21)],
    line=dict(width=2, color='blue'),
    mode='lines')


#绘制点和斜率线、梯度线
def drawLines(p):
    #绘制点
    marker = go.Scatter3d(
        x=[p['x']],
        y=[p['y']],
        z=[func(p['x'], p['y'])],
        marker=dict(size=5, color='blue'),
        mode='markers')
    
    #斜率的放缩值，根据图像需要任意设定
    slopeScale=0.0005
    
    #x方向斜率线，只绘出开始和结束点
    lineSlopex = go.Scatter3d(
        x=[p['x']] * 2,
        y=[p['y'], p['y'] + slopex(p['x'], p['y']) * slopeScale],
        z=[func(p['x'], p['y'])] * 2,
        line=dict(width=8, color='rgb(0,255,0)'),
        mode='lines')

    #y方向斜率线，只绘出开始和结束点
    lineSlopey = go.Scatter3d(
        x=[p['x'], p['x'] + slopey(p['x'], p['y']) * slopeScale],
        y=[p['y']] * 2,
        z=[func(p['x'], p['y'])] * 2,
        line=dict(width=8, color='rgb(0,255,0)'),
        mode='lines')

    #x、y方向斜率线相加得到梯度方向矢量
    lineGradient = go.Scatter3d(
        x=[p['x'], p['x'] + slopey(p['x'], p['y']) * slopeScale],
        y=[p['y'], p['y'] + slopex(p['x'], p['y']) * slopeScale],
        z=[func(p['x'], p['y'])] * 2,
        line=dict(width=8, color='rgb(255,0,0)'),
        mode='lines')

    #负梯度方向矢量，即梯度下降矢量
    lineDescent = go.Scatter3d(
        x=[p['x'], p['x'] - slopey(p['x'], p['y']) * slopeScale],
        y=[p['y'], p['y'] - slopex(p['x'], p['y']) * slopeScale],
        z=[func(p['x'], p['y'])] * 2,
        line=dict(width=8, color='rgb(255,0,255)'),
        mode='lines')

    return [lineSlopex, lineSlopey, lineGradient, lineDescent, marker]


datas = [surf, linex, liney]
datas = datas + drawLines(point)

#----------------------------------------绘图
layout = go.Layout(
    title='f(x,y)=x^3+y^3+2*x+400*y',
    width=800,
    height=800,
    scene=dict(
        xaxis=dict(title='x'),
        yaxis=dict(title='y'),
        zaxis=dict(title='f(x,y)'),
    ))

fig = go.FigureWidget(datas, layout=layout)
py.iplot(fig)
```


---
>[点击这里进入**人工智能DBD嘚吧嘚**目录，观看全部文章](https://www.jianshu.com/p/ff37dbc75edb)
---
###每个人的智能新时代
如果您发现文章错误，请不吝留言指正；
如果您觉得有用，请点喜欢；
如果您觉得很有用，欢迎转载~
---
END