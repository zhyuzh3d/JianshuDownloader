这篇文章介绍使用Tensorflow'低级api编程的方法，包括：
*  管理你的tensorflow程序（运算图graph）和运行时（会话session），不依赖Estimators
* 使用```tf.Session```运行tensorflow操作
* 在低级编程中使用高级元素（dataset，layer，feature columns）
* 搭建自定义的train loop训练周期，不依赖于Estimators

推荐优先使用高级接口。了解低级接口的意义在于：
* 实验和调试更加简单
* 更好的理解高级接口的运作模式

---
###张量值
张量tensor是tensorflow的核心数据单元，它是由数值构成的多维数组。张量的等级rank就是维度，整数元组shape表示了每个维度的长度。
```
3. # rank 0 ，shape [],标量
[1., 2., 3.] # rank 1，shape [3]，向量
[[1., 2., 3.], [4., 5., 6.]] # rank 2，shape [2, 3]，2x3矩阵
[[[1., 2., 3.]], [[7., 8., 9.]]] # rank 3，shape [2, 1, 3]，2行1列3层深
```
>维数rank等于方括号的层数，等于shape内数字个数。

Tensorflow使用Numpy arrays表示张量值。

---
###浏览Tensorflow核心

Tensorflow核心编程就是两个事情：
* 构建计算图```tf.graph```
* 使用```tf.Session```执行计算图

####Graph
计算图computational graph就是一系列Tensorflow操作单元的排列组合。
计算图由两部分构成：
* ops，操作。这是计算图的节点，它消耗张量，也产生张量。
* tensor，张量。这是图的边线edges，它展示了数值如何在图内流动。绝大多数tensorflow函数都返回```tf.Tensor```。
>tf.Tensor并不包含数值，它只是控制计算图里面的元素

```
import tensorflow as tf
a = tf.constant(3.0, dtype=tf.float32)
b = tf.constant(4.0) #也是tf.float32
total = a + b
print(a)
print(b)
print(total)
```
运行得到的不是7.0，而是三个张量，因为这里只是构建了计算图graph，而没有运行它。
```
Tensor("Const:0", shape=(), dtype=float32)
Tensor("Const_1:0", shape=(), dtype=float32)
Tensor("add:0", shape=(), dtype=float32
```

graph中的每个操作都有唯一自动赋予的名字，比如上面的'add:0'，如果有更多add操作，就会是'add_1:0','add_2:0'等。

