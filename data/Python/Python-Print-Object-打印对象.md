---
##使用dir(obj)

这将输出所有属性和方法
```
from io import BytesIO
f=BytesIO()
print('object:',f)
print('details:',dir(f))
```
输出
```
object: <_io.BytesIO object at 0x104168e08>
details: ['__class__', '__del__', '__delattr__', '__dict__', '__dir__', '__doc__', '__enter__', '__eq__', '__exit__', '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__iter__', '__le__', '__lt__', '__ne__', '__new__', '__next__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setstate__', '__sizeof__', '__str__', '__subclasshook__', '_checkClosed', '_checkReadable', '_checkSeekable', '_checkWritable', 'close', 'closed', 'detach', 'fileno', 'flush', 'getbuffer', 'getvalue', 'isatty', 'read', 'read1', 'readable', 'readinto', 'readinto1', 'readline', 'readlines', 'seek', 'seekable', 'tell', 'truncate', 'writable', 'write', 'writelines']
```
从这里可以看到我们还可以针对每个字段进行打印，比如```f.__class__```，```f.__dict```，```f.read```,```f.tell```等等，而默认print出来的就是```f.__str__()```的结果。

---
##使用obj.__dict__

输出自定义对象的属性和方法
```
class A(object):
    def __init__(self):
        self.b =1
        self.c =2
    def do_nothing(self):
        pass
    
a = A()
print('object:',a)
print('details:',a.__dict__)
print('items:',', '.join(['%s:%s' % item for item in a.__dict__.items()]))
```
输出
```
object: <__main__.A object at 0x10389e390>
details: {'b': 1, 'c': 2}
items: b:1, c:2
```

---
END

