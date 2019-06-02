[智能决策上手系列教程索引](https://www.jianshu.com/p/0d2e46e69f58)
---

在上一篇，我们读取了数百条拉勾网关于“人工智能”职位招聘的信息，存储了数百个职位信息文件，这一篇我们提取一些有用的数据放到excel文件进行观察和整理、分析。

[上一篇：网络数据抓取-拉勾网职位列表和详情-requests案例](https://www.jianshu.com/p/c240daad86a2)

### 确定需要提取的数据

>[如果您还没有抓取，请从这里直接下载100个json搁置职位文件](https://pan.baidu.com/s/1_vfiIdIPGzAyBuRx4__BsA)  密码:tfdv

参照上一篇，我们使用下面的代码随便读取并输出一个职位数据文件`xxxxx.json`的数据，注意目录和文件名可能需要调整：
```
#cell-1
import json
def readJob(fileName):
    with open(fileName,'r') as f:
        job=json.load(f)
        print(json.dumps(job,indent=2,ensure_ascii=False))
readJob('./data/lagou_ai/jobs/2363876.json')
```
运行得到一个json对象，开始部分类似：
![image.png](imgs/4324074-303dc10cad6bd20e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

我们只提取以下几个内容：
* 职位编号positionId
* 职位名positionName
* 工作经验workYear
* 学历要求education
* 发布时间createTime
* 薪资salary
* 工作地city
* 公司名companyFullName
* 公司规模companySize
* 公司融资financeStage
* 职位分类firstType
* 职位二级分类secondType
* 职位详情details



### 处理特殊字段

在上面工作经验、薪资、公司规模都是一个范围，这不太方便分析，我们把它拆开，比如薪资“15k-30k”拆分成`salaryLow=15`和`salaryHigh=30`：

```
#cell-0.5
def range2two(s, unit):
    s = s.replace(unit, '')  #去掉单位k、年、人
    s = s.replace(' ', '')  #去掉空格
    l = s.split('-')
    res = {
        'low': str(l[0]), 
        'high': str(l[1]) if len(l) > 1 else 'None'
    }
    print(res)
range2two('12k-20k','k')
range2two('13','k')
```
最后两行是测试，运行输出以下内容表示正常：
![image.png](imgs/4324074-1311e7a520aa4ea8.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

测试成功后整理代码：
```
#cell-0.5
def range2two(s, unit):
    s = s.replace(unit, '')  #去掉单位k、年、人
    s = s.replace(' ', '')  #去掉空格
    l = s.split('-')
    res = {
        'low': str(l[0]), 
        'high': str(l[1]) if len(l) > 1 else 'None'
    }
    return res
```

### 完善readJob函数，返回csv的一行字符串

修改和完善提取数据的代码,把表头分为可以直接读取的labels和需要转化的labels2：
```
#cell-1
import json
labels=['positionId','positionName','workYear','education','createTime','salary','city','companyFullName','companySize','financeStage','firstType','secondType','details']
labels2=['salary_low','salary_high','workYear_low','workYear_high','companySize_low','companySize_high']

def readJob(fileName):
    with open(fileName,'r') as f:
        job=json.load(f)
        line=[]
        for key in labels:
            line.append(str(job[key]).replace(',','，')) #添加所有labels的字段，用中文逗号替换英文逗号，避免分割混乱
            
        salaries=range2two(job['salary'],'k')
        workYears=range2two(job['workYear'],'年')
        companySizes=range2two(job['companySize'],'人')
        line+=[salaries['low'],salaries['high']]
        line+=[workYears['low'],workYears['high']]
        line+=[companySizes['low'],companySizes['high']]
        
        return ','.join(line)
        
test=readJob('./data/lagou_ai/jobs/2363876.json')
print(test)
```
因为.csv文件使用英文逗号分割每个表格单元的，所以如果数据里面有英文逗号就会造成混乱，`.replace(',','，')`可以用中文逗号替换掉英文逗号，避免混乱。
最后两行是测试，注意输出结果应该有6个单独的数字：
![image.png](imgs/4324074-73d3e63287dad3fa.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

### 读取并保存一个职位到csv文件

测试成功后去掉结尾test那两行。
新建一个cell编写存储.csv文件的代码：

```
#cell-3
with open('./data/lagou_ai/jobs.csv', 'w', encoding="gb18030") as f:
    text = ''
    text += ','.join(labels + labels2)

    text += '\n'
    text += readJob('./data/lagou_ai/jobs/2363876.json')
    f.write(text)
    f.close()
    print('>>OK!')
```
这将生成一个`jobs.csv`文件，用excel打开它可以看到有两行内容，注意检查最后几列是否正常：
![image.png](imgs/4324074-c79e86bb2d5d047b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

### 读取全部职位存储到jobs.csv

首先要取得jobs文件夹下所有的文件名，然后循环操作就可以了。

```
#cell-3
import os
files = os.listdir('./data/lagou_ai/jobs/')  #获取所有文件列表
with open('./data/lagou_ai/jobs.csv', 'w', encoding="gb18030") as f:
    text = ''
    text += ','.join(labels + labels2)

    for fname in files:
        if not fname.find('.json')==-1: 
            text += '\n'
            text += readJob('./data/lagou_ai/jobs/' + fname)
    f.write(text)
    f.close()
    print('>>OK!')
```
代码说明：
*  `os.listdir('./data/lagou_ai/jobs/')`得到这个文件夹下所有的文件的列表，甚至包含了隐藏文件。类似`['2178923982.json','237218937.json',...]`
* ` if not fname.find('.json')==-1: `如果不是`xxx.json`格式的文件名就不执行操作，比如对于隐藏文件就不操作。`'123'.find('23')`等于1，左数从0开始，第1位置上就是23，`'123'.find('a')`等于-1，因为根本找不到。

运行上面代码得到一个excel表，包含了数百行职位信息。
![image.png](imgs/4324074-5cdc363eb6a93d33.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

### 清理excel表中错误数据

我们看到其实搜索“人工智能”得到的很多职位和人工智能都不相关，甚至有很多销售、行政类的职位。
我们可以根据firstType和secondType过滤到这些错误数据，把它们直接删除。
点击excel表格列的顶端，然后【开始-排序和筛选】，升序降序任意，弹窗默认【扩展选定区域】，然后确定，相同secondType的就会排在一起，根据需要可以把“销售、运营、推广、行政”等明显有问题的职位删除掉，得到比较有效的内容。
![image.png](imgs/4324074-c3ba87a499dc17ce.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
>如果只想保留secondaType是“人工智能”的职位，可以把它们一起复制剪切出来另存一个.csv表格。
如果你想用代码直接实现也可以，需要增加`if job['secondtype']=='人工智能':`，具体请自己试试看~

### 回顾总结
总体代码(主义文件夹路径)：
```

# coding: utf-8

# ### 读取一个文件

# In[16]:


def range2two(s, unit):
    s = s.replace(unit, '')  #去掉单位k、年、人
    s = s.replace(' ', '')  #去掉空格
    l = s.split('-')
    res = {
        'low': str(l[0]), 
        'high': str(l[1]) if len(l) > 1 else 'None'
    }
    return res


# In[25]:


import json
labels = [
    'positionId', 'positionName', 'workYear', 'education', 'createTime',
    'salary', 'city', 'companyFullName', 'companySize', 'financeStage',
    'firstType', 'secondType', 'details'
]
labels2 = [
    'salary_low', 'salary_high', 'workYear_low', 'workYear_high',
    'companySize_low', 'companySize_high'
]


def readJob(fileName):
    with open(fileName, 'r') as f:
        job = json.load(f)
        line = []
        for key in labels:
            line.append(str(job[key]).replace(',','，'))  #添加所有labels的字段，用中文逗号替换英文逗号，避免分割混乱

        salaries = range2two(job['salary'], 'k')
        workYears = range2two(job['workYear'], '年')
        companySizes = range2two(job['companySize'], '人')
        line += [salaries['low'], salaries['high']]
        line += [workYears['low'], workYears['high']]
        line += [companySizes['low'], companySizes['high']]

        return ','.join(line)


# In[37]:


import os
files = os.listdir('./data/lagou_ai/jobs/')  #获取所有文件列表
with open('./data/lagou_ai/jobs.csv', 'w', encoding="gb18030") as f:
    text = ''
    text += ','.join(labels + labels2)

    for fname in files:
        if not fname.find('.json')==-1: 
            text += '\n'
            text += readJob('./data/lagou_ai/jobs/' + fname)
    f.write(text)
    f.close()
    print('>>OK!')
```

总结：
* 首先确定哪些数据需要提取
* 如果有特殊字段需要单独处理一下
* cvs是英文逗号和换行符分割组成的
* 要得到全部文件列表然后循环执行操作



---
[智能决策上手系列教程索引](https://www.jianshu.com/p/0d2e46e69f58)
---
###每个人的智能决策新时代
如果您发现文章错误，请不吝留言指正；
如果您觉得有用，请点喜欢；
如果您觉得很有用，欢迎转载~
---
END