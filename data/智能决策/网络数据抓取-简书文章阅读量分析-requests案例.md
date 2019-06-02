[智能决策上手系列教程索引](https://www.jianshu.com/p/0d2e46e69f58)
---


以前在简书发了一些文章，涉及的分类特别杂乱，有TensorFlow的，有Web开发的，还有一些小学生编程教程和绘图设计教程...最近又在做人工智能通识专题和智能决策系列教程的文章。
这些天很多简友关注我，但我很迷茫，并不知道哪些文章最受大家重视，对大家更有用些，而简书也没有这方面的统计功能开放给作者们使用。
我就想能不能自己把这些变化数据抓取下来，自己分析一下，于是就开动写这个案例教程了。
>这个教程推荐使用Chrome浏览器和Jupyter Notebook编辑器。Notebook的安装请参照[安装Anaconda：包含Python编程工具Jupyter Notebook](https://www.jianshu.com/p/471763354ebc)

## 有哪些数据可以获取？

从自己的文章列表页面可以看到总体【关注数】和每篇文章的【观看数】都是直接获取的，**我们只要汇总每天哪些文章观看数增加了，再对比粉丝数的变化，就能知道哪些文章引发的关注最多**。

![image.png](imgs/4324074-d8a8bed3549fdf3f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


>因为目测我的文章每天总阅读量的增加数，和每天粉丝的增加数相差不太大，也就是说，**大部分阅读都引发了被关注**，所以两者之间是强关联的。
如果不是这样，比如每天增加阅读1万，粉丝增加100，那就不好说了，因为可能A文章被观看100次都引发了被关注，而B文章被观看了9000次却没有引发一个被关注，那么就没办法从单个文章阅读量上分析粉丝变化，也就猜不出哪些文章更受喜欢。

## 爬虫数据是在html里还是在动态json请求里？

首先我们要知道页面上这些数据是怎么来的，是直接html标签显示的？还是通过JavaScript动态填充的？请参阅[系列教程的前4节](https://www.jianshu.com/p/0d2e46e69f58)。

我们的套路：
1. 右键【显示网页源代码】，打开的就是浏览器地址栏里面的地址请求直接从服务器拉取到的html数据，如果这里可以Ctrl+F搜索到需要的数据（比如可以搜到“人工智能通识-AI发展简史-讲义全篇”），那么用最简单的html数据提取就可以。

1.  如果上面一个办法搜不到，那就右键【检查元素】，然后查看Network面板里面type为xhr的请求，点击每一个，看哪个Response里面可以Ctrl+F搜到我们需要的数据。（很多时候可以从请求的英文名字里面猜个八九不离十）

在这个案例里，我们需要的数据看上去就在网页源代码里面，暂且是这样。
![image.png](imgs/4324074-39a405b5b405bf6b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

## 怎么用header和params模拟浏览器？

为了不让网站的服务器知道我们是爬虫，就还要像浏览器一样发送附加的额外信息，就是header和params。

我们右键【检查】，然后切换到【Network】网络面板，然后刷新网页，我们会看到一个和网页地址一致的请求。
如下图，我的主页地址是https://www.jianshu.com/u/ae784c57b353，就看到Network最顶上的是ae784c57b353：

![image.png](imgs/4324074-3fd72f7df17e3f24.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

如果我们切换到请求的Response响应结果面板，就可以看到这个请求获取的实际就是网页源代码。它的type类型是document，也就是html文档。

就是它了，我们需要它的header头信息和params参数。
【右击-Copy-Copy Request Headers】就能复制到这个请求的头信息了。
![image.png](imgs/4324074-1eede170495ad12c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

但是，如果你留意，就会发现这个请求的Response结果（也就是网页源代码）并不是包含所有文章，而只是只包含了9个文章。但是如果我们用鼠标往下滚动页面，发现文章就会越来越多的自动添加进来。（右侧的滚动条越变越短）

我们刷新页面重置，然后清空Network网络面板，一点点轻轻往下滚动，直到列表里出现了一个xhr请求：
![image.png](imgs/4324074-c5ca5ec0f3ead19c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

点击这个请求，可以在Headers里看到它的Parameters参数，其实就是请求名称的问号后面的部分：
![image.png](imgs/4324074-cf5c225b56206c79.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

`order_by`是排序，`page`是第几页。所以不是简书文章列表不分页，默认加载的是`page=1`，而当你往下滚动的时候自动添加下一页的内容`page=2,page=3...`。

我们查看它的Response也会发现，它所得到的内容和我们上面的网页源代码格式是一致的：
![image.png](imgs/4324074-fb14a24590155406.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


## 设定参数

打开Jupyter Notebook，在第一个cell单元编写代码，设定相关参数(headers字段涉及到个人隐私已经被我简化了，你须要在浏览器里面复制自己的)：

```
url = 'https://www.jianshu.com/u/ae784c57b353'
params = {'order_by': 'shared_at', 'page': '1'}
headers = '''
GET /u/ae784c57b353 HTTP/1.1
Host: www.jianshu.com
Connection: keep-alive
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7
Cookie: read_mode=day; default_font=font2; locale=zh-CN;....5b9fb068=1538705012
If-None-Match: W/"31291dc679ccd08938f27b1811f8b263"
'''
```
但是这样的headers格式是个长串字符，我们需要把它改写成params那样的字典，手工改太麻烦也容易改错，我们再添加一个cell使用下面代码自动改写(不熟悉的话可以暂时不用理解它，以后随着学习深入就很快会看懂了)：
```
def str2obj(s, s1=';', s2='='):
    li = s.split(s1)
    res = {}
    for kv in li:
        li2 = kv.split(s2)
        if len(li2) > 1:
            res[li2[0]] = li2[1]
    return res


headers = str2obj(headers, '\n', ': ')
```

## 发起Request请求

先用最简单的代码发送请求检查是否正确：
```
import requests
html = requests.get(url, params=params, headers=headers)
print(html.text)
```
正常的话应该输出和网页源代码差不多的内容。

## 获取标题数据

在页面一个文章上【右键-检查】打开Elements元素面板，我们来仔细看每个文章标准的一段：
![image.png](imgs/4324074-ba28c7455a037b55.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

从图上可以看到每个`<li>`标签对应一个文章，我们需要的三个内容（红色框）：
* 文章编号,`/p/0fed5efab3e5`,也是查看文章的链接地址,每文章唯一。
* 文章的标题，`人工智能通识-AI发展简史-讲义全篇`。
* 文章的阅读量，`272`

因为数据都是在html标签里面，所以我们需要使用BeautifulSoup功能模块来把html变为容易使用的数据格式，先尝试抓到标题。把上面的代码改进一下：

```
import requests
from bs4 import BeautifulSoup

html = requests.get(url, params=params, headers=headers)
soup = BeautifulSoup(html.text, 'html.parser')
alist = soup.find_all('div', 'content')
for item in alist:
    title = item.find('a', 'title').string
    print(title)
```

全部运行输出结果如下有9个文章：

![image.png](imgs/4324074-5f805d1bebcd5414.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

## 获取文章编号和阅读量

我们对上面的代码改进一下：
```
import requests
from bs4 import BeautifulSoup

html = requests.get(url, params=params, headers=headers)
soup = BeautifulSoup(html.text, 'html.parser')
alist = soup.find_all('div', 'content')
for item in alist:
    line = []
    titleTag = item.find('a', 'title')  #标题行a标记
    line.append(titleTag['href'])  #编号
    line.append(titleTag.string)  #标题    

    read = item.find('div', 'meta').find('a').contents[2]
    line.append(str(int(read)))  #编号,先转int去掉空格回车，再转str才能进line

    print(','.join(line))
```
在这里我们使用`[href]`的方法获取了`<a class="wrap-img" href="/p/0fed5efab3e5" target="_blank">`这个标记内的属性，这个方法同样适用于更多情况，比如`[class]`可以获得`warp-img`字段。

另外`item.find('div', 'meta').find('a').contents[2]`这里，我们利用了`find`只能找到内部第一个符合条件的标记的特点；`contents[2]`这是由于a标记内包含了多个内容，`<i class="iconfont ic-list-read"></i> 20`，试了几下，发觉`[2]`是我们想要的内容。

以上代码运行全部可以输出以下内容：
![image.png](imgs/4324074-ca0ef8e13984a827.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


## 获取粉丝数和文章总数

我们把流程分成两步走：
1. 获取文章总数和粉丝总数
1. 根据文章总数循环获取每页的数据

把上面的cell内容都选中，按`Ctrl+/`都临时注释掉。然后在这个cell上面添加一个新的cell，用来读取文章总数`acount`和关总数`afocus`:
```
import requests
from bs4 import BeautifulSoup

html = requests.get(url, headers=headers)
soup = BeautifulSoup(html.text, 'html.parser')
afuns = soup.find('div', 'info').find_all('div','meta-block')[1].find('p').string
acount = soup.find('div', 'info').find_all('div','meta-block')[2].find('p').string
afuns=int(afuns)
acount=int(acount)
print('粉丝:',afuns,'文章', acount)
```
`find`只获取第一个符合条件的标记，`find_all`是获取所有符合条件的标记。
要对比着html源代码来看：
![image.png](imgs/4324074-5bfd834b0e4ae4d5.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


正常应该输出两个数字。

## 获取全部文章数据

选择刚才屏蔽掉的代码，再次按`ctrl+/`恢复可用。
然后修改成以下内容：
```
import math
import time

pages=math.ceil(acount/9)
data=[]
for n in range(1,pages+1):
    params['page']=str(n)
    html = requests.get(url, params=params, headers=headers)
    soup = BeautifulSoup(html.text, 'html.parser')
    alist = soup.find_all('div', 'content')
    for item in alist:
        line = []
        titleTag = item.find('a', 'title')  #标题行a标记
        line.append(titleTag['href'])  #编号
        line.append(titleTag.string)  #标题    

        read = item.find('div', 'meta').find('a').contents[2]
        line.append(str(int(read)))  #编号,先转int去掉空格回车，再转str才能进line

        data.append(','.join(line))
        print('已获取:',len(data))
    time.sleep(1)
        
print('\n'.join(data))
```
这里使用了`math.ceil(acount/9)`的方法获取总页数，ceil是遇小数就进1，比如`ceil(8.1)`是9，`ceil(9.0)`也是9，这样即使最后一页只有1个文章也不会被遗漏。

`for n in range(1,12)`这个for循环中，每一次n都被自动加1，获取第一页时候n是1，第二页时候n是2...所以`params['page']=str(n)`就可以自动变页。

`print('已获取:',len(data))`这行其实没有用，因为获取页面需要十几秒钟，如果中间不打印点什么会看上去像是无反应或死机。`len(data)`是指data这个列表的长度length。

`time.sleep(1)`每读取一页就停1秒，以免被服务器发觉我们是爬虫而封禁我们。

## 存储文章数据

我们上面使用逗号分开文章的序号、标题和阅读量，然后再加入data列表，`data.append(','.join(line))`;同样，最后我们输出时候使用回车把data所有文章连在一起，`print('\n'.join(data))`。

实际上，我们可以直接把它存储为excel可以读取的.csv文件。最下面新建一个cell添加以下代码：
```
with open('articles.csv', 'w', encoding="gb18030") as f:
    f.write('\n'.join(data))
    f.close()
```
这里注意,`w`是write写入模式，`encoding="gb18030"`是为了确保中文能正常显示。

运行后就能在你对应的Notebook文件夹内多出一个articles.csv文件，用excel打开就能看到类似下面的数据:
![image.png](imgs/4324074-02dedb92240b6931.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

## 每天使用不同的文件名存储

我们每天爬取一下所有文章的数据，每天存为一个excel表，都叫做`articles.csv`肯定会重名。我们应该用不同的日期来命名就好很多，比如`articles-201810061230.csv`表示2018年10月6日12点30分统计的记录，这样看起来就清楚多了。

如何获取当前电脑的日期时间？计算机里面记录时间的最简单方法就是，只记录从某一年开始经过了多少毫秒，大多是从1970年开始算的。只要知道距离1970年1月1日0时0分0秒0毫，过了多少毫秒，那么这个时间就能计算出是哪年哪月哪日。

我们修改一下上面的代码：
```
tm = str(int(time.time()))
fname = 'articles_' + tm + '.csv'
with open(fname, 'w', encoding="gb18030") as f:
    f.write('\n'.join(data))
    f.close()
```
这样存储的就是类似`articles_1538722108.csv`文件名的文件了。

>如果要变回年月日的显示，需要使用datatime功能模块,例如
`import time,datetime`
`tm=int(time.time())`
`print(datetime.datetime.fromtimestamp(tm).strftime('%Y-%m-%d %H:%M:%S'))`
这个会输出类似`2018-10-05 14:47:11`这样的结果

## 增量存储粉丝数

我们需要把每一天抓取到的关注数和文章数存储到一个excel表里，而不是分开的，我们新增一个cell，添加如下代码,实现每次运行就向`total.csv`文件增加一行数据：
```
from os.path import exists
alabels = ['time', 'funs', 'articles']
adata = [tm, afuns,  str(acount)] #acount是数字，需要转化
afname='./articles_total.csv'
if not exists(afname):
    with open(afname, 'a', encoding="gb18030") as f:
        f.write(','.join(alabels)+'\n')
        f.close()
with open(afname, 'a', encoding="gb18030") as f:
    f.write(','.join(adata)+'\n')
    f.close()
```
`exists`是存在的意思，如果文件存在，就正常往里添加新数据，如果不存在就先添加一个表头`time,focus,articles`。

## 最后回顾

这个文章里我们做了下面几个练习：
1. 根据问题思考需要哪些数据，能不能抓取到
1. 分析页面，找到这些数据在哪里，是html文档里还是单独的请求
1. 找到请求，复制headers，搞清楚params
1. 发送请求，用beautifulsoup帮助找到需要的数据
1. 根据文章总数，循环处理分页
1. 把获取到的数据存储为excel可以识别的csv文件
1. 利用时间自动创建不同的文件
1. 文件的增量添加写入，每次添加一行数据

最终整理到一起的代码如下，添加了afuns、aword、alike等数据。
注意必须更换自己的headers才能使用：
```
#cell-1 设置参数

url = 'https://www.jianshu.com/u/ae784c57b353'
params = {'order_by': 'shared_at', 'page': '1'}
headers = '''
GET /u/ae784c57b353 HTTP/1.1
Host: www.jianshu.com
Connection: keep-alive
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7
Cookie: read_mode=day; default_font=font2; locale=zh-CN; ......b9fb068=1538705012
If-None-Match: W/"31291dc679ccd08938f27b1811f8b263"
'''

#cell-2 转化headers

def str2obj(s, s1=';', s2='='):
    li = s.split(s1)
    res = {}
    for kv in li:
        li2 = kv.split(s2)
        if len(li2) > 1:
            res[li2[0]] = li2[1]
    return res


headers = str2obj(headers, '\n', ': ')

# cell-3 发送整体请求，获取基本信息、文章总数

import requests
from bs4 import BeautifulSoup

html = requests.get(url, headers=headers)
soup = BeautifulSoup(html.text, 'html.parser')
afocus = soup.find('div', 'info').find_all('div','meta-block')[0].find('p').string
afuns = soup.find('div', 'info').find_all('div','meta-block')[1].find('p').string
acount = soup.find('div', 'info').find_all('div','meta-block')[2].find('p').string
awords = soup.find('div', 'info').find_all('div','meta-block')[3].find('p').string
alike = soup.find('div', 'info').find_all('div','meta-block')[4].find('p').string
acount=int(acount)
print('>>文章总数', acount)

#cell-4 循环获取每一页数据

import math
import time

aread = 0
pages = math.ceil(acount / 9)
data = []
for n in range(1, pages + 1):
    params['page'] = str(n)
    html = requests.get(url, params=params, headers=headers)
    soup = BeautifulSoup(html.text, 'html.parser')
    alist = soup.find_all('div', 'content')
    for item in alist:
        line = []
        titleTag = item.find('a', 'title')  #标题行a标记
        line.append(titleTag['href'])  #编号
        line.append(titleTag.string)  #标题

        read = item.find('div', 'meta').find('a').contents[2]
        aread += int(read)  #计算总阅读量
        line.append(str(int(read)))  #编号,先转int去掉空格回车，再转str才能进line

        data.append(','.join(line))
        print('已获取:', len(data))
    time.sleep(1)


#cell-5 存储文章数据新文件

tm = str(int(time.time()))
fname = './data/articles_' + tm + '.csv'
with open(fname, 'w', encoding="gb18030") as f:
    f.write('\n'.join(data))
    f.close()

#cell-6 增量存储基础信息

from os.path import exists
alabels = ['time', 'focus', 'funs', 'articles', 'words', 'like', 'read']
adata = [tm, afocus, afuns, str(acount), awords, alike, str(aread)]
afname='./articles_total.csv'
if not exists(afname):
    with open(afname, 'a', encoding="gb18030") as f:
        f.write(','.join(alabels)+'\n')
        f.close()
with open(afname, 'a', encoding="gb18030") as f:
    f.write(','.join(adata)+'\n')
    f.close()

#cll-7 提示完成

print('>>完成，保存在%s'%fname)
```

>过几天收集到一些数据之后再分享数据分析相关的内容，请留意我的文章更新~

---
[智能决策上手系列教程索引](https://www.jianshu.com/p/0d2e46e69f58)
---
###每个人的智能决策新时代
如果您发现文章错误，请不吝留言指正；
如果您觉得有用，请点喜欢；
如果您觉得很有用，欢迎转载~
---
END

