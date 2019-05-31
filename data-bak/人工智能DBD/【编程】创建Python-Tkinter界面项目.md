欢迎关注我的专栏( つ•̀ω•́)つ[【人工智能通识】](https://www.jianshu.com/c/e9a7b7b7024d)
[【专题】Python-Tkinter项目编程入门](https://www.jianshu.com/p/0f5011b3d6bb)

---

##主要工具
- 编写工具：VSCode
- 编写语言：Python
- 项目管理：Github+Git
- 编写界面：Tkinter

##初始化项目

1. 新建一个JianshuDownloader文件夹
1. 使用VSCode打开这个文件夹
1. 在Github上创建JianshuDownloader项目，勾选Initialize this repository with a README，自动创建一个README.md文件
1. 在VSCode中菜单【终端-新建终端】打开终端，输入`git init`初始化项目
1. `git config --global user.name "zhyuzh"`命令设置你的任意名字
1. `git config --global user.email "zhyuzh3d@hotmail.com"`命令设置任意你的邮箱
1. `git remote add origin https://username:password@github.com/zhyuzh3d/JianshuDownloader.git`链接到你的Github项目，注意修改这里你的路径（/zhyuzh3d)，以及你的用户名（与后面zhyuzh3d一致，不是邮箱）和密码
1. `git pull origin master` 拉取远程Github项目文件，得到README.md文件
1. 在VSCode中新建一个dev文件夹用来放置代码，文件夹内再新建一个main.py文件，随便写点注释文字如`#JianshuDownloader`，保存，如果提示install ...lint那就点击install安装，这是安装代码提示器
1. 在源代码管理器面板的输入处随便写点什么如`初始化`,然后Ctrl+回车提交到本地Git
1. 然后从三个点的菜单选择【推送到】，再从弹出的列表选择唯一选项，推送到Github
1. 在Github中检查你的JianshuDownloader项目中是否已经新增了dev文件夹和main.py文件

>如果遇到技术问题，可以参考这两个文章：
[软件技术-零基础搭建Golang的vsCode开发环境](https://www.jianshu.com/p/4a3b9863577b)
[【编程】VSCode下Git与Github同步](https://www.jianshu.com/p/f16fabba0148)

##测试界面
对于Python3.x，Tkinter已经是标准内置模块，可以直接使用而不需要单独安装。

修改main.py文件，添加以下内容进行测试：
```
from tkinter import *
from tkinter import ttk
import random

root = Tk()
root.title('MyApp')
root.resizable(width=False, height=False)
root.config(background='#EEE')
root.geometry('300x150')

def gen():
    val.set(repr(random.random()))

val = StringVar()
val.set('3.14')
ttk.Frame(root, height=20).grid()
lb=ttk.Entry(root,textvariable=val).grid(row=1, column=1, pady=10, padx=10,ipady=5,sticky='nsew')
bt = ttk.Button(root, text='Random', width=20, command=gen).grid(
    row=2, column=1, ipady=10, ipadx=10, sticky=E)

root.mainloop()

```
可以用`python main.py`来运行这段代码，也可以使用Run Code插件来运行，这会弹出一个小窗口，上面有个按钮，点击将随机改变输入框内的数字。

![](imgs/4324074-ccc62ffb5b23aa04.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

几点说明：
- `root = Tk()`是初始化界面窗口，最后要`mainloop()`启动它
- `root.geometry('300x150')`这个奇葩写法可以设定窗口的尺寸
- `def gen():`定义了gen函数，并在下面`command=gen`当按钮点击时候调用它
- `val = StringVar()`初始化一个字符串变量，并在`textvariable=val`动态绑定它
- `grid(row=2, column=1, ipady=10, ipadx=10, sticky=E)`这是添加到画面并设定位置，按照row-col行列模式，ipady和ipadx是内边距，`sticky=E`这里的E是指东面右侧对齐


>后续我们再深入使用Tkinter界面工具。


---
欢迎关注我的专栏( つ•̀ω•́)つ[【人工智能通识】](https://www.jianshu.com/c/e9a7b7b7024d)

---
###每个人的智能新时代
如果您发现文章错误，请不吝留言指正；
如果您觉得有用，请点喜欢；
如果您觉得很有用，欢迎转载~
---
END