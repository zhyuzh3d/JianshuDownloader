[智能决策上手系列教程索引](https://www.jianshu.com/p/0d2e46e69f58)
---

下划线_是很神奇的一个符号，在Python里有很多特殊作用。

##  表示刚才输出的内容

用下划线表示**最近一次输出的内容**，这个在很多教程问答中出现，请认真看下面这个：
![image.png](imgs/4324074-a76f7462b25f2722.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

使用`python3`命令进入python的解释器状态：
* 第一行输入`s='a,b,c,d'`然后就回车第二行输入`_`，报错`not defined`未定义，说明刚才什么也没输出（不是吗？）。
* 然后输入单个的`s`回车，输出了字符串`'a,b,c,d'`，然后再执行`s.split(',')`用逗号分割成为列表，成功！
* 然后输入`a=99`，再换行输入`_`，得到的仍然是刚才输出的列表（不是字符串啦！）
* 再输入`a`，回车输出`99`,这也把'_'变成了`99`，然后`+1`就会累加上去。
* 后来我们又创建了列表c，并输出它，也就指定到了`_`，并且可以使用`_[0:1]`取得第一个元素，说明下划线不仅仅可以表示输出的字符串和数字，还可以是更复杂的东西。


>注意:这种用法只能在命令行中使用，禁止在.py文件或者Notebook中使用。

## “我不在乎这个东西”

下划线还可以当做**毫无意义的占位符号**，比如for循环的格式是`for n in range(0,100):`这里的n有些时候根本没有用，但又不能省略，那么就可以用下划线鄙视它一下：
```
for _ in range(10):     
    print('哈') 
```
这里只是大笑十声，那么如果用n也毫无用处，但是下面这个情况就还是需要n的：
```
for n in range(10):     
    print('第'+str(n)+'声大笑') 
```
这个用法可以扩展到元组构成的列表：
```
li=[('a',99),('b',100)]
for _,v in li:
    print(v)
```
输出99和100。如果变成`for v,_ in li:`就会输出a和b。如果变成`for v in li`就会输出两个完整的元组('a',99)和('b',100)。

还有一些其他情况也可以用下划线表示占位：
```
a=(101,102,103,104,105)
x,_,z,_,_=a
print(x,z)
```
直接创建xz两个变量，输出101和103，我们不在乎其他的。
下面是更厉害的占位：
```
a = (101, 102, 103, 104, 105)
x, *_, m = a
print(x, m)
```
星号是乘法，在这里就把中间的几个都占位了，输出101和105。

## _abc 单下划线开头，表示私有不被导出
单个下划线开头的名称只能在当前文件使用，不能导出到其他文件调用。
比如下面的gongkai对象可以在被别的文件`import`这个文件后调用，但`_siyou`却不能被使用:
```
#a.py文件
class gongkai():
    _hide=99
    vis=100
    def _hideMethod(self):
        print('...')
    def visMethod(self):
        print('>>',self._hide,self.vis)
class _siyou():
    vv=88
```
```
#b.py文件
from a import * 
print(gongkai)
c=gongkai()
print(c._hide,c.vis)
c.visMethod()
#print(_siyou)
```
把a.py和b.py放在一个文件，命令行进入这个文件夹，运行`python3 b.py`会发现gongkai的都能正常显示，`_hide`的下划线根本没用，一样可以输出。但是整个`_siyou`都不能使用了。

下划线开头的顶级名称会被import禁用。但其他的下划线开头的名称作为私有，这就只是一种惯例而已。

>但其实python根本不存在私有这个概念的，即使上面的__siyou也可以通过`from a import __siyou`正常导入，只是*星号会忽略它。如果你再a.py里面添加一行`__all__=['_siyou']`那么`import *`之后，_siyou可以用，gongyou却不可以用了。

## abc_ 下划线结尾，只是避免和系统自带关键字重名
这也是一个惯例，比如不能`from=100`因为from是关键字，只能改为`from_=100`（如果你非要坚持用from这个词的话)。

再比如下面这个s类是对str字符串的扩展，避免了split命名重复：
```
class s(str):
    def split_(self):
        return 100
aa=s('a,b,c')
print(aa.split_(),aa.split(','))
```
输出100和 ['a', 'b', 'c']。

## __abc 双下划线开头，表示碾压子类同样的名称

上面我们用s(str)扩展了str类，避免了split方法混淆，但如果真的混淆了，那么该听谁的呢？
如果在class a里面使用了双下划线的名称开头，那么不管以后怎么扩展，都是它说了算，比如：
```
class A:
    __v=100
    v=200
    def p(self):
        print(self.__v,self.v)
class B(A):
    __v=99
    v=199
b=B()
b.p()
#输出100，199
```
输出100和199。v被子类B覆盖了，但A把子类的__v给碾压了。

## __abc__ 双下划线开头又结尾，表示这是系统需要的功能

这样的名称一般不会用到，但也不要去修改。比如`__init__`用来初始化类。

## gettext的_是一个用于i18n/l18n的方法
i18n就是Internationalization（i+18个字母+n组成）国际化；l就是Localization本地化。
如果你`import getext`那么就会有下划线这个方法,其实就是`gettext.gettext`的缩写。

## 1_000_000 分割数字,相当于数字中的千分位逗号

`a=1_000_000`就是100万，`1_0_0`就是100。


---
[参考文章](https://hackernoon.com/understanding-the-underscore-of-python-309d1a029edc)
---
[智能决策上手系列教程索引](https://www.jianshu.com/p/0d2e46e69f58)
---
###每个人的智能决策新时代
如果您发现文章错误，请不吝留言指正；
如果您觉得有用，请点喜欢；
如果您觉得很有用，欢迎转载~
---
END