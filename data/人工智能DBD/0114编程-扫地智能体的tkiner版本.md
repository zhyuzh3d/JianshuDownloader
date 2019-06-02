>[点击这里进入**人工智能嘚吧嘚**目录，观看全部文章](https://www.jianshu.com/p/ff37dbc75edb)
---

这篇是对之前[0109编程-基于Plotly实现的简单智能体思路](https://www.jianshu.com/p/111d5d917453)文章
扫地bot智能体的修改和改进:
- 使用tkiner生成窗体，每按空格键行走一步。
- 实时显示行走步数和剩余灰尘数量。
- 使用了面向对象的方式定义灰尘和机器人。
- 添加了far参数用来增强智能体在上下左右四个方向的视野，修改这个参数可以有效增强扫地效率。


![](imgs/4324074-d0003a0ac93c6763.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

以下是完整代码(部分代码和思路来自蔡媛媛同学)。

```
from tkinter import *
import random
import time

dusts_li = [] #灰尘实例的列表,dust{x,y,id,color,canvas,update()}

#定义Robot类
class Robot:
    def __init__(self, canvas, color,x,y):
        self.canvas = canvas
        self.color=color
        self.id = canvas.create_oval(
            x - 25, y - 25, x + 25, y + 25, fill=color, outline=color)
        self.x = x
        self.y = y
    def update(self): #更新自身的位置。删除旧图形，添加新图形。
        self.canvas.delete(self.id)
        self.id = canvas.create_oval(
            self.x - 25, self.y - 25, self.x + 25, self.y + 25, fill=self.color, outline=self.color)

#定义Dust类
class Dust:
    def __init__(self, canvas, color, x, y):
        self.canvas = canvas
        self.id = canvas.create_oval(
            x - 5, y - 5, x + 5, y + 5, fill=color, outline=color)
        self.x = x
        self.y = y

#获取近邻四格的灰尘索引
def getNearDusts(bot):
    res=[[] for i in range(5)] #左上右下中
    far=200 #robot的视野长度
    for d in dusts_li: #对100个灰尘实例分别放入左上右下中四个列表
        if bot.x-25-far<=d.x<bot.x-25 and bot.y-25<=d.y<bot.y+25:
            res[0].append(d)
        elif bot.x-25<=d.x<bot.x+25 and bot.y+25<=d.y<bot.y+25+far:
            res[1].append(d)
        elif bot.x+25<=d.x<bot.x+25+far and bot.y-25<=d.y<bot.y+25:
            res[2].append(d)
        elif bot.x-25<=d.x<bot.x+25 and bot.y-25-far<=d.y<bot.y-25:
            res[3].append(d)
        elif bot.x-25<=d.x<bot.x+25 and bot.y-25<=d.y<bot.y+25:
            res[4].append(d)
    return res  #返回分组后的列表[[d11,d4],[],[d2],[],[d5]]

#定义reset方法避免出范围
def reset(n):
    if n<25:
        n=25
    if n>475:
        n=475 
    return n

step=0
#移动bot方法
def moveBot(event):
    idli = getNearDusts(robot) #获得分组后实例列表[[d11,d4],[],[d2,d7],[],[d5]]
    countli = [len(d) for d in idli[:4]] #获得分组计数列表[2,0,2,0]
    maxcount = max(countli) #最高值2

    #寻找方向，多个方向上数量相同情况下随机，否则可能卡在死角不动
    nli = [n for n in range(len(countli)) if countli[n] == maxcount] #最高值索引的列表[0,2]
    n = nli[random.randint(0, len(nli) - 1)] #随机一个，0或者2，与idli匹配，表示左上右下中

    px=robot.x
    py=robot.y
    
    #移动robot数据
    if n == 0:
        robot.x = reset(robot.x - 50)
    elif n == 1:
        robot.y = reset(robot.y + 50)
    elif n == 2:
        robot.x = reset(robot.x + 50)
    elif n == 3:
        robot.y = reset(robot.y - 50)

    #吸取中位置的尘土
    for dst in idli[4]:
        dusts_li.remove(dst)
        canvas.delete(dst.id)

    #移动robot
    robot.update()
    
    #计数
    global step
    if robot.x!=px or robot.y!=py:
        step+=1
    retext()

#tkiner初始化
root = Tk()
root.title("Robot")
root.geometry("500x500+1000+100")

canvas = Canvas(root, width=500, height=500, bd=0, highlightthickness=0)

#生成灰尘
for i in range(100):
    dust = Dust(canvas, "grey", random.randint(0, 490), random.randint(0, 490))
    botpos = canvas.coords(dust.id)
    dusts_li.append(dust)

#初始化bot
robot = Robot(canvas, "red", random.randint(0, 475), random.randint(0, 475))

#状态文字
state = {}

def retext():
    if 'id' in state:
        canvas.delete(state['id'])
    state['id'] = canvas.create_text(
        (100, 20), text='STEP:{}  LEFT:{}'.format(step, len(dusts_li)))


retext()

#创建界面
canvas.bind_all("<space>", moveBot)
canvas.pack()
root.mainloop()

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