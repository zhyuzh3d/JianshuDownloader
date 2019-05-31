>[点击这里进入**人工智能嘚吧嘚**目录，观看全部文章](https://www.jianshu.com/p/ff37dbc75edb)
---

以前未登录情况下爬取豆瓣网电影页面没遇到过限制，但最近请求频繁时候导致返回Forbidden 403服务器拒绝响应的情况，暂时可行的方法是正常在页面登录注册，然后请求Requests携带header信息发送请求，适当放慢请求频率。

##解析复制到的Request header字符串

先从浏览器控制台复制到请求头，然后利用函数str2dict解析成dict格式，稍后发送请求时候需要使用到。
```
#使用headers,不使用的话频率稍高就会返回繁忙403
header_str='''
GET /top250 HTTP/1.1
Host: movie.douban.com
Connection: keep-alive
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
Referer: https://movie.douban.com/chart
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7
Cookie: __utmc=223455111; __utmz=234495111.1512303343....106952.
'''
def str2dict(s,s1=';',s2='='):
    li=s.split(s1)
    res={}
    for kv in li:
        li2=kv.split(s2)
        if len(li2)>1:
            res[li2[0]]=li2[1]
    return res
headers=str2dict(header_str,'\n',': ')
```

##发送请求

发送请求获取Top250电影名称和年份信息
```
import requests
from bs4 import BeautifulSoup
import time

top250=[]

url = 'https://movie.douban.com/top250?start='

for i in range(10):
    print('processing page',i)
    purl = url + str(i * 25)
    res = requests.get(purl,headers=headers)
    soup = BeautifulSoup(res.text)
    movies = soup.find_all('div', 'info')
    for mov in movies:
        title = mov.find('span', 'title').text
        yearTag = mov.find('div', 'bd').find('p').contents[2]
        year = yearTag.split('/')[0].strip()
        top250.append({
            'title':title,
            'year':year
        })
    time.sleep(1)
print(len(top250),top250[:3])
```

##直接使用API拉取JSON数据

原本豆瓣还提供了一些用于第三方开发者读取数据的接口API，可以通过这些API直接读取数据，目前官方已经停止这些接口的维护，是否能持续继续使用也是未知的。
以下代码可以一次性获取TOP250的完整JSON格式数据。
注意最后的ensure_ascii为False表示其中包含非ascii码汉字,如果不使用ensure_ascii参数将输出字母乱码。
```
#使用API
import requests
import json
import time

top250 = []

api = 'http://api.douban.com/v2/movie/top250?start=0&count=250'

res = requests.get(api)
movies = json.loads(res.text)['subjects']
print(json.dumps(movies[0], indent=2, ensure_ascii=False))
```

##绘制佳片的年代分布

使用plotly进行绘图。
```
import plotly.offline as py
import plotly.graph_objs as go
py.init_notebook_mode()
movies_dict={}
for mov in top250:
    year=mov['year'][:4]
    if year in movies_dict:
        movies_dict[year]+=1
    else:
        movies_dict[year]=1
data=go.Bar(
    x=[year for year in movies_dict],
    y=[movies_dict[year] for year in movies_dict]
)
fig=go.FigureWidget([data])
fig
```
![](imgs/4324074-baae7a3b50a58390.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



---
>[点击这里进入**人工智能DBD嘚吧嘚**目录，观看全部文章](https://www.jianshu.com/p/ff37dbc75edb)
---
###每个人的智能新时代
如果您发现文章错误，请不吝留言指正；
如果您觉得有用，请点喜欢；
如果您觉得很有用，欢迎转载~
---
END