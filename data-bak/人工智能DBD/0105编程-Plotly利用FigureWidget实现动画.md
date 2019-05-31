>[点击这里进入**人工智能嘚吧嘚**目录，观看全部文章](https://www.jianshu.com/p/ff37dbc75edb)
---
Ploly可以在Jupyter Notebook中显示复杂的图表，甚至可以动画，可以交互。但这篇文章的问题是，**可以利用Plotly在Notebook中做页面小游戏吗？**
接下来几篇文章我们从另外一个角度看看Plotly和Notebook结合带来的更多可能。
[Plotly官网](https://plot.ly/)

提到Plotly的动画实现，很多都是基于figure图形的frames帧属性和transition过场属性实现的，也就是需要预先就计算出动画的参数，放入不同的帧，实现动画，或者利用过场从一个参数变为另一个参数。——这都是已确定的动画，而游戏中包含大量不确定动画组合，因此这个方法基本行不通。
[传统的Plotly动画实现方法](https://plot.ly/python/animations/#reference)

以下内容包含：
- 零基础用Ploly图表创建地图
- 调整地图和角色的样式
- 动画图表上的角色

本节的最终效果如下
![](imgs/4324074-ebc815fc7be7bb6a.gif?imageMogr2/auto-orient/strip)

## 用Ploly图表创建地图

要在Notebook中直接显示Plotly图表，需要导入Offline模块并初始化它
```
import plotly.offline as py
py.init_notebook_mode()
```
当然我们还需要其他几个模块导入，plotly.graph_objs图形对象（graphic objects），time用来控制动画间隔时间，random随机移动位置。
```
import plotly.graph_objs as go
import time
import random
```
用plotly创建图表很简单，只要给go.FigureWidget方法传入一个dict{'x':[2],'y':[2]}即可。如下，它创建了一个图表，其中只有一个数据点在xy坐标(2,2)位置。
```
import plotly.offline as py
import plotly.graph_objs as go
import time
import random

py.init_notebook_mode()

data = dict(x=[2], y=[2])
f = go.FigureWidget([data])
f
```
![](imgs/4324074-667cd1f55cd64bfb.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

如果我们把`data = dict(x=[2], y=[2])`改为`data = dict(x=[1,2], y=[2,3])`则得到两个点(1,2),(2,3)并且自动连线了。
![](imgs/4324074-aaab15fab66b8b7f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

##调整地图和角色的样式

现在的问题是地图的坐标范围并非固定我们需要的0~100，角色点看上去也太小。

我们先修改一下表示角色的点的样子，用下面的代码变大变红,marker标记属性正是表示点的样式，其中symbol元件表示点的形状。
[更多Marker样式](https://plot.ly/python/marker-style/)，[Symbol可选参数](https://plot.ly/python/reference/#scatter-marker-symbol)
```
import plotly.offline as py
import plotly.graph_objs as go
import time
import random

py.init_notebook_mode()

data = go.Scatter(
    x=[50], y=[50], marker={
        'color': 'red',
        'size': 25,
        'symbol': 'circle'
    })
f = go.FigureWidget([data])
f
```
![](imgs/4324074-22540311e358ae0d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

坐标则需要为go.FigureWidget方法传入第二个参数layout，这里分别设置了x和y的坐标xaxis、yaxis，并且关闭了autosize自动放缩坐标范围。
```
import plotly.offline as py
import plotly.graph_objs as go
import time
import random

py.init_notebook_mode()

data = go.Scatter(
    x=[50], y=[50], marker={
        'color': 'red',
        'size': 25,
        'symbol': 'circle'
    })
layout = go.Layout(
    title='TEST',
    autosize=False,
    width=500,
    height=500,
    xaxis=dict(
        autorange=False,
        range=(0, 100),
        dtick=10,
        showline=True,
        mirror='ticks',
    ),
    yaxis=dict(
        autorange=False,
        range=(0, 100),
        dtick=10,
        showline=True,
        mirror='ticks',
    ))

f = go.FigureWidget([data],layout)
f
```
![](imgs/4324074-6c0c1aad8bd0c986.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

##动画图表上的角色

到了最关键的时刻，如何动画？
对于figurewidgets来说，只要不断更新它的数据，就能实现动画。比如，我们不断修改data的x、y的数字就能让红点角色动起来。

在Jupyter Notebook中新建一个cell，用`scatter = f.data[0]`获取到plotly的data对象，注意这个data的x和y都是列表，列表第一个对应的即红点的坐标，我们每一秒更新一下这个x，y数据，红点就会移动起来。
```
scatter = f.data[0]
for i in range(10):
    scatter.x=[scatter.x[0]+random.randint(-1, 1)*10]
    scatter.y=[scatter.y[0]+random.randint(-1, 1)*10]
    time.sleep(1)
```
执行上面这个cell就能看到动画效果。
>这个代码每秒随机的移动一个单元，注意，有可能会移动到画面以外，下篇文章我们将实现更多的游戏功能。

---
>[点击这里进入**人工智能DBD嘚吧嘚**目录，观看全部文章](https://www.jianshu.com/p/ff37dbc75edb)
---
###每个人的智能新时代
如果您发现文章错误，请不吝留言指正；
如果您觉得有用，请点喜欢；
如果您觉得很有用，欢迎转载~
---
END