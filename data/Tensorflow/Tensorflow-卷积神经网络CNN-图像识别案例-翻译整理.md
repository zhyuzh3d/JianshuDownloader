这个案例是针对CIFAR-10图像集进行分类的练习，将会使用6万张图像进行训练和测试共10个分类。

---
##准备工作

下载CIFAR-10图片素材文件

[百度云下载链接](https://pan.baidu.com/s/17z4Agw2Lz7PFYxRUwrca5g)(密码:ar1q)

[官方下载页面](https://www.cs.toronto.edu/~kriz/cifar.html)(只需要下载Python版本)

这个数据集共包含了10个分类60000张图片，每个分类10000张。

十个分类是：
airplane, automobile, bird, cat, deer, dog, frog, horse, ship, and truck.

---
##案例概要

我们的目标是基于这些图片训练一个模型，能够识别任意图片属于哪一个分类：
* 创建一个典型的神经网络结构，用于训练和评估
* 构建一个模板可以用于更加复杂更加庞大的情况

####这个教程中将包含
* 核心数学元素，包括卷积convolution，修正的线性激活rectified linear activation，最大池化max pooling，局部相应标准化local response normalization等。
* 训练过程中视觉化网络状况，包含输入图像、损失函数、激活分支与梯度。
* 对学习得到的参数计算移动平均值，并在评估中使用，进而提升预测性能。
* 实现一个全时段系统化缩减的学习率进度。
* 对输入数据进行预取prefetch，隔离模型硬盘读取和昂贵的图像预处理。
* 设置多CPU平行运算，共享与更新多GPU运算中的变量。


####模型架构
这是一个由卷积层和非线性层交替组合成的多层结构。这些层之后使用全连接层导向最终的一个softmax分类器。
通过几个小时的GPU运算，这个模型可以最多达到86%的准确率，它由100多万个参数构成，推测一张图片需要19.5M累加命令操作。

---
##代码说明
[Github代码地址](https://github.com/tensorflow/models/tree/master/tutorials/image/cifar10/)

* [cifar10_input.py](https://github.com/tensorflow/models/blob/master/tutorials/image/cifar10/cifar10_input.py "cifar10_input.py")，读取本地CIFAR-10二进制数据文件
* [cifar10.py](https://github.com/tensorflow/models/blob/master/tutorials/image/cifar10/cifar10.py "cifar10.py")，构建模型
* [cifar10_train.py](https://github.com/tensorflow/models/blob/master/tutorials/image/cifar10/cifar10_train.py "cifar10_train.py")，训练模型（CPU或GPU）
* [cifar10_multi_gpu_train.py](https://github.com/tensorflow/models/blob/master/tutorials/image/cifar10/cifar10_multi_gpu_train.py "cifar10_multi_gpu_train.py")，在多GPU上进行计算
* [cifar10_eval.py](https://github.com/tensorflow/models/blob/master/tutorials/image/cifar10/cifar10_eval.py "cifar10_eval.py")，评价预测的准确性


---
##CIFAR-10 模型

请参照[cifar10.py](https://github.com/tensorflow/models/blob/master/tutorials/image/cifar10/cifar10.py)
这个模型包含了765个操作，我们可以通过下面这些模块重新构造整个计算图：
* Model inputs，inputs() 和 distorted_inputs()方法添加读取和处理图像的操作，为后面训练和评价做准备。
* Model prediction，inference()方法添加分类操作。
* Model training，loss()和train()提供计算损失、梯度、变量更新功能，并且视觉化统计信息。

####模型输入Model inputs
[参照cifar10_input.py](https://github.com/tensorflow/models/blob/master/tutorials/image/cifar10/cifar10_input.py)。
inputs() 和distorted_inputs()负责读从二进制图像数据读取文件。由于这些文件包含固定的长度，所以使用tf.FixedLengthRecordReader读取。

图像处理过程包括，参照```inputs```方法的定义。
* 将图片裁切到24x24像素，评价时候使用图片的中心部分，训练时候使用随机位置。使用```tf.image.resize_image_with_crop_or_pad ```方法。
* 将图片变亮漂白，这样可以使模型对颜色变化不敏感。使用```tf.image.per_image_standardization```方法。

针对训练，我们添加一系列的扰乱，这样可以使数据集变大。参照```distorted_inputs```方法的定义。
* 随机左右翻转。使用```tf.random_crop```和```tf.image.random_flip_left_right```。
* 随机改变图像的亮度。```tf.image.random_brightness```.
* 随机改变图像的对比度。```tf.image.random_contrast```.

在```_generate_image_and_label_batch```中，我们把图像附加到统计概要中，```tf.summary.image('images', images)```，这样就可以在tensorboard中看到被调整后的图片效果。
![](imgs/4324074-49f26ab359951809.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

####模型预测Model Prediction
请参照[cifar10.py](https://github.com/tensorflow/models/blob/master/tutorials/image/cifar10/cifar10.py)
预测的实现主要在```inference()```函数里。
整个模型主要由以下操作组成：
* conv1，卷积层和线性修正作为激活。
* pool1，最大池化层。
* norm1，局部反应标准化LRN(Local Response Normalization)。
* conv2，卷积层和线性修正作为激活。
* norm2，局部反应标准化LNR。
* pool，最大池化层。
* local3，使用RELU激活的全连接层。
* local4，使用RELU激活的全连接层。
* softmax_linear，线性转换校正值（未归一化）。

示意图如下：
![](imgs/4324074-8471c6b4da2fdd5e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

####模型训练Model Training
训练神经网络识别N种类型的常用方法是multinomial logistic regression多项逻辑回归，也就是softmax regression。Softmax对网络输出应用softmax非线性化，并且计算预测结果和标签之间的交叉熵。为了规则化，我们对全部学习到的变量应用权重衰减损失weight decay losses。模型的函数就是计算全部交叉熵损失与权重衰减的和，就如```loss()```方法返回的那样。
我们使用tf.summary.scalar把它显示在TensorBoard中：
![](imgs/4324074-a38b24b4ac21a76e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

我们全程使用带有指数衰减exponentially decay学习率learning rate的标准的梯度下降算法gradient desenet algorithm。
![](imgs/4324074-59449db4918e5fe9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

```train()```函数添加操作，使梯度下降计算的目标最小化，并更新学习到的权重变量。（参照tf.train.GradientDescentOptimizer）它返回一个操作，这个操作将执行训练train需要的全部操作，并使用一个图片批次batch images来更新模型。

---
##加载和训练模型Launch and Trainning model
命令行中执行命令开始训练
```python cifar10_train.py```。
输出如下内容
```
Filling queue with 20000 CIFAR images before starting to train. This will take a few minutes.
2015-11-04 11:45:45.927302: step 0, loss = 4.68 (2.0 examples/sec; 64.221 sec/batch)
2015-11-04 11:45:49.133065: step 10, loss = 4.66 (533.8 examples/sec; 0.240 sec/batch)
2015-11-04 11:45:51.397710: step 20, loss = 4.64 (597.4 examples/sec; 0.214 sec/batch)
2015-11-04 11:45:54.446850: step 30, loss = 4.62 (391.0 examples/sec; 0.327 sec/batch)
2015-11-04 11:45:57.152676: step 40, loss = 4.61 (430.2 examples/sec; 0.298 sec/batch)
2015-11-04 11:46:00.437717: step 50, loss = 4.59 (406.4 examples/sec; 0.315 sec/batch)
...
```
这个脚本每10步报告一次total losss直到处理完成。一些小提示：
* 第一批次数据非常的慢，可能需要几分钟。因为需要对20000张处理好的图片进行洗牌shuffle。
* 报告的损失是整批次的平均损失，这个损失是交叉熵corss entropy和所有权重衰减weight decay的和。
* 留意每个批次的处理速度。上面显示的截图是运行在GPU上的（Tesla K40c），使用CPU会慢很多。
* 如果第一批次实在太慢，可以降低初始化填充队列的图片数量，在cifar10_input.py中修改min_fraction_of_examples_in_queue值。

cifar10_train.py会自动不定期的保存chekpoint检查点文件，但不会对模型计算评价evaluate，但检查点文件将被cifar10_eval.py使用。

cifar10_train.py最终报告的文字可以观察到训练的过程，我们可以通过tf.summary.FileWriter将更多内容显示到TensorBoard。
* loss值是逐渐减少的还是仅仅是噪波扰动？
* 是否提供合适的图片给模型进行训练？
* 梯度gradient、权重weight、激活函数activation的数值是否都合理？
* 当前的学习率learning rate是多少？
![](imgs/4324074-d9010b69beb16a67.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![](imgs/4324074-232f21a227f7b712.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

---
##评价模型Evaluate Model
接下来我们使用cifar10_eval.py来评价得到的模型是否足够有效。它使用inference()方法构建模型，并使用10000张图片进行评价。它以精密度precision=1为标准计算预测结果和实际图片标签之间的差距。

cifar10_eval.py使用之前训练的checkpoint检查点进行评价。命令行执行下面命令：
```python cifar10_eval.py```
应该可以得到类似下面的输出：
```
2015-11-06 08:30:44.391206: precision @ 1 = 0.860
...
```
仅显示精准度，同时也会显示在TensorBorad中。
训练脚本计算了所有学习得到的变量的移动平均Moving average值，评价脚本使用这个移动平均版本替换模型的所有参数。

---
##使用多GPU卡进行计算Training a Model Using Multiple GPU Cards
...略...

---
###探索人工智能的新边界
如果您发现文章错误，请不吝留言指正；
如果您觉得有用，请点喜欢；
如果您觉得很有用，感谢转发~
---
END









