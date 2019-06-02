[智能决策上手系列教程索引](https://www.jianshu.com/p/0d2e46e69f58)
---

这一篇我们针对之前爬取的拉勾网职位信息进行词频统计，看一下出现频率最高的关键词是哪些。
>[如果您还没有抓取，请从这里直接下载100个json搁置职位文件](https://pan.baidu.com/s/1_vfiIdIPGzAyBuRx4__BsA)  密码:tfdv

## 读取数据

由于我们之前是吧每个职位都存储为单个的csv文件，所以我们先把它们的details职位要求细节信息读取出来。代码如下，具体说明参照之前的文章。
```
#cell-1 定义读取细节的函数
def readDetail(fileName):
    with open(fileName, 'r') as f:
        job = json.load(f)
        details = job['details'].lower()
        details = details.replace(' ', '').replace('\xa0', '')
        return details
```
```
#cell-2 读取文件列表，把细节信息合并到text
import os

text = ''
folder = '/Users/zhyuzh/Desktop/Jupyter/spiders/data/lagou_ai/jobs1000/'
files = os.listdir(folder)
jobCount = 0
for n in range(0, 1000):
    if not files[n].find('.json') == -1:
        details = readDetail(folder + files[n])
        if details.find('python') != -1 or details.find('tensorflow') != -1:
            jobCount += 1
            text += details
print('>>Got jobs:', jobCount)
```

##jieba分词
要统计单词的出现频率，首先我们要进行切词，仍然使用jieba分词。
```
#cell-3使用jieba分词
import jieba
words = jieba.lcut(text)  # 默认是精确模式
cuted=' '.join(words)
print(cuted[:100])
```
这里`print(cuted[:100])`只输出前100个字看情况，应该得到类似这样的输出，每个词或标点被用空格分开了：
`职位 描述 ： 岗位职责 ： 1 . 展开 机器 学习 / 深度 学习 等 相关 领域 研究 和 开发 工作 ； 2 . 负责 从事 深度 学习 框架 搭建 ， 包括 机器 学习 、 图像处理 等 的` 

##nltk词频统计

nltk全称是Natural Language Toolkit，自然语言工具包，是专门用来做文本语言分析的工具，和jieba类似，nltk包含了更多功能，但它是针对英文的，对中文来说有些功能还不太好，比如它的中文分词就不如jieba。
[nltk官方网站](http://www.nltk.org/)

如果还没安装的话可以用命令`conda install nltk`或者`pip3 install nltk`进行安装。

使用下面代码统计单词出现的频率（次数）：
```
#cell-4统计词频
from nltk.probability import FreqDist
fdist = FreqDist(words)
tops=fdist.most_common(50)
print(tops)
```
`FreqDist`会根据文本进行单词统计，注意，英文每个单词中间都是有空格的，而中文字词之间没有空格，所以必须使用jieba分词之后的文本。
`. most_common(50)`是打印出现最多的50个单词及相应的次数。
得到类似下面的结果:
`[('、', 5079), ('，', 4179), ('的', 2984), ('；', 2003), ('.', 1438), ('和', 1299), ('：', 1175), ('等', 1105), ('。', 1085), ('学习', 1024), ('有', 945), ('/', 903), ('算法', 885), ('经验', 746), ('相关', 696), ('2', 692), ..., ('系统', 273)]`

## 去除冗余单字

上面的输出中，我们看到很多单个的标点或汉字，肯定不是我们需要的内容，我们用下面的代码删除它们。
```
#cell-5去除单字
delarr=[]
for key in fdist:
    if len(key)<2:
        delarr.append(key)
for key in delarr:
    del fdist[key]
    
tops=fdist.most_common(50)
print(tops)
```
这里注意上面用使用`FreqDist `方法得到的`fdist`其实就是一个字典，类似`{'的':2984,';':2003}`这样的对象，`del fdist['的']`的方法可以删除第一个字段。

我们先把所有要删除的字段放入delarr中，然后循环删除它。
删除之后再次打印top50，单个的词和标点就消失了：
`[('学习', 1024), ('算法', 885), ('经验', 746), ('相关', 696), ('熟悉', 675), ('技术', 564), ('能力', 561), ('机器', 544), ('开发', 537), ('优先', 531), ('数据', 511), ('工作', 484), ('职位', 471), ('人工智能', 462), ('描述', 440), ('负责', 434), ('python', 381), ...,('实现', 181)]`

##保留有效词

我们打印100个，然后把不相关的都去除。
```
#cell-6 打印单词
tops=fdist.most_common(100)
t=""
for key in tops:
    t+='\''+key[0]+'\''
    t+=','
print(t)
```
得到输出`'学习','算法','经验','相关','熟悉','技术','能力','机器','开发','优先','数据','工作','职位','人工智能','描述','负责','python',...,'计算',`

我们手工选择要删除的，然后把这些也删除掉：
```
#cell-7 保留有效词
usearr=['学习','算法','经验','机器','数据','人工智能','python','深度','分析','应用','模型','系统','研究','设计','优化','计算机','团队','产品','平台','研发','项目','数学','专业','处理','java','c++','框架','问题','实现','用户','基础','数据挖掘','自然语言','编程','语言','数据分析','识别','推荐','沟通','建模','实际','理解','挖掘','linux','nlp','智能','硕士','文本','视觉','场景','tensorflow','提升','需求','知识','互联网','编程语言','本科','代码','计算']
for key in usearr:
    if delarr2.index(key)==-1:
        del fdist[key]
tops=fdist.most_common(50)
print(tops)
```
然后得到更好的列表：
`[('学习', 1024), ('算法', 885), ('经验', 746), ('相关', 696), ('熟悉', 675), ('技术', 564), ('能力', 561), ('机器', 544), ('开发', 537), ('优先', 531),...,('实现', 181)]`

##绘制图表

参考[上一篇文章](https://www.jianshu.com/p/210e4d324f25)我们使用plotly进行图表绘制：
```
#cell-8绘制图表
import plotly
import plotly.graph_objs as go

plotly.offline.init_notebook_mode(connected=False)

keywords=[item[0] for item in tops]
weights=[item[1] for item in tops]

plotly.offline.iplot({
    "data": [go.Scatter(x=keywords, y=weights)],
    "layout": go.Layout(title="拉勾网人工智能职业关键词分布")
})
```
输出大致如下图：
![image.png](imgs/4324074-89e7733b32dca543.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

##总结
汇总步骤如下：
1. 读取文件，获得text文本
1. 用jieba分词，获得空格隔开的文本
1. 用nltk的FreqDist统计词频,获得词频字典对象
1. 用most_common提取前面50个
1. 去除单个字和标点符号，或者保留需要的单词
1. 绘图统计

汇总代码如下(使用保留词，没有使用删除表单单个字)：
```
#cell-1
def readDetail(fileName):
    with open(fileName, 'r') as f:
        job = json.load(f)
        details = job['details'].lower()
        details = details.replace(' ', '').replace('\xa0', '')
        return details
#cell-2
import os

text = ''
folder = '/Users/zhyuzh/Desktop/Jupyter/spiders/data/lagou_ai/jobs1000/'
files = os.listdir(folder)
jobCount = 0
for n in range(0, 1000):
    if not files[n].find('.json') == -1:
        details = readDetail(folder + files[n])
        if details.find('python') != -1 or details.find('tensorflow') != -1:
            jobCount += 1
            text += details
print('>>Got jobs:', jobCount)

#cell-3
import jieba
words = jieba.lcut(text)  # 默认是精确模式
cuted=' '.join(words)
print(cuted[:100])

#cell-4
from nltk.probability import FreqDist
fdist = FreqDist(words)
usearr=['学习','算法','经验','机器','数据','人工智能','python','深度','分析','应用','模型','系统','研究','设计','优化','计算机','团队','产品','平台','研发','项目','数学','专业','处理','java','c++','框架','问题','实现','用户','基础','数据挖掘','自然语言','编程','语言','数据分析','识别','推荐','沟通','建模','实际','理解','挖掘','linux','nlp','智能','硕士','文本','视觉','场景','tensorflow','提升','需求','知识','互联网','编程语言','本科','代码','计算']
for key in usearr:
    if delarr2.index(key)==-1:
        del fdist[key]
tops=fdist.most_common(50)
print(tops)

#cell-5
import plotly
import plotly.graph_objs as go

plotly.offline.init_notebook_mode(connected=False)

keywords=[item[0] for item in tops]
weights=[item[1] for item in tops]

plotly.offline.iplot({
    "data": [go.Scatter(x=keywords, y=weights)],
    "layout": go.Layout(title="拉勾网人工智能职业关键词分布")
})
```

---
[智能决策上手系列教程索引](https://www.jianshu.com/p/0d2e46e69f58)
---
###每个人的智能决策新时代
如果您发现文章错误，请不吝留言指正；
如果您觉得有用，请点喜欢；
如果您觉得很有用，欢迎转载~
---
END