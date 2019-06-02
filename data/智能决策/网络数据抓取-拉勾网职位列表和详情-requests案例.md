[智能决策上手系列教程索引](https://www.jianshu.com/p/0d2e46e69f58)
---

这次我们来比较完整的抓取拉勾网上面“人工智能”相关招聘信息以及招聘要求详情。

### 分析页面，寻找数据来源

打开拉勾网，搜索“人工智能”得到下面这个页面。
共30页，每页展示15个职位，应该最多共计450个职位,但不知道为什么页面上写[职位(500+)]。

![image.png](imgs/4324074-55e9a1802e52ba39.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

【右键-查看网页源代码】，然后【Ctrl+F】搜索任意一个职位中比较独特的单词，比如“骏嘉财通”，搜不到，这说明数据肯定不在html源代码里面。

![image.png](imgs/4324074-9d946875c4742f47.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

只能从网络面板中查找了，【右键-检查元素】，切换到【Networks】面板。为了清晰一些，我们先点清除，然后点底部的页面分页按钮【2】，得到如下图情况，注意type类型为xhr的两个请求，它们很可能包含我们所需要的数据：
![image.png](imgs/4324074-2195fbc1118ab856.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

点击请求查看详细，如下图，在预览【preview】面板中看到，`positionAjax.json?needAddtionalResult=false`就是我们需要的请求。

![image.png](imgs/4324074-01c5780c0769991e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

如上图，职位列表数据存在于这个请求结果的`.content.positionResult.result`下面。

### 设置参数，复制url、header和params

点击请求可以直接【右键-Copy-Copy ...】复制到链接地址`link address`，复制到请求头`request headers`。
在右侧Headers面板底部有【FormData】可以看到params的列表，其中`first`看不出意思，`pn`应该就是页数，大概是page number的意思，`kd`不知什么意思，但肯定就是我们的搜索词。

![image.png](imgs/4324074-ea8be1cbcf8f94d7.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

按照以前我们的方法，在Notebook中新建Python 3文件，复制粘贴两个cell单元，代码如下（headers需要替换成你自己复制的内容）。
>注意一定要去掉`Content-Length: ...`一行

```
#cell-1
url = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false'
params = {
    'first': 'false',
    'pn': '2',
    'kd': '人工智能',
}
headers='''
POST /jobs/positionAjax.json?needAddtionalResult=false HTTP/1.1
Host: www.lagou.com
Connection: keep-alive
Origin: https://www.lagou.com
X-Anit-Forge-Code: 0
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
Accept: application/json, text/javascript, */*; q=0.01
X-Requested-With: XMLHttpRequest
X-Anit-Forge-Token: None
Referer: https://www.lagou.com/jobs/list_%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD?labelWords=&fromSearch=true&suginput=
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7
Cookie: JSESSIONID=ABAAABAAAGFA......f756e6=1538875676
'''
```

```
#cell-2 转换headers为字典
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

### 发起请求，获取职位信息列表

先测试一个页面，只获取职位标题：
```
#cell-3
import requests
import pandas as pd

jsonData = requests.get(url, params=params, headers=headers)
data = pd.read_json(jsonData.text, typ='series')

jobs = data['content']['positionResult']['result']
print(json.dumps(jobs[0], indent=2, ensure_ascii=False))
```
代码的一些说明：
* 这次我们没有使用`import json`模块，而是使用了更为强大的`pandas`模块，它是最常用的数据处理模块之一。
* 这里的`jobs = data['content']['positionResult']['result']`请参照上面Network面板请求的preview预览对照。
* `json.dumps(jobs[0], indent=2,ensure_ascii=False)`中`jobs[0]`是指职位列表的第一个，`json.dumps(...)`是把它按正常格式显示出来，否则直接`print(jobs[0])`也可以，但就会混乱不换行。

运行全部代码，正常应该输出第二页第一个职位的全部信息:
![image.png](imgs/4324074-c7aeec0510c96e36.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


这样我们就可以知道:
* `jobs[0]['positionId']`就是职位索引，是唯一性的数字
* `jobs[0]['positionName']`就是职位名
* `jobs[0]['workYear']`就是要求工作经验
* `jobs[0]['education']`就是要求学历
* `jobs[0]['city']`就是工作地点
* `jobs[0]['salary']`就是薪资
* `jobs[0]['companyFullName']`就是公司名（图中未显示到）
* `jobs[0]['industryField']`就是公司行业，“金融”
* `jobs[0]['companySize']`就是公司员工数量
* `jobs[0]['firstType']`就是这个职位的类别，“产品|需求|项目类”，（图中未显示到）
* `jobs[0]['secondType']`就是这个职位的二级分类，“数据分析”，（图中未显示到）
* ...


###存储数据，把每个职位信息存为单独文件

因为数据很多，我们也说不准以后会用到哪个，所以我们把每个`job`都存储为一个文件，以后只要读取就可以了，避免因为少存了数据还要重新抓取的麻烦。

改进上面的cell-3代码（为确保可以运行，必须在Notebook代码文件所在文件夹下创建data文件夹，进入data文件夹依次创建lagou_ai文件夹、jobs文件夹，否则会报错）:
```
#cell-3
import json
import requests

jsonData = requests.get(url, params=params, headers=headers)
json.loads(jsonData.text)
jobs = data['content']['positionResult']['result']
for job in jobs:
    fname='./data/lagou_ai/jobs/'+str(job['positionId'])+'.json'   
    with open(fname,'w') as f:
        f.write(json.dumps(job))
        f.close()
```
代码说明：
* 这个代码将自动存储15个`.json`文件在`./data/lagou_ai/jobs/`文件夹下。
* 这次没有使用`pandas`模块，仍然使用了`json`模块，因为`pandas`不方便把json变为可以写入文件的字符串，而`json.dumps(...)`就很好用。
* `fname='./data/lagou_ai/jobs/'+str(job['positionId'])+'.json' `，这是利用每个职位索引`positionId`都是唯一不重复的特性，创建不重复的文件名。

完整运行代码，可以在`./data/lagou_ai/jobs/`文件夹下生成15个数字文件名的文件，你可以尝试用下面的代码打开其中一个，试试看`pandas`是否可以正常使用这些数据，注意这里的`file:`后面内容应该是完整路径（苹果系统的Command+Alt+C）：
```
import pandas as pd
data = pd.read_json('file:/Users/zhyuzh/Desktop/Jupyter/spiders/data/lagou_ai/jobs/3128720.json', typ='series')
print(data['positionName'])
```

### 读取二层页面，获取单个职位要求的详情

在网页里面点击任意一个职位进入查看详情，例如`https://www.lagou.com/jobs/4263258.html`：
![image.png](imgs/4324074-25be7c5ff904ff32.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

参照我们最开始的方法可以发现，我们需要的信息就在右键html网页源代码里面，就在一个`class='job_bt'`的dd标签里面：
![image.png](imgs/4324074-bf53dbb1ca4bbe54.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

我们需要使用`beautifulsoup`来处理html内容：
```
#cell-2.5
from bs4 import BeautifulSoup
def readJobDetails(pid):
    html = requests.get('https://www.lagou.com/jobs/'+str(pid)+'.html', headers=headers)
    soup = BeautifulSoup(html.text, 'html.parser')
    res=soup.find('dd','job_bt').text.replace('\n','')
    return res

print(readJobDetails(4263258))    
```
这里`.text.replace('\n','')`去掉了回车换行，最后一行`print(readJobDetails(4263258)) `执行了测试，成功了就可以把它删除。
成功的话会输出一大堆字符串，和上面html代码截图差不多。

### 完善代码，读取更多职位列表页面

我们来把代码整合一下，刚才我们只读取过一页15个职位基本信息，或者单个职位的详细信息，我们把它整合到一起，最终代码如下(注意替换`headers`并去除`content-length`)：
```

# coding: utf-8

# ## 拉钩搜索‘人工智能’职位列表，包含二级页面详情

# ### 设置

# In[1]:


url = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false'
params = {
    'first': 'false',
    'pn': '1',
    'kd': '人工智能',
}
savePath='./data/lagou_ai'
headers='''
!!!必须替换POST /jobs/positionAjax.json?needAddtionalResult=false HTTP/1.1
Host: www.lagou.com
Connection: keep-alive
Origin: https://www.lagou.com
X-Anit-Forge-Code: 0
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
Accept: application/json, text/javascript, */*; q=0.01
X-Requested-With: XMLHttpRequest
X-Anit-Forge-Token: None
Referer: https://www.lagou.com/jobs/list_%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD?labelWords=&fromSearch=true&suginput=
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7
Cookie: JSESSIONID=ABAAABA...538875676
'''


# In[2]:


#转换headers为字典
def str2obj(s, s1=';', s2='='):
    li = s.split(s1)
    res = {}
    for kv in li:
        li2 = kv.split(s2)
        if len(li2) > 1:
            res[li2[0]] = li2[1]
    return res


headers = str2obj(headers, '\n', ': ')


# ### 读取单个职位详情的函数

# In[3]:


from bs4 import BeautifulSoup


def readJobDetails(pid):
    html = requests.get(
        'https://www.lagou.com/jobs/' + str(pid) + '.html', headers=headers)
    soup = BeautifulSoup(html.text, 'html.parser')
    res = soup.find('dd', 'job_bt').text.replace('\n', '')
    return res


# ### 发起请求

# In[4]:


import json
import requests
import time

for n in range(1, 30):
    params['pn'] = n
    jsonData = requests.get(url, params=params, headers=headers)
    data = json.loads(jsonData.text)
    jobs = data['content']['positionResult']['result']
    for job in jobs:
        pid = str(job['positionId'])
        fname = savePath + '/jobs/' + pid + '.json'
        job['details'] = readJobDetails(job['positionId'])
        with open(fname, 'w') as f:
            f.write(json.dumps(job))
            f.close()
        print('>Got job:', pid)
        time.sleep(1)
    time.sleep(1)
print('>Finished!')
```
代码的几个说明：
* 顶部`params`的`pn`恢复为1，之前我们一直使用的是2...
* 将存储文件的目录放到开始`savePath`设置，方便以后修改
* `def readJobDetails...`必须要放在`for n in range...`前面，先`def`然后才能使用。
* 因为过程超过400秒也就是有八九分钟，所以用`print('>Got job:', pid)`只是让过程能够有点反应，看上去不像死机。
* 每读取一页列表，`time.sleep(1)`休息1秒，每读取一个详情页面也要`time.sleep(1)`休息一秒。这样比较低调不容易被封禁。

运行整个代码，可以在`./data/lagou_ai/jobs`下生成450个`xxxxxxx.json`文件,你可以在资源管理器(win)或者访达(mac)中查看文件一个个变多以确保程序顺路进行中。

最后别忘了测试一下存储的数据是否正确：
```
import pandas as pd
data = pd.read_json('file:/Users/zhyuzh/Desktop/Jupyter/spiders/data/lagou_ai/jobs/5177921.json', typ='series')
print(data['positionName'])
print(data['details'])
```


### 总结

* 先分析页面，知道数据从哪里来、什么格式？（网页源代码html?Network面板的xhr请求到的json数据?)
* 然后找到对应的headers和params(如果有的话，详情页就没有)
* 根据数据来源格式确定使用BeautifulSoup还是json模块来解析，具体解析方法要多看教程多查资料多学习
* 发起Request请求get数据，然后解析到我们需要的内容
* 利用`def`定义不同的函数处理单独的请求可以让代码更清晰
* 把获取的内容存储到文件(简单横竖列表数据存.csv，复杂结构存.json)，注意要转为字符串存储，注意文件名要唯一。
* 尽可能在必要的位置合理的使用`time.sleep(1)`延缓一下
* 代码要一点点测试，如果要`for n in range(1,30)`那就先`for n in range(1,2)`试一下能不能成功。

---
[智能决策上手系列教程索引](https://www.jianshu.com/p/0d2e46e69f58)
---
###每个人的智能决策新时代
如果您发现文章错误，请不吝留言指正；
如果您觉得有用，请点喜欢；
如果您觉得很有用，欢迎转载~
---
END