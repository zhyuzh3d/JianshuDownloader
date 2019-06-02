欢迎关注我的专栏( つ•̀ω•́)つ[【人工智能通识】](https://www.jianshu.com/c/e9a7b7b7024d)

---

使用VSCode开发网站页面，结合Golang开发服务端。

![](imgs/4324074-96818189c5c73f4b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

上一篇文章：[软件技术-零基础Golang开发网站服务器](https://www.jianshu.com/p/da82708419c4)
[人工智能通识-2019年3月专题汇总](https://www.jianshu.com/p/72685b77cfff)


##Hello world！

在项目文件夹中创建用于存放网页文件的`web`文件夹，在里面创建一个`index.html`文件。这里我们创建的是Golang的`src/app/web`文件夹。

然后在里面撰写html代码，注意Html语法与Golang完全不同，Html是标签化的语言，就是用很多标签元素表示页面上的元素（文字、图片、按钮什么的），`<标签名 属性="值">标签内容</标签>`是每个元素的标准格式。

```
<html>

<head>
    <title>首页</title>
</head>

<body>
    <h1>Hello world!</h1>
</body>

</html>
```

几点说明：
- 这里有4个标签，`html,head,title,body,h1`,其中`title`和`h1`中间有文字内容。
- 这里其实有三层标签嵌套，$html \to head \to title$或者$html \to body \to h1$。
- `html`代表整个页面，它包含`head`头部和`body`主体两大块，几乎所有页面都应该是这样的结构。

保存之后，从文件夹中打开这个页面，可以看到效果，注意顶部标题栏显示的title是`首页`。
![](imgs/4324074-f4105b8b49962852.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



##实时预览

每次修改代码都要切换到浏览器中刷新页面，感觉比较麻烦，我们来安装一个插件让页面自动刷新。
![](imgs/4324074-05eca45a38ba30fe.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
从Code的左侧扩展按钮打开扩展面板，搜索`live server`，然后安装install它。
安装之后，切换到`index.html`代码，在右下角状态栏出现Go Live按钮，点击就会弹起浏览器并打开当前页面。

![](imgs/4324074-1c7c19d1af34bf47.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

如上图所示，你可以把这个浏览器窗口放在屏幕右侧，和Code并排。然后当你在Code中修改代码并保存的时候，右侧浏览器页面就会自动刷新。

##优化界面

改进一下我们的`index.html`首页，修改`body`中间的内容：

```
<html>

<head>
    <title>我的首页</title>
</head>

<body>
    <div style="text-align:center;margin-top: 100px">
        <h1>~欢迎来到我的网站~</h1>
        <a href='/page/login.html'>点击注册</a>
    </div>
</body>

</html>
```

注意这几个提示：
- `h1`和`a`标签都嵌套在`div`标签内，所以都会受到`div`限制；
- `style`是标签属性，用来表示标签的样式，`text-algin`文字对齐居中`center`，`margin-top`是距离顶部的空白；
- `h1`是最大的标题（`h2..h5`是更小的），`a`表示这个文字是可以点的链接，点击会跳转到`href`指向的URL。

保存后自动刷新如下图：
![](imgs/4324074-6ef8ea868f47e7e1.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

点击蓝色链接会跳转到一个`Cannot Get "/login"`错误页面，因为这个页面我们还没制作。

##添加login页面

在`web`文件夹下添加`page`文件夹，在`page`下创建`login.html`文件，添加以下内容：
```
<html>

<head>
    <title>登录页</title>
</head>

<body>
    <div style="text-align:center;margin-top: 100px">
        <h1>~登录页~</h1>
    </div>
</body>

</html>
```
但这个时候我们在`index.html`首页中点击那个连接，仍然会跳转到错误页面，同时注意它的地址栏就会发现`index.html`和`login.html`这两个页面的URL地址不一样，一个是`http://127.0.0.1:xxxx/src/app/web/index.html`，另一个是简单的`http://127.0.0.1:xxxx/page/login.html`，明显后者看起来更合理。

##设置Live Server的根目录

但是`http://127.0.0.1:xxxx/page/login.html`这个页面是打不开的，因为`Live Server`默认是把`http://127.0.0.1:xxxx`绑定到`$GOPATH`的目录的，但我们希望能绑定到`src/app/web`这个目录。

![](imgs/4324074-289ebd38f628f418.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

从Preference菜单（MacOS的Code菜单，Windows的File菜单）选择Settings设置，打开Setting设置面板，左侧从Extensions扩展列表中找到Live Sever Config，单击Edit in settings.json打开设置文件。

在设置文件中添加`"liveServer.settings.root":"/src/app/web/"`一行（上面一行要结尾要加英文逗号),然后`settings.json`看起来是这样：
```
{
    "explorer.confirmDragAndDrop": false,
    "explorer.confirmDelete": false,
    "liveServer.settings.donotShowInfoMsg": true,
    "liveServer.settings.root":"/src/app/web/"
}
```
注意格式必须正确，导数第二行内容结尾有英文逗号，最后一行结尾没有逗号。

注意这里的`"/src/app/web/"`是你的项目`$GOPATH`目录，如果不同的话你需要调整。

完成之后重新打开`index.html`页面的`Go Live`，浏览器内的链接就可以正常工作了。

> 但是至此为止，我们只是解决了`Live Server`的链接问题，如果我们把这些页面放到服务器上，还是不能让用户正常访问的，在下一节我们将继续学习如何手写一个简单的网页文件服务器。

---
欢迎关注我的专栏( つ•̀ω•́)つ[【人工智能通识】](https://www.jianshu.com/c/e9a7b7b7024d)

---
###每个人的智能新时代
如果您发现文章错误，请不吝留言指正；
如果您觉得有用，请点喜欢；
如果您觉得很有用，欢迎转载~
---
END``