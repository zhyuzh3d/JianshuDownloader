>[点击这里进入**人工智能嘚吧嘚**目录，观看全部文章](https://www.jianshu.com/p/ff37dbc75edb)
---
这只是一个小技巧，用@property装饰器为类添加属性设定约束和只读属性。
直接看代码：

```
class man(object):
    @property
    def birth(self):
        return self._birth

    @birth.setter
    def birth(self, value):
        if value<1900 or value >2018:
            raise ValueError('超出范围')
        else:
            self._birth = value

    @property
    def age(self):
        return 2018 - self._birth


m = man()
m.birth = 200
m.age
```
运行将抛出异常ValueError,因为birth.setter被装饰了，限定了设置m.birth的取值范围。

如果改为`m.birth=2000`,那么就能正常输出18。但如果直接修改`m.age=100`就会抛出异常`AttributeError: can't set attribute`，因为这个age属性也被装饰了，并没有`self._age=value`这样的语句供设置。

```
@property
    def birth(self):
```
这两行其实意思就是`birth=property(birth)`对函数进行包裹装饰。


---
>[点击这里进入**人工智能DBD嘚吧嘚**目录，观看全部文章](https://www.jianshu.com/p/ff37dbc75edb)
---
###每个人的智能新时代
如果您发现文章错误，请不吝留言指正；
如果您觉得有用，请点喜欢；
如果您觉得很有用，欢迎转载~
---
END