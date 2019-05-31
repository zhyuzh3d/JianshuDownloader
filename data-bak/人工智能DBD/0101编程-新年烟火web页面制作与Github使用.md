>[点击这里进入**人工智能嘚吧嘚**目录，观看全部文章](https://www.jianshu.com/p/ff37dbc75edb)
---

![](imgs/4324074-99e3a5868b437005.gif?imageMogr2/auto-orient/strip)

这实际是一个3D的VR网页，我们今天只看一下如何把开始的kksmagic文字变为元旦快乐。
[最终结果展示页面点这里](https://zhyuzhqq.github.io/kksMagic/)
[github项目地址](https://github.com/zhyuzh3d/kksMagic)
>因为是横屏的，微信里打开网页都是竖屏不能旋转，所以最好在浏览器打开或者电脑上打开。这个确实是个很老的项目了，可能在有些手机上显示很慢甚至不能正常显示。

主要涉及内容：
- github网站的注册
- github上创建个人网页
- PPT做图片
- 发布个人网页

## Github网站登录注册

没有什么特别说明的，[点这里进入Github网站注册Sign up](https://github.com)

![](imgs/4324074-c76f596763e40d30.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

为什么要注册这个网站？因为我们做的网页需要放在互联网上发链接给其他人看，所以就需要：
1. 有个网络服务器存储我们的网页文件
1. 有个浏览器地址链接到我们的网页文件

对于第一条，按理说我们要租网络服务器才行；对于第二条，我们要购买域名还要到公安部去备案才行。但都不需要，有了github就能搞定了，你可以在github创建和存储几乎任意多网页。

## Github创建个人网站

按道理创建网站是要写代码的，但还有一个办法就是直接复制别人的网页过来。上面的[Github项目地址](https://github.com/zhyuzh3d/kksMagic)其实就是放烟花的网页项目，你只要把它拷贝过去成为自己的项目Project，再换一下图片就可以发布了。

怎么拷贝别人的项目？点Fork就好了！
![](imgs/4324074-013262b08abe5c06.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

然后再回到[自己的Github首页](https://github.com/)就可以左侧仓库面板（Repositories）出现了被复制过来的项目名，点进去就可以进行修改了。
![](imgs/4324074-812b20c43660707e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

这其实是个文件管理器，这里的index.html文件就是我们看到的放烟花的网页文件，熟悉网页制作的话以后你可以自己研究怎么修改，现在我们直接点击dist进去。
![](imgs/4324074-27b9eed67a368c74.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

## 用PPT更换图片
打开PPT软件，添加一个文字，粗一些，大一些，编辑成“元旦快乐”，可以为每个字设置不同颜色，然后右键另存为图片pattern.png。

![](imgs/4324074-a31cab3f3cc47a6f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

回到网站，点击进入dist/kksFireWorks/imgs/目录，点击pattern.png，然后删除它。
![](imgs/4324074-05f90900befdbc1a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
然后点击Commit changes，提交修改，也就是保存，确认删除。
![](imgs/4324074-22c796d1ab1fb3b6.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

然后点击Upload files上传文件。
![](imgs/4324074-c872bc9a06629086.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

把PPT存储的额pattern.png拖拽到弹窗中，等待上传完成，然后点击底部的Commit changes再次提交保存。

![](imgs/4324074-092e90df4094cdf4.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

最后可以在dist/kksFireWorks/imgs/位置看一下pattern.png是否已经更新完成。

## 发布网页

点击链接kksmagic回到项目顶层，然后点击Settings设置。

![](imgs/4324074-9932414a993081ff.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

向下滚动找到GitHub Pages，Source源下面选择Master branch，然后点击Save保存，稍等页面刷新后就可以看到你的个人网页链接了，点击这个链接观看一下效果。
![](imgs/4324074-2d5cf944823861c1.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
>由于发布往往需要几分钟时间，所以可能过一会才能正常显示，要耐心等一会刷新页面再试。

## 汇总

- GitHub是全球最大的开源代码社区，很多牛X的开源项目在这里都可以找到，而且可以轻松Fork复制成为自己的分支项目。
- Github的每个项目Project也就是每个仓库Repository，存储着我们的全部文件。
- GitHub可以在线管理文件，删除、上传、新建，甚至能编辑很多代码文件，比如html、js等。
- GitHub Pages可以将我们项目的index.html页面作为首页发布成链接，快速创建可以分享的网页地址。

>如果你熟悉Html和js，可以[参考项目说明](https://github.com/zhyuzh3d/kksMagic)，进行更多关于烟火的参数修改，这些参数都在index.html和index.js中，你可以把项目复制到本地或者直接在线点击铅笔按钮修改。

---
>[点击这里进入**人工智能DBD嘚吧嘚**目录，观看全部文章](https://www.jianshu.com/p/ff37dbc75edb)
---
###每个人的智能新时代
如果您发现文章错误，请不吝留言指正；
如果您觉得有用，请点喜欢；
如果您觉得很有用，欢迎转载~
---
END