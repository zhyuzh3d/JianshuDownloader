>[点击这里进入**人工智能嘚吧嘚**目录，观看全部文章](https://www.jianshu.com/p/ff37dbc75edb)
---

plotly可以绘制3d空间的散点、线段或者表面。


![](imgs/4324074-44ec93e55b477a1b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

代码并不复杂，只是注意go.Surface()的参数中只用了z，它是包含了y个row的list，每个row又是包含了x个col的值，每个值就是z的数值，共有x*y个值，示意如[[z,z,z,....共x个],[z,z,z,....共x个],[z,z,z,....共x个]...共y个]。这看起来就像excel表格，列是x值（从0起），行是y值（从0起），每单元格是z值。

![](imgs/4324074-a06205b417971dc9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


```
#生成3d图f(x,y)曲面
import plotly.offline as py
import plotly.graph_objs as go
import random
import math
py.init_notebook_mode()

#原函数
def func(x, y):
    res = math.pow(x, 2) + math.pow(y, 2) + x * y * 0.5
    return res

#------------------------------------数据
surf = go.Surface(
    z=[[func(x - 100, y - 100) for x in range(0, 200, 40)]
       for y in range(0, 400, 40)],
    opacity=1,
    colorscale='Hot')

datas = [surf]
print(surf['z'])

#----------------------------------------绘图
layout = go.Layout(
    autosize=False,
    width=1200,
    height=1200,
)

py.iplot(datas)
```

>colorscale的可选值有:
Greys,YlGnBu,Greens,YlOrRd,Bluered,RdBu,Reds,Blues,Picnic,Rainbow,Portland,Jet,Hot,Blackbody,Earth,Electric,Viridis,Cividis.

##参考链接
[官方文档](https://plot.ly/python/reference/#surface)
[官方示例](https://plot.ly/python/3d-surface-plots/)

---
>[点击这里进入**人工智能DBD嘚吧嘚**目录，观看全部文章](https://www.jianshu.com/p/ff37dbc75edb)
---
###每个人的智能新时代
如果您发现文章错误，请不吝留言指正；
如果您觉得有用，请点喜欢；
如果您觉得很有用，欢迎转载~
---
END