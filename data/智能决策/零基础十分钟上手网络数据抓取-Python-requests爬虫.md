[智能决策上手系列教程索引](https://www.jianshu.com/p/0d2e46e69f58)
---

这是为零基础（会开机、会打字、会上网）新手撰写的教程，所以在此之前你不需要做任何准备，不需要买书，甚至不需要下载和安装软件。事实上，当你在电脑上看到我这个文章的时候，我就知道你已经准备就绪了~

####**智慧来自于经验，智能来自于数据**。
互联网是全人类最大的数据源，没有之一。
这篇文章将介绍如何利用简单的代码从网络上抓取数据并进行简单的统计分析。
案例是基于豆瓣全球电影排行列表的，这个案例可以帮助你回答诸如以下问题：
* “哪一年好电影最多？”
* “什么时代上映的好电影比较多？”
* “电影整体制作水平的历史发展情况是什么样？”



## 1. 编程工具
人工智能目前最主流的编程语言是Python，它也被认为是最适合新手学习的编程语言。
首先我们需要一个软件在里面写代码，就像我们有了word才能撰写文档一样。

**最简单的方法是使用阿里云天池数据智能平台的在线编写工具Notebook，你可以直接在浏览器里写Python代码，并且运行你的代码查看效果。**

[**阿里云天池Notebook传送门(你可能需要注册登录并完成实名认证)**](https://tianchi.aliyun.com)
![阿里云天池Notebook.png](imgs/4324074-2761d607cf9d8576.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

>用阿里云的在线编辑工具写Python代码，并且放在他们的服务器上，还要用他们的服务器运行你的代码，更重要的是还使用他们的网络带宽来为我们搜集数据。——我们这样做可能有点过分，但至少现在还行得通。如果以后天池限制了这个功能，那么推荐安装Anaconda软件，它也提供了几乎一样功能的JupyterNotebook供大家使用。
[Anaconda官方传送门](https://www.anaconda.com/)
[Anaconda快速安装上手教程](https://www.jianshu.com/p/471763354ebc)

## 2. 开始编程

我们假定你已经完成阿里云的账号注册和登录，正常打开了Notebook，点击左侧【我的Notebook】，然后点击下面的蓝色【+新建】按钮创建了一个文件（私有或公有都可以），如下图。
>如果你看到的和下面不同，可能需要点私有或公有下面的那个文件，然后右上角找到【编辑】按钮点击。

![Notebook界面说明](imgs/4324074-1d7e01942cceb5c3.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

我们把其他的cell单元都删掉（点击右上角的小圆x），只留下最上面的一个cell，并且把里面的内容都删掉。
任意设定文件名，然后点保存按钮将我们的这个文件保存到阿里云的服务上，右侧红色的disconnected字样将消失，如果以后再出现disconnected字样可以点击它边上的电源按钮进行连接。

![保存和连接服务器](imgs/4324074-b96cddf92509044a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


然后我们再cell里面写以下代码（当然可以复制粘贴）：
```
import requests
page=requests.get('https://www.baidu.com/')
print(page.text)
```
这里有三句话
 1.  ```import requests```导入我们需要的requests功能模块。requests（请求）这个模块是帮我们向互联网发出请求和获取数据的。
**我们每次在浏览器里面看到的文字、图片和视频都是来自于互联网上面别人的服务器，每次我们再浏览器地址栏输入或粘贴网站链接地址，就是向远在外地的别人的服务器发出请求。**
比如我们在地址栏输入```www.baidu.com```,浏览器就会发送一个请求给百度公司的服务器电脑，他们的服务器收到请求后就会把网页发送给我们的浏览器，浏览器把页面展现在我们面前，如下图。
![浏览器发送请求获取数据文件](imgs/4324074-445eb75d20cc0360.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

1. ```page=requests.get('https://www.baidu.com/')```这句命令的意思就是获取（get)百度网站的数据。实际上我们获取到的就是浏览器打开百度网址时候首页画面的数据信息，下一句就会显示这个数据。
1. ```print(page.text)```这句是把我们获取数据的文字（text）内容输出（print）出来。print到哪里呢？接下来我们就点击运行按钮看一下效果。
![运行代码获取百度首页文件数据](imgs/4324074-352bd475c55ba27a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

我们看到浅蓝色小字output（输出）下面出现了横向很长的一堆字符，这实际就是百度首页的文件数据。我们平常看到的百度首页画面就是浏览器基于这些字符显示出出来的。

**恭喜你！已经实现了爬取网页数据的第一个案例！***

## 3.理解HTML
但是上面充满尖括号的一片字符似乎对我们没有什么作用，接下来我们看如何从这些字符里面提取些有价值的数据。
这样的充满尖括号的数据就是我们从服务器收到的网页文件，就像Office的doc、pptx文件格式一样，网页文件一般是html格式。
我们的浏览器可以把这些html代码数据展示成我们看到的网页。
![html文件数据](imgs/4324074-6fa382c54dc8a106.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
**html全称叫做超文本标记语言**

**我们看到的每个元素（一段文字、一个图片或一个视频等等），都是一个标记元素，每个网页都是由成百上千的标记元素组成的。
**比如```<img src="https://ss0.bdstatic.com/5aV1bjqh_Q23odCf/static/superman/img/logo_top_86d58ae1.png"></img>```表示在浏览器显示一个图片，img是图片单词image的简写，src是源文件source的简写，如果我们直接复制src双引号内的内容到浏览器地址栏，就可以看到这张图片。
又比如```<div>新闻标题</div>```表示在浏览器显示四个文字“新闻标题”。

综上，**每个标记的文字内容都是夹在两个尖括号中间的，结尾尖括号用/开头，尖括号内（img和div）表示标记元素的类型（图片或文字），尖括号内可以有其他的属性（比如src）**
![标记元素](imgs/4324074-3b4dbc3c7c769599.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

**标记内容文字才是我们需要的数据，但我们要利用id或class属性才能从众多标记中找到需要的标记元素。**

我们可以在电脑浏览器中打开任意网页，然后【右键-检查】打开元素查看器（Elements），就可以看到组成这个页面的成百上千个各种各样的标记元素。
>我使用的是谷歌浏览器（chrome），其他浏览器可能菜单稍有不同。

![元素查看器](imgs/4324074-a0e3675692bad729.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

我们注意到，**标记元素是可以一层一层嵌套的**（注意标记左侧后退的空白和那些小三角的位置）。比如下面就是body嵌套了div元素，body是父层、上层元素，这个div是子层、下层元素。
```
<body>
    <div>十分钟上手数据爬虫</div>
</body>
```

## 4. 提取数据
回到Notebook，我们新建一个文件，任意名称，清理掉多余的cell单元，只留下一个单元，输入或粘贴以下代码：
```
import requests
from bs4 import BeautifulSoup
html=requests.get('https://movie.douban.com/top250?start=0')
soup = BeautifulSoup(html.text, 'html.parser')
for item in soup.find_all('div',"info"):
  title=item.div.a.span.string #获取标题
  yearline=item.find('div','bd').p.contents[2].string #获取年份那一行
  yearline=yearline.replace(' ','') #去掉这一行的空格
  yearline=yearline.replace('\n','') #去掉这一行的回车换行
  year=yearline[0:4] #只取年份前四个字符  
  print(title,'\t',year)
```
运行它就会输出很多电影名称和上映年份。
![输出电影名称和年份](imgs/4324074-69a99e6686b0c3c2.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


看上去有些复杂，我们来一行一行的分析：
1. **获取页面数据**
```import requests```和```html=requests.get('https://movie.douban.com/top250?start=0')```这两行上面解释过了，是获取页面数据。我们可以打开这个链接看一下，它是豆瓣网统计的全球250部最佳电影列表，每页25个，共10页，每个电影包含了标题、导演、年份等信息。

[豆瓣电影TOP250传送门](https://movie.douban.com/top250?start=0)

![豆瓣TOP250电影](imgs/4324074-30cd05604fb2dae4.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

1. **解析数据**
我们需要使用BeautifulSoup这个功能模块来把充满尖括号的html数据变为更好用的格式。
```from bs4 import BeautifulSoup```这个是说从(from)bs4这个功能模块中导入BeautifulSoup，是的，因为bs4中包含了多个模块，BeautifulSoup只是其中一个。
```soup = BeautifulSoup(html.text, 'html.parser')```这句代码就是说用html解析器(parser)来分析我们requests得到的html文字内容，soup就是我们解析出来的结果。

1. **For循环**
豆瓣页面上有25部电影，而我们需要抓取每部电影的标题、导演、年份等等信息。就是说我们要循环25次，操作每一部电影。```for item in soup.find_all('div',"info"):```就是这个意思。
首先我们在豆瓣电影页面任意电影标题【右键-检查】（比如“肖申克的救赎”），打开Elements元素查看器。

![每部电影对应的标记元素（嵌套很多内容）](imgs/4324074-9934093874b3b23a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

**```find_all('div',"info")```，find是查找，find_all就是查找全部，查找什么呢？查找标记名是```div```并且class属性是```info```的全部元素，也就是会得到25个这样的元素的集合**。
```for item in 集合:```的含义就是针对集合中的每个元素，循环执行冒号：后面的代码，也就是说，**下面的几行代码都是针对每部电影元素(临时叫做item)执行的.**

1. **获取电影标题**
```title=item.div.a.span.string```中item代表的是上面图片中的整个`div`元素(class='info')，那么它下一层（子层）`div`再下一层`a`再下一层`span`(class='title'的)里面的文字“肖申克的救赎”就是我们需要的电影标题，所以是`.div.a.span`然后取内容`.string`

![获取标题](imgs/4324074-c770b5e7b2b2f13b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

>注意，一层层的点下去的方法只适合于获取到每层的第一个元素，比如前面图中我们知道实际有三个span，其他两个英文名、其他译名，但我们只取到第一个。

2. **获取年份段落**

`yearline=item.find('div','bd').p.contents[2].string`这句话综合了`find_all`和`.p`两种方法，取到了item下面第二个`div`（class='bd')。
`.contents[2]`是取得这一行第3个文字小节,content单词是内容的意思，`<br>`标记将整个`p`标记内容分成了三段（0段，1段，2段）。

![br将contents内容分为三段](imgs/4324074-985fce6e91f798d2.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

所以，`yearline=item.find('div','bd').p.contents[2].string`这句话得到的是`1994 / 美国 / 犯罪 剧情`这行，但实际上它还包含了很多空格和回车换行符号的。所以我们再使用两个replace替换掉空格和回车。replace是替换的意思，在数据里`\n`是表示换行回车。
```
yearline=yearline.replace(' ','') #去掉这一行的空格
yearline=yearline.replace('\n','') #去掉这一行的回车换行
```

3. **获取年份数字**
经过上面的处理，我们得到了干净的`1994 / 美国 / 犯罪 剧情`，我们只要截取前面4个数字就可以了，也就是从第0个字符截取到第4个字符之前（0，1，2，3），我们使用`year=yearline[0:4]`就可以实现。

4. **输出和复制到excel**
`print(title,'\t',year)`，中间的`'\t'`是制表符，我们可以直接鼠标选择output输出的内容，右键复制，然后打开excel新建空白文件，然后选择合适的表格区域范围，**【右键-选择性粘贴】弹窗中选择Unicode文本**，就可以把数据粘贴到excel表格中。
![复制输出内容](imgs/4324074-771586f43ae88f6a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![粘贴到Excel](imgs/4324074-3072a2de944a91d2.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

## 3. **采集更多电影**
上面代码只是帮我们输出第一页25部电影信息，要采集第二页可以把requests请求的链接地址更换一下`html=requests.get('https://movie.douban.com/top250?start=25')`，每页25个递增，第三页就是```start=50```，以此类推。
最后把全部250个电影数据反复10遍粘贴到Excel表格就可以了。

当然我们有更好的方法，比如利用for循环自动采集10个页面的数据。
```
import requests
from bs4 import BeautifulSoup
start=0
for n in range(0,10):
    html=requests.get('https://movie.douban.com/top250?start='+str(start))
    start+=25
    soup = BeautifulSoup(html.text, 'html.parser')
    for item in soup.find_all('div',"info"):
        title=item.div.a.span.string #获取标题
        yearline=item.find('div','bd').p.contents[2].string #获取年份那一行
        yearline=yearline.replace(' ','') #去掉这一行的空格
        yearline=yearline.replace('\n','') #去掉这一行的回车换行
        year=yearline[0:4] #只取年份前四个字符  
        print(title,'\t',year)
```
这是把刚才的几乎全部代码放到了新的循环里面`for n in range(0,10):`里面。`range(0,10)`就是生成一个0~9的集合。另外，每次`requests`请求之后我们还添加了`start+=25`这行，就是每次叠加25的意思，第一次循环`start`是0，然后加25变25，第二次就是25，然后加25变50，以此类推。

运行这个代码，稍等一下运行结束，就能看到output全部250部电影信息了。

## 4.生成统计数据

我们把采集到的数据粘贴到Excel文件中，最顶上插入一行【影片名、年份】。
![Excel数据](imgs/4324074-779853810069e6a4.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

接下来我们利用这些数据研究一下哪些年盛产好电影。
如上图，点击B栏全选这一列。然后选择【插入-数据透视表】
![插入数据透视表](imgs/4324074-42e3f1da081cba2c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

然后弹窗中选择【新工作表】，其他保留默认，点确定。
![创建数据透视表](imgs/4324074-47a7fea819aa686b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

然后在右侧把年份拖拽到下面的行中。
![拖拽到行](imgs/4324074-cf70f32fc2833d45.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

同样再拖拽到值里面。
![拖拽到值](imgs/4324074-17ed6b54ac6d0be9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

然后点击表格里面的【求和项：年份】，再点击【字段设置】，弹窗中选择【计数】，然后确认，就能统计出每个年份上映的电影数量。
![image.png](imgs/4324074-ace67765f388d7d6.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

很多年份都是1或2，但表格滚动到下面就会看到1994、1995哪些年上映的电影比较多。
![90年代佳片较多](imgs/4324074-a115c7d3daa90b31.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

选择AB两栏，然后点击【插入-柱形图图标】，就能得到最终的统计图。
![插入柱形图](imgs/4324074-61fa80d22c6754f2.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

最终统计图如下，可以清楚的看到全球最佳电影的年份分布情况，可以得到一些结论，比如上个世纪90年代初开始电影制作水平有了明显的提升，至90年代中期以后，虽然一直处于较高水平，但没有太大幅度的提高了；2010年贡献了最多数量的好电影，此后至今的8年虽然佳片不断（12年除外），但整体走低，2017年观众认可度达到最低点。

![全球佳片历史分布](imgs/4324074-7fe3a715c1413149.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

>虽然这些数据可以客观说明一些情况，但要知道，首先数据量不是很大，我们也只考虑了数量，没考虑排名影响等其他因素，另外，经典电影获得最终评分认同也需要一些时间，所以武断的得出的结论也很可能是不正确不全面的。

## 5.后续学习资源

如果你已经掌握了上面介绍的内容，那么一定要趁热进取。
推荐先认真学习BeautifulSoup更多的搜索获取元素数据的方法，如果你有一些编程基础的话推荐先浏览官方文档，或者你可以在简书搜索Python入门教程和BeautifulSoup相关教程先慢慢学习，后续我会陆续制作相关教程，陪各位新手一起继续学习下去。

[Html标签技术基础入门](http://www.w3school.com.cn/html/index.asp)
[Python基础入门教程](http://www.runoob.com/python/python-tutorial.html)
[BeautifulSoup中文官方文档传送门](https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.zh.html)


简单学习了解之后，你可以试试看能否尝试统计到350部电影的国家地区分布情况。

---
[智能决策上手系列教程索引](https://www.jianshu.com/p/0d2e46e69f58)
---
###每个人的智能决策新时代
如果您发现文章错误，请不吝留言指正；
如果您觉得有用，请点喜欢；
如果您觉得很有用，欢迎转载~
---
END


