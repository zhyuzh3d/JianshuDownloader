Variables变量用于共享、持久化状态管理。

```tf.Variable```表示此数值在计算过程中可能会变化，它独立于```sess.run```上下文存在。因此我们可以在sessionA中利用ops操作改变这个变量，进而在sessionB中使用这个变量，以此达到传递共享数值的目的。

---
###创建变量

使用```tf.get_variable(name,shape,dtype,initializer)```创建变量。

如果设定了初initializer初始化函数返回明确的值，那么不能同时使用shape参数，否则必须指定shape。

```
import tensorflow as tf
sess=tf.Session()

v1 = tf.get_variable("v1", [1, 2, 3]) #随机0～1之间
v2 = tf.get_variable("v2", [1, 2, 3],initializer=tf.zeros_initializer) #全0
v3 = tf.get_variable("v3", dtype=tf.int32,initializer=tf.constant([23, 42])) #不能同时设定shape！

init=tf.global_variables_initializer()
sess.run(init)

print(sess.run(v1))
print(sess.run(v2))
print(sess.run(v3))
```
打印结果
```
[[[-0.8628024   0.6660923   0.8403772 ]
  [-0.5985474  -0.073349    0.23826087]]]
[[[0. 0. 0.]
  [0. 0. 0.]]]
[23 42]
```
#####变量集合Variable collections
将一组变量放入集合进行管理
```
import tensorflow as tf
sess=tf.Session()

v1 = tf.get_variable("v1", [1, 2, 3])
tf.add_to_collection("mycollection", v1) #将v1放入名称为mycollection的集合

mycollection=tf.get_collection("mycollection")
print(mycollection) #一个列表

init=tf.global_variables_initializer()
sess.run(init)

print(sess.run(mycollection[0])) #获取v1
```
打印结果
```
[<tf.Variable 'v1:0' shape=(1, 2, 3) dtype=float32_ref>]
[[[-0.28881794  0.46018004 -0.83893764]
  [-0.93932706  0.84757173  0.78609943]]]
```
默认情况```tf.Variable```都会被放入两个默认的集:
* ```tf.GraphKeys.GLOBAL_VARIABLES```可用于多设备共享变量
* ```tf.GraphKeys.TRAINABLE_VARIABLES```会被计算梯度下降

也可以在创建变量的时候立即放入集合，语法：
```
my_local = tf.get_variable(name="my_local",
                                   shape=(),
                                   collections=[tf.GraphKeys.LOCAL_VARIABLES])
```
或者直接设定变量可被训练：
```
my_non_trainable = tf.get_variable("my_non_trainable",
                                   shape=(),
                                   trainable=False)
```

#####Device placement设备放置

可以把变量限定在特定设备，例如下面代码把v变量放置在GPU1下面：
```
with tf.device("/device:GPU:1"):
  v = tf.get_variable("v", [1])
```

分布式计算中变量的设备非常重要，放置不当可能导致运算缓慢甚至出错。```tf.train.replica_device_setter```方法可以自动化处理。
```
cluster_spec = {
    "ps": ["ps0:2222", "ps1:2222"],
    "worker": ["worker0:2222", "worker1:2222", "worker2:2222"]}
with tf.device(tf.train.replica_device_setter(cluster=cluster_spec)):
  v = tf.get_variable("v", shape=[20, 20])  
```
---
###初始化变量

变量在使用前必须被初始化。使用low level api的时候必须手工明确初始化，hight level api中的```tf.contrib.slim, tf.estimator.Estimator and Keras```会自动在训练前完成初始化。

* 一次性初始化所有变量```tf.global_variables_initializer()```
* 初始化单个变量```session.run(my_variable.initializer)```
* 查看哪些变量没被初始化```session.run(tf.report_uninitialized_variables())```

注意,```tf.global_variables_initializer()```初始化时候并没有固定顺序，如果某个变量依赖于其他变量的求值，那将遇到错误。当所有变量没被初始化完成的时候，用```variable.initialized_value()```来获取计算值，而不要直接使用变量。
```
v = tf.get_variable("v", shape=(), initializer=tf.zeros_initializer())
w = tf.get_variable("w", initializer=v.initialized_value() + 1)
```

---
###使用变量

