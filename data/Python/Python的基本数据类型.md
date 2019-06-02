### 变量
变量代表内存中的一个位置，可以是数据、对象、方法等
Python中的变量没有类型，不需要单独声明，直接等号赋值即可，如`a=100`
变量名称遵循标识符规范
多个变量可以连续赋相同值，如`a=b=c=100`相当于abc分别等于100
多个变量可以同时赋予不同值，如`a,b=100,'hello'`相当于`a=100`和`b='hello'`
```
>>> a,b = 1,3
>>> a,b
(1, 3)
>>> a,b = b,b+1
>>> a,b
(3, 4)
```

### 查看数据类型
用`type()`和`isinstance()`方法查看数据类型，区别是type是最底层子类，isinstance是父类。
```
>>> a='hello'
>>> type(a)
<class 'str'>
>>> type(a)==str
True
>>> isinstance(a,str)
True
```
```
>>> a=True #布尔值是int的子类
>>> type(a)
<class 'bool'>
>>> isinstance(a,int)
True
>>> isinstance(a,float)
False
```


### 删除数据
del命令可以删除变量，实际上只是删除引用，内存中的数据会被自动回收
```
>>> c=100
>>> c
100
>>> del c
>>> c
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'c' is not defined
```


### 标准数据类型
Number（数字）
String（字符串）
List（列表）
Tuple（元组）
Set（集合）
Dictionary（字典）
其中Number和String是基本数据类型，List、Tuple、Set、Dictionary是容器类型


### Number数字
Python3 数字支持 int整数(包含bool布尔)、float浮点数（小数）、complex复数
bool只有True和Flase两个值，相当于1和0
复数由real实部和imag虚部两个浮点数组成，`100+2.1j`格式，如果只有虚部，则实部为0，如`c=200j`,J不分大小写
系统中float小数的精度可以使用`sys.float_info`查看；
Python3支持不同类型数字之间的直接计算，其中会把范围较窄的转换为较宽的类型，宽窄依次是complex>float>int
```
>>> a=True
>>> b=30
>>> a+b
31
>>> a=10
>>> b=0.2
>>> a+b
10.2
```
数字之间可以相互转换，`int()`,`float()`,`complex()`方法，注意复数必须分开real或imag部分单独转换
```
>>> int(10.2)
10
>>> c=100+20j
>>> int(c)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: can't convert complex to int
>>> float(c.real)
100.0
```
`int('x', base=10)`,base可以使用二进制0b、八进制0o、十六进制0x表示
```
>>> a=int('011',8)
>>> a
9
>>> a=0b11
>>> a
3
>>> a=0o11
>>> a
9
>>> a=0x11
>>> a
17
```
Python3整数范围可以用`sys.maxsize`查看，但实际上python3允许使用任意大小的整数。
```
>>> 10**100
10000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
```
`float('inf')`表示无限大的浮点数，`float('-inf')`表示无限小
浮点小数按精度截取使用`round(10/3,3)`截取三位3.333;math.ceil较大整数，floor取较小整数。
```
>>> import math
>>> math.ceil(10/3)
4
>>> math.floor(10/3)
3
```

