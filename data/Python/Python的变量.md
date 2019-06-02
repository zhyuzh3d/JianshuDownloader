### 概念
Python变量是用于存储值的保留内存位置。换句话说，python程序中的变量将数据提供给计算机进行处理。
Python中的每个值都有一个数据类型。Python中不同的数据类型是Numbers，List，Tuple，Strings，Dictionary等。
变量可以用任何名称声明，甚至可以用a，aa，abc等字母表来声明。
变量名称规范遵循Python标识符规范，即字母数字下划线混合，但不能数字开头。用下划线开头表示特殊含义。
Python3支持Unicode作为变量名，即中文变量名也支持，但不推荐。
```
>>> 名字='王小明' #符合语法，但不推荐
>>> print(名字)
王小明
```

### 推荐的命名习惯
常量下划线连大写如CAPS_WITH_UNDER；
类或异常用首字母大写驼峰式如CapWords；
其他用下划线连小写lower_with_under；
如果是内部使用那么下划线开头_lower_with_under。


### 赋值
Python 中的变量不需要声明。每个变量在使用前都必须赋值，变量赋值以后该变量才会被创建。
在 Python 中，变量就是变量，它没有类型，我们所说的"类型"是变量所指的内存中对象的类型。
等号（=）用来给变量赋值。
等号（=）运算符左边是一个变量名,等号（=）运算符右边是存储在变量中的值。
Python允许你同时为多个变量赋值。
```
>>> a,b=1,'a'
>>> x=y=3
>>> a,b,x,y
(1, 'a', 3, 3)
```

### 全局变量和局部变量
所有变量都只能在其所在的代码块或其子代码块中使用，在整个模块或程序中都能使用的变量成为全局变量，其他都视为局部变量
```
a=100
def func():
    b=10
    a=a+b
print(a,b) #报错，b没有定义，子代码块中定义的变量无法在父层代码中使用
```
注意以上情况对于流程控制产生的代码块不适用，例如
```
a=100
i=100
for i in range(3):
    b=10
    a=a+b
print(a,b,i) #正确运行，得到130 10 2
```
```
a=100
if True:
    b=10
    a=a+b
print(a,b) #正确运行，得到110 10
```
Python会优先使用最近的局部变量，同名的更高层级变量和全局变量将被忽视
```
a=100
def func():
    a=99
    print(a) #输出99
func()
print(a) #输出100而不是99
```
局部代码块中可以使用global来创建全局变量
```
a=100
def func():
    global a
    a=99
    print(a) #输出99
func()
print(a) #输出99，a已经被覆盖
```


### 删除变量
使用del删除,删除后变量将变为未定义，不能再使用.
```
>>> del a
>>> a
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'a' is not defined
```

### None空变量
空变量表示变量存在，但未赋值
```
def fn():
    global a
    return
b=fn()
print(b) #输出None
print(a) #报错NameError
```

### 变量的类型
变量有很多种类型如int、str、list等，但同一变量改变类型是很危险的，应严格避免