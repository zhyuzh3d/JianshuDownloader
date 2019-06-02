依照Python官方的方法手工安装python和tensorflow以及一个个手工安装众多的模块是很麻烦的，也常出现难缠的奇葩问题。
这个文章带领大家完全从零开始利用Anaconda一下子把Python和上百个科学计算模块都装好，并且开始用Python真正的编写代码。

###Anaconda介绍

**Anaconda [ænə'kɑndə] 水蟒。它是一个Python语言的免费增值发行版，用于进行大规模数据处理, 预测分析, 和科学计算, 致力于简化模块的管理和部署。**

![logo](imgs/4324074-469c6fda536e52d1.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


>**免费增值**：有免费版也有收费版，或者软件免费但有内购，总之，发行者还是希望用户付钱的。Anaconda是由Anaconda公司开发和发行的，可以完全免费使用，但该公司还有其他收费产品如Anaconda Enterprise（企业版）和Training（培训与认证）等

>**Python发行版**：由于Python是开源的，就像小米华为都基于Android安卓开发了各自的手机系统一样，也有很多公司对Pytho进行改造和再包装，然后免费发行出来或者商业销售。当然，这些第三方的发行版或多或少都会做一些有价值的改进，否则也就没有存在的必要了。常见的Python发行版除了Anaconda外还有WinPython、Python(x,y)等，但易用度和流行度都不如Anaconda。


###模块化开发

我们实际编程开发中使用的Python并不仅仅是指从Python官方网站下载的那个安装包所带来的内容，也不是仅仅是指使用Python官方的那些编程命令来写代码。

我们不会真的自己亲手去写每一个功能，那样的话全世界会有成千上万的程序员反反复复写着同样的功能同样的代码，——这太浪费了。

我们可以把自己曾经写好的一段代码重新拿来在新的编程项目里面使用，就好像把一张照片复制一份放到新的相册一样。同样我们扩大到更多人，大家把自己写好的一段段代码贡献出来，互相分享，互相借鉴（复制），这样一来，我们真实的编程开发就变成了用各种代码片段来搭积木了。这就是模块化。

全世界的开发者已经为Python开发了数以万计的各种模块，实现千变万化的功能，我们可以把这些模块自由组合成各种软件和程序。
![模块化开发](imgs/4324074-6ee8018d284cb8f8.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


那么问题也来了，怎么安装别人编写的模块？安装后怎么卸载？怎么更新已经用到的模块？如果Jack开发的A模块里面又使用了Tom开发的B模块，这种情况又该怎么办？

我们需要一个模块管理工具，就像手机的App store应用商店那样来帮我们管理各种各样的模块。

在编程领域，并不会使用一个有界面的软件来做模块管理，因为程序员们更喜欢直接输入命令代码，比如```shangdian anzhuang wangzherongyao```(让应用商店安装一个王者荣耀)。

在Anaconda中就自带了这样一个模块管理器，它的名字不叫shangdian，而是叫做conda，后面我们会学到具体怎么召唤它出来干活。

Anaconda的商店还自带了“模块全家桶”，当大家安装Anaconda的时候，默认就把超过150个数据科学和机器学习相关的常用模块都安装好，这就让我们省了很多事。

### 下载与安装
直接进入[**Anaconda官方站点**](https://www.anaconda.com/)然后点击右上角【Download】按钮，进入下载页面之后选择Windows版本或者MacOS苹果电脑版本，然后点击左边Python3.6版本的Download按钮就会开始下载了。
因为有数百个模块打包在一起，所以文件比较大，请慢慢等待。
![下载安装包](imgs/4324074-b40277e7c16cb2fa.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

也可以从[**百度云下载Anaconda5.2的Win/Mac安装文件](链接:https://pan.baidu.com/s/1pJ38MmXNBOcXYsj8kqhBTg)  密码:1jc3

下载后直接安装，一步一步都使用默认选项不修改即可（VS code可以skip跳过）。
windows下这个安装过程可能很慢，需要十几分钟。

安装完成后，打开命令行工具（windows的Anaconda Prompt[prɒmpt],Mac下使用终端），输入```conda info```回车，应该得到类似下面的信息。
>Windows10要使用Anaconda Prompt命工具，在【所有程序列表-Anaconda3下面】，或者直接在小娜搜索框里输入Anaconda也可以找到它。MacOS直接使用系统的命令行工具在【全部程序-实用工具-终端】。

![Anaconda信息](imgs/4324074-840d7326cbf1c82f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

>如果你是专业人士，更多[不同版本的安装包在这里](https://docs.anaconda.com/anaconda/packages/pkg-docs)

###数据科学全家桶

在命令行工具输入`conda list`然后回车，在列表中寻找是否有下面几个模块，这些我们在后面都会经常用到：
* Numpy 基础的科学计算库，可以用它做各种矩阵运算。
* Pandas 基于Numpy的数据分析工具，擅长处理数据。
* Scipy 是Python中核心的科学计算工具包，包含了像积分、插值、统计、图像等等很多工具,与Numpy紧密结合。
* Scikit-learn 机器学习库，包含了大量的机器学习算法和数据集，很容易上手使用。
* Matplotlib 知名的图表绘制工具，用于数据可视化帮助我们理解数据和监视机器学习的过程。
* Seaborn 基于matplotlib的更方便好用的数据可视化工具。

###使用Conda

conda是模块管理工具（商店），我们先尝试用它来安装著名的深度学习框架tensorflow。

在终端或者prompt里面输入命令`conda install tensorflow`，然后会出现`Solving environment`转圈好一会请耐心等待，然后出现很多文字表示哪些内容将要被下载和安装：

![安装tensorflow](imgs/4324074-652992f8474a1700.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

我们输入y确认开始。然后就会看到很多下载和安装进度。过一会最后会显示`done`表示完成。
>如果遇到出错，可以重新`conda install tensorflow`再试几次就会成功了。

下面是更多的一些conda命令：
* conda info 查看conda自身的信息
* conda update conda 更新升级conda自己
* conda install xxx 安装某个模块
* conda update xxx 更新升级某个模块
* conda --help 显示帮助文字内容
* conda list 显示所有已经安装的模块
* conda remove xxx 删除某个已经安装的模块
* python --version 显示python的版本

[更多常用conda命令看这里](https://conda.io/docs/_downloads/conda-cheatsheet.pdf)

###使用Anaconda navigator

Anaconda还自带了一个有界面的工具管理箱Anaconda navigator，如下图：
![navigator](imgs/4324074-42c61f66274c5f8d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

在Home里面可以看到各种已经安装的有用的工具，尤其是jupyter lab和jupyter notebook，在后续我们都会一直使用，现在你也可以点进去看一下。

Environment环境里面可以看到我们已经安装的各种模块。
>**Python版本** ：Python这个编程语言（本质也是个软件程序）一直在不断升级更新，比如我们使用上面的`python --version`看到的版本是3.6.5，过几个月可能就会升级到3.6.8甚至3.8、4.0之类。但是，我们现在写的代码是用的3.6.5的标准规则，升级之后难免会有些变化，甚至导致我们现在写的代码在明年就会有问题。
**模块版本**：当然我们编程的时候还会引用很多其他人发布的模块，而这些模块如果升级了，我们的代码也可能在模块的新版本里面就不能正常运行。
**Environment环境**：我们编写的代码依赖于当时的python版本和所有引用的模块版本才能正常运行，这些版本的约束就是python编程的Environment环境，如果环境变了就可能会出问题；同样如果我们以后要修改以前的旧代码，也要再返回到旧的Environment环境才能顺利修改。如果我们切换不同的环境，conda命令（比如安装、删除等）都会只针对这个环境来操作。所以我们可以在环境A使用python2.7的语法编程，在环境B使用python3.6的语法。
**Channel渠道**：是指conda install命令从哪里下载需要安装的模块包。默认都是从Anaconda下载的。

###Hello world!

学习任何编程语言的开始都是从让计算机输出一行`hello world!`文字开始的。
我们从Anaconda navigator的Home打开Jupyter notebook。
> Jupyter [ˈdʒʌpaɪtɚ]是一个完全生造的词，可能是从jupiter木星/丘比特一词演化得到的。

Jupyter notebook其实是打开一个网页，但很像是文件管理器，你可以在这里创建自己的文件，并编写代码。
![文件列表](imgs/4324074-0919adac753a4dd2.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

右上角New按钮可以创建Python3代码、文字文件或者文件夹。如图我在桌面Desktop这里创建了一个Untitled Folder文件夹。
点击文件夹的小图标可以Rename改名。
![](imgs/4324074-d2809c274a538110.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

改名之后点进去文件夹，然后New一个Python 3文件。
在输入框中输入`print('Hello world!')`，然后按【shift+回车】,这行代码就会被运行，下面显示出Hello world！
![hello world](imgs/4324074-26584bf45fdf1683.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

当前这个代码文件还是叫Untitled，你可以直接点击上面红线指示的Untitled文字修改文件名。返回到刚才的文件夹页面，可以看到这个.ipynb文件。
![folder文件](imgs/4324074-eb1f3a1aa28324b2.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


后续我们会使用Jupyter notebook带领大家一起学习Python编程和机器学习的知识内容。


###相关资源
* [**常用命令**](https://conda.io/docs/_downloads/conda-cheatsheet.pdf)
* [**Anaconda官网**](https://www.anaconda.com/)
* [**相关单词术语解释**](https://conda.io/docs/glossary.html#activate-deactivate-environment)
* [**帮助文档**](https://docs.anaconda.com/anaconda/user-guide/getting-started)



