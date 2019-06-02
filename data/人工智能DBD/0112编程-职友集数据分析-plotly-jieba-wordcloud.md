>[点击这里进入**人工智能嘚吧嘚**目录，观看全部文章](https://www.jianshu.com/p/ff37dbc75edb)
---

[上一篇介绍了职友集职位数据的网页源码文件的爬取](https://www.jianshu.com/p/465eccb9d2f9)，得到了170个网页。
这篇文章将介绍如何从网页数据中解析数据，并进行可视化展示。

## 从文件夹中读取数据
```
#读取所有文件列表
import os
keyw='python'
files=os.listdir('/Users/zhyuzh/Desktop/Jupyter/tutor/jobui/{}/'.format(keyw))
#files=os.listdir(r'C:\user\...\{}'.format(keyw)) #win下注意用r转义，不要用斜杠结尾
files
```
files的结果大致如下：
![](imgs/4324074-3ab6e03a57d64391.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

##读取一个文件提取职位数据，转化为dict字段

readjob函数接收一个fname参数，就是上面files列表的单个元素。
读取html文件数据，用BeautifulSoup解析，提取职位标题title、城市city、pay薪资，details详情等信息，并把薪资拆分为起薪pay_low和上限pay_hig两个数值。
注意这里使用了find、find_all、contents、text等方法
函数最后返回整个job的字典对象。
```
#读取一个文件，返回一个job字典
from bs4 import BeautifulSoup

def readjob(fname):
    with open('./jobui/{}/{}'.format(keyw,fname),'r') as f: #'r'在win下改为‘rb',byte
        html=f.read()
        #html=html.decode('utf-8') #win下打开此行
        soup=BeautifulSoup(html)       

        jobtag=soup.find('div','jk-box jk-matter j-job-detail')
        title=jobtag.find('h1',{'title':True}).text
        city=jobtag.find('ul').find_all('li')[0].contents[1]      
               
        pay=jobtag.find('span','fs16 fwb f60').text        
        pay_li=pay.replace('¥','').split('-')
        pay_low=pay_li[0].strip()
        pay_hig=pay_li[0].strip() if len(pay_li)>1 else pay_low
        
        details=jobtag.find('div','hasVist cfix sbox fs16').text.strip()
        
        job={
            'title':title,
            'city':city,
            'pay_low':pay_low,
            'pay_hig':pay_hig,
            'details':details
        }
        
        return job
```

##将所有文件转为job字典，并放入jobs_all列表
注意由于原本职友集网站的职位列表页面就有一些第三方广告的招聘职位，这样职位的链接link也之前被我们存储到了文件夹中，但实际上这些第三方的页面完全与职友集标准的职位详情页面不同，我们的readjob函数也无法解析，所以使用`try...except...`方法避免因为出错而终止。
```
jobs_all=[]
for file in files:
    try:
        job=readjob(file)
        jobs_all.append(job)
    except:
        print('Err:',file)
print('OK!')
```
这时候所有职位信息都已经放入jobs_all列表，共有上百个元素，它看起来这样：
![](imgs/4324074-d9cddbaeb199cb8b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

##从jobs_all统计城市分布

```
#统计城市
cityjobs={}
for job in jobs_all:
    city=job['city']
    city=city.split('-')[0]
    if city in cityjobs:
        cityjobs[city]+=1
    else:
        cityjobs[city]=1
cityjobs
```
cityjobs看起来这样:
![](imgs/4324074-781108e2e2e36e7d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

##使用plotly画图表
使用Anaconda的prompt工具，输入命令`conda install plotly`安装plotly。
柱状图
```
import plotly.offline as py
import plotly.graph_objs as go
py.init_notebook_mode()
citydata=go.Bar(
    x=[key for key in cityjobs],
    y=[cityjobs[k] for k in cityjobs]
)
f = go.FigureWidget([citydata])
f
```
生成图如下：
![](imgs/4324074-ff68b37a3cfa63ab.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

饼状图
```
citydata_pie=go.Pie(
    labels=[key for key in cityjobs],
    values=[cityjobs[k] for k in cityjobs]
)
f = go.FigureWidget([citydata_pie])
f
```
生成图如下：
![](imgs/4324074-7298d00f05f357f3.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

##使用结巴切词
使用Anaconda的prompt工具，输入命令`conda install -c conda-forge jieba`安装jieba中英文分词工具。

```
import jieba
text=' '.join([job['details'].replace('\n','') for job in jobs_all])
seg_list = jieba.cut(text, cut_all=False)
' ' .join(seg_list)
```
输出的切词结果如下：
![](imgs/4324074-d8fd13e386415605.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

使用正则表达式过滤掉中文：
```
import re
pattern = re.compile(r'^[a-zA-Z0-1]+$')
words = [w for w in seg_list if pattern.match(w)]
cuted = ' '.join(words)
print(cuted)
```
输出结果如下：
![](imgs/4324074-82ff601ec95cd11d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

##使用wordcloud生成词云
使用Anaconda的prompt工具，输入命令`conda install -c conda-forge wordcloud`安装词云工具。
需要下载字体文件并放到代码文件一起,[思源中文字体，点击可以直接下载使用](https://pan.baidu.com/s/19VEuo7lfurJhPYIOS-uZRw)

```
from wordcloud import WordCloud
fontpath = 'SourceHanSansCN-Regular.otf'

wc = WordCloud(
    max_font_size=500,
    min_font_size=20,
    width=1600,  #图像宽度
    height=1200, #图像高度
    font_path=fontpath, #字体文件要放在和代码一起
    background_color='white',
    collocations=False,
    margin=20
)
wc.generate(cuted)
```
使用Matplotlib显示图片：
```
import matplotlib.pyplot as plt
plt.figure(dpi=120)
plt.imshow(wc, interpolation="bilinear")
plt.axis('off')
```
最后输出结果：
![](imgs/4324074-737acf4a373d5cf0.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

##关于pay薪资的数据处理
因为薪资可能是`4000~6000`，也可能是`4k~6k`或者`1.2~2.4万/月`之类，所以要进行处理，根据实际需要可能有不同，下面代码仅供参考：
```
import re
jobs=[{'pay_low':'1.2','pay_hig':'1.5万/月'},{'pay_low':'4.5','pay_hig':'6k'}]
for job in jobs:
    if job['pay_hig'].find('万')!=-1:#包含万
        job['pay_hig']=re.compile('[0-9\.]+').findall(job['pay_hig'])[0] #提取数字和小数点
        job['pay_hig']=str(int(float(job['pay_hig'])*10000))
        job['pay_low']=str(int(float(job['pay_low'])*10000))
    if job['pay_hig'].find('k')!=-1 or job['pay_hig'].find('千')!=-1:#包含千
        job['pay_hig']=re.compile('[0-9\.]+').findall(job['pay_hig'])[0] #提取数字和小数点
        job['pay_hig']=str(int(float(job['pay_hig'])*1000))
        job['pay_low']=str(int(float(job['pay_low'])*1000))   
jobs
```
输出:
![](imgs/4324074-376b0020e2e31be1.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

几点说明：
- `'1.3万/月'.find('万')`返回3，即第三个位置找到`万`字，如果找不到就返回-1
- `re.compile('[0-9\.]+').findall('1.3万/月')`可以得到`['1.3']`。
- `str(int(float('1.3')*1000))`得到字符串`'1300'`

>[**关于windows和mac的python文件读写编码的不同请参照这里**](https://www.jianshu.com/p/e3926fc1352c)



---
>[点击这里进入**人工智能DBD嘚吧嘚**目录，观看全部文章](https://www.jianshu.com/p/ff37dbc75edb)
---
###每个人的智能新时代
如果您发现文章错误，请不吝留言指正；
如果您觉得有用，请点喜欢；
如果您觉得很有用，欢迎转载~
---
END