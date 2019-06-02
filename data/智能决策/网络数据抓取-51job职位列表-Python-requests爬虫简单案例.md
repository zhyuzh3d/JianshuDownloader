[智能决策上手系列教程索引](https://www.jianshu.com/p/0d2e46e69f58)
---


这是一个简单的单页面数据抓取案例，但也有些值得注意的坑。这里快速解释一下代码。

抓取的是51job网站，搜索“人工智能”然后得到的招聘职位基本信息，职位名、公司名、薪资等等。
![image.png](imgs/4324074-baf7d44c0cca3652.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

数据直接就在【右键-查看源代码】的网页源代码里，也可以【右键-检查】从Elements元素面板看到：

![image.png](imgs/4324074-895b0b051b493857.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

我们注意到职位列表都在`class='dw_table'`的元素下面，但是第一个`class='el title'`的是表头，不应该包含，虽然它下面也有`t1,t2,t3`但是它的`class='t1'`是个`<span>`，而正常的职位的`t1`是个`<p>`

下面是主要代码：
```
from bs4 import BeautifulSoup
import requests
import time
headers = {
    'User-Agent': 'Mozilla/5.0'
}
url='https://search.51job.com/list/070300,000000,0000,00,9,99,%25E4%25BA%25BA%25E5%25B7%25A5%25E6%2599%25BA%25E8%2583%25BD,2,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='
html= requests.get(url,headers=headers)
html=html.text.encode('ISO-8859-1').decode('gbk') ##注意这个坑！
soup=BeautifulSoup(html, 'html.parser')

for item in soup.find('div','dw_table').find_all('div','el'):
    shuchu=[]
    if item.find('p','t1'):
        title=item.find('p','t1').find('a')['title']            
        company=item.find('span','t2').string   #爬公司名称
        address=item.find('span','t3').string   #爬地址
        xinzi = item.find('span', 't4').string  #爬薪资
        date=item.find('span','t5').string   #爬日期
        shuchu.append(str(title))

        shuchu.append(str(company))
        shuchu.append(str(address))
        shuchu.append(str(xinzi))
        shuchu.append(str(date))
        print('\t'.join(shuchu))
time.sleep(1)

```

有几个坑需要注意：
* `html=html.text.encode('ISO-8859-1').decode('gbk') `没有这句中文就会乱码。因为如果网页里没有说明自己是什么编码，Requests模块就会把它当做`'uft-8'`编码模式处理，而偏巧51job的网页就没有说明自己的编码格式，那就会使用网页默认的`'ISO-8859-1'`编码，这就矛盾了，所以要强制重新编码`encode`然后再解码`decode`，这里使用`gbk`确保中文正常显示。
* 上面代码用` if item.find('p','t1'):`排除掉了第一行表头,参照上面的网页截图。
* `shuchu.append(str(title))`这里都加了`str(...)`是防止有些时候公司名、薪资、地址可能有空的，空的计算机会认为是`None`，我们用`str(None)`就是`'None'`,变成了一个字符串，不再是空了。因为后面的`'\t'.join(shuchu)`中`shuchu`列表里面如果有空就会出错。


最终输出的结果大致是：
![image.png](imgs/4324074-8604332a351787ee.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

---
[智能决策上手系列教程索引](https://www.jianshu.com/p/0d2e46e69f58)
---
###每个人的智能决策新时代
如果您发现文章错误，请不吝留言指正；
如果您觉得有用，请点喜欢；
如果您觉得很有用，欢迎转载~
---
END
