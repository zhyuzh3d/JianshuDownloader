>[点击这里进入**人工智能嘚吧嘚**目录，观看全部文章](https://www.jianshu.com/p/ff37dbc75edb)
---

Python中的@操作符称之为装饰器`decorator['dɛkəretɚ]`，它用来改变函数、方法或类的功能，但又不直接修改它们的代码，就像锦上添花，增加新功能，添花但不用去重新织锦，所以叫做**装饰器**。

- 什么是装饰器@decorator？
- 参数怎么通过装饰器传递 *args,**kargs？
- 带参数的装饰器是怎么回事@decorator(x=3)？
- 类装饰器怎么用class decorator？


##基本装饰器

**Python中的每个东西都是对象，函数也是个对象，既然是对象自然就能作为参数传递，也能作为结果返回**，比如:
```
def decorator(func):  #装饰函数，没有额外功能
    return func


def div(a, b):  #除法函数
    return a / b


chufa = decorator(div)  #把div函数装饰一下，功能不变
chufa(10, 5)
```
这个代码输出2.0。

**Python的函数内可以嵌套函数**，我们把上面代码修改一下：
```
def decorator(func):  #装饰函数，没有额外功能
    def wrapper(a, b):  #包裹函数，把被除数放大10倍
        a = a * 10
        return func(a,b)

    return wrapper


def div(a, b):  #除法函数
    return a / b


chufa = decorator(div)  #把div函数装饰一下，功能不变
chufa(10, 5)
```
这个代码会输出20.0.
它的执行顺序如下图：
![](imgs/4324074-96c8185641ebf5ab.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


好了，我们来把它改为@装饰器的写法：

```
def decorator(func):  #装饰函数，没有额外功能
    def wrapper(a, b):  #包裹函数，把被除数放大10倍
        a = a * 10
        return func(a, b)

    return wrapper


@decorator #这句话相当于div=decorator(div)
def div(a, b):  #除法函数
    return a / b


div(10, 5)
```
输出结果仍然是20.0.`@decorator`这句话就相当于`div=decorator(div)`，和上面使用的`chufa = decorator(div)`是一样的，`div`函数自身被装饰了并且覆盖了原来的`div`函数。

所以我们可以说
```
@hanshu_A
def hanshu_B(...):
  ...
```
**就是`hanshu_B=hanshu_A(hanshu_B)`，B变为被A装饰之后的函数，需要注意的是`hanshu_A`应该接受一个函数作为参数，并返回一个函数作为结果。**

## 原函数的参数

上面例子里wrapper函数使用了a,b两个参数，为了让装饰器函数`decorator`更通用，可以使用\*args表示任意多个参数列表如`(1,2,3,4)`,或者**args表示任意字典对象参数如`(a=1,b=2,c=3)`。

修改代码如下：
```
def decorator(func):  #装饰函数，没有额外功能
    def wrapper(*args):  #包裹函数，把被除数放大10倍
        return func(args[0]*10,args[1])

    return wrapper


@decorator #这句话相当于div=decorator(div)
def div(a, b):  #除法函数
    return a / b


div(10, 5)
```
或者：
```
def decorator(func):  #装饰函数，没有额外功能
    def wrapper(**kargs):  #包裹函数，把被除数放大10倍
        return func(kargs['a'] * 10, kargs['b'])

    return wrapper


@decorator  #这句话相当于div=decorator(div)
def div(a, b):  #除法函数
    return a / b


div(a=10, b=5)
```
也可以两个连用，保持参数原封不变传递：

```
def decorator(func):  #装饰函数，没有额外功能
    def wrapper(*args, **kargs):  #包裹函数，把被除数放大10倍
        print('do nothing...')
        return func(*args, **kargs)

    return wrapper


@decorator  #这句话相当于div=decorator(div)
def div(a, b):  #除法函数
    return a / b


div(a=10, b=5)
```

## @decorator(x=3)带参数的装饰器
简单说，
```
@decorator(x=3)
def func(...):
...
```
**就是`func=decorator(x=3)(func)`，这时候`decorator(x=3)就要返回一个装饰器才行**，例如下面将add加法函数的参数放大100倍的代码：
```
def decorator_big(n):
    def decorator(func):  #装饰函数，没有额外功能
        def wrapper(*args):  #包裹函数，把被除数放大10倍
            return func(*[x * n for x in args])

        return wrapper

    return decorator


@decorator_big(n=100)  #这句话相当于div=decorator(div)
def add(a, b):  #除法函数
    return a + b


add(10, 5)
```
输出[1000,500],1500

## 类装饰器
类装饰器需要定义`__init__`和`__call__`两个方法，如下：
```
class my_decorator(object):

    func=None
    def __init__(self, f):
        print("inside my_decorator.__init__()")
        self.func=f

    def __call__(self,*args):
        print("inside my_decorator.__call__()")
        self.func()

@my_decorator
def aFunction():
    print("inside aFunction()")

print('-----')
aFunction()
```
输出结果：
```
inside my_decorator.__init__()
-----
inside my_decorator.__call__()
inside aFunction()
```
从这里可以看出
```
@my_decorator
def aFunction():
...
```
**就是`aFunction=my_decorator(aFunction)`**，和上面的函数装饰器一样思路，更多内容需要读者多多体会了。

---
>[点击这里进入**人工智能DBD嘚吧嘚**目录，观看全部文章](https://www.jianshu.com/p/ff37dbc75edb)
---
###每个人的智能新时代
如果您发现文章错误，请不吝留言指正；
如果您觉得有用，请点喜欢；
如果您觉得很有用，欢迎转载~
---
END