### 版本说明
Python 3.0在设计的时候没有考虑向较早版本相容
Python 2.6作为一个过渡版本，基本使用了Python 2.x的语法和库，同时考虑了向Python 3.0的迁移，允许使用部分Python 3.0的语法与函数。
除非为了使用旧的Python2.x项目代码或只支持2.x的第三方库，否则不推荐使用2.x进行编程

### 死人的print函数
Python 2.6与Python 2.7里面，以下三种形式是等价的：
```
print "fish"
print ("fish") #注意print后面有个空格
print("fish") #print()不能带有任何其它参数
```
但python3.x只能使用后两者，print语句被python3废弃，只能使用print函数

### Unicode
Python3中字符串是Unicode (utf-8)编码，支持中文做标识符。
python2中是ASCII编码，需要更改字符集才能正常支持中文，所以在.py文件中会看到#-*- coding: UTF-8 -*-。
```
#python3中
>>> 中国 = 'china' 
>>>print(中国) 
china

#python2中
>>> str = "我爱北京天安门"
>>> str
'\xe6\x88\x91\xe7\x88\xb1\xe5\x8c\x97\xe4\xba\xac\xe5\xa4\xa9\xe5\xae\x89\xe9\x97\xa8'
>>> str = u"我爱北京天安门"
>>> str
u'\u6211\u7231\u5317\u4eac\u5929\u5b89\u95e8'
```

### 除法运算
单斜杠/,Python2中整数相除得整数，浮点小数相除得浮点；Python3中结果总是浮点数。
```
#python3
>>print(10/5)
2.0
```
双斜杠//,Python2和3相同，都是除法结果去掉小数部分
```
>>print(10//3)
3
```

### 异常处理
Python2中try:...except ERR,e:...，在Python3中改为了try:...except ERR as e:...
```
#Python3
try:
    open('a.txt','r')
except Exception as e:
    print(e) #这里也不要使用e.message
```
python 2中触发异常可以用raise IOError, "file error"或raise IOError("file error")两种方式。
python 3中触发异常只能用raise IOError("file error")。
异常StandardError 被Python3废弃，统一使用Exception

### xrange和range
Python3中不再使用xrange方法，只有range方法
range在Python2中返回列表，而在Python3中返回range可迭代对象
```
a=range(10)
print(a)
print(list(a))
```
输出
```
range(0, 10)
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
```

### 八进制字面量
Python3中只能使用0o...格式，对于01000格式将抛出错误,而在Python2中两种都能使用
```
>>> 01000
  File "<stdin>", line 1
    01000
        ^
SyntaxError: invalid token
>>> 0o1000
512
```

### 不等运算符
在Python2中有两个不等运算符!=和<>，在Python3中去掉了<>，只有!=符号表示不等。

### repr
在Python2中双反引号``可以替代repr函数，在Python3中去掉了双反引号的表是方法，只能用repr方法

### 模块改名
StringIO模块现在被合并到新的io模组内。 new, md5, gopherlib等模块被删除。 
httplib, BaseHTTPServer, CGIHTTPServer, SimpleHTTPServer, Cookie, cookielib被合并到http包内。
取消了exec语句，只剩下exec()函数。 

### long类型
在Python2中long是比int取值范围更大的整数，Python3中取消了long类型，int的取值范围扩大到之前的long类型范围

### bytes类型
Python3新增了bytes类型,使用b开头的字符串定义：
```
>>> b = b'china' 
>>> type(b) 
<type 'bytes'> 
```
str对象和bytes对象可以使用.encode() (str -> bytes) or .decode() (bytes -> str)方法相互转化。
```
>>> s = b.decode() 
>>> s 
'china' 
>>> b1 = s.encode() 
>>> b1 
b'china' 
```

### dict类型
Python3中dict的.keys()、.items 和.values()方法返回迭代器，而之前的iterkeys()等函数都被废弃。
同时去掉的还有 dict.has_key()，可以用in来代替。
```
di={
    'a':1,
    'b':2,
    'c':3
}
for item in d.items():
    print(item)
print('c' in di)

```
输出
```
('gggg', {'a1': 1})
('b', 12)
True
```

### next()函数和.next()方法
my_generator = (letter for letter in 'abcdefg')
python 2中可以用  next(my_generator) 和 my_generator.next() 两种方式。
python 3中只能用 next(my_generator)这种方式。

### 列表推导
不再支持`[n for n in a,b]`语法，改为`[n for n in (a,b)]`或`[n for n in [a,b]]`
```
a=1
b=2
c=[n for n in [a,b]]
print(c)
```
输出[1,2]

### input
python 2 中通过input 输入的类型是 int，只有通过 raw_input()输入的类型才是str.
python 3中通过input输入的类型都是是str，去掉了row_input()方法。

### 比较符
Python 2 中任意两个对象都可以比较，`11 < 'test'`返回True
Python 3中只有同一数据类型的对象可以比较，`11 < 'test'`报错，需要调用正则判断，改为`import re;11 < int('test') if re.compile('^[0-9]+$').match('test') else 0`否则就报错

### 其他
exec语句被python3废弃，统一使用exec函数

execfile语句被Python3废弃，推荐使用exec(open("./filename").read())

Python3中这些方法不再返回list对象：dictionary关联的keys()、values()、items()，zip()，map()，filter()，但是可以通过list强行转换

迭代器iterator的next()函数被Python3废弃，统一使用next(iterator)

file函数被Python3废弃，统一使用open来处理文件，可以通过io.IOBase检查文件类型

apply函数被Python3废弃

更多内容请你在实践中慢慢体会。
