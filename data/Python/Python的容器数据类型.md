### Sequence序列对象

lists列表, 元组tuples, and range

通用序列操作：
* item in或not in sequence：判断item在或者不在序列中
* +或*符号：将两个序列相加或把一个序列内容复制n倍, 注意*可能得到的是同一对象的多个引用
* s[n]:第n个元素，超出范围IndexError
* s[i:j]:第i到j个元素的切片，包含第i个不包含第j个，i为负数相当于0，j超范围相当于最多
* s[i:j:k]:第i到j个元素间隔k个取出
* len(s):序列的元素总数
* min(s)和max(s):按照排序的最小或最大一项
* s.index(x,i,j):ij可选。序列中x的位置，i和j限定搜索范围,返回x的位置或ValueError
* s.count(x):s中包含x的重复数量,找不到返回0
* for x in s:循环处理序列中的每一项
* s[i:j] = t:将序列的i到j项替换为t,如果t为序列则直接元素对应替换，无论t数量多少；如果t为非序列，则i到j变为一个t对象
* s[i:j]=[]:相当于删除i到j项（不含j），等同del s[i:j]
* s.append(x):将x添加到s，等同s[len(s):len(s)]=[x]
* s.clear():清理所有元素
* s.copy():复制整个序列，相当于s[:]
* s.extend(t) or s += t:合并两个序列，相当于s[len(s):len(s)] = t
* s.insert(i, x):将x插入到i位置，相当于s[i:i] = [x]
* s.pop(i)：获取第i项并从序列中删除它，如果i省略则指向最后一个
* s.remove(x)：移除x项,如果不存在则ValueError
* s.reverse()：翻转顺序


### list列表
* 构造方法：[],[1,2,3],[for i in range(10)],list('abc'),list((1,2,3))
```
>>> sorted((3,2,1))
[1, 2, 3]
>>> list((1,2,3))
[1, 2, 3]
```
* 负数索引从 list 的尾部开始向前计数来存取元素。任何一个非空的 list 最后一个元素总是 li[-1]
* sorted(list, key=None, reverse=False)为列表排序，生成新排序列表
```
>>> li=[{'a':22},{'a':12},{'a':100}]
>>> sorted(li,key=lambda x:x['a'])
[{'a': 12}, {'a': 22}, {'a': 100}]
```
* list.sort()将list排序，list必须为基本对象，不能是容器对象；而sorted则可以利用key对更复杂对象排序。

### Tuples元组
* 构造方法：(a,b),(a,),(a,b,c),tuple([1,2,3])
* 元组一旦创建将不可修改
* Tuple没有没有append或extend方法，没有 remove 或 pop 方法、没有 index 方法。
* 可以使用 in 来查看一个元素是否存在于 tuple 中。

### range
* 构造方法：range(start,stop,step),range(10),range(5,50,5);step不能为0
```
>>> list(range(0, -10, -1))
[0, -1, -2, -3, -4, -5, -6, -7, -8, -9]
>>> list(range(0))
[]
>>> list(range(1, 0))
[]
```
* range无论数字多少，总是占用同样小的内存。
* range可以比较
```
>>> range(0, 3, 2) == range(0, 4, 2)
True
```
range存在.start,.stop,.step属性


### 集合类型set
*  集合支持x in set, len(set), and for x in set等语法
*  集合中没有重复元素
*  isdisjoint是否完全无交集
```
>>> a={1,2,3,4}
>>> b={3,4,5,6}
>>> a.isdisjoint(b)
False
>>> c={5,6}
>>> a.isdisjoint(c)
True
```
* issubset(other)是否子集；相当于set <= other
* issuperset(other)是否超集；相当于set >= other
* union(other)与other合并；
* intersection(*others)交集
* difference(*others)在此集合但不在other集合
* symmetric_difference(others)不在交集但在此集合或other集合
* copy()复制集合
* update(*others)将others添加进来
* intersection_update(*others)取交集
* add(elem),remove(elem)添加和移除元素,如果不存在则抛出异常KeyError
* discard(elem)删除元素,如果不存在不报错
* pop()任意去掉一个元素
* clear()清空

### 字典dict
* Dictionary 是 Python 的内置数据类型之一, 它定义了键和值之间一对一的关系。
* 每一个元素都是一个 key-value 对, 整个元素集合用大括号括起来
* 您可以通过 key 来引用其值, 但是不能通过值获取 key
* 在一个 dictionary 中不能有重复的 key。给一个存在的 key 赋值会覆盖原有的值
* dictionary 的 key 是大小写敏感的
* Dictionary 的值可以是任意数据类型, 包括字符串, 整数, 对象, 甚至其它的 dictionary。
* 在单个 dictionary 里, dictionary 的值并不需要全都是同一数据类型, 可以根据需要混用和匹配。
* 构建方法：{'a':11,'b':22},{11:'22',22:'bb'},键只能是索引数字(正负数和小数都可)或字符串
```
>>> a = dict(one=1, two=2, three=3)
>>> b = {'one': 1, 'two': 2, 'three': 3}
>>> c = dict(zip(['one', 'two', 'three'], [1, 2, 3]))
>>> d = dict([('two', 2), ('one', 1), ('three', 3)])
>>> e = dict({'three': 3, 'one': 1, 'two': 2})
>>> a == b == c == d == e
True
```
* len(d)字典属性数量
* del d[key]删除key，如果不存在则KeyError
* clear()，copy()
* fromkeys(seq[, value])用seq序列做键值key，所有键都等于value
* get(key)获取值，但不出错
* items(),keys(),values()返回一个可枚举的对象

```
>>> dishes = {'eggs': 2, 'sausage': 1, 'bacon': 1, 'spam': 500}
>>> keys = dishes.keys()
>>> values = dishes.values()

>>> # iteration
>>> n = 0
>>> for val in values:
...     n += val
>>> print(n)
504

>>> # keys and values are iterated over in the same order (insertion order)
>>> list(keys)
['eggs', 'sausage', 'bacon', 'spam']
>>> list(values)
[2, 1, 1, 500]

>>> # view objects are dynamic and reflect dict changes
>>> del dishes['eggs']
>>> del dishes['sausage']
>>> list(keys)
['bacon', 'spam']

>>> # set operations
>>> keys & {'eggs', 'bacon', 'salad'}
{'bacon'}
>>> keys ^ {'sausage', 'juice'}
{'juice', 'sausage', 'bacon', 'spam'}
```
* pop(key)删除一个属性，不存在的话报错；popitem()删除最后一个属性
* setdefault(key[, default])设置默认值,不存在的话自动添加
* update(other)更新属性值，不存在的话自动添加








