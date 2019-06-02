[智能决策上手系列教程索引](https://www.jianshu.com/p/0d2e46e69f58)
---

前面三篇文章介绍了如何利用Headers模拟浏览器请求，如何嵌套For循环抓取二级页面。但针对的都是Html文件数据，这一篇我们来看一下另外一种情况的数据以及更加复杂的Headers模拟。

案例是拉勾网（一个招聘网站）抓取某个公司全部招聘信息，然后分析中大型人工智能公司的人才需求分布情况。

这次我们使用Anaconda的Jupyter Notebook。

[Anaconda安装教程](https://www.jianshu.com/p/471763354ebc)


## 1. 理解页面

打开[这个页面](https://www.lagou.com/gongsi/j94.html),这是思必驰科技（一家专注于人工智能语音技术的科技公司）在拉勾网的全部招聘职位列表。

![思必驰招聘职位](imgs/4324074-622f16166af29495.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

我们可以看到共有47个招聘职位。但是，如果我们【右击-查看网页源代码】，然后【Ctrl+F】搜索第一个职位的名称“运维技术专家”却什么也搜不到，实际上整个页面只有600行左右，并没有包含任何职位信息。

**数据不在请求的Html文件里面，数据在哪？**

这几年的网站很多都采用了类似游戏的模式：你打开游戏软件的时候，本机电脑里面没有任何玩家信息，但是游戏软件启动后会向服务器请求数据（而不是Html文件），拿到这些数据之后，游戏软件就把各种在线玩家数据显示在屏幕上，让你能够看到他们。

换成网页就是：你刚打开网页的时候，请求的Html文件没有数据，但是网页在浏览器运行之后，网页自己就会向服务器请求数据，网页拿到数据之后，它就会把各种数据填充到页面上，你就看到了这些数据，——但这些数据并不是像以前那样直接写在html文件里的。

![动态填充数据页面流程](imgs/4324074-6bc9881ca058cf06.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

这些能够动态请求数据和填充数据的代码就是Html网页内运行的JavaScript脚本代码，它们可以做各种事情，尤其善于玩弄数据。

JS（JavaScript）从服务器获取的数据大多是json格式的，类似下面这种对象（Python里面也叫dict字典），也有xml格式的，这里暂时用不到就不介绍了。

```
data={
  'title':'内容标题',
  'text':'文字内容'
}
```

这个格式看上去比html一堆尖括号标记看上去舒服多了。但如何拿到这个数据呢？

## 2. 理解数据请求Request

我们知道Elements面板显示了所有标记元素，而Network面板显示了所有浏览器发出的请求Request，既然JS是向服务器发出请求的，那么就一定会在Network面板留下痕迹。

还是[刚才的页面](https://www.lagou.com/gongsi/j94.html),【右键-检查】切换到Network面板，点击红色小按钮清空，然后点击上面的第2页按钮，查看Network里面的变化。
![Network查看JS的xhr请求](imgs/4324074-d88db0ce0d539e1e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

我们注意到`searchPosition.json`这行，它的类型（Type）是`xhr`，数据请求都是这个类型的。

点击`searchPosition.json`可以看到这个请求的详细信息。
![Headers详细信息](imgs/4324074-e02c41f27092ca07.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
和之前的稍有不同，它没有Parameters数据（因为地址栏没有`?aaa=xxx&bbb=yyy`这类结尾了），但是多了`Form Data`表单数据，其实和Parameters作用相同，就是向服务器说明你要哪个公司(`companyId`)的数据、第几页（`pageNo`）、每页多少个职位（`pageSize`）等等。

再点击上面的【preview】预览，可以看到这个请求实际获得了什么数据：
![数据结构预览](imgs/4324074-1a227d19f6a98014.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

如图，小三角一路点下去，就能看到这个数据实际和页面展示的职位列表是一一对应的。所以我们只要拿到这个数据就OK了！

## 3. 发送数据请求

上面看到，我们需要的数据都在`searchPosition.json`这个Request请求里面，【右键-Copy-Copy link address】复制请求地址。

![复制请求地址](imgs/4324074-7e97fd1ba66d7c42.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

打开Notebook，新建Python 3文件，粘贴过去。
```
#单元1
url='https://www.lagou.com/gongsi/searchPosition.json'
```
向这个地址发送请求：
```
#单元2
import requests
jsonData=requests.get(url)
print(jsonData.text)
```
全部运行后得到下图结果，我们的爬虫请求被服务器识别了！
![直接发起数据请求失败](imgs/4324074-93f5b50ca5e8a799.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

>并不是所有数据请求都会被识别，拉勾网服务器做了这方面的检测，有些网站就没有检测机制，可以直接获取有效数据。

回顾上面截图的浏览器Request请求的Headers信息，实际上浏览器发送请求的时候还携带了很多Request headers(包含Cookie），以及Form data数据（对应我们以前提到过的Parameters信息）。

## 4. 添加params和headers

`params`就是`Form Data`，从浏览器的`Network`面板直接手工复制，然后修改成为Python的字典对象（就是大括号包含的一些属性数据），注意都要加上引号，每行结尾有逗号。
`header`可以用右键`searchPosition.json`然后【Copy-Copy Request headers】复制到，但是注意这个字符很多而且换行，所以要用三个单引号才能包括起来。
>注意！这里我删除了其中一行`Content-Length: 86`,因为在发送Request请求的时候Python会自动计算生成`Content-Length`数值（不一定是86）。如果这里不删除就会导致重复引发错误。

修改单元1的代码：
```
#单元1
url='https://www.lagou.com/gongsi/searchPosition.json'
params={
    'companyId': '94',
    'positionFirstType': '全部',
    'schoolJob': 'false',
    'pageNo': '2',
    'pageSize': '10'
}
headers='''
POST /gongsi/searchPosition.json HTTP/1.1
Host: www.lagou.com
Connection: keep-alive
Origin: https://www.lagou.com
X-Anit-Forge-Code: 38405859
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
Accept: application/json, text/javascript, */*; q=0.01
X-Requested-With: XMLHttpRequest
X-Anit-Forge-Token: fcd0cae2-af8a-44b7-ae08-6cc103677fc1
Referer: https://www.lagou.com/gongsi/j94.html
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7
Cookie: JSESSIONID=ABAAABAAAGFRGDA8929AE8AEDDF675B0A416152D50F1155; user_trace_token=20180914214240-a4f27a86-ee75-49d4-a447-7d7ec6386510; _ga=GA1.2.764376373.1536932562; LGUID=20180914214241-0d64224c-b824-11e8-b93f-6544005c3644; WEBTJ-ID=20180917170602-165e6c78d78209-0f57b51c336360b-3461790f-1296000-165e6c78d7953; __utmc=14951595; __utmz=14951595.1537175176.1.1.utmcsr=m_cf_cpt_sogou_pc|utmccn=(not%20set)|utmcmd=(not%20set); X_HTTP_TOKEN=b53ce1f559f492d4aa675d08aaffa8d93; _putrc=67FE3A6CCEBE7074123F83D1B170EADC; login=true; hasDeliver=0; index_location_city=%E5%85%A8%E5%9B%BD; unick=%E6%8B%89%E5%8B%BE%E7%94%A8%E6%88%B75537; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf677e6=1536922564,1537493466; TG-TRACK-CODE=hpage_code; _gid=GA1.2.969240417.1537831173; gate_login_token=2b25e668e5c44f984fa699aa1142cccd6a9c3d914111e874bf297af1b325c383; __utma=14951595.764376373.1536932562.1537589263.1537831174.12; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1537831174; LGRID=20180925071933-4b7c4ce8-c3330-11e8-bb1c-5254005c3644
'''
```
>注意，不要直接复制使用上面的headers代码，其中的信息涉及到我的个人隐私，所以都被修改过了，不能正常使用。必须自己复制你的浏览器里面`searchPosition.json`的真实`Request Headers`

## 5. 把headers转化为字典对象

headers是一长串字符，不符合Python要使用的字典对象格式`{'key':'value'}`的格式，我们必须转化它一下。

你可以像处理`params`那样手工加引号加逗号，也可以使用下面这个代码实现自动转化，有兴趣的话可以参考代码里的注释理解，或者不管什么意思直接使用也行。

```
#单元1.5
def str2obj(s,s1=';',s2='='):
    li=s.split(s1)
    res={}
    for kv in li:
        li2=kv.split(s2)
        if len(li2)>1:
            res[li2[0]]=li2[1]
    return res
headers=str2obj(headers,'\n',': ')
print(headers)
```

把这个放在紧跟单元1后面，然后全部运行，可以看到输出的结果大致如下：
![转化后的header](imgs/4324074-727b91027fa27107.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

## 6. 重新发送请求
这次我们模拟浏览器，携带我们复制来的Headers和Form Data数据重新发送请求，查看输出结果：
```
#单元2
import requests
jsonData=requests.get(url,params=params,headers=headers)
print(jsonData.text)
```

我们运行全部代码，可以看到正常输出的结果数据：
![获取数据成功](imgs/4324074-2f915db3c3e8047a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

## 7. 解析json数据

`json`数据格式其实和我们一直用的字典对象几乎是一样的，类似这样：
```
zidian={
  'a':'1',
  'b':{
    'b1':'2-1',
    'b2':'2-2'
  }
}
```
**json数据和字典对象都是可以一层层嵌套的（上面b1就是嵌套在b对象里面的）。如果我们要获取b2的值就可以`print(zidian['b']['b2'])`，它会输出`'2-1'`**

我们可以用下面的代码把刚才Request获得的很多json数据整齐的显示出来：
```
import json
import requests
jsonData=requests.get(url,params=params,headers=headers)
data=json.loads(jsonData.text)
print(json.dumps(data,indent=2,ensure_ascii=False))
```
这里我们import引入了json功能模块，然后使用`data=json.loads(jsonData.text)`的`loads`方法把Request获得的字符串数据转换为正式的json对象格式，`dumps`方法就是把json对象再变为字符串输出。是的，loads和dumps是相反的功能，但是我们的dumps加了`indent=2,ensure_ascii=False`就能让输出的字符串显示的很整齐了，如下图：
![整齐显示的json对象](imgs/4324074-1a219af04a3649ee.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

这样，我们就可以从图中的层级一层层找到需要的数据信息了，比如`data['content']['data']['page']['result']`就是我们需要的职位的列表对象，我们可以用for循环输出这个列表的每一项：
```
import json
import requests
jsonData=requests.get(url,params=params,headers=headers)
data=json.loads(jsonData.text)
#print(json.dumps(data,indent=2,ensure_ascii=False))
jobs=data['content']['data']['page']['result']
for job in jobs:
    print(job['positionName'])
```
得到的结果是：
![输出职位名称](imgs/4324074-2c052b1b3befc0e0.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

## 8. 输出数据到Excel

我们只要针对每个job进行详细的处理，就可以输出更多内容了：
```
import json
import requests
import time

hud=['职位','薪酬','学历','经验']
print('\t'.join(hud))
for i in range(1,6):
    params['pageNo']=i
    jsonData=requests.get(url,params=params,headers=headers)
    data=json.loads(jsonData.text)
    jobs=data['content']['data']['page']['result']
    for job in jobs:
        jobli=[]
        jobli.append(job['positionName'])
        jobli.append(job['salary'])
        jobli.append(job['education'])
        jobli.append(job['workYear'])
        print('\t'.join(jobli))
    time.sleep(1)   
```
从浏览器可以看到总共有47个职位，每页10个共5页，所以这里都抓取了：
![最终输出数据](imgs/4324074-b487d21934b44b9e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

直接鼠标选中，然后复制，打开Excel表格新建，选择足够大区域，右键，选择性粘贴，选择Unicode，就能得到数据表格了。

## 10. 抓取二级职位详情页面

最后附上抓取职位详情页面的代码，综合了我们这几节前面使用的很多内容，仅供参考和理解：
```
#cell-1
url='https://www.lagou.com/gongsi/searchPosition.json'
params={
    'companyId': '94',
    'positionFirstType': '全部',
    'schoolJob': 'true',
    'pageNo': '1',
    'pageSize': '10'
}
headers='''
POST /gongsi/searchPosition.json HTTP/1.1
Host: www.lagou.com
...
LGRID=20180925071933-4b7c4ce8-c050-11e8-bb5c-5254005c3644
'''
jobheaders='''
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
...
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36
'''
```
这里的`jobheader`是给二级页面使用的。你必须复制自己浏览器`https://www.lagou.com/jobs/5151679.html?source=pl&i=pl-6`页面的Request请求`5151679.html?source=pl&i=pl-6`的信息header信息，我这里只是示意，不能直接复制使用。

```
#cell-2
def str2obj(s,s1=';',s2='='):
    li=s.split(s1)
    res={}
    for kv in li:
        li2=kv.split(s2)
        if len(li2)>1:
            res[li2[0]]=li2[1]
    return res
headers=str2obj(headers,'\n',': ')
jobheaders=str2obj(jobheaders,'\n',': ')
```
这里只是最后一行，也转化jobheaders对象。

```
#cell-3
import json
import requests
import time
from bs4 import BeautifulSoup

hud=['页数','职位','薪酬','学历','经验','描述']

def getJobs(compId=94,school='true',pageCount=1):
    for i in range(1,1+pageCount):
        params['pageNo']=str(i)
        params['companyId']=compId
        params['schoolJob']=school
        
        params['pageNo']=i
        jsonData=requests.get(url,params=params,headers=headers)
        data=json.loads(jsonData.text)
        #print(json.dumps(data,indent=2,ensure_ascii=False))
        jobs=data['content']['data']['page']['result']
        
        for job in jobs:
            jobli=[str(i)]
            jobli.append(job['positionName'])
            jobli.append(job['salary'])
            jobli.append(job['education'])
            jobli.append(job['workYear'])
            
            #请求二级详情页面
            pid=job['positionId']
            joburl='https://www.lagou.com/jobs/'+str(pid)+'.html'
            jobhtml=requests.get(joburl,headers=jobheaders)
            jobsoup= BeautifulSoup(jobhtml.text, 'html.parser')
            desc=jobsoup.find('dd','job_bt').div.text  
            desc=desc.replace('\n','')
            jobli.append(desc)
            time.sleep(1) 
            
            print('\t'.join(jobli))
        time.sleep(1) 
```
这里没有直接使用，而是def了一个函数getJobs，带有三个参数compId公司序号，school是否社招，pageCount一共有多少页。

```
#cell-4
print('\t'.join(hud))
getJobs(94,'false',5)
```
启动。

## 本篇小节

* 页面可以不直接包含数据，而是通过运行JavaScript代码，从服务器重新获取数据，再填充到页面上。
* 任何向服务器发起的请求都可以在Network面板找到信息，带了哪些参数params（Form Data)，带了什么样的headers，等等
* json数据和字典对象用起来一样，从Request获取的文本text数据需要用json.load转换一下，然后就可以用shuju['aa']['bb']的方法一层层找到我们需要的信息

---
[智能决策上手系列教程索引](https://www.jianshu.com/p/0d2e46e69f58)
---
###每个人的智能决策新时代
如果您发现文章错误，请不吝留言指正；
如果您觉得有用，请点喜欢；
如果您觉得很有用，欢迎转载~
---
END