### String字符串
使用单引号、双引号或者三个引号包裹的文本内容
```
'allows embedded "double" quotes'
"allows embedded 'single' quotes"
'''Three single quotes'''
"""Three double quotes"""
```
特殊字符可以用反斜杠转义,如\n表示回车，\'表示单引号，\"表示双引号,需要print输出时候会被转义
```
>>> s='A\nB\'C\"d'
>>> print(s)
A
B'C"d
```
三个引号支持多行文本，也可用于注释内容
```
>>> '''
... AAA
... BBB
... '''
'\nAAA\nBBB\n'
```
如果需要把长内容换行输入，可以使用()方法如下：
```
>>> s=('ab' 'c')
>>> s
'abc'
>>> s=('a'
... 'bc')
>>> s
'abc'
```
Python没有表示单个字符的类型，字符串可以索引获得单个字符,但不能通过索引进行修改
```
>>> s='abcde'
>>> s[0],s[:2],s[2:],s[1:3]
('a', 'ab', 'cde', 'bc')
>>> s[2]='x'
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: 'str' object does not support item assignment
```
Python3字符串默认uft-8编码`str(object=b'', encoding='utf-8', errors='strict')`
以b开头的字符串返回一个字节byte类型，以r开头的字符串禁止转义（多用于正则表达式），以u开头的字符串与默认utf8编码一致，u可省略
```
>>> b=b'abc'
>>> b
b'abc'
>>> s=r'A\nB'
>>> print(s)
A\nB
```
以f开头的字符串表示字符串中{}内用相应的变量替换,和format方法作用很像
```
>>> weight=100
>>> s=f'wei:{weight}'
>>> s
'wei:100'
>>> s='weight:{w}'.format(w=weight)
>>> s
'weight:100'
>>> height=90
>>> s='wei:{1},hei:{0}'.format(height,weight)
>>> s
'wei:100,hei:90'
>>> s='ratial:{:}'.format(10/3)
>>> s
'ratial:3.3333333333333335'
>>> s='ratial:{:.5}'.format(100/3) #保留共5位数字
>>> s
'ratial:33.333'
```
更多format示例：
```
>>> name = "Fred"
>>> f"He said his name is {name!r}."
"He said his name is 'Fred'."
>>> f"He said his name is {repr(name)}."  # repr() 等同 !r
"He said his name is 'Fred'."
>>> width = 10
>>> precision = 4
>>> value = decimal.Decimal("12.34567")
>>> f"result: {value:{width}.{precision}}"  # 嵌套
'result:      12.35'
>>> today = datetime(year=2017, month=1, day=27)
>>> f"{today:%B %d, %Y}"  # 使用date数据格式化标准
'January 27, 2017'
>>> number = 1024
>>> f"{number:#0x}"  # 指定16进制
'0x400'
```
在print方法中，可以结合%进行变量替换
```
>>> a='ABC'
>>> print('a is %s' % a) #这里的%s的s是string，表示是个字符串变量,如果是数字则%d
a is ABC
```
`str.join(iterable)`可用于连接可枚举对象如list
```
>>> li=['a','b','c']
>>> '-'.join(li)
'a-b-c'
```
lstrip()移除左侧空白字符,rstrip()移除右侧空白字符,strip()两端同时移除
```
>>> s='\n    ABC'.lstrip()
>>> s
'ABC'
```
str.lower()全部转小写,str.upper()转大写
str.replace(old, new[, count])替换字符，count表示替换总数。可以用来删除某些字符。
```
>>> s='abc123'
>>> s.replace('bc','BC')
'aBC123'
>>> s.replace('12','')
'abc3'
```
如果要特殊替换的话需要使用正则表达式，例如替换非数字内容：
```
>>> p=re.compile('[^0-9]{1}')
>>> re.sub(p,'-',s)
'---123'
```
index和find用来查找字符串中特定字符，找到则返回位置，否则index报错而find返回-1;in可以直接判断是否存在
```
>>> s='abc123'
>>> s.find('2')
4
>>> s.rfind('2')
4
>>> s.index('2')
4
>>> '2' in s
True
```
`tr.split(sep=None, maxsplit=-1)`用于将字符串切割成列表，例如：
```
>>> '1,2,3'.split(',')
['1', '2', '3']
>>> '1,2,3'.split(',', maxsplit=1)
['1', '2,3']
>>> '1,2,,3,'.split(',')
['1', '2', '', '3', '']
```
`str.zfill()`为数字填充空位0
```
>>> "42".zfill(5)
'00042'
>>> "-42".zfill(5)
'-0042'
```
加法符号可以把字符串相加，乘法符号*用来表示重复字符的个数
```
>>> s='A'*5
>>> s
'AAAAA'
```


### bytes字节

字节是二进制的数据，可以用bytes方法生成，也可以用b加字符串格式
```
>>> b=b'hello'
>>> b
b'hello'
>>> b=bytes('hello','ascii')
>>> b
b'hello'
```
由于字符串默认用ascii编码模式,所以并不支持中文。使用'utf8'或'gbk'编码可支持中文
```
>>> b=b'你好'
  File "<stdin>", line 1
SyntaxError: bytes can only contain ASCII literal characters.
>>> b=bytes('你好','ascii')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
UnicodeEncodeError: 'ascii' codec can't encode characters in position 0-1: ordinal not in range(128)
>>> b=bytes('你好','utf8')
>>> b
b'\xe4\xbd\xa0\xe5\xa5\xbd'
```
字节和字符串转换用encode和decode，但要注意编码和解码格式要一致
```
>>> s='你好'
>>> s.encode()
b'\xe4\xbd\xa0\xe5\xa5\xbd'
>>> s.encode(encoding='utf8')
b'\xe4\xbd\xa0\xe5\xa5\xbd'
>>> s.encode(encoding='ascii')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
UnicodeEncodeError: 'ascii' codec can't encode characters in position 0-1: ordinal not in range(128)
```

### None
空值，它不是任何值
```
>>> a=None
>>> a==False
False
```
Python没有undefined类型，对于不确定情况只能try...except尝试
```
del k
try:
    k
except NameError:
    print('set to None')
    k=None
print(k)
```
输出
```
set to None
None
```

