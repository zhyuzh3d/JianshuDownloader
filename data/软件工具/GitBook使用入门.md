---
## GitBook是什么？

####Git

Git可能是目前全球最通用软件编程、软件开发项目的管理工具，帮助开发人员对项目文件和开发进度进行管理，支持版本历史管理和多人协作管理等必须功能。

####GitHub
GitHub是Git在线化，就是有人把自家的git服务向所有人公开了，每个开发者都能使用它来在线管理自家的项目。目前它已经是全球最大的开源软件项目集散地地，很多知名的项目比如Nodejs，Tensorflow等等都是发布在GitHub上面的开源项目。

开源意味着你可以随时把整个项目的源代码拷贝到你的计算机上，和项目的开发人员同步看到项目的代码内容，看到项目的发展过程；也意味着你可以提出自己对项目代码的改进意见，并提及给项目管理人员，如果你的建议足够好或者你修改进的代码足够精彩，那么它会出现在项目的下一个版本中向全世界人发布。

####GitBook
GitHub是基于Git技术的，是面向做软件开发的程序员的。GitBook同样是基于Git技术的，但它最初定位是面向软件说明文档的编写者的，但它同样适合任何类型的文字编辑工作者。

**GitBook是使用软件项目的先进管理经验打造的在线文档书籍撰写工具**。

[Git官网](https://git-scm.com/)   /   [GitHub官网](https://github.com/) /  [GitBook官网（新版，需要翻墙）](https://www.gitbook.com/) /  [GitBook官网(旧版不需要翻墙)](https://legacy.gitbook.com/)

---
##GitBook工具链
[**GitBook在线网站旧版**](https://legacy.gitbook.com/)/[新版](https://www.gitbook.com/)
可以在线协作一起写书，并且直接发布到这个网站，方便分享和公众阅读。

[**GitBook开源项目**](https://github.com/GitbookIO/gitbook)
这是一个机遇Node.js的本机服务软件，他可以在断网状态下载浏览器内展示你的书籍。

[**GitBook Editor本机编辑器**](https://legacy.gitbook.com/editor)
离线的编辑器，支持Windows和MacOS、Linux，类似office word那种，但更简单写出书也更漂亮。

---
##GitBook Editor编辑器

####书籍管理

如果您没有梯子，可以在一开始选择Do that later暂不登录
![延迟登录](imgs/4324074-06693acf7aaf1686.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

**从菜单GitbookEditor设置书籍存储目录Change Library Path，接下来书籍所有文件都会放到这里**
![设置目录](imgs/4324074-dce426f4aef5484a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


然后可以随便创建一个新书+new book，名称任意如MyFirstBook。

点左上角铅笔图标可以返回书籍列表。

####文章管理


![撰写界面](imgs/4324074-65b49bac8fb43822.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
左侧列出了文章的内容列表TOC(Table of content)，就是书的目录了。FILES文件模式是这个项目的实际使用的文件，先不用管。

已经有两篇文章introduction本书说明和First Chapter第一章。点击可以在右侧主区域打开并编辑。新建、重命名、删除、上下拖拽调整顺序，这些不再多说。

####本地预览

请参照下一段GitBook本地服务
---
##GitBook本地服务

####安装

使用命令行安装GitBook本地服务。

```
npm install gitbook-cli -g
```

####启动服务
然后cd进入你的书籍目录，比如xx/import/mybookname，然后执行命令启动服务
```
gitbook serve
```

如果你遇到问题，那么可能需要初始化一下。

####初始化项目

```
gitbook init
```

[更多使用参照这里](https://github.com/GitbookIO/gitbook/blob/master/docs/setup.md)

>其实可以使用任意的编辑器来修改md文档，不仅仅限于Editor。

---
##发布到legacy.gitbook.com

####创建GitHub仓库

首先需要登录[GitHub官网](https://github.com)注册登录并创建一个项目start a project（仓库reposi'tory)。
![创建项目](imgs/4324074-5baea746992e10ea.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

任意项目名称，其他默认，你将会得到一个GitHub仓库地址类似```https://github.com/zhyuzh3d/mytestbook.git```


####上传到Github(自备梯子)

然后在编辑器book菜单sync,这会弹出提示需要输入上面的.git地址，然后要输入GitHub用户名和密码，稍后本地的书籍文件就上传到GitHub仓库了。

####关联GitHub和GitBook(自备梯子)
回到legacy.gitbook.com，使用GitHub账号登录，然后从右上角头像Account Setting账号设置进入，左侧选GitHub，右侧Integration整合，install，这将让你选择把哪个repository仓库同步过来，可以选全部。

####从GitHub仓库创建书籍
创建一本新书，然后从SETTINGS进入，再点左侧GitHub，然后输入你的GitHub仓库名，这样就把GitHub仓库变成GitBook书籍的形式展示了。
在GitBook里面点read阅读这个书籍，和本机serve的效果是一样的，而且当我们本机Editor修改之后，只要sync一下就能自动同步刷新了。

这个书籍的链接可分享或者发给朋友，当然确保你的朋友自备梯子...

####其他同步到GitHub的方法
使用命令行或者界面化的Git工具，比如SourceTree，将import下的mytestbook文件夹推送到GitHub目录。
[SourceTree教程看这里](https://www.jianshu.com/p/be9f0484af9d)

####在线编写（自备梯子）
也可以完全使用legacy的在线编写工具撰写书籍。

---
##MardDown语法

GitBook都是基于markdown语法的，其实就是一些特殊的符号表示文字样式，比如一个#加空格代表这是一行大标题，两个##加空格代表这是二号标题，一个*加空格代表这是一个列表，>加空格代表后面的文字是注释，等等。

很多编辑器和网站都支持markdown语法，比如你现在看的这个简书文章就是markdown语法撰写的。

你可以在网上搜索markdown找到很多教程。[这里是简书的官方教程](https://www.jianshu.com/p/q81RER)

---
##结语

依赖于GitHub社区，GitBook很可能成为新的通用工具。但由于被墙也就并不推荐普通用户使用。

如果需要的话可以优先考虑国内的[看云kanCloud](https://www.kancloud.cn).

---
###致力于让一切变得简单
如果您发现文章错误，请不吝留言指正；
如果您觉得有用，请点喜欢；
如果您觉得很有用，欢迎转载~
---
END







