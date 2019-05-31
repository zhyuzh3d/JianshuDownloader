>[点击这里进入**人工智能DBD嘚吧嘚**目录，观看全部文章](https://www.jianshu.com/p/ff37dbc75edb)
---

##介绍与安装

SeleniumIDE是一个网页自动化工具，它可以自动记录你在浏览器内的一切操作，一步步都录制下来，并且可以自动重新播放，可以说就是我们浏览网站所有动作的录像机。——这就实现了页面的自动化，主要用来web开发测试。

**[Selenium官方网站](https://www.seleniumhq.org/)**,Selenium包含两个工具，一个是今天我们要介绍的IDE，另外一个是Webdriver稍后我们介绍。

SeleniumIDE其实是一个浏览器插件，你可以直接在谷歌Chrome浏览器应用商店安装，[电脑上点这个链接](https://chrome.google.com/webstore/detail/selenium-ide/mooikfkahbdckldjjndioackbalphokd)。

![](imgs/4324074-f95e24323a366d55.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

安装成功之后浏览器右上角会出现一个新的图标。

![](imgs/4324074-21ec378a9f48ee0b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


##简单使用

点击图标打开IDE窗口，第一次启动你需要创建一个新项目create new project，输入任意一个名称PROJECT NAME比如 `mytest`，然后输入任意一个地址BASE URL比如`https://www.baidu.com`，然后Start Recording就会弹出一个浏览器窗口，IDE也会变为这样。

![左侧为IDE，右侧是被监控的窗口](imgs/4324074-22f9d196bc1f3e1a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

默认这时已经开始记录了，在IDE右上角录像按钮已经激活。
![](imgs/4324074-bcd0bad5d96d63a7.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

这样你就可以在右侧浏览器窗口执行动作了，比如在输入框输入一些文字进行，然后点击搜索按钮，跳转到新的页面，这些动作都会被自动记录到IDE的动作列表里面去。

![](imgs/4324074-0db4671db0970dbb.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

例如图中红色框出的一行就是一个动作，其中：
- Command命令type表示这是打字动作
- Target目标id=kw表示页面上那个百度输入框
- Value值是“人工智能通识”表示我刚才打字的内容，就是搜索内容

下面一行send keys表示下一动作，就是我点击了百度搜索按钮。

我们点击一行动作，下面就会显示这些详情，并且提供了很方便修改的按钮，比如点击下图红框按钮就可以直接到右侧浏览器窗口中点另外的链接或者按钮，自动会改变Target，同样也可以在这里修改Value改变搜索内容。

![](imgs/4324074-ccc92c345ee3c6b5.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

注意Target这个下拉菜单，Target就是我们在浏览器中点击的元素，但是IDE是怎么找到这个元素的呢？可以有很多种方法，比如在页面上自动搜索你点击的文字，或者搜索这个元素的html标记名或者css样式或者id属性什么的，你可以在这个下拉菜单改变搜索方法。

![](imgs/4324074-9fe3ceb19a9af54c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

每条动作右侧都有一个三点按钮，点击可以执行删除动作delete、增加动作insert等操作。
![](imgs/4324074-154ed84ba4ee4d52.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



好了，如果你觉得可以了，那就点击右上角红色闪烁按钮暂停录像，再保存一下吧~ 然后点击播放按钮开始自动重现你刚才的浏览器动作~

![](imgs/4324074-d0c8386de8084e2e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

你将会看到右侧浏览器自动打开百度，自动输入“人工智能通识”，并进行搜索，就像有人操作一样。

##循环执行

每次播放都只是运行一次，有没有办法运行多次呢？

先了解一下几个特殊动作：
![](imgs/4324074-bd7b274e1a0d586a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

`execute script`表示运行一个代码，Target就是要被运行的代码，return是输出结果，Value是表示运行结果的变量。上面图上这一条看上去挺复杂的动作其实就是`var counter=1`

![](imgs/4324074-7c77f9906db55fa3.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

`do`命令其实没啥意思，但会把下面的命令都往右推一下，表示下面这些命令都要被它执行。

![](imgs/4324074-9ff9473b128041ca.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

又是`execute script`，这次相当于`counter=counter+1`，这里要用`${}`把我们之前设定的变量括起来。

![](imgs/4324074-5885d525684efc6a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

最后我们需要给`do`动作一个结尾，`repeat if`方法就是判断是否重复上面这些`do`动作，如果`if(counter<5)`就`repeat do`。

好了，有了这几个动作，再次点击播放按钮，就会看到动作被重复4次。

##从页面中提取文字

能不能把页面上的文字作为var变量使用呢？
看一下这个图：

![](imgs/4324074-2d9fee6d44791a04.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

`store text`就是把页面上某个元素的文字保存为变量，在这里insert插入了一个`store text`命令，目标Target使用按钮直接从浏览器左上角点`换肤`链接文字，Value设置为`mytext`，这就相当于`var mytext=从浏览器中搜索css=.s-skin > .title这个元素得到的文字`。有了`mytext`我们就能在下面type打字动作中使用`${mytext}`了。

运行一下，什么结果呢？每次都是百度搜索“换肤”了。

##动态变量

能不能每次搜索不一样的单词呢？

看一下这个图(红色为新增，蓝色为修改，绿色为调整位置)：
![](imgs/4324074-b36fe48c2ccb655f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- 使用`execute script`在开始创建`names= ['周杰伦','赵丽颖','鹿晗','蜘蛛侠','孙悟空']`列表。
- 中间再增加`name=${names}[${counter}]`这句，因为在Type打字的Value内并不能计算方括号。
- 打字动作的Value改为`${name}${mytext}`，注意这里不需要使用加号。

---
>[点击这里进入**人工智能DBD嘚吧嘚**目录，观看全部文章](https://www.jianshu.com/p/ff37dbc75edb)
---
###每个人的智能新时代
如果您发现文章错误，请不吝留言指正；
如果您觉得有用，请点喜欢；
如果您觉得很有用，欢迎转载~
---
END