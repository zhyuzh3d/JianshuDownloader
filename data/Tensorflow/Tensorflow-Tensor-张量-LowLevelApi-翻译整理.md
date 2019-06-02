Tensorflow，如名所示，是一个定义和计算求解张量tensor的框架。

Tensor张量就是基于数据类型dtype定义的n维数组。

```tf.Tensor```对象表示最终将产生一个值，但自身并不直接是一个值。

先使用tensor张量和计算操作ops编织一个计算图graph，然后再运行它获得结果。

Tensor两个属性：数值类型dtype和数值形状（维数与长度）shape。

每个tensor内的数值必须是同样类型；并且数值类型dtype必须是已知的，shape是半已知的（比如[None,3]表示n个三元数组)。

对于大部分操作来说，如果输入的张量形状确定，那么操作结果输出的张量形状也是确定的，但有些时候只有在计算图被执行的时候才能知道张量的形状。

特殊张量```tf.Variable、tf.constant、tf.placeholder、tf.SparseTensor```将留在稍后文章中介绍。
>注意下面的```tf.Variable()```所生成的张量是固定不变的，每次张量被执行的时候，它只会有一个值。

---
###Rank等级：张量的维度

Rank  属性名称
0      标量Scalar (只有大小magnitude only)
1	矢量Vector (大小与方向magnitude and direction)
2	矩阵Matrix (数字表table of numbers)
3	三维张量3-Tensor (数字立方体cube of numbers)
n	N维张量n-Tensor (你猜you get the idea)

#####Rank 0:标量
```
mammal = tf.Variable("Elephant", tf.string)
ignition = tf.Variable(451, tf.int16)
floating = tf.Variable(3.14159265359, tf.float64)
its_complicated = tf.Variable(12.3 - 4.85j, tf.complex64)
```
>注意：在tensorflow中字符串string被当作标量处理，而不是数组队列。

######Rank 1:矢量，数组
```
mystr = tf.Variable(["Hello"], tf.string)
cool_numbers  = tf.Variable([3.14159, 2.71828], tf.float32)
first_primes = tf.Variable([2, 3, 5, 7, 11], tf.int32)
its_very_complicated = tf.Variable([12.3 - 4.85j, 7.5 - 6.23j], tf.complex64)
```

######Higher rank更高等级:更多层的数组
```
mymat = tf.Variable([[7],[11]], tf.int16)
myxor = tf.Variable([[False, True],[True, False]], tf.bool)
linear_squares = tf.Variable([[4], [9], [16], [25]], tf.int32)
squarish_squares = tf.Variable([ [4, 9], [16, 25] ], tf.int32)
rank_of_squares = tf.rank(squarish_squares)
mymatC = tf.Variable([[7],[11]], tf.int32)
my_image = tf.zeros([10, 299, 299, 3])  # batch x height x width x color
```

######获取tensor的rank等级
```
import tensorflow as tf
sess= tf.Session()

t=tf.Variable([ [4, 9], [16, 25] ], tf.int32)
img = tf.zeros([10, 299, 299, 3])

init = tf.global_variables_initializer()
sess.run(init)

v1=sess.run(tf.rank(t))
v2=sess.run(tf.rank(img))

print(v1,v2)
```
注意必须run运行张量，才能在运行中获取张量的rank。以上代码输出2，4。
```
2 4
```

######张量切片索引

因为张量本身是一个n维的嵌套数组，每个单元如何使用索引访问？
rank0只有一个值不存在索引问题。
rank1是数组，直接my_vector[2]形式就可以，甚至[]中可以使用tensor动态变化。
rank2是数字表，my_matrix[1, 2]得到的是一个标量数字，使用冒号选择子层数组，my_matrix[:, 3]选择第三列。

---
###Shape形状
张量的形状是指在每个等级（rank维度）上元素的数量，因为一个张量可能不止1个维度，所以，形状也是多个数字组成的数组。可以是数组[3,2],元组(3,3),也可以是个整数4，还可以是```tf.TensorShape```对象例如```TensorShape([16, 256]),TensorShape([None, 256])```。

当计算图graph被计算的时候，tensorflow自动推断张量的形状，由于等级可能是未知也可能已知的，所以形状也可能是未知的。