在计算图中，变量可以当作```tf.tensor```张量对象使用。例如
```
v = tf.get_variable("v", shape=(), initializer=tf.zeros_initializer())
w = v + 1
```
设定变量的值，可以直接使用变量自带的方法```assign, assign_add,assign_sub```等。

```
import tensorflow as tf
sess=tf.Session()

v = tf.get_variable("v", shape=(), initializer=tf.zeros_initializer())
assignment = v.assign_add(1)

init=tf.global_variables_initializer()
sess.run(init)

print(sess.run(assignment)) #或者assignment.op.run(), 或assignment.eval()
```
输出
```
1.0
```

由于类似梯度下降算法这样的优化器会在运算时候不断修改变量，所以变量是不稳定的。我们可以用```tf.Variable.read_value```方法读取变化之后的值。
```
import tensorflow as tf
sess=tf.Session()

v = tf.get_variable("v", shape=(), initializer=tf.zeros_initializer())
assignment = v.assign_add(1)


init=tf.global_variables_initializer()
sess.run(init)

print(sess.run(v.read_value()))
with tf.control_dependencies([assignment]):
    w = v.read_value()    
    print(sess.run(w))
```
打印结果
```
0.0
1.0
```

---
###共享变量Sharing variables

Tensorflow有两种方法共享变量：
* 显式的传递```tf.Variable```对象
* 隐式的使用```tf.variable_scope```包裹```tf.variable```对象

比如下面的示意代码中，我们创建了一个卷积层（线性整流单元）：
```
def conv_relu(input, kernel_shape, bias_shape):
    # 创建变量 "weights".
    weights = tf.get_variable("weights", kernel_shape,
        initializer=tf.random_normal_initializer())
    # 创建变量"biases".
    biases = tf.get_variable("biases", bias_shape,
        initializer=tf.constant_initializer(0.0))
    conv = tf.nn.conv2d(input, weights,
        strides=[1, 1, 1, 1], padding='SAME')
    return tf.nn.relu(conv + biases)
```
上面的代码定义了conv_relu方法，其中有两个变量weight和biases。看上去很清楚，但是，当我们使用它的时候就遇到了问题：
```
input1 = tf.random_normal([1,10,10,32])
input2 = tf.random_normal([1,20,20,32])
x = conv_relu(input1, kernel_shape=[5, 5, 32, 32], bias_shape=[32])
x = conv_relu(x, kernel_shape=[5, 5, 32, 32], bias_shape = [32])  # 失败！
```
我们试图链接两个卷积层，但计算机在计算的时候无法清楚是重新创建weight和biases还是继续使用已经存在的。
下面的代码正确的创建两个卷积层，使用新的变量：
```
def my_image_filter(input_images):
    with tf.variable_scope("conv1"):
        # 这里创建的变量被重新命名为 "conv1/weights", "conv1/biases".
        relu1 = conv_relu(input_images, [5, 5, 32, 32], [32])
    with tf.variable_scope("conv2"):
        # 这里创建的变量被重新命名为 "conv2/weights", "conv2/biases".
        return conv_relu(relu1, [5, 5, 32, 32], [32])
```
如果你需要共享变量而不是重新创建，以下两种语法都可以实现：
```
with tf.variable_scope("model"):
  output1 = my_image_filter(input1)
with tf.variable_scope("model", reuse=True): #注意这里reuse=True
  output2 = my_image_filter(input2)
```
```
with tf.variable_scope("model") as scope:
  output1 = my_image_filter(input1)
  scope.reuse_variables() #注意这里！
  output2 = my_image_filter(input2)
```
其中上一种方法可以改进为
```
with tf.variable_scope("model") as scope: # 注意这里的as scope
  output1 = my_image_filter(input1)
with tf.variable_scope(scope, reuse=True): #注意这里传入的scope
  output2 = my_image_filter(input2)
```

---
###本篇小结

* 创建变量```tf.get_variable(name,shape,dtype,initializer)```
* 变量集合```tf.add_to_collection("mycollection", v1)```
* 置入不同的设备
* 变量初始化方法```tf.global_variables_initializer()```和```session.run(my_variable.initializer)```
* 使用变量
* 修改变量```assign, assign_add,assign_sub```
* 共享变量```tf.variable_scope```

---
###探索人工智能的新边界
如果您发现文章错误，请不吝留言指正；
如果您觉得有用，请点喜欢；
如果您觉得很有用，感谢转发~
---
END





