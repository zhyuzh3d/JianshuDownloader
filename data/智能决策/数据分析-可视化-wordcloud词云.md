[智能决策上手系列教程索引](https://www.jianshu.com/p/0d2e46e69f58)
---
![image.png](imgs/4324074-befd8f48f86554b7.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

我们使用已经合并在一起的拉勾网数百个职位招聘详情文件来进行这个练习。
[百度云下载文件](https://pan.baidu.com/s/1HG7rcgeLTpcemo-oT_KebA) 密码:bvb8

##读取文件

读取并打印出前面100个字符
```
text=''
with open('./lagou-job1000-ai-details.txt','r') as f:
    text=f.read()
    f.close()
print(text[:100])
```
输出
`职位描述：岗位职责：1.展开机器学习/深度学习等相关领域研究和开发工作；2.负责从事深度学习框架搭建，包括机器学习、图像处理等的算法和系统研发;3.支持公司相关产品深度学习相关研究；岗位要求：1.机器`

##jieba分词

```
#cell-2
import jieba
words = jieba.lcut(text)
cuted=' '.join(words)
print(cuted[:100])
```
输出被空格分开的文本：
`职位 描述 ： 岗位职责 ： 1 . 展开 机器 学习 / 深度 学习 等 相关 领域 研究 和 开发 工作 ； 2 . 负责 从事 深度 学习 框架 搭建 ， 包括 机器 学习 、 图像处理 等 的`

##安装wordcloud和matplotlib

[词云wordcloud的官方项目地址](https://github.com/amueller/word_cloud)

推荐直接用`pip3 install wordcloud`进行安装。
如果是conda则要使用-c切换通道为conda-forge，命令是
`conda install -c conda-forge wordcloud`可能比较慢，耐心等就好。

[matplotlib视觉化模块官方网址](https://matplotlib.org/)
安装命令`pip3 install matplotlib`或`conda install matplotlib`。

##生成词云对象
```
#cell-3
from wordcloud import WordCloud
fontpath='SourceHanSansCN-Regular.otf'

wc = WordCloud(font_path=fontpath,  # 设置字体
               background_color="white",  # 背景颜色
               max_words=1000,  # 词云显示的最大词数
               max_font_size=500,  # 字体最大值
               min_font_size=20, #字体最小值
               random_state=42, #随机数
               collocations=False, #避免重复单词
               width=1600,height=1200,margin=10, #图像宽高，字间距，需要配合下面的plt.figure(dpi=xx)放缩才有效
              )
wc.generate(cuted)    
```
首先，默认情况wordcloud是不支持中文显示的，所以要先添加一个中文字体文件，一般是`.ttf或.otf`格式，你可以从网上搜索‘字体下载’找到想要的字体。上面代码中使用的是[思源中文字体，点击可以直接下载使用](https://pan.baidu.com/s/19VEuo7lfurJhPYIOS-uZRw)

`WordCloud(...)`命令包含了很多参数，其中就包含了我们上面设定的字体路径`font_path`。
注意这里`width=1600,height=1200,margin=100`图像宽高只是原始图像的大小，至于后面显示出来的时候可能还会被放缩。它的更多参数可以查看下面链接[wordcloud官方WordCloud方法说明](https://amueller.github.io/word_cloud/generated/wordcloud.WordCloud.html#wordcloud.WordCloud)

##显示词云图

我们用matplotlib的imshow就是image-show把图片显示出来。
```
#cell-4
import matplotlib.pyplot as plt
plt.figure(dpi=100) #通过这里可以放大或缩小
plt.imshow(wc, interpolation='catrom',vmax=1000)
plt.axis("off") #隐藏坐标
```
可以得到如下图效果：
![image.png](imgs/4324074-c5eb33376a83ce89.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


## 去除冗余单词

我们可以利用jieba的del_word功能去掉冗余单词。
修改cell-2代码：
```
#cell-2
import jieba

removes =['熟悉', '技术', '职位', '相关', '工作', '开发', '使用','能力','优先','描述','任职']
for w in removes:
    jieba.del_word(w)

words = jieba.lcut(text)
cuted = ' '.join(words)
print(cuted[:100])
```
这里用for循环依次删除了各个冗余词，也可不用for循环，改为lcut之后对words进行处理：
```
words = jieba.lcut(text)
words = [w for w in words if w not in removes]
```
整体运行，得到下图：
![image.png](imgs/4324074-ad6fb852df8ff02e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



## 区分中英文

如果我们只关注英文技术点，比如python，tensorflow等，那就忽略中文内容。
使用正则表达式来匹配提取哪些由a~z小写字母和A~Z大写字母加上0~9数字组成的单词。
修改cell-2如下：
```
#cell-2
import jieba
words = jieba.lcut(text)
import re
pattern = re.compile(r'^[a-zA-Z0-1]+$')
words = [w for w in words if pattern.match(w)]
cuted = ' '.join(words)
print(cuted[:100])
```
完整执行，得到下图：
![image.png](imgs/4324074-e0b2ea96509f7787.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


我们可以从这个图中看到人工智能技术相关职位所需要的掌握的主要技能。

## 改变造型

我们让单词按照特定的造型来排列。首先我们需要一张造型图片，下面是一张AI文字造型图片，请把它右键另存为`ai-mask.png`文件。
![image.png](imgs/4324074-a972a1fcb3d62faa.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

前面在`wc = WordCloud(font_path=fontpath...`中有很多参数可以设置，其中就有mask遮罩参数，可以指定一张读取的图片数据，根据官方说明，这个数据应该是`nd-array`格式，这是一个多维数组格式(N-dimensional Array)。

我们使用PIL模块中的Image.open('...')可以读取图片，然后利用numpy来转换为`nd-arry`格式。
修改cell-3,读取图片并增加mask参数：
```
#cell-3
from wordcloud import WordCloud
fontpath='SourceHanSansCN-Regular.otf'

import numpy as np
from PIL import Image
aimask=np.array(Image.open("ai-mask.png"))

wc = WordCloud(font_path=fontpath,  # 设置字体
               background_color="white",  # 背景颜色
               max_words=1000,  # 词云显示的最大词数
               max_font_size=100,  # 字体最大值
               min_font_size=5, #字体最小值
               random_state=42, #随机数
               collocations=False, #避免重复单词
               mask=aimask, #造型遮盖
               width=1600,height=1200,margin=2, #图像宽高，字间距，需要配合下面的plt.figure(dpi=xx)放缩才有效
              )
wc.generate(cuted)  
```
完整执行后得到下图：
![image.png](imgs/4324074-f38e9bd5b1eef584.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

可以看到原本图片上白色的部分被留空，有颜色的部分才会放置单词。

## 改进颜色

默认情况图片上文字的颜色都是随机的，我们可以使用图片来控制文字的颜色。

`WordCloud`方法提供了一个color_func颜色函数的参数，用一个函数来改变每个词的颜色，在这里我们直接使用上面深色的AI图片颜色来控制。

```
from wordcloud import WordCloud
from wordcloud import ImageColorGenerator
fontpath='SourceHanSansCN-Regular.otf'

import numpy as np
from PIL import Image
aimask=np.array(Image.open("ai-mask.png"))

genclr=ImageColorGenerator(aimask)

wc = WordCloud(font_path=fontpath,  # 设置字体
               background_color="white",  # 背景颜色
               max_words=1000,  # 词云显示的最大词数
               max_font_size=100,  # 字体最大值
               min_font_size=5, #字体最小值
               random_state=42, #随机数
               collocations=False, #避免重复单词
               mask=aimask, #造型遮盖
               color_func=genclr,
               width=1600,height=1200,margin=2, #图像宽高，字间距，需要配合下面的plt.figure(dpi=xx)放缩才有效
              )
wc.generate(cuted)    
```
在上面，我们引入了`from wordcloud import ImageColorGenerator`方法，它是直接用来生成一个`color_func`颜色函数的，它括号里需要一个nd-array多维数组的图像，恰好我们上面的aimask就是这个格式，直接用就可以。

重新运行得到最开始看到的图，
和原图对比，就能看到文字颜色的规律了：
![image.png](imgs/4324074-a68d584b9c31aa9d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

如果需要使用单色或根据单词变色，可以使用下面的函数。注意它括号内的参数和返回的颜色格式（下面是直接返回黑色）：
```
def genclr2(word, font_size, position, orientation, random_state=None,**kwargs):
    clr='hsl(0, 0%, 0%)'
    return clr
```

## 汇总
1. 读取文件
1. jieba分词
1. 利用re正则表达式选出英文单词
1. 生成词云对象，利用图片遮罩形状和改变颜色
1. 使用Matplotlib来显示图片

完整代码如下：
```
#cell-1
text=''
with open('./lagou-job1000-ai-details.txt','r') as f:
    text=f.read()
    f.close()
print(text[:100])

#cell-2
import jieba
words = jieba.lcut(text)
import re
pattern = re.compile(r'^[a-zA-Z0-1]+$')
words = [w for w in words if pattern.match(w)]
cuted = ' '.join(words)
print(cuted[:500])

#cell-3
from wordcloud import WordCloud
from wordcloud import ImageColorGenerator
fontpath='SourceHanSansCN-Regular.otf'

import numpy as np
from PIL import Image
aimask=np.array(Image.open("ai-mask.png"))

genclr=ImageColorGenerator(aimask)

wc = WordCloud(font_path=fontpath,  # 设置字体
               background_color="white",  # 背景颜色
               max_words=1000,  # 词云显示的最大词数
               max_font_size=100,  # 字体最大值
               min_font_size=5, #字体最小值
               random_state=42, #随机数
               collocations=False, #避免重复单词
               mask=aimask, #造型遮盖
               color_func=genclr,
               width=1600,height=1200,margin=2, #图像宽高，字间距，需要配合下面的plt.figure(dpi=xx)放缩才有效
              )
wc.generate(cuted)  

#cell-4
import matplotlib.pyplot as plt
plt.figure(dpi=150) #通过这里可以放大或缩小
plt.imshow(wc, interpolation='catrom',vmax=1000)
plt.axis("off") #隐藏坐标
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