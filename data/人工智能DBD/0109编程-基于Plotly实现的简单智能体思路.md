>[点击这里进入**人工智能嘚吧嘚**目录，观看全部文章](https://www.jianshu.com/p/ff37dbc75edb)
---

人工智能是研究什么的？
—— 智能体Agent。

研究智能体的什么？
——感知能力、思维能力、行动能力。

假设有一种极其简单的单细胞病毒生物，它可以感知到周边环境中糖分的浓度，如果浓度低于上一位置它就后退，如果浓度高于上一位置它就前进。
- 感知能力就是对周边糖分的分辨能力。
- 思维能力就是根据糖分变化决定如何行动。
- 行动能力就是实现前进或后退。

更多智能体相关的讨论可以参考经典人工智能教材《人工智能：一种现代方法》。

下面用代码模拟一个简单的扫地机器人智能体：
- 感知能力：查找当前位置的灰尘dust。
- 思维能力：找到周边上下左右四个位置的中的随机一个。
- 行动能力：清理当前位置的灰尘和上下左右行进。

![](imgs/4324074-5a1810392fb901d5.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


####创建地图和灰尘
dusts和bot都是一个列表的列表，`[[],[],...]`，bot其实使用单层[x,y]也可以。
dusts是所有灰尘的实际位置列表，`[[32,11,1],[87,22,1]...]`,三个数字前两个是x,y坐标，第三个1表示未被清理。

mapGrid是地图每个方格单元列表,二维嵌套,`[[{},{},...],[{},{},...],...]`,以便于通过横列col和行row索引到，比如mapGrid[col][row]获得一个单元。
mapGrid的每个单元是一个dict，可以包含很多信息，其中'dusts'属性是灰尘在dusts中的序号的列表。`{'dusts':[34,21]}`表示这个位置有两个灰尘，分别是dusts[34]和dusts[21]。

```
import plotly.offline as py
import plotly.graph_objs as go
import time
import random
import math

py.init_notebook_mode()

dusts = [[random.randint(0, 99), random.randint(0, 99), 1] for i in range(100)]
bot = [[random.randint(0, 9), random.randint(0, 9)]]

#尘土放入地图
mapGrid = [[{'dusts': []} for x in range(10)] for y in range(10)]
for i in range(len(dusts)):
    col = math.floor(dusts[i][0] / 10)
    row = math.floor(dusts[i][1] / 10)
    mapGrid[col][row]['dusts'].append(i)

fig = go.Figure()
bot_data = dict(
    x=[bot[0][0] * 10 + 5],
    y=[bot[0][1] * 10 + 5],
    mode='markers',
    name='bot',
    marker={
        'color': 'red',
        'size': 25,
        'symbol': 'circle'
    })
dust_data = dict(
    x=[d[0] for d in dusts if d[2] == 1],
    y=[d[1] for d in dusts if d[2] == 1],
    mode='markers',
    name='dust',
    marker={
        'color': 'gray',
        'size': 5,
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

f = go.FigureWidget([dust_data, bot_data], layout)
```
####清理当前位置灰尘的函数

在这里def的函数并没有使用位置参数，而是直接针对bot的位置进行清理，并且清理后直接更新了plotly数据。这只是为了偷懒。
注意`mapGrid[bot[0][0]][bot[0][1]]['dusts']`获得当前位置灰尘索引的列表，如[34,21]。
` [d[0] for d in dusts if d[2] == 1]`这两句是重建plotly的数据。

```
#清理当前位置
def clean():
    cell_dusts = mapGrid[bot[0][0]][bot[0][1]]['dusts']
    for d in cell_dusts:
        dusts[d][2] = 0
    f.data[0]['x'] = [d[0] for d in dusts if d[2] == 1]
    f.data[0]['y'] = [d[1] for d in dusts if d[2] == 1]    

clean()
```

####移动机器人的函数
canto是可能的移动方向，上下左右四个x,y构成的方向向量。
`moveto = canto[random.randint(0, len(canto) - 1)]`,是随机一个方向，注意random.randint(a,b)的时候，a和b都可能取到，所以要减1。
对nextpos进行0~9的约束，防止超出地图范围。
最终返回的`bot[0] != orgpos`表示是否bot真的被移动了，因为有可能移动超出0~9范围导致被自动重置回来，这种情况下应该不计算步数。

```
#移动机器人
def bot_move():
    canto = [[1, 0], [-1, 0], [0, 1], [0, -1]]
    moveto = canto[random.randint(0, len(canto) - 1)]
    orgpos = [bot[0][0], bot[0][1]]
    nextpos = [bot[0][0] + moveto[0], bot[0][1] + moveto[1]]
    if nextpos[0] < 0:
        nextpos[0] = 0
    if nextpos[0] > 9:
        nextpos[0] = 9
    if nextpos[1] < 0:
        nextpos[1] = 0
    if nextpos[1] > 9:
        nextpos[1] = 9
    bot[0] = [nextpos[0], nextpos[1]]
    
    f.data[1]['x'] = [bot[0][0] * 10 + 5]
    f.data[1]['y'] = [bot[0][1] * 10 + 5]
    
    return bot[0] != orgpos
```

####显示游戏
用f做变量很不合理，但懒就不改了...
直接f在Notebook中显示图像。
```
f
```

####进行50次并统计剩余灰尘数量

step是实际步数，run是循环执行次数，由于有些时候bot超出范围被重置回来就没有形成实际步数，所以run>=step。
注意只在形成实际移动的情况下才`time.sleep`，没实际移动就不停顿等待。

```
step = 0
run = 0
for i in range(1000):
    if step < 50:
        domove = bot_move()
        run += 1
        if domove:
            step += 1
            
            time.sleep(0.1)
            clean()
            

print(run, step, len([d for d in dusts if d[2] == 1]))
```

####更智能的思维能力

一般情况这个结果都很糟糕，行动50步，但只能清理掉1/3左右的灰尘，而实际我们知道如果按照某个顺序逐个位置清理，不重叠的路径，那么平均应该可以清理掉50个灰尘才对。

下面的代码改变了移动策略，bot先判断上下左右四个位置的灰尘数量，然后向灰尘最多的方向前进（如果同样多就随机选一个）。

使用了三个cell代码实现这个策略。

把范围约束定义为函数备用。
```
#如果超出范围就重置
def rerange(n):
    if n < 0:
        n = 0
    if n > 9:
        n = 9
    return n
```

直接根据bot的位置计算上下左右四个格子灰尘数量，返回最多灰尘的方向。
```
#计算上下左右四个格子的粒子数，返回最多一格的方向
def evaluate():
    pos = bot[0]
    canto = [[1, 0], [-1, 0], [0, 1], [0, -1]]
    posli = [[pos[0] + offset[0], pos[1] + offset[1]] for offset in canto]
    countli = []
    for n in range(len(posli)):
        p = posli[n]
        if p[0] == rerange(p[0]) and p[1] == rerange(p[1]):
            cell_dusts=[d for d in mapGrid[p[0]][p[1]]['dusts'] if dusts[d][2]==1]
            countli.append(len(cell_dusts))
        else:
            countli.append(-1)
    maxn = max(countli)
    gotoli = [i for (i, v) in enumerate(countli) if v == maxn]
    randgoton = gotoli[random.randint(0, len(gotoli)-1)]
    return canto[randgoton]

evaluate()
```
改写原有的移动机器人的函数。
```
#移动机器人
def bot_move():
    orgpos = [bot[0][0], bot[0][1]]
    offset = evaluate()
    nextpos = [orgpos[0] + offset[0], orgpos[1] + offset[1]]
    nextpos[0]=rerange(nextpos[0])
    nextpos[1]=rerange(nextpos[1])
    bot[0] = [nextpos[0], nextpos[1]]

    f.data[1]['x'] = [bot[0][0] * 10 + 5]
    f.data[1]['y'] = [bot[0][1] * 10 + 5]

    return bot[0] != orgpos
```
这样的bot的清理效率要远高于随机的情况，有时候会明显高于50%，但有些情况bot陷入空白区域也会乱转导致低于预期。
当然还可以考虑预测两步的情况，上下左右四个位置，以及每个位置周边3个位置，共4组4个位置分别求灰尘总数，然后向此方向前进。当然还有有其他的算法，比如考虑[1,0][2,0]这样的更远的位置。总之，扩大智能体的感知能力肯定可以明显提高清理效率。

>这是极其简陋的智能体案例，其实主要用来帮助新手熟悉python语法用的，尤其是数组的操作。如果你有更好的想法请留言分享给大家~


---
>[点击这里进入**人工智能DBD嘚吧嘚**目录，观看全部文章](https://www.jianshu.com/p/ff37dbc75edb)
---
###每个人的智能新时代
如果您发现文章错误，请不吝留言指正；
如果您觉得有用，请点喜欢；
如果您觉得很有用，欢迎转载~
---
END