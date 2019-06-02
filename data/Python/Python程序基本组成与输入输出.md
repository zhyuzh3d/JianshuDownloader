###  变量与类型
在python程序中，一切数据结构都是存储在堆空间中的对象。python程序中的变量都是引用变量，可以指向任何类型的对象。

### 语句与表达式
常用的语句包括：
结构定义语句（函数定义和类定义）
赋值语句（普通赋值和扩展赋值）
控制语句（if-else条件、for循环、while循环、continue、break和return）
模块引入语句（import和from-import）
异常语句（异常捕获try-except/finally、异常抛出raise）
变量作用域声明语句（global和nonlocal）
上下文管理语句（with）
断言语句（assert）
常用的表达式：
布尔表达式
算术表达式
比较表达式
简单集合构造表达式（例如，[1,2,3]）
复杂集合构造表达式（例如，[x+1 for x in y]）
lambda表达式
调用表达式
属性解引用表达式
元素解引用表达式

### 模块与包
python模块被引入到程序中时，是堆空间的一个对象。python模块中通常包含python对象的定义以及python语句。当一个模块被首次引入时，python解释器会执行对应的python文件，并同时创建一个模块类型对象。模块中的全局对象会被作为属性添加到该模块对象的属性集合中。
模块引用方式：
（1）通过关键字import
（2）通过关键字from...import...
python中的模块也是一种普通对象，可以被当作参数任意传递。
python的包是一个包含init.py文件的文件，当首次引入一个包时，init.py文件会被默认执行。
python包在程序中本质上也是一个模块对象，其特性与模块基本相同。

### 类与实例
python中的类，是一个类类型的对象，可以通过关键字class在程序任何地方定义。
python中的类可以继承多个基类，子类中的属性可以覆盖父类的属性来实现重载。
实例对象可以拥有自身的属性字典，不与其他实例对象共享。

### 函数与方法
通过关键字def在程序任何地方定义。
当一个函数对象被作为参数时，其执行所需的环境也会被作为闭包进行过程间的传递。
python中的lambda表达式本质上是一个匿名的函数，使用起来与函数几乎无差别。
python中的方法实则是被动态绑定闭包的函数，可分为类方法、实例方法和静态方法。
类方法：属于某个类，在调用时，其所属的类对象会被隐式地传递给方法的第一个参数。
实例方法：其对应的实例对象会被隐式地传递给该方法的第一个参数。
静态方法：不属于任何类或实例，在调用时，其效果等同于一个自由函数，不存在任何隐式参数传递 

### 动态对象
python中的对象具体可以分为不可变对象和可变对象。
不可变对象是指对象的内部属性不可以变，常见的不可变对象包括整数、浮点数、字符串和元组等。
可变对象则是指对象的内部属性是可以被任意改变的。可变对象具有非常强的动态性，其内部属性可以被任意添加、修改或删除。
python中的反射是指可以利用一些元对象的设施来访问、更改和删除对象属性（包括方法的追加和调用等）。
python中常用的反射 函数包括hasattr()、getattr()、setattr()和delattr()等。
python中提供了exec()和eval()函数，exec()用于执行一段动态构造的语句块；eval()则用于执行一个动态构造的表达式。

### 注释内容
使用#或者引号包裹的内容

### __main__
当py文件是被调用时，__name__的值为模块名，当文件被执行时，__name__为'__main__'
为了确保py文件可以被直接运行，也可以被import作为模块导入，每个py代码中都应包含：
```
if __name__ == '__main__':
    dosthing(args)
```
这里的args是指`python xxx.py xxx`中的[`xxx.py`,`xxx`]
Python使用缩进对齐组织代码的执行，所有没有缩进的代码（非函数定义和类定义），都会在载入时自动执行，这些代码，可以认为是Python的main函数

### 文件开头的!#
为类Unix系统提供更多信息，
第一行以 #! 开头的代码, 在计算机行业中叫做 "shebang", 也叫做 sha-bang / hashbang / pound-bang / hash-pling, 其作用是"指定由哪个解释器来执行脚本".
一般我们用来指定使用python的版本，系统会优先查找这个地址的执行文件
```
#!/usr/bin/python3
```

