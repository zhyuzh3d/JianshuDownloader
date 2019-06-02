[智能决策上手系列教程索引](https://www.jianshu.com/p/0d2e46e69f58)
---


>不断更新
部分内容来自于翻译整理

1. ### 多行输出
在Notebook的中开头cell中添加以下代码可以实现多行输出：
```
from IPython.core.interactiveshell import InteractiveShell 
InteractiveShell.ast_node_interactivity = 'all' #默认为'last'
```

例如:
![](imgs/4324074-4671c5cb4b65a333.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

如果需要一劳永逸的在每个文件中自动实现这个功能，可以在macOS的/Users/your_user_name/.ipython/profile_default/或者windows的C:\Users\your_profile\.ipython\profile_default文件夹下创建ipython_config.py文件。（mac下你可以在终端进入这个目录touch ipython_config.py来创建)。
然后打开ipython_config.py文件，添加以下两行：
```
c = get_config()
c.InteractiveShell.ast_node_interactivity = "all"
```
保存，重启Notebook后生效。
![](imgs/4324074-fe08efcb020169b8.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

[更多设置点这里看官方说明](https://ipython.org/ipython-doc/3/config/intro.html)

>感谢[离宫2](https://www.jianshu.com/u/093aadc4509e)提示这个技巧。




1. ### module 'numpy' has no attribute '__version__'
`import pandas as pd`就报这个错误，原因未知，解决方法就是-f强制重新安装：
```
conda install -f numpy
conda install -f pandas
```

1. ####Jupyter Notebook可能是当今最常用的数据科学工具
    写Python代码很多人会告诉你要用Pycharm，但那是开发Python项目用的，  那种由成百上千个文件组成、包含数万行代码的项目必须要很专业的复杂工具才行。
但如果你的目的是数据分析、算法研究等方面的工作，那么Jupyter Notebook    最适合你，因为它足够简单，让你可以专注于数据和算法的逻辑而不是工具。 

1. ###JupyterNotebook不仅可以写代码还能输出图像、表格等
    你可以用用下面一些代码实验（代码来自天池实验室）:   
     ```
     %matplotlib inline
    import numpy as np
     import matplotlib.pyplot as plt
     from scipy.special import jn
     from IPython.display import display, clear_output
    import time
    x = np.linspace(0,5)
    f, ax = plt.subplots()
    ax.set_title("Bessel functions")
    for n in range(1,10):
        time.sleep(1)
        ax.plot(x, jn(x,n))
        clear_output(wait=True)
        display(f)    
    plt.close()
    ```
    得到如下图所示：
![image.png](imgs/4324074-b4a2771d449c0f2b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
常用的绘图分析工具有Matplotlib、Seaborn、plot.ly。

1. #### 使用Anaconda来安装最省事

    如果你要快速开始Python编程，直接下载Anaconda是最简单的，它包含了你所需要的一切，甚至连Python都不需要单独安装。
开机，下载和安装Anaconda，打开Anaconda navigator就看到Jupyter notebook了。
Anaconda3.5.2：
[**百度网盘下载(非VIP较慢)**](https://pan.baidu.com/s/1s8dHBd4PKBRu6t1R0o33Dw)
[**官方下载(Windows电脑使用)**](https://repo.anaconda.com/archive/Anaconda3-5.2.0-Windows-x86_64.exe)
[**官方下载(苹果电脑使用)**](https://repo.anaconda.com/archive/Anaconda3-5.2.0-MacOSX-x86_64.pkg)

1. ### 更省事的是阿里云天池Notebook实验室

    这是一个在线版的Notebook，什么都不需要安装就能开始编码和运行！
唯一麻烦的就是需要你注册并实名认证。
**你在网页里编写Python代码，然后免费在阿里云服务器上运行并返回结果。你写的代码也存在服务器上，不用再担心会丢失了，它甚至包含了代码版本管理功能！**
[**阿里云天池Notebook**](https://tianchi.aliyun.com/)
已知的确缺点有：
    * 不能随意的安装第三方功能模块。不过它已经自带了很多，大多数情况都足够了。
    * 不能安装Notebook插件。基本上也不是问题，没事谁也不折腾这个。
    * 要命的是你不能像控制自己的电脑一样控制远程服务器，当你在爬取某个网站数据的时候，网站发现你的IP（阿里云服务器的IP）访问不正常要求在浏览器内做人工识别字符验证，这时候你就无助了。——如果在你自己电脑上就只要打开浏览器操作一下就OK了。

1. ### Ipython是Jupyter的前身

    Jupyter项目是从Ipython项目演进过来的，所以当你看到存储的文件是`.ipynb`时候不要奇怪，就是ipython notebook的意思。实际上以后在很多地方都会看到Ipy字样。

1. ### JupyterLab是Notebook的加强版

    在Anaconda navigator里面还有一个JupyterLab。Lab在Notebook基础上增加了更多的功能，如果你已经使用过一段时间的Notebook，那可以试试看Lab。

1. ### Shift+回车执行单元代码

    快速运行并输出结果，并跳转到下一个单元。

1. ###代码自动完成

    在代码顶部添加`%config IPCompleter.greedy=True`这一行并且shift+回车运行，对于接下来运行过的内容都会被列入自动提示中。
**按Tab键弹出自动提示**
如下图，输入my然后Tab键就弹出上面自定义的两个变量名，然后按回车直接输入`myCount`，按向下箭头键再回车就输入`myNum`。
![image.png](imgs/4324074-87ad1dcf246add93.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
同样对于`import`导入的功能模块也可以提示。比如下图，输入`requ`然后按tab就自动补全输入`requests`（因为已经导入，并且是唯一的，而刚才的`myCount`和`myNum`都是`my`开头）。
输入到`requests.`的时候按tab就会弹出`requests`包含的所有功能命令，继续输入`g`就得到下图的情况。
![image.png](imgs/4324074-e0b7ab63ec6964a9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

1. ### 不要把代码都写在一个单元cell里！

    这非常重要！
但也不要每行一个cell...
合理安排，一个cell就是一个小的逻辑单元，这样既可以理清思路，又方便单独运行每个cell方便测试寻找问题。
推荐把相关的设置变量都集中放在最上面单独一个或几个cell，这样以后使用时候可以集中修改，不影响代码逻辑。
比如下图中的代码，以后修改只要修改两个变量`num1、num2`就可以直接运行得到结果。
![image.png](imgs/4324074-a402b2914f5ddc16.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
另外一个建议就是把能够独立的代码变为一个`def`单独拿出去作为cell内容,比如下面把求整体方差`avri`分拆出了两个`def`函数，`avg`求平均数，`sqr`求两数差的平方。（代码仅供示意）
![image.png](imgs/4324074-88e4c6b4879718db.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

1. ### Cell不仅可以写代码，还能Markdown
    Markdown是用来写文章的，比如这个简书文章就是用markdown语法写的。
新建cell可以选markdown用来写代码注释。
写起来是这样的：![image.png](imgs/4324074-2a917edb5b64a9d2.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
shift回车运行后是这样的（双击可以返回到修改模式）：
![image.png](imgs/4324074-eaa0084741a6d607.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

1. ###  更改默认打开的项目
    默认Notebook总是打开电脑中我的文档目录，以下方法可以让它打开指定的目录。
打开命令行工具输入
`jupyter notebook --generate-config`
然后会返回一个地址，找到它（可能是隐藏文件），用写字板打开那个文件`jupyter_notebook_config.py`:
![image.png](imgs/4324074-31d9cf45ab953b9a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
然后再顶部添加(等号后面引号内换成你自己的文件夹地址)
`c.NotebookApp.notebook_dir = '/Users/zhyuzh/Desktop/Jupyter'`
然后重新打开Jupyter Notebook就会默认打开这个文件夹了。
    >苹果电脑显示隐藏文件的命令：
`defaults write com.apple.finder AppleShowAllFiles -bool YES `
苹果电脑下复制当前文件夹路径快捷键
`Command+Option+C`

1. ### 扩展插件

    插件可以让Notebook变得更好用一些。一般情况我们不需要安装插件，等你使用久了再慢慢了解。
[**官方Github插件主题列表**](https://github.com/topics/jupyterlab-extension)
[**非官方contrib贡献插件列表**](https://jupyter-contrib-nbextensions.readthedocs.io/en/latest/index.html)
非官方贡献版插件更多更容易安装些，因为可以一次都装上，要用哪个再开启哪个。
安装命令:
`conda install -c conda-forge jupyter_contrib_nbextensions`
运行后可能稍等一下才有反应，根据提示按y。
然后再启用,比如启用collapsible_headings:
`jupyter nbextension enable collapsible_headings/main`
注意`/main`是必须的。
`collapsible_headings`插件可以让Notebook把一个cell折叠起来，在cell菜单下出现`insert head cell`字样：
![image.png](imgs/4324074-55eeae90d4e4ad15.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
    >这个插件在JupyterLab下面好像不能用。不过Lab自身就可以双击折叠一个cell，比这个更方便些。

    >`collapsible_headings/main`其实是指文件夹`collapsible_headings`下的`main.js`文件。所有可用的文件夹名称都可以在电脑里搜索`nbextensions`文件夹找到。苹果电脑的位置类似`/anaconda3/pkgs/jupyter_contrib_nbextensions-0.5.0-py36_0/lib/python3.6/site-packages/jupyter_contrib_nbextensions/nbextensions`
    >JupyterNoteBook的插件本质都是NodeJs的npm插件。如果你了解nodejs那么很容易搞明白它的原理。

1. ###格式化自动美化代码

    代码整齐很重要！
对于Python来说混乱的代码格式可能是致命的！
这里介绍安装`code-pretty`自动格式化插件，先执行命令开启：
`jupyter nbextension enable code_prettify/code_prettify`
依照[官方说明](https://jupyter-contrib-nbextensions.readthedocs.io/en/latest/nbextensions/code_prettify/README_code_prettify.html)还需要执行另外一个命令安装必要的第三方功能模块：
`conda install yapf`
然后就可以看到Notebook如下图出现一个小锤头工具。点击它就能把当前cell的代码自动格式化变整齐了，也可以使用快捷键`Ctrl+L`（苹果下也是ctrl不是Command）。
![image.png](imgs/4324074-c31ce66f49948ce4.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

1. ### 用`?`输出帮助提示
    比如下图:
![image.png](imgs/4324074-42f2183d02367414.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

1. ###运行或载入外部Python文件
      使用`%run`代码可以直接外部的执行.py文件，比如在Notebook文件夹内有一个`a.py`文件：
      ```
      aa='haha'
      print(aa)
     ```
    那么可以用下面代码直接在Notebook内运行它(注意这里的`./`表示在同一文件夹下)
     ```
    %run ./a
    print('>>'+aa)
    ```
    ![image.png](imgs/4324074-28426c6c2e526001.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
如果使用`%load`则直接把代码读进来(下面是`%load ./a`运行的结果)：
![image.png](imgs/4324074-96ad7fd20259e240.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

1. ### 公式编辑器LaTeX
    Notebook的Markdown单元是支持LateX公式编辑的，比如输入`\\( P(A \mid B) = \frac{P(B \mid A) \, P(A)}{P(B)} \\)`运行得到下图：
![image.png](imgs/4324074-38dae826504c914d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
关于LaTeX语法可以在简书里搜索。

1. ###可以保存为.py或pdf文件
    从`file`菜单可以保存为多种格式。


---
[智能决策上手系列教程索引](https://www.jianshu.com/p/0d2e46e69f58)
---
###每个人的智能决策新时代
如果您发现文章错误，请不吝留言指正；
如果您觉得有用，请点喜欢；
如果您觉得很有用，欢迎转载~
---
END