####Tensorboard
信息板提供了视觉化的计算效果，使用步骤：
1. 把计算图graph保存到Tensorboard的摘要文件,这将产生一个event事件文件。
```
import os
import tensorflow as tf

#存储event文件夹
dir_path = os.path.dirname(os.path.realpath(__file__))
sum_path=os.path.join(dir_path,'models') #不要使用斜杠

#构造计算图
a = tf.constant(3.0, dtype=tf.float32)
b = tf.constant(4.0)
total = a + b


#写入tensorboard该要
writer = tf.summary.FileWriter(sum_path)
writer.add_graph(tf.get_default_graph())

#运行图
sess=tf.Session()
sess.run(total)
```
运行上面的代码，将在.py所在文件夹内产生一个models文件夹,文件夹里面又一个events开头的文件，里面记录着tensorflow的运行情况，然后命令行cd进入当.py所在文件，执行以下命令启动tensorboard服务（按ctrl+C两次退出）:
```
tensorboard --logdir models
```
然后打开浏览器，输入地址```http://localhost:6006/```就打开了Tensorboard页面，点击顶部的GRAPHS可以看到我们的加法运算操作，类似下图
![](imgs/4324074-d2d5b6ca3c0651dd.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

####Session
建造计算图graph之后，必须使用会话```session=tf.Session()``来运行它。如果说graph是.py文件，那么session就是让它变为可执行程序。

当使用session.run()来运行最终输出的张量节点的时候，tensorflow会自动反向跟踪整个graph并计算所有节点，如上面的代码中，最终输出是7.0。

也可以一次运行run多个张量：
```
import tensorflow as tf

a = tf.constant(3.0, dtype=tf.float32)
b = tf.constant(4.0)
total = a + b

sess=tf.Session()
v=sess.run({'ab':(a,b),'total':total})
print(v)
```
得到一个字典:
```
{'ab': (3.0, 4.0), 'total': 7.0}
```
同样的graph使用```tf.Session().run()```都是全新的运算，可能得到不同的结果，例如：
```
import tensorflow as tf
sess=tf.Session()

vec = tf.random_uniform(shape=(3,))
out1 = vec + 1
out2 = vec + 2
print(sess.run(vec))
print(sess.run(vec))
print(sess.run(out1))
print(sess.run(out2))
print(sess.run((out1, out2)))
```
输出不同的随机值,注意((out1,out2))的结果：
```
[0.82387817 0.65216887 0.32529306]
[0.10036051 0.535251   0.38202   ]
[1.2352179 1.8258253 1.4338707]
[2.6720245 2.1600003 2.9119837]
(array([1.4428363, 1.3376999, 1.7375625], dtype=float32), array([2.4428363, 2.3377   , 2.7375627], dtype=float32))
```
有些tensorflow函数返回的不是```tf.Tensor ```而是```tf.Operations```,运行run一个operation操作会返回None。但可以使用这个技巧获得一些特别作用，比如：
```
init = tf.global_variables_initializer()
sess.run(init)
```

####Feeding

标准格式下，graph总是产生相对固定的运行结果，这没有什么意义。但是graph可以接收外部的placeholder传入的变化的输入，placeholder就像一个promise承诺稍后提供数据，像一个函数那样。

```
import tensorflow as tf
sess=tf.Session()

x = tf.placeholder(tf.float32)
y = tf.placeholder(tf.float32)
z = x + y

print(sess.run(z, feed_dict={x: 3, y: 4.5}))
print(sess.run(z, feed_dict={x: [1, 3], y: [2, 4]}))
```
输出
```
7.5
[3. 7.]
```
这段代码可以看作定义了一个函数，然后运行了它:
```
 def zfunc(x,y):
    return x+y
print(zfunc(3,4.5))
```
---
###Datasets

Placeholder用于简单的实验，Datasets才是将数据输入模型的更好方法。
要从数据集datasets得到一个可运行的```tf.tensor```,需要先把它转为```tf.data.Iterator```迭代器，然后使用迭代器的```get_next()```方法。

如下示例代码，使用了```try...catch...```捕获异常，避免超过终点的错误:
```
import tensorflow as tf
sess=tf.Session()

my_data = [
    [0, 1,],
    [2, 3,],
    [4, 5,],
    [6, 7,],
]
dataset = tf.data.Dataset.from_tensor_slices(my_data)
next_item = dataset.make_one_shot_iterator().get_next()

while True:
  try:
    print(sess.run(next_item))
  except tf.errors.OutOfRangeError:
    break
```
---
###Layers

可训练的模型必须能够改变graph的值，从而在在相同输入数据的时候获得新的输出。层Layer是推荐的方法，用来像graph里面添加可训练的参数。

Layers将变量和操作打包。比如密集连接层densely-connected-layer为所有的输入执行加权求和操作到每个输出，以及可选的激活函数activation function，由图层对象管理连接权重weighted和偏移值bias。

层的使用流程包括：
* 创建
* 初始
* 运行 

```
import tensorflow as tf
sess=tf.Session()

#创建一个节点的密集层，传入n个三元数组，units=2输出二维数组
x = tf.placeholder(tf.float32, shape=[None, 3])
linear_model = tf.layers.Dense(units=2)
y = linear_model(x)

#初始化所有变量
init = tf.global_variables_initializer()
sess.run(init)

#运行层，通过x传入数据
v=sess.run(y, {x: [[1, 2, 3],[4, 5, 6]]})
print(v)
```
注意，tf.global_variables_inistializer方法只初始化以上的graph，所以应该在graph建造完成之后运行。
打印出的结果
```
[[-2.037472   3.9676275]
 [-5.741477  10.678923 ]]
```

每个layer在创建的时候可以直接传递placeholder，比如上面的代码可以简化成下面
```
import tensorflow as tf
sess=tf.Session()

x = tf.placeholder(tf.float32, shape=[None, 3])
y = tf.layers.dense(x, units=1) #简写

init = tf.global_variables_initializer()
sess.run(init)

print(sess.run(y, {x: [[1, 2, 3], [4, 5, 6]]}))
```
这次会打印出两个1元数组
```
[[-3.4608526]
 [-8.070822 ]]
```
---
###Feature Columns

可以使用```tf.feature_column.input_layer```快速实验特征列，它只接受dense column密集列，如果是分类列Catergorical column，就必须经过指示列```tf.feature_column.indicator_column```包裹，示例代码如下。

```
import tensorflow as tf
sess=tf.Session()

#特征数据
features = {
    'sales' : [[5], [10], [8], [9]],
    'department': ['sports', 'sports', 'gardening', 'gardening']}

#特征列
department_column = tf.feature_column.categorical_column_with_vocabulary_list(
        'department', ['sports', 'gardening'])
department_column = tf.feature_column.indicator_column(department_column)

#组合特征列
columns = [
    tf.feature_column.numeric_column('sales'),
    department_column
]

#输入层（数据，特征列）
inputs = tf.feature_column.input_layer(features, columns)

#初始化并运行
init = tf.global_variables_initializer()
sess.run(tf.tables_initializer())
sess.run(init)

v=sess.run(inputs)
print(v)
```
上面代码输出如下结果，可以看到input输入层将每个商品的features转为3维矢量，前两个0，1独热表示分类运动sport或园艺gardening，第三个数字表示销售数量salse。
```
[[ 1.  0.  5.]
 [ 1.  0. 10.]
 [ 0.  1.  8.]
 [ 0.  1.  9.]]
```

###Training
最简单的训练流程包括：
1. 构建计算图
    * 定义数据
    * 定义模型
    * 损失函数
    * 优化方法
2. 初始化
3. 多次训练
4. 进行预测

下面来看一段完整的代码，尝试根据给定的线性数据推算线性函数模型并进行预测：
```
import tensorflow as tf

#两个输入数据，yi=-xi+1
xi =[[1,], [2,], [3,], [4,]]
yi =[[0,], [-1,], [-2,], [-3,]]

#两个浮点占位器，不能使用整数，那将产生稀疏值
x = tf.placeholder(tf.float32, shape=[None, 1])
y_true = tf.placeholder(tf.float32, shape=[None, 1])

#定义模型，一个线性的密集层
y_pred = tf.layers.dense(x, units=1)

#设定损失函数，使用均方差，MSE=sum(squar(x-x'))/n
loss = tf.losses.mean_squared_error(labels=y_true, predictions=y_pred)

#设定优化器，梯度下降优化器
optimizer = tf.train.GradientDescentOptimizer(0.1)
train = optimizer.minimize(loss)

#初始化以上全部变量
init = tf.global_variables_initializer()
sess = tf.Session()
sess.run(init)

#进行训练
for i in range(1000):
  sess.run((train, loss),feed_dict={x:xi,y_true:yi})

#进行预测，正确结果应该输出-11
print(sess.run(y_pred,feed_dict={x:[[12,]],y_true:[[None]]}))
```
输出结果,非常接近我们正确值了。
```
[[-10.999997]]
```
如果降低训练次数1000到100，或者将优化器梯度下降参数从0.1降为0.01,那么都将产生稍大的误差。

---
###本篇小结


* 张量值的等级rank和形状shape
* Tensorflow的核心：
    * 计算图graph：ops，tensor
    * 会话运行时session：run，init
    * 信息板tensorboard：summary，event文件
    * 喂食数据feed：placeholder，feed_dict
* 数据集Datasets：iterator，get_next()
* 层Layer：
    * 创建
    * 初始化
    * 运行
* 特征列Feature columns：
    *  input_layer(features,columns)
    *  indicator_column(categorical_column)
* 训练Train:features-graph-init-train-predict
    ```sess.run((train, loss),feed_dict={x:xi,y_true:yi})```

---
###探索人工智能的新边界
如果您发现文章错误，请不吝留言指正；
如果您觉得有用，请点喜欢；
如果您觉得很有用，感谢转发~
---
END














