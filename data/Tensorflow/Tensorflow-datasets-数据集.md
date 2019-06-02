
tf.data包含了对数据进行读取、操作、输入模型的各种方法。

---

####理解流程

在[鸢尾花案例](https://www.jianshu.com/p/b86c020747f9)中的train_input_fn喂食函数中，使用了tf.data对数据进行处理：
```
#针对训练的喂食函数
def train_input_fn(features, labels, batch_size):
    dataset = tf.data.Dataset.from_tensor_slices((dict(features), labels))
    dataset = dataset.shuffle(1000).repeat().batch(batch_size) #每次随机调整数据顺序
    return dataset
```
这个train_input_fn输入函数后面被train使用：
```
#开始训练模型！
batch_size=100
classifier.train(input_fn=lambda:train_input_fn(train_x, train_y,batch_size),
                 steps=1000)
```
由此可见，train_input_fn可以把特征数据features(train_x)和标签数据labels(train_y)联合成一个dataset，以供分类器的训练函数train使用。

我们print(train_x):
```
     SepalLength  SepalWidth  PetalLength  PetalWidth
0            6.4         2.8          5.6         2.2
1            5.0         2.3          3.3         1.0
2            4.9         2.5          4.5         1.7
...
```
print(train_y)，左侧是序号，右侧是花的类型0、1、2
```
0      2
1      1
2      2
...
```
下面分别介绍train_input_fn的三个参数

---
####特征数据Features
*  features：包含单个列表字段的字典dict，格式如{'feature_name':[]}；或者pandas.DataFrame对象。

>pandas.DataFrame(data,index,columns,dtype,copy)语法
data:dict,numpy ndarray或DataFrame
index,columns:Index或类似数组
dtype:数值类型，默认None会进行自动推断
copy:布尔值，是否从输入拷贝

```
#测试DataFrame
import pandas as pd
import numpy as np
d = {'col1': [1, 2], 'col2': [3, 4]}
df = pd.DataFrame(data=d, dtype=np.int8)
d2=np.random.randint(low=0, high=10, size=(5, 5))
df2 = pd.DataFrame(d2,columns=['a', 'b', 'c', 'd', 'e'])

print(df,'\n',d2,'\n',df2)
```
输出可以看到DataFrame的基本样式：
```shell
#df
     col1  col2
0     1     3
1     2     4 

#d2
 [[2 4 6 4 2]
 [9 4 5 0 3]
 [1 5 1 4 5]
 [9 3 8 0 1]
 [1 3 0 5 0]] 

#df2
   a  b  c  d  e
0  2  4  6  4  2
1  9  4  5  0  3
2  1  5  1  4  5
3  9  3  8  0  1
4  1  3  0  5  0
```
实际上鸢尾花案例中的train_x就是pandas.read_csv生成的DataFrame对象
```
#载入训练数据
train = pd.read_csv(train_path, names=FUTURES, header=0)
train_x, train_y = train, train.pop('Species')
```

---
####标签数据Labels
标签数据应该是一个数组，依照特征数据的顺序为每个样本example做了标记。在鸢尾花案例中就是用0、1、2标记了每朵鸢尾花的类型。

---
####批次尺寸Batch_size
批次尺寸必须是一个整数，对模型训练中的梯度下降运算效率有影响。建议不要超过样本数量，32，64，128...

---
####切片Slices
在鸢尾花案例中使用了tf.data.Dataset.from_tensor_slices方法，它得到一个tf.data.Dataset对象：
```
def train_input_fn(features, labels, batch_size):
    dataset = tf.data.Dataset.from_tensor_slices((dict(features), labels))
    print(dataset)
    ...
```
打印出来得到一个TensorSliceDataset对象,里面包含了特征列名称和数值类型：
```xml
<TensorSliceDataset
    shapes: (
        {
          SepalLength: (), PetalWidth: (),
          PetalLength: (), SepalWidth: ()},
        ()),
    types: (
        {
          SepalLength: tf.float64, PetalWidth: tf.float64,
          PetalLength: tf.float64, SepalWidth: tf.float64},
        tf.int64)>
```
如果我们有个数据的形状shape是(100,28,28),那么就可以把它切成100百个切片，每个切片是28x28的矩阵。

---
####操作数据

Dataset将按照固定顺序进行迭代，每次生成一个元素。
然后我们用下面的方法对数据进行了处理:
```
    dataset = dataset.shuffle(1000).repeat().batch(batch_size) 
```
shuffle,随机扰乱数据，1000表示使用的缓存数量，必须比样本数量大才有意义。
repeat,重复，达到数据尾端然后再返回，如果要限定周期数量，可以添加count参数。
batch，批次，将样本进行堆叠，比如把100个(28,28)的二维数据可以堆叠成(100,28,28)的三维数据。
如下，batch之后print(dataset),输出中出现了问号，这是由于反复分批次堆叠处理之后，最后一批的数量并不确定和之前每批次一样多。
```
<TensorSliceDataset
    shapes: (
        {
          SepalLength: (?,), PetalWidth: (?,),
          PetalLength: (?,), SepalWidth: (?,)},
        (?,)),

    types: (
        {
          SepalLength: tf.float64, PetalWidth: tf.float64,
          PetalLength: tf.float64, SepalWidth: tf.float64},
        tf.int64)>
```
---
####张量Tensor

######张量是TensorFlow 程序中的主要数据结构。张量是 N 维（其中 N 可能非常大）数据结构，最常见的是标量、向量或矩阵。张量的元素可以包含整数值、浮点值或字符串值。

Tensor包含两个属性：
* 数据类型(例如float32, int32, or string等)
* 数据形状(定义数据的维数，特征数据中得到或运算时得到)

Tensor内的每个数据元素都具有相同的确定类型。
Tensor的维度又叫做等级rank：
 >Rank	Math entity
0	标量Scalar (只有大小之分)
1	向量Vector (有大小和方向的区别)
2	矩阵Matrix (数字组成的表)
3	3-Tensor (数字立方体)
n	n-Tensor (...)

```
#rank0
mammal = tf.Variable("Elephant", tf.string)
ignition = tf.Variable(451, tf.int16)
floating = tf.Variable(3.14159265359, tf.float64)
its_complicated = tf.Variable(12.3 - 4.85j, tf.complex64)

#rank 1
mystr = tf.Variable(["Hello"], tf.string)
cool_numbers  = tf.Variable([3.14159, 2.71828], tf.float32)
first_primes = tf.Variable([2, 3, 5, 7, 11], tf.int32)
its_very_complicated = tf.Variable([12.3 - 4.85j, 7.5 - 6.23j], tf.complex64)

#更高rank
mymat = tf.Variable([[7],[11]], tf.int16)
myxor = tf.Variable([[False, True],[True, False]], tf.bool)
linear_squares = tf.Variable([[4], [9], [16], [25]], tf.int32)
squarish_squares = tf.Variable([ [4, 9], [16, 25] ], tf.int32)
mymatC = tf.Variable([[7],[11]], tf.int32)
```
表示多张图片数据的rank4张量(数量X宽X高X颜色)
```
my_image = tf.zeros([10, 299, 299, 3])  # batch x height x width x color
```
可以用[n,m]方法获得张量的特定切片
```
my_scalar = my_vector[2]
my_scalar = my_matrix[1, 2] #得到的是rank0标量
my_row_vector = my_matrix[2] #得到的是rank1向量
my_column_vector = my_matrix[:, 3] #得到一整列向量
```
张量的形状shape是指张量每个元素的维数。
![张量的形状、层级、维度](imgs/4324074-fe00ccede90172b4.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

---
###探索人工智能的新边界
如果您发现文章错误，请不吝留言指正；
如果您觉得有用，请点喜欢；
如果您觉得很有用，感谢转发~
---
END





