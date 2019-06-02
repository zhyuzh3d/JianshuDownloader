>[点击这里进入**人工智能嘚吧嘚**目录，观看全部文章](https://www.jianshu.com/p/ff37dbc75edb)
---

##匹配
用来验证字符串的格式。
匹配不通过返回None，通过的话可以用ma.group(0)获得匹配结果。
```
import re
ma = re.compile(r'^[a-z]+$').match('5ha-v44v')  #match对象，不匹配返回None
ma == None #True
```

##搜索
match总是从开头匹配，search没有限制。
```
ma=re.compile(r'[a-z]+').match('5ha-v44v')    # No match
se=re.compile(r'^[a-z]+$').search('5ha-v44v')  #match
se2=re.compile(r'[a-z]+').search('5ha-v44v')  #match

print(ma,se,se2.group(0)) #输出None None ha
```

##提取
findall搜索返回字符串数组，所以也可以用来提取。
```
ma=re.compile(r'[a-z]+').findall('88')    # []
ma2=re.compile(r'[a-z]+').findall('5ha-v44d') #['ha', 'v', 'd']
print(ma,ma2) #输出[] ['ha', 'v', 'd']
```
finditer可以用来返回结果字符串的位置。
```
ma=re.compile(r'[a-z]+').finditer('5ha-v44d') #['ha', 'v', 'd']
for m in ma:
    print(m.start(),m.end(),m.group(0))
```
![](imgs/4324074-0094449e193edbd4.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

##复杂提取
利用\[..]()提取符合匹配的字符串。
利用(.+?)提取被特定字符包裹的字符串。
```
a=re.compile(r'[0-9\.]+').findall('1.3万/月') #['1.3']
b=re.compile(r'3(.+?)月').findall('1.3万/月') #['万/']
print(a,b) #['1.3'] ['万/']
```
(?P<name>)结合groupdict()可以获得单个内容。
```
m = re.match(r"(?P<first_name>\w+) (?P<last_name>\w+)", "Malcolm Reynolds")
m.groupdict() #{'first_name': 'Malcolm', 'last_name': 'Reynolds'}

```
(?<=...)表示只取在...之后位置范围内的。
```
m = re.search('(?<=-)\w+', 'spam-egg')
m.group(0) #'egg'
```


##flag参数
re.I 忽略大小写
re.L 表示特殊字符集 \w, \W, \b, \B, \s, \S 依赖于当前环境
re.M 多行模式
re.S 即为' . '并且包括换行符在内的任意字符（' . '不包括换行符）
re.U 表示特殊字符集 \w, \W, \b, \B, \d, \D, \s, \S 依赖于 Unicode 字符属性数据库
re.X 为了增加可读性，忽略空格和' # '后面的注释

---
>[点击这里进入**人工智能DBD嘚吧嘚**目录，观看全部文章](https://www.jianshu.com/p/ff37dbc75edb)
---
###每个人的智能新时代
如果您发现文章错误，请不吝留言指正；
如果您觉得有用，请点喜欢；
如果您觉得很有用，欢迎转载~
---
END