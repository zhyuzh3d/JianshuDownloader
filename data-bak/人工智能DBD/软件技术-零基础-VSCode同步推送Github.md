欢迎关注我的专栏( つ•̀ω•́)つ[【人工智能通识】](https://www.jianshu.com/c/e9a7b7b7024d)
[【汇总】2019年4月专题](https://www.jianshu.com/p/e1afed853866)

---

如何设置VSCode实现项目文件的同步？

![](imgs/4324074-5526e92a1ea5e783.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
[人工智能通识-2019年3月专题汇总](https://www.jianshu.com/p/72685b77cfff)

##关于Github

到目前为止，我们的代码都存储在本地，如果你的电脑硬盘突然坏掉了，那么你所有代码都会丢失，只能重写。

我们可以利用把代码传到Github网站上去，就安全了。

[Github官方站点](https://github.com/)


Github是什么？可以说几乎全世界所有开发者都会把自己的开源项目放到这个网站上，它是全球最大的开发者社区，如果你想成为一个真正的开发者，肯定要从把项目放到这里开始。

Github能做什么？存储我们的项目文件，而且可以保存每次我们上传的历史版本，什么概念？今天上传一次，明天上传一次，后天又上传一次，Github会把三次都保存下来，如果后天你发现还是今天的版本最好，那么你可以直接返回到今天的代码状态，而不需要去一行行手工修改。

此外，Github还能实现多人协作（几个人一起开发一个项目）以及问题跟踪管理等功能。



##安装Git

Github需要先安装Git软件。

[Git官方站点](https://git-scm.com/)

下载适合自己系统的版本，然后安装即可。

![](imgs/4324074-3a3ac449deddc8d8.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


##配置并提交到Git

在VScode的**终端**中输入以下命令配置你的用户名和邮箱（任意填写）：
```
git config --global user.name "zhyuzh"
git config --global user.email "zhyuzh3d@hotmail.com"
```

然后输入以下命令`git init`初始化Git设置:
![](imgs/4324074-cc12b5cf96013a47.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
注意你应该处在当前的项目（工作空间）目录中，我这里是Golang文件夹。

这个命令的结果是在项目文件夹下创建一个`.git`文件夹，可能是隐身的。

如果你要删除Git设置，只要删掉这个文件夹就可以，比如使用命令`rm -rf .git`。

同时，我们再Code窗口左侧的**源代码管理**按钮上也看到出现了蓝色的数字指示，点击这个按钮可以看到下面列出来很多文件，这表示这些文件都还没有提交到Git里面。

![](imgs/4324074-5c3071abdd957338.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

在Message输入框随便输入什么，然后按Ctrl加回车就能进行提交了。过一会提交成功后这些列表就会消失，**更改**变为0。

>有些时候由于删掉了`.git`文件夹然后又重新设置，可能导致虽然更改了文件，但是这里没有变化不能提交。遇到这个问题只要关掉退出VSCode然后重新打开就好了。


##创建Github仓库

我们要先到[Github](https://github.com)注册账号，然后创建一个项目（Start New Project或者叫新建仓库New Repository）。
![](imgs/4324074-696aad6608d0f998.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

然后弹窗新窗口中如下设置，注意不要勾选最底部的`Initialize...`选项。

![](imgs/4324074-a0b0fc6efbac57e2.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

点击绿色的Create repository创建仓库按钮，注意新页面中的这个信息：
![](imgs/4324074-f729b3db58345c1f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

复制它，回到Code的终端，确认在当前项目文件夹Golang下面，然后结合这个地址执行下面的命令。

`git remote add origin https://username:password@github.com/zhyuzh3d/goWeb.git`

这里的`username`是你的Github用户名而不是邮箱，注意密码前面冒号隔开，后面@隔开。你的后面路径也一定会不同。如果输错了需要修改，可以删除`.git`文件重新`init`，或者使用下面的命令修改地址：

`git remote set-url origin https://username:password@github.com/zhyuzh3d/goWeb.git`

或者用下面的命令只删掉`remote`设置：
`git remote remove origin`

>这个命令的结果就是改变`.git/config`文件的内容，你可以手工打开这个文件进行查看或删改。

> 如果需要从远程Github拉取（复制、克隆）项目文件，可以使用`git pull origin master`。

##推送到Github仓库

在源代码管理面板点击菜单按钮，选择**推送到**，弹出的输入框中下拉选`origin ...`

![](imgs/4324074-1bf233b983890120.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

>如果你之前修改过`remote`,可能需要重新启动VSCode才会显示正确的下拉选项。

然后多等一会，你的代码就会同步到Github网站了，你可以直接在网站上查看你提交的代码：
![](imgs/4324074-8d237328a2e32bb0.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

**但切记不要在网站上修改、新增或删除文件，只能看不能动**


##小结

使用Github版本源文件管理的过程是：
- 安装了Git
- 有Github账号，并且创建了对应仓库
- VSCode中为项目初始化了`git init`有了`.git`文件夹
- 设置了`remote`，链接到Github远程仓库
- 先要推送到本地Git仓库，就是Ctrl+回车
- 从菜单**推送到**远程Github仓库

之后如果代码文件有了修改，那么就可以直接Ctrl+回车提交到本地Git，再菜单推送到Github，反复如此即可。

更多Git和Github内容请参考网络上的各种文章，坑很多，非必要情况无须学习。

---
欢迎关注我的专栏( つ•̀ω•́)つ[【人工智能通识】](https://www.jianshu.com/c/e9a7b7b7024d)

---
###每个人的智能新时代
如果您发现文章错误，请不吝留言指正；
如果您觉得有用，请点喜欢；
如果您觉得很有用，欢迎转载~
---
END