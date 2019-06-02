[智能决策上手系列教程索引](https://www.jianshu.com/p/0d2e46e69f58)
---
收集一些零散的小技巧备用，不断更新。

###多个字符批量替换

```
import re

def multReplace(text, rpdict):
    rx = re.compile('|'.join(map(re.escape, rpdict)))
    return rx.sub(lambda match:rpdict[match.group(0)], text)
```
它可以批量执行replace的功能。rx是一个竖线分割的**或者**表达式，比如`'a|b|c|d`，这个表达式可以匹配出符合abcd任何一个字母匹配的列表。
`rx.sub()`方法传入了一个`lambda`函数，表示可以对rx匹配列表中的每个匹配都执行一个替换，效果如下：
![](imgs/4324074-05169d8644718f68.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


### 利用二进制位操作加密解密
把语句字符串转为二进制，然后与秘钥单词的二进制进行异或运算得到密文，对密文再用秘钥单词二进制异或还原回去。
```
def enctrypt(text, key):
    text_asc_arr = [ord(t) for t in text]  #将’你好 Python！‘转为ascii码列表[20320, 22909, 32,...]
    key_asc_arr = [ord(t) for t in key]  #将key转为ascii码列表[24,32,1543]
    key_len = len(key_asc_arr)#秘钥单词长度
    for n in range(len(text_asc_arr)):
        k = n % key_len #秘钥单词循环往复使用
        text_asc_arr[n] = text_asc_arr[n] ^ key_asc_arr[k] #异或操作成为[451,223,116,...]
    return ' '.join([bin(t)[2:] for t in text_asc_arr]) #返回字符串拼接格式‘1010101 101011 1100 01...'


def decrypt(text, key):
    asc_str_arr = text.split(' ') #将字符串拆成列表‘1010101 1010...'-->['101010','1010',...]
    text_asc_arr = [int(s, 2) for s in asc_str_arr] #转成ascii列表[451,223,116,...]
    key_asc_arr = [ord(t) for t in key]#转为ascii码列表[24,32,1543]
    key_len = len(key_asc_arr)#秘钥单词长度
    for n in range(len(text_asc_arr)):
        k = n % key_len#秘钥单词循环往复使用
        text_asc_arr[n] = text_asc_arr[n] ^ key_asc_arr[k]#异或操作成为[20320, 22909, 32,...]
    return ''.join([chr(int(t)) for t in text_asc_arr])#返回字符串拼接格式‘你好 Python！'


en = enctrypt('你好 Python！', '我很好')
de = decrypt(e, 'wobuhao')
de2 = decrypt(e, '我很好')
print(en)
print(de)
print(de2)
```
输出结果
```
10110101110001 11011110101 101100101011101 110001001000001 101111111110001 101100100001001 110001001111001 101111111100111 101100100010011 1001110100010000
ⴆښ夿戴徙奨或徐奼鵲
你好 Python！
```

### 序列的比较运算
序列的比较是逐个比较的，即第一个元素大的就大，第一个相等那么第二个大的就大，以此类推，缺少的视为0。不同类型元素不能比较。range不能比较。hash类型的dict和set更不能比较。
```
>>> [0,1,2]<[1,0,0]
True
>>> ['a','b','c']>['a','b','b']
True
>>> 'abc'<'ac'
True
>>> ('a','b')>('-','b')
True
>>> ['a',1]<['a',2]
True
>>> ['a','b']<['a',2]
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: '<' not supported between instances of 'str' and 'int'
```

### print与%百分号格式化

%d后面必须对应数字，%s必须对应字符串，注意`%(a,b)`。注意字典和列表可以用str()强转，字典总是转出单引号的属性。
```
a='xx'
b=100
c=[1,2,'yy']
d={'a':1,"b":3}
print('\"%s\"%d'%(a,b)+str(c)+str(d).replace('\'','\"'))
```
输出
```
"xx"100[1, 2, 'yy']{"a": 1, "b": 3}
```

### *args和**args

*args表示不确定的参数个数，**args表示不确定的键值对参数个数。如下：
```
def demo(args_f,*args_v):
    print(args_f)
    print('---')
    for x in args_v:
        print(x)
demo('a','b','c','d')

print('========')
def demo2(**args_v):
    for k,v in args_v.items():
        print(k,v)
demo2(name='yjzn',age=9)
```
输出结果:
```
a
---
b
c
d
========
name yjzn
age 9
```


### @装饰器

装饰器就是扩展已知函数的功能，如下例子中，deco函数返回一个函数（wrapper函数)，实际`@decp`就是`f2a=deco(f2)`的简写，相当于在f2的基础上包裹了一层，多加了`print('Origen func:',*args)`功能。

所谓装饰，就是锦上添花，在原来的函数上添花，在f2和f1上添花`print('Origen func:',*args)`,这里的*args代表不确定数量的函数传递。

```
def deco(func):
    def wrapper(*args):
        print('Origen func:',*args)
        func(*args)
    return wrapper

def f2(a,b):
    print('Add func2:',a,b)

f2a=deco(f2)
f2a(1,2)
print('---')

@deco
def f1(a,b):
    print('Add func1:',a,b)
f1('a','b')
```
输出结果
```
Origen func: 1 2
Add func2: 1 2
---
Origen func: a b
Add func1: a b
```


### Python3的try..except..异常捕获
```
f=open('a.text','wb')
try:
    f.write("hello world")
except Exception as e:
    print(e)
finally:
    f.close()
```
这里'wb'要求写入字节，而`f.write('hello')`是字符串报错。注意`except TypeError as e:`，以前是使用`except TypeError,e:`。另外`print(e.message)`也是不行的。


### 设置pip资源为阿里云镜像

设置文件的位置：
windows：C:/User/用户名/pip/pip.ini
macOS: ~/.pip/pip.conf

文件内容
```
[global]
index-url = http://mirrors.aliyun.com/pypi/simple/
[install]
trusted-host=mirrors.aliyun.com
```
>macOS的隐藏文件显示命令：`defaults write com.apple.finder AppleShowAllFiles  YES`，如果已有可能需要复制到桌面，修改后再复制回去覆盖。


### 集合相减
```
a=[1,2,3,4,5]
b=[2,4]
c=[n for n in a if n not in b]
print(c)
```
输出`[1,3,5]`

### 列表内for循环简写
`[x for x in range(1,10)]`得到`[1, 2, 3, 4, 5, 6, 7, 8, 9]`
可以结合下划线只取元组列表的第n个元素:
```
a=[('a',1),('b',2)]
c=[c for c,_ in a]
print(c)
```
输出`['a', 'b']`

### zip

将两个列表合并为一个元组列表：
```
a=['a','b']
b=[1,2]
c=zip(a,b)
for m in c:
    print(m)
```
输出`('a', 1)('b', 2)`

### 两个列表同步排序
先合并成元组列表，然后用sorted解决：
```
keywords=['c','a','b']
weights=[3,2,1]
comb=zip(keywords,weights)
def comp(item):
    return item[1]
comb=sorted(comb,key=comp)
for o in comb:
    print('>>',o)
```
输出
```
3
2
1
>> ('b', 1)
>> ('a', 2)
>> ('c', 3)
```

### lambda
`lambda 参数：返回值`，对应于`def hanshu(参数):return 返回值`这样的格式。
```
def comp(item):
     return item[1]
comb=sorted(comb,reverse=True,key=comp)
```
合并为
```
comb=sorted(comb,reverse=True,key=lambda k:k[1])
```

### 无法替换去除的空格
`str.replace(str1,str2,max)`官方说明就这么多，str1和str2只能是字符串，不能用正则。
有时候replace怎么也去不掉某些空格，这是因为空格有很多种，除了一般的`' '`还有`'\xa0'`。

repr是替换掉反引号，反引号就是键盘左上角波浪键~下面那个`，用repr可以打印出字符串的本来面貌，把`\xa0`原样打印出来。
```
import re
s='AA \xa0BB'
print(s)
print(repr(s))
print(s.replace(' ',''))
print(s.replace(' ','').replace('\xa0',u''))
print(re.sub('\s+','',s))
```
输出的结果是：
![image.png](imgs/4324074-935705873c10f2a8.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
从上面看到，re.sub还是很强大的，可以把各种空格都当做\s来替换，+是数量表示一个或多个，就是不管多少个空格和\xa0都会被一个\s+都替代。但是正则表达式re比较麻烦，不推荐使用。

**遇到类似问题的解决思路是：用repr把它打印出来，看看都是什么，然后逐个replace。**

###格式化输出对象
可以利用json.dumps(obj,indent=2,ensure_ascii=False)来把一个对象、dict漂亮整齐的打印出来
```
import json
obj={
    'a':1,
    'b':{
        'b1':11,
        'b2':22,
    }
}
s=json.dumps(obj, indent=2,ensure_ascii=False)
print(s)
```
得到结果：
![image.png](imgs/4324074-61b326e9e7393562.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

### repr(s)字符串表示
只是用来开发和debug用的，没什么实际意义。
```
s='hello'
n=9/5
print(s,n)
print(repr(s),repr(n))
```
输出只是差个引号:
```
hello 1.8
'hello' 1.8
```

###网页数据导致的乱码
如果html页面header里面没有包含编码格式，那么BeautifulSoup就会当做网页默认编码'ISO-8859-1'来处理，导致乱码。
解决办法就是重新编码再解码成'gbk'中文字符:
```
s='ËÕÖÝÇàÌìÍøÂç¿Æ¼¼ÓÐÏÞ¹«Ë¾'
s=s.encode('ISO-8859-1').decode('gbk')
print(s)
```
输出中文名。

### 检测文件是否存在
```
from os.path import exists
if exists('c.txt'):
    with open('c.txt','a') as f:
        f.write('exist') 
        f.close()
else:
    with open('c.txt','a') as f:
        f.write('none')
        f.close()
```
### 将时间戳数字转换成日期小时
time.time()获取当前时间戳。
datetime.datetime.fromtimestamp(tm)将数字转化为日期对象
strftime转化为可读字符串，YmdHMS年月日时分秒
```
import time,datetime
tm=int(time.time())
s=datetime.datetime.fromtimestamp(tm).strftime('%Y-%m-%d %H:%M:%S')
print(s)
```
输出:2018-10-09 07:48:52

### 字符串转为字典对象
适用于复制出来的headers
```
def str2obj(s, s1=';', s2='='):
    li = s.split(s1)
    res = {}
    for kv in li:
        li2 = kv.split(s2)
        if len(li2) > 1:
            res[li2[0]] = li2[1]
    return res
headerstr='''
a: 111
b: 333
ccc
'''
headers = str2obj(headerstr, '\n', ': ')
print(headers)
```
输出：{'a': '111', 'b': '333'}


---
[智能决策上手系列教程索引](https://www.jianshu.com/p/0d2e46e69f58)
---
###每个人的智能决策新时代
如果您发现文章错误，请不吝留言指正；
如果您觉得有用，请点喜欢；
如果您觉得很有用，欢迎转载~
---
END







