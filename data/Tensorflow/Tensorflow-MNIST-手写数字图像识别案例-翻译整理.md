本篇文章主要介绍如何创建卷积神经网络（CNN：Convolutional Neural Network）用来训练模型，识别手写数字图片。

Tensorflow的layer模型可以帮助我们方便的构建神经网络，包括密集层dense layer layer（full-connected layer全连接层）或卷积层convolutional layer。

---
##下载数据集
![](imgs/4324074-ea653013ab4a803a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

这个数据集包含了6000个训练样本和1000个测试样本，都是手写数字0~9，灰度图片28像素x28像素。

[MNIST dataset 手写数字集图片官方地址](http://yann.lecun.com/exdb/mnist/) 
[百度网盘下载，密码:w0sk](https://pan.baidu.com/s/1_Gkdf0z-NeUFH3Cc9Ue66A)

---
##代码框架
```
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

tf.logging.set_verbosity(tf.logging.INFO) #设定输出日志的模式

#我们的程序代码将放在这里

#这个文件能够直接运行，也可以作为模块被其他文件载入
if __name__ == "__main__":
  tf.app.run()
```

---
##关于卷积神经网络

卷积神经网络Convolutional neural networks (CNNs) 是目前图像识别领域最先进的模型结构。CNNs对图像应用各种过滤并从中学习得到高级结构，进而实现图像分类。

卷积神经网络包含3个组成部分：
* **Convolutional layers卷积层** 对图像应用特定数量的卷积过滤。对于每个子区域，神经层都会在输出特征映射中产生单个值，卷积层通常会将一个ReLU（Rectified Linear Units修正线性单元）激活函数应用到输出，进而在模型内产生一个非线性的结果。
![](imgs/4324074-b6712b436c2392bc.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


>**修正线性单元 (ReLU, Rectified Linear Unit)**,一种激活函数,&fnof;(x)=max(0,x),其规则如下：如果输入为负数或 0，则输出 0;如果输入为正数，则输出等于输入。ReLU属于非饱和算法non-saturating neurons，就是说没有把输出值限定在某个特定区间，与它对应的饱和算法有sigmod：&fnof;(x)=(1+e<sup>-x</sup>)<sup>-1</sup>；tanh:&fnof;(x)=|tanh(x)|,&fnof;(x)=tanh(x);

>**激活函数 (activation function)**,一种函数（例如**ReLU**或 **S型函数**），用于对上一层的所有输入求加权和，然后生成一个输出值（通常为非线性值），并将其传递给下一层。

* **Pooling layers池化层**，对卷积层提取的图像数据进行向下采样，减少特征维度，加快处理速度。常用的池化算法是最大化池化max pooling，它把输入的图像分成不重叠的子矩形区域，对每个子区域，保留最大值，忽略其他值，也控制了整体的过采样。理论基础是特征之间的关联比局部特征更加重要。
![](imgs/4324074-70ed64c8d2b3238f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

* **Dense layer密集层（full-connected layer全连接层）**，基于卷积层提取的特征和池化层的向下采样，进行分类classification。
![RoI pooling to size 2x2. In this example region proposal (an input parameter) has size 7x5.](imgs/4324074-955e8b2b868f2d83.gif?imageMogr2/auto-orient/strip)

标准意义上讲，CNN网络是组合堆叠多个卷机模块，进行特征提取。每个卷积模块包含一个卷积层以及跟随其后的池化层。最后的卷积模块跟随着一个或多个密集层以进行分类。CNN网络中最后的密集层为每个可能的分类设定了一个节点，并对这每个节点使用sigmod函数输出0~1之间的值，表示该图形属于某个分类的可能性。

---
##构建CNN MNIST分类器

1. **Convolutional Layer卷积层 #1**: 应用 32 5x5 滤镜提取5x5像素子区域，使用ReLU激活函数
1. **Pooling Layer池化层 #1**: 执行最大化池化2x2滤镜，步幅stride=2确保区域不重叠
1. **Convolutional Layer卷积层 #2**: 应用64 5x5过滤,使用ReLU激活函数
1. **Pooling Layer池化层 #2**: Again, performs max pooling with a 执行最大池化2x2过滤，步幅2
1. **Dense Layer密集层 #1**: 1,024个神经元, 丢弃正则率0.4 (训练过程中可能性低于0.4的元素将被丢弃)
1. **Dense Layer密集层 #2 (Logits Layer逻辑层)**: 10个神经元, 对应0~9数字

```tf.layers```对象包含了创建以上三种神经层的方法：
* ```conv2d()```,创建2维的卷积层，参数包含：过滤数量，过滤核心尺寸，填充padding，激活函数。
* ```max_pooling2d()```, 使用最大化算法创建一个2维池化层。参数包含：过滤尺寸、步幅。
* ```dense()```,创建密集层，参数包含：神经元数量、激活函数。

这些方法都接收一个张量tensor作为输入，然后经过变换再输出一个新的张量，这样就可以一环一环相连起来。

接下来我们向代码结构文件中添加```cnn_model_fn(features, labels, mode)```函数，它接收MNIST数据的特征、标签和mode（TRAIN,EVAL,PREDICT)，返回train训练、loss损失函数、predict预测三个方法。这是Tensorflow Estimator的标准接口。
>更多自定义Estimator的详情请看[Tensorflow-Estimator-自定义估算器](https://www.jianshu.com/p/5495f87107e7)以及[Tensorflow-Estimator-估算器-翻译整理](https://www.jianshu.com/p/8d7fa685c22f)两篇文章。

添加后的代码如下：
```
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import numpy as np
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

tf.logging.set_verbosity(tf.logging.INFO) #设定输出日志的模式

#我们的程序代码将放在这里
def cnn_model_fn(features, labels, mode):
    #输入层，-1表示自动计算，这里是图片批次大小，宽高各28，最后1表示颜色单色
    input_layer = tf.reshape(features["x"], [-1, 28, 28, 1])

    #1号卷积层，过滤32次，核心区域5x5，激活函数relu
    conv1 = tf.layers.conv2d(
        inputs=input_layer,#接收上面创建的输入层输出的张量
        filters=32,
        kernel_size=[5, 5],
        padding="same",
        activation=tf.nn.relu)

    #1号池化层，接收1号卷积层输出的张量
    pool1 = tf.layers.max_pooling2d(inputs=conv1, pool_size=[2, 2], strides=2)

    #2号卷积层
    conv2 = tf.layers.conv2d(
        inputs=pool1,#继续1号池化层的输出
        filters=64,
        kernel_size=[5, 5],
        padding="same",
        activation=tf.nn.relu)
    
    #2号池化层
    pool2 = tf.layers.max_pooling2d(inputs=conv2, pool_size=[2, 2], strides=2)

    #对2号池化层的输入变换张量形状
    pool2_flat = tf.reshape(pool2, [-1, 7 * 7 * 64])
    
    #密度层
    dense = tf.layers.dense(inputs=pool2_flat, units=1024, activation=tf.nn.relu)
    
    #丢弃层进行简化
    dropout = tf.layers.dropout(
      inputs=dense, rate=0.4, training=mode == tf.estimator.ModeKeys.TRAIN)

    #使用密度层作为最终输出，unit可能的分类数量
    logits = tf.layers.dense(inputs=dropout, units=10)
    
    #预测和评价使用的输出数据内容
    predictions = {
      #产生预测，argmax输出第一个轴向的最大数值
      "classes": tf.argmax(input=logits, axis=1),
      #输出可能性
      "probabilities": tf.nn.softmax(logits, name="softmax_tensor")
    }

    #以下是根据mode切换的三个不同的方法，都返回tf.estimator.EstimatorSpec对象
  
    #预测
    if mode == tf.estimator.ModeKeys.PREDICT:
        return tf.estimator.EstimatorSpec(mode=mode, predictions=predictions)

    #损失函数(训练与评价使用)，稀疏柔性最大值交叉熵
    loss = tf.losses.sparse_softmax_cross_entropy(labels=labels, logits=logits)

    #训练，使用梯度下降优化器，
    if mode == tf.estimator.ModeKeys.TRAIN:
        optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.001)
        train_op = optimizer.minimize(
            loss=loss,
            global_step=tf.train.get_global_step())
        return tf.estimator.EstimatorSpec(mode=mode, loss=loss, train_op=train_op)

    #评价函数（上面两个mode之外else）添加评价度量(for EVAL mode)
    eval_metric_ops = {
        "accuracy": tf.metrics.accuracy(
            labels=labels, predictions=predictions["classes"])}
    return tf.estimator.EstimatorSpec(
        mode=mode, loss=loss, eval_metric_ops=eval_metric_ops)



#这个文件能够直接运行，也可以作为模块被其他文件载入
if __name__ == "__main__":
  tf.app.run()
```

这时候以上代码还不能运行。以下将逐个代码块详细解说。

---
####Input Layer输入层

```tf.layers```中创建神经层的方法参数格式是：
```[batch_size,imgage_width,imgage_height,channels]```
* **batch_size批次尺寸**,在训练过程中梯度下降所使用的样本子集的大小。
* **image_width和image_height**,图像的宽高。
* **channels通道**,图片像素的颜色通道数，一般是3（RGB），在这里是黑白图片只有1个颜色。

MNIST的图片是28x28单色，[batch_size,28,28,1],我们用-1表示依靠features['x']数量动态计算得到这个数值，那么把它变换一下：
#### ```input_layer = tf.reshape(features["x"], [-1, 28, 28, 1])```
在这里batch_size作为一个超参数hyperparameters，如果我们使用batch_size=5，那么input_layers的形状就是[5,28,28,1],它将包含5x28x28x1=3920个值，每个值表示一个颜色，每784个值表示一张图，5张为一批次。


---
#### Convolutional layer #1卷积层1号

```
conv1 = tf.layers.conv2d(
    inputs=input_layer,
    filters=32,
    kernel_size=[5, 5],
    padding="same",
    activation=tf.nn.relu)
```
我们使用了32次5x5像素过滤filters，使用ReLU作为激活函数。由于承接了input_layer的输出，所以进入的张量形状是[batch_size,28,28,1].
padding参数有两个可选，默认的"valid"或"same"，为了保持输出的宽高不变，我们选择了"same",Tensorflow会自动用0补齐以确保图像是28x28像素。(如果不使用padding，那么在28x28个网格中只有24x24的区域可以放置5x5的面片，如下图所示黄色区域，也就是会产生24x24的张量。)

![](imgs/4324074-efad3fc01ac94cb7.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

激活函数ReLU将应用在卷积输出的张量上。最终从conv2d层输出的张量形状是[batch_size,28,28,32],这里的32是指我们进行了32次过滤产生的不同结果。

---
####Pooling Layer #1池化层1号

####```pool1 = tf.layers.max_pooling2d(inputs=conv1, pool_size=[2, 2], strides=2)```
conv1作为输入层，将会输入的张量形状是[batch_size,28,28,32]。
pool_size设定了最大池化过滤的尺寸[width,height]就是[2,2]。
stredes表示过滤的步长，我们这里设定了stredes=2，表示滤镜对子区域subregions进行提取是按照宽高分别间隔2像素进行的，由于过滤尺寸也是[2,2],所以不会产生重叠也不会产生丢失。
![](imgs/4324074-7f7c4e7fb383118d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![](imgs/4324074-08a16b2ad18c0760.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

max_pooling层pool1输出的张量形状是[batch_size,14,14,32],因为2x2过滤把宽高减少了一半。

---
##Convolutional layer #2 & Pooling layer #2卷积层2号和池化层2号

```
conv2 = tf.layers.conv2d(
    inputs=pool1,
    filters=64,
    kernel_size=[5, 5],
    padding="same",
    activation=tf.nn.relu)

pool2 = tf.layers.max_pooling2d(inputs=conv2, pool_size=[2, 2], strides=2)
```
2号卷积层我们使用了64次5x5区域的过滤，仍然是ReLU激活函数。而2号池化层我们仍然使用了[2,2]区域2步幅间隔的设定。

注意2号卷积层设定了padding="same"且64次过滤，所以输出的张量形状是[batch_size,14,14,64]。
池化层2号则再次把维度降低到[batch_size,7,7,64]。

---
####Dense layer密集层

接下来我们将添加一个1024神经元ReLU激活的密集层（全连接层），基于上面卷积层和池化层得到的结果进行分类。

首先，我们把上面pool2池化层得到的特征映射features map([batch_size,7,7,64])展开，转换到[batch_size,features]。

####```pool2_flat = tf.reshape(pool2, [-1, 7 * 7 * 64])```

-1表示这个维度根据计算得到，在这里我们将得到一个[batch_size,3136]的张量（7*7*64=3136）。

然后我们再把这个结果传递到密集层Dense layer：

####```dense = tf.layers.dense(inputs=pool2_flat, units=1024, activation=tf.nn.relu)```

为了改进我们模型的结果，增加一个dropout丢弃规则，
```
dropout = tf.layers.dropout(
    inputs=dense, rate=0.4, training=mode == tf.estimator.ModeKeys.TRAIN)
```
这里rate=0.4表示在训练过程中，40%的元素会被随机丢弃。注意training参数限定了尽在训练模式下才执行随机丢弃，预测和评价时候不丢弃。

最终，由于使用了1024个神经元，dropout输出的张量形状是[batch_size,1024]。

---
####Logits layer逻辑层

逻辑层是我们神经网络的最后一层，他将输出预测的原始数据。我们使用dense创建了10个神经元的密集层，表示0~9个数字，使用默认的linear线性激活函数。

####```logits = tf.layers.dense(inputs=dropout, units=10)```

这样，我们的CNN卷积神经网络最后输出的张量形状就是[batch_size,10]。

---
####生成预测函数

以上，逻辑层生成的张量是[batch_size,10]。我们用两个函数将这个原始数据转为两个不同的格式，作为最终的预测结果：
* **每个样本的预测分类predicted class**,0~9中的一个数字。
* **每个样本属于每个分类的可能性probabilities**，样本可能是0，可能是1，可能是2，可能是...

####```tf.argmax(input=logits, axis=1)```

对于我们这个案例，每个样本的预测分类，就是逻辑层输出张量中对应行中值最高的元素。我们使用argmax方法取得它：

####```tf.argmax(input=logits, axis=1)```
注意这里axis等于1而不是0，因为我们从逻辑层获得的张量形状是[batch_size,10]，也就是10对应的列中每个元素，选取值最大的元素返回。

我们把预测结果封装到一个字典,放入EstimatorSpec对象：
```python
predictions = {
    "classes": tf.argmax(input=logits, axis=1),
    "probabilities": tf.nn.softmax(logits, name="softmax_tensor")
}
if mode == tf.estimator.ModeKeys.PREDICT:
  return tf.estimator.EstimatorSpec(mode=mode, predictions=predictions)
```

---
####Calculate loss计算损失函数

对于训练和预测，我们需要定义一个损失函数loss function来评估我们的模型预测的有多么准确。对于多个类别的分类问题，交叉熵算法是最常用的测量标准。
```
onehot_labels = tf.one_hot(indices=tf.cast(labels, tf.int32), depth=10)
loss = tf.losses.softmax_cross_entropy(
    onehot_labels=onehot_labels, logits=logits)
```
这里cast是转变数据类型的方法，labels的数据类似[1, 9, 6,7,3...]，我们把它转为one_hot独热格式的张量:
```
[[0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
 ...]
```

```tf.one_hot```带有两个参数：
* **indices索引**，独热数组哪一个热，比如上面第一行对应的labels是1，就是第1个是1（其他都是0）；
* **depth深度**，独热数组有多少个元素，在这里就是有多少个分类。

然后，我们计算onehot_labels和逻辑层输出的张量[batch_size,10]的这两者的柔性最大交叉熵。
```
loss = tf.losses.softmax_cross_entropy(
    onehot_labels=onehot_labels, logits=logits)
```
```tf.losses.softmax_cross_entropy```方法返回一个标量scalar张量。

---
####设置训练操作Configure the training Op

在以上，我们定义了loss函数用于评估我们预测模型最终logits层输出的结果与实际标签labels的差异度，下面让我们的模型在训练的时候反复优化这个差异度，让模型达到最佳。
我们使用随机梯度下降函数stochastic gradient desent作为优化算法，使用学习率learning_rate=0.1：
```python
if mode == tf.estimator.ModeKeys.TRAIN:
  optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.001)
  train_op = optimizer.minimize(
      loss=loss,
      global_step=tf.train.get_global_step())
  return tf.estimator.EstimatorSpec(mode=mode, loss=loss, train_op=train_op)
```
在这里，我们看到，所谓的训练操作train_op就是优化函数optimizer根据损失函数loss，一步一步尝试构造更好的模型结构。

---
####添加评价度量Evaluation metrics

```python
eval_metric_ops = {
    "accuracy": tf.metrics.accuracy(
        labels=labels, predictions=predictions["classes"])}
return tf.estimator.EstimatorSpec(
    mode=mode, loss=loss, eval_metric_ops=eval_metric_ops)
```


---
##训练和评价CNN MNIST分类器

上面我们已经完成了CNN MNIST模型函数的编写，下面我们继续实现模型的训练和预测。

---
####载入训练和测试数据

首先从把从[百度网盘（密码:w0sk）](https://pan.baidu.com/s/1_Gkdf0z-NeUFH3Cc9Ue66A)下载的MNIST_data文件夹（包含四个文件）放在和我们的代码相同目录下。

![](imgs/4324074-9fb9e3f4e61321ab.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


然后我们添加main主函数，代码载入数据集
```
dir_path = os.path.dirname(os.path.realpath(__file__))
data_path=os.path.join(dir_path,'MNIST_data')
def main(args):
    #载入训练和测试数据
    mnist = input_data.read_data_sets(data_path)
    train_data = mnist.train.images #得到np.array
    train_labels = np.asarray(mnist.train.labels, dtype=np.int32)
    eval_data = mnist.test.images #得到np.array
    eval_labels = np.asarray(mnist.test.labels, dtype=np.int32)
```

>你也可以参照  [这篇文章](https://www.jianshu.com/p/a19fbde26670)  自己手工从官方下载这个数据集。

---
####创建估算器Estimator

Estimator是Tensorflow的一个高级接口high-level API，专门用来对模型进行训练、和评估和预测的。

在main里面添加下面的代码
```
    #创建估算器
    mnist_classifier = tf.estimator.Estimator(
        model_fn=cnn_model_fn, model_dir="/tmp/mnist_convnet_model")
```
这里使用的两个参数：
* **model_fn**，我们在上面创建神经网络CNN的主要函数，里面实现了训练、评价和预测功能。
* **model_dir**，这是设置我们训练出来的模型存储的目录，只要这里设置一次，以后Tensorflow都会自动从这里读取我们训练好的模型，不需要我们添加任何其他代码。当然也可以再训练，会覆盖更新。

---
####设置日志钩子logging hook

CNN训练需要花一点时间，呆看屏幕没有任何反应等待会很难熬，我们可以让Tensorflow在训练的时候输出一些有用的日志信息。

```
    #设置输出预测的日志
    tensors_to_log = {"probabilities": "softmax_tensor"}
    logging_hook = tf.train.LoggingTensorHook(
        tensors=tensors_to_log, every_n_iter=50)
```
我们在这里用tensors_to_log字典来存储需要打印出来的数据，注意这里的softmax_tensor，实际是我们在上面定义过的名称（实际上我们在编写整个计算模型时候定义的张量name都可以）：
```
predictions = {
      "classes": tf.argmax(input=logits, axis=1),
      "probabilities": tf.nn.softmax(logits, name="softmax_tensor")
    }
```
然后，我们创建了钩子函数LoggingTensorHook，并关联到我们的需要输出的张量，每50次迭代打印一次。

---
####训练模型

为了训练模型，我们必须创建一个喂食数据的函数train_input_fn,向main函数添加以下代码：
```
    #训练喂食函数
    train_input_fn = tf.estimator.inputs.numpy_input_fn(
        x={"x": train_data},
        y=train_labels,
        batch_size=100,
        num_epochs=None,
        shuffle=True)
```
我们使用了```numpy_input_fn```方法，它的参数里面xy对应了我们的训练特征数据和训练标签数据，batch_size表示每步数step最少训练100个样本，num_epochs=None周期数不设定表示我们一直训练直到到达指定步数为止（训练时候设定）。shuffle=true洗牌为真表示我们将随机调整样品顺序。

我们再向main函数添加代码启动训练：
```
    #启动训练
    mnist_classifier.train(
        input_fn=train_input_fn,
        steps=20000,
        hooks=[logging_hook])
```
在这里我们设定了步数20000，并且把日志钩子logging_hook传递进去。

不要着急，我们先继续添加一些其他内容。

---
####评价模型Evaluate model

训练完成后，我们希望使用测试数据集来评估一下我们的模型的精确度，看它是否足够好。继续向main函数添加下面的代码:
```
    #评价喂食函数
    eval_input_fn = tf.estimator.inputs.numpy_input_fn(
        x={"x": eval_data},
        y=eval_labels,
        num_epochs=1,
        shuffle=False)
    
    #启动评价并输出结果
    eval_results = mnist_classifier.evaluate(input_fn=eval_input_fn)
    print(eval_results)
```
同样，我们也需要一个评价喂食函数，不断把需要评价的图片数据输入到模型，然后再把模型输出的预测结果和我们真实的标签对比，这样就能知道我们的模型是不是足够准确。
注意在这里我没设置周期是1，不进行反复训练；设置shuffle=False也不随机调整顺序。

---
####运行吧！

整个过程可能需要一些时间，不要着急，训练20000步数会很慢，请耐心等候。

续，十多分钟过去了，目前才到step3000多...求祝福，求光环...
续，我也不知道最终用了多久，大概1个多小时，这是运行后的结果,精度接近97%：
```
INFO:tensorflow:Saving dict for global step 20004: accuracy = 0.9691, global_step = 20004, loss = 0.10082044
{'accuracy': 0.9691, 'loss': 0.10082044, 'global_step': 20004}
```


下面是完整代码,如果你的代码运行中出现问题，可以复制它：
```
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import numpy as np
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

tf.logging.set_verbosity(tf.logging.INFO) #设定输出日志的模式

#我们的程序代码将放在这里
def cnn_model_fn(features, labels, mode):
    #输入层，-1表示自动计算，这里是图片批次大小，宽高各28，最后1表示颜色单色
    input_layer = tf.reshape(features["x"], [-1, 28, 28, 1])

    #1号卷积层，过滤32次，核心区域5x5，激活函数relu
    conv1 = tf.layers.conv2d(
        inputs=input_layer,#接收上面创建的输入层输出的张量
        filters=32,
        kernel_size=[5, 5],
        padding="same",
        activation=tf.nn.relu)

    #1号池化层，接收1号卷积层输出的张量
    pool1 = tf.layers.max_pooling2d(inputs=conv1, pool_size=[2, 2], strides=2)

    #2号卷积层
    conv2 = tf.layers.conv2d(
        inputs=pool1,#继续1号池化层的输出
        filters=64,
        kernel_size=[5, 5],
        padding="same",
        activation=tf.nn.relu)
    
    #2号池化层
    pool2 = tf.layers.max_pooling2d(inputs=conv2, pool_size=[2, 2], strides=2)

    #对2号池化层的输入变换张量形状
    pool2_flat = tf.reshape(pool2, [-1, 7 * 7 * 64])
    
    #密度层
    dense = tf.layers.dense(inputs=pool2_flat, units=1024, activation=tf.nn.relu)
    
    #丢弃层进行简化
    dropout = tf.layers.dropout(
      inputs=dense, rate=0.4, training=mode == tf.estimator.ModeKeys.TRAIN)

    #使用密度层作为最终输出，unit可能的分类数量
    logits = tf.layers.dense(inputs=dropout, units=10)
    
    #预测和评价使用的输出数据内容
    predictions = {
      #产生预测，argmax输出第一个轴向的最大数值
      "classes": tf.argmax(input=logits, axis=1),
      #输出可能性
      "probabilities": tf.nn.softmax(logits, name="softmax_tensor")
    }

    #以下是根据mode切换的三个不同的方法，都返回tf.estimator.EstimatorSpec对象
  
    #预测
    if mode == tf.estimator.ModeKeys.PREDICT:
        return tf.estimator.EstimatorSpec(mode=mode, predictions=predictions)

    #损失函数(训练与评价使用)，稀疏柔性最大值交叉熵
    loss = tf.losses.sparse_softmax_cross_entropy(labels=labels, logits=logits)

    #训练，使用梯度下降优化器，
    if mode == tf.estimator.ModeKeys.TRAIN:
        optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.001)
        train_op = optimizer.minimize(
            loss=loss,
            global_step=tf.train.get_global_step())
        return tf.estimator.EstimatorSpec(mode=mode, loss=loss, train_op=train_op)

    #评价函数（上面两个mode之外else）添加评价度量(for EVAL mode)
    eval_metric_ops = {
        "accuracy": tf.metrics.accuracy(
            labels=labels, predictions=predictions["classes"])}
    return tf.estimator.EstimatorSpec(
        mode=mode, loss=loss, eval_metric_ops=eval_metric_ops)



dir_path = os.path.dirname(os.path.realpath(__file__))
data_path=os.path.join(dir_path,'MNIST_data')
def main(args):
  #载入训练和测试数据
    mnist = input_data.read_data_sets(data_path)
    train_data = mnist.train.images #得到np.array
    train_labels = np.asarray(mnist.train.labels, dtype=np.int32)
    eval_data = mnist.test.images #得到np.array
    eval_labels = np.asarray(mnist.test.labels, dtype=np.int32)
    
    #创建估算器
    mnist_classifier = tf.estimator.Estimator(
        model_fn=cnn_model_fn, model_dir="/tmp/mnist_convnet_model")
    
    #设置输出预测的日志
    tensors_to_log = {"probabilities": "softmax_tensor"}
    logging_hook = tf.train.LoggingTensorHook(
        tensors=tensors_to_log, every_n_iter=50)
    
    #训练喂食函数
    train_input_fn = tf.estimator.inputs.numpy_input_fn(
        x={"x": train_data},
        y=train_labels,
        batch_size=100,
        num_epochs=None,
        shuffle=True)
    
    #启动训练
    mnist_classifier.train(
        input_fn=train_input_fn,
        steps=20000,
        hooks=[logging_hook])
    
    #评价喂食函数
    eval_input_fn = tf.estimator.inputs.numpy_input_fn(
        x={"x": eval_data},
        y=eval_labels,
        num_epochs=1,
        shuffle=False)
    
    #启动评价并输出结果
    eval_results = mnist_classifier.evaluate(input_fn=eval_input_fn)
    print(eval_results)    


#这个文件能够直接运行，也可以作为模块被其他文件载入
if __name__== "__main__":
    tf.app.run()
```

---
###探索人工智能的新边界
如果您发现文章错误，请不吝留言指正；
如果您觉得有用，请点喜欢；
如果您觉得很有用，感谢转发~
---
END





