欢迎关注我的专栏( つ•̀ω•́)つ[【人工智能通识】](https://www.jianshu.com/c/e9a7b7b7024d)

---
如何将用户的姓名、邮箱数据存储到服务器的数据库中？首先我们要了解和安装数据库。

![](imgs/4324074-7883b52aed193c8c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

上一篇文章[软件技术-零基础网页和Golang服务器数据通信](https://www.jianshu.com/p/0538784981db)
[人工智能通识-2019年3月专题汇总](https://www.jianshu.com/p/72685b77cfff)


##什么是数据库

数据库是什么？

简单的理解，excel表格就是数据库，我们可以通过excel打开它往里面写入各种数据，也可以读取数据和删除数据，还能在excel中搜索，比如找出所有叫Tom的人的数据资料。

**数据库就是一种数据的存储、读写、查找机制，可以看做就是一种软件**。

数据最基础的操作是CURD，即创建（Create）、更新（Update）、读取（Retrieve）和删除（Delete）。

数据可以划分为两种，**结构化数据Structured和非结构化数据Unstructured**，excel表那种整齐的数据都是结构化的，每个数据都包含姓名、性别、身高...等固定字段；但是像小说、评论文字、音视频这种就不是结构化，数据格式不统一不确定。

对于结构化数据可以使用标准的**SQL语言（Structured Query Language结构化查询语言）对数据进行操作**，这类数据库也叫做关系型数据库，知名的有：

![](imgs/4324074-fcc07b5c3dbf7057.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- **Oracle RDBMS数据库**，一种高性能的商业化关系型数据库软件，售价昂贵，多用于政府和大型企业。
- **微软的SQL Server**，售价数万甚至数十万，虽然有免费的开发者版本，但并不能在正式部署时候使用。
- **Oracle公司的MySQL**，分为昂贵的企业版和免费开源的社区版。MySQL可能是曾经使用最广泛的数据库软件，但后来由于Oracle对开源软件的态度很不稳定，所以开发者正在快速逃离。
- **开源免费的MariaDB**，这是MySQL创始人带领社区力量重新开放的数据库，是MySQL的新生，很多老用户都转移到这里。
- **开源免费的PostgreSQL**，适合大型商业项目使用的关系型数据库，它比MariaDB更复杂更强大，对于一般Web项目不推荐使用，支持的编程语言也不多，不支持Golang。


而对于非结构化数据则难以建立统一的处理方式，我们统称为NoSQL数据库，也叫非关系型数据库，主要知名的NoSQL数据库有：

![](imgs/4324074-308990ffcd0bf12d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- **mongoDB**,应用最广的NoSQL数据库，开源，有付费的企业版也有免费的社区版。这是一种文档型数据库，每个数据像是一个文档，可以灵活存储各种信息，而且具有强大的查询能力。
- **Apache Cassandra**，这是有Facebook基于Google的BigTable技术推出的非关系型数据库产品，它是开源免费的，它易于分布式部署（就是安装在很多台不同城市的电脑上协同工作），适合大型商业服务软件使用。
- **Redis**，开源免费，这是一个基于内存的高性能数据库服务，它的数据结构只有非常简单的几种，但功能强大。常被用来做性能要求很高的部分数据存储服务。
- **Apache Hbase**，他也是一款开源免费软件，基于谷歌BigTable技术的分布式数据库，和Cassandra类似，目前已经是大数据技术的核心内容之一。Hbase和Cassandra很像，Cassandra相对更完整；而Hbase需要依赖其他组件才能实现完整数据库功能，也恰好因为这个，它可以很好地融入到当今主流的大数据技术中去。

关于数据库，需要了解的更多几点：
- 各种数据库各有所长，没有哪一个是万能的。
- 很多项目都是多种数据库综合使用，充分利用每种数据库的优势强强组合。
- 选择数据库要根据具体的需求来选，企业并不一味追求价格敏感。
- SQL数据库的操作大同小异，都遵循统一的SQL通用标准语法。
- NoSQL数据库会有些不同，可能需要逐渐积累经验。
- 很多数据库都支持分布式存储到很多机器上。
- 很多云服务商（比如阿里云腾讯云）都提供了云端租用数据库的产品，这也是很多企业的首选，——而不是完全依赖于公司自己安装部署数据库。

我们接下来会只使用MongoDB，因为它是NoSQL数据库，存储快速，但同时又是NoSQL数据库中查询能力最强使用最简单的。

##安装MongoDB

直接到官方网站下载社区版Community安装包，注意确认操作系统正确。
[点这里进入下载页面](https://www.mongodb.com/download-center/community)

![](imgs/4324074-a9d8d67686d13e4d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

对于windows用户，请选择安装MongoDB as a service，使用默认的Server Name等设置即可。安装成功后数据库就自动运行了，可以从程序里面或者目录`C:\Program Files\MongoDB\Server\4.0\bin\`打开`mongo.exe`启动管理。

对于MacOS用户：
- 下载tgz文件解压，然后前往文件夹`/usr/local/`，创建`mongo`文件夹，把解压得到的bin文件夹拷贝进去，然后在用户目录（小房子首页，或者前往`~`)使用快捷键`Command+shift+.`显示隐藏文件，打开`.bash_profile`文件，添加下面内容：
```
#mongoDB
export PATH=/usr/local/mongo/bin:$PATH
```
- 使用`source .bash_profile`命令刷新设置。
- 使用`sudo mkdir -p ~/data/db`命令创建必须的文件夹，这个文件夹就在用户目录。
- 使用命令`mongod --dbpath ~/data/db`启动数据库服务，这个`~/data/db`必须和上面创建的文件夹一致。

>macOS下也可以使用`brew install mongodb-community@4.0`命令进行安装，然后`brew services start mongodb-community@4.0`命令启动数据库。

安装成功后我们可以在新窗口执行命令`mongo`能够进入命令提示符状态，尝试使用下面的代码创建数据：
```
db.inventory.insertOne(
   { item: "canvas", qty: 100, tags: ["cotton"], size: { h: 28, w: 35.5, uom: "cm" } }
)
```
成功的话回访一些标准信息：

![image.png](imgs/4324074-1a04170878e9b253.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

##数据库管理工具Compass

都是命令的方法看上去不太方便，我们可以安装MongoDB Compass软件来进行管理。

[点这里进入下载页面](https://www.mongodb.com/download-center/compass?jmp=docs)，注意选择正确的操作系统。

![](imgs/4324074-a51e032251460846.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

下载后直接安装。

启动后，链接到主机Connect to Host使用默认设置，

在左侧Test下的inventory中可以看到我们刚才用命令创建的数据。

![](imgs/4324074-c66274e8202addfa.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

我们点击左下角的加号创建一个数据库，DataBase Name为myweb，数据集Collection Name为user用户，接下来我们将用Golang把用户从网页发送来的数据存储在这里。

![](imgs/4324074-85293889c0d68966.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



>  这是使用界面软件管理数据库的方法，在下一篇我们介绍如何使用Golang将用户名存储到mongo数据库里面。







---
欢迎关注我的专栏( つ•̀ω•́)つ[【人工智能通识】](https://www.jianshu.com/c/e9a7b7b7024d)

---
###每个人的智能新时代
如果您发现文章错误，请不吝留言指正；
如果您觉得有用，请点喜欢；
如果您觉得很有用，欢迎转载~
---
END