### 输出
Python两种输出值的方式: 表达式语句和 print() 函数。
第三种方式是使用文件对象的 write() 方法，标准输出文件可以用 sys.stdout 引用。
如果你希望输出的形式更加多样，可以使用 str.format() 函数来格式化输出值。
如果你希望将输出的值转成字符串，可以使用 repr() 或 str() 函数来实现。
str()： 函数返回一个用户易读的表达形式。
repr()： 产生一个解释器易读的表达形式。
```
>>> s = 'Hello, Runoob'
>>> str(s)
'Hello, Runoob'
>>> repr(s)
"'Hello, Runoob'"
>>> str(1/7)
'0.14285714285714285'
>>> x = 10 * 3.25
>>> y = 200 * 200
>>> s = 'x 的值为： ' + repr(x) + ',  y 的值为：' + repr(y) + '...'
>>> print(s)
x 的值为： 32.5,  y 的值为：40000...
>>> #  repr() 函数可以转义字符串中的特殊字符
... hello = 'hello, runoob\n'
>>> hellos = repr(hello)
>>> print(hellos)
'hello, runoob\n'
>>> # repr() 的参数可以是 Python 的任何对象
... repr((x, y, ('Google', 'Runoob')))
"(32.5, 40000, ('Google', 'Runoob'))"
```
两个print会打印在不同的两行，如果希望连续不换行打印，前一个结尾使用end参数
```
>>> print('a',end='');print('b')
ab
```
rjust可以右侧添加空白，ljust左侧添加空白，format方法中数字{:xd}字符串{:ns}有类似作用
```
>>> print('{0:3s}{1:3s}{2:3s}'.format('a','b','c'));print('a'.ljust(2),'b'.ljust(2),'c'.ljust(2));
a  b  c  
a  b  c
```
zfill()用于在数字左侧空位补0
```
>>> '12'.zfill(5)
'00012'
>>> '-3.14'.zfill(7)
'-003.14'
>>> '3.14159265359'.zfill(5)
'3.14159265359'
```

### 字符串的format方法
format()方法是用format参数替换字符串中大括号，默认为依次替换，{3}可以指定使用第三个参数
```
>>> '{}-{}'.format('a','b')
'a-b'
>>> '{1}-{0}-{1}'.format('a','b')
'b-a-b'
>>> '{b}-{a}'.format(a='a',b='b')
'b-a'
```
format中'!a' (使用 ascii()), '!s' (使用 str()) 和 '!r' (使用 repr()) 可以用于在格式化某个值之前对其进行转化:
```
>>> print('{a!r}-{a}'.format(a='\n\'OK\''))
"\n'OK'"-
'OK'
```
format中{a:10}表示a至少占10个字符位置，{a:2s}或{a:2d}类似，可以用来对齐
format中字符串可以使用[]直接访问参数字典的同名属性
```
>>> table = {'Google': 1, 'Runoob': 2, 'Taobao': 3}
>>> print('Runoob: {0[Runoob]:d}; Google: {0[Google]:d}; Taobao: {0[Taobao]:d}'.format(table))
Runoob: 2; Google: 1; Taobao: 3
>>> table = {'Google': 1, 'Runoob': 2, 'Taobao': 3}
>>> print('Runoob: {Runoob:d}; Google: {Google:d}; Taobao: {Taobao:d}'.format(**table))
Runoob: 2; Google: 1; Taobao: 3
```
% 操作符也可以实现字符串格式化。 它将左边的参数作为类似 sprintf() 式的格式化字符串, 而将右边的代入, 然后返回格式化后的字符串. 例如:
```
>>> import math
>>> print('常量 PI 的值近似为：%5.3f。' % math.pi)
常量 PI 的值近似为：3.142。
```

### 读取输入
Python提供了 input() 内置函数从标准输入读入一行文本，默认的标准输入是键盘。
input 可以接收一个Python表达式作为输入，并将运算结果返回。
```
str = input("请输入：");
print ("你输入的内容是: ", str)
```