![](imgs/4324074-f4dc38ba4ab90152.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

######获取张量的形状
```
import tensorflow as tf
sess= tf.Session()

t=tf.Variable([ [4, 9], [16, 25] ], tf.int32)
img = tf.zeros([10, 299, 299, 3])

my_matrix=tf.Variable([[1,2],[2,4],[4,3]])
zeros = tf.zeros(my_matrix.shape[1])

print(t.shape)
print(img.shape)
print(my_matrix.shape)
print(zeros)
```
输出:
```
(2, 2)
(10, 299, 299, 3)
(3, 2)
Tensor("zeros_1:0", shape=(2,), dtype=float32)
```
注意zeros是一个行数2，列数未知的张量。

######改变```tf.Tensor```的形状
因为shape就是指张量每层数组的元素数，所以我们可以使用```tf.reshape```方法改变张量，也就是元素数量，注意在转变过程中元素总数不能变多也不能变少，张量的形状也不能出现小数。

```
import tensorflow as tf
rank_three_tensor = tf.ones([3, 4, 5]) #3x4x5=60共60的数字立方体
matrix = tf.reshape(rank_three_tensor, [6, 10])  #变为6x10 matrix
matrixB = tf.reshape(matrix, [3, -1])  # 3x20matrix，-1 表示自动计算这维度元素个数.
matrixAlt = tf.reshape(matrixB, [4, 3, -1])  # 4x3x5数字立方

notgood = tf.reshape(matrixB, [6,2])  #代码报错，因为6x2不等于60，无法决定取舍
notgood2 = tf.reshape(matrixAlt, [13, 2, -1])  #代码报错，因为13x2无法被60整除!
```
---
###数据类型tf.Datatype

```tf.cast```可以用来转化数据类型
```
#整数转到小数
float_tensor = tf.cast(tf.constant([1, 2, 3]), dtype=tf.float32)
```
使用张量的dtype来获取张量的数据类型。

---
###计算张量

除了使用```tf.Session().run()```方法以外，还可以用张量的eval()方法快速计算张量结果：
```
import tensorflow as tf
sess=tf.Session()

constant = tf.constant([1, 2, 3])
tensor = constant * constant

with sess.as_default():
    print(tensor.eval())    
print(tensor.eval(session=sess)) #格式不同
```
```Tensor.eval(session,feed_dict)```输出
```
[1 4 9]
[1 4 9]
```
使用喂食字典的示例
```
import tensorflow as tf
sess=tf.Session()

p = tf.placeholder(tf.float32)
t = p + 1.0
v=t.eval(session=sess,feed_dict={p:2.0}) #此处p必须与placeholder变量名相同
print(v)
```
输出
```
3
```
注意，如果张量的值依赖一个队列queues，那么只会计算队列一遍。结合队列的情况需要先呼叫```tf.train.start_queue_runners```

---
###打印张量
print方法打印的是Tensor对象，不是计算得到的值。```tf.print()```方法是一个操作，被计算的时候打印输出。
```
import tensorflow as tf
sess=tf.Session()

t=tf.Variable(5, tf.int32)
tf.Print(t, [t])
t = tf.Print(t, [t]) #计算时被打印
result = t + 1

init = tf.global_variables_initializer()
sess.run(init)

print(t)
sess.run(result)
```
输出结果
```
Tensor("Print_1:0", shape=(), dtype=int32)
[5]
```
---
###本篇小结

* 张量的基本概念
* Rank 张量的等级，就是维度，是数组嵌套的层数
    *  rank0标量，1矢量，2矩阵，3数字立方体 
    *  获取等级```sess.run(tf.rank(t))
    * 获取元素my_matrix[1, 2]，my_matrix[:, 2]
* Shape张量的形状就是每个等级的元素数量
    * 获取张量形状```直接 print(t.shape)```
    * 改变张量的形状```tf.reshape(t,[m,n,..]),元素数必须保持不变
 *数据类型tf.Datatype,```t.eval(session=sess,feed_dict={p:2.0})```
 * 打印张量操作```tf.print(t,[t])```

---
###探索人工智能的新边界
如果您发现文章错误，请不吝留言指正；
如果您觉得有用，请点喜欢；
如果您觉得很有用，感谢转发~
---
END





