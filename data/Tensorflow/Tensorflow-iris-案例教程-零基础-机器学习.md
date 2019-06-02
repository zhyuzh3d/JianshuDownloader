这篇文章将和大家一起完成Tensorflow的经典鸢尾花分类案例。
完整过程可能需要一些时间，但您没有必要一次性完成它。

--
####准备工作

如果您还不了解鸢尾花分类问题是什么
[请点这里认真完成阅读（不需要写任何代码）](https://www.jianshu.com/p/da18f0cd7f60)

如果您还没有安装Python和Tensorflow
[Windows用户点这里认真阅读并完成安装](https://www.jianshu.com/p/da18f0cd7f60)
[苹果MacOS用户点这里认真阅读并完成安装](https://www.jianshu.com/p/1bf82604a6da)

从百度云下载需要用到的文件
[点击这里，提取码dwdk](https://pan.baidu.com/s/1jJSIdBw)

--
####了解数据集
下载到的资料中包含两个看起来像excel格式的文件，iris_training.csv和iris_test.csv。
iris_training.csv顾名思义是训练数据集，iris_test.csv是测试数据集。

接下来，我们会先把训练数据“喂”给计算机，让它吃掉并消化好，这样它就能自己从数据中找到植物学家区分三种鸢尾花类型的规则。

然后我们再用训练出来的规则尝试去鉴定我们的测试数据，如果鉴定出来的结果和植物学家的看法一致，那么我们就可以说这个规则很有效。


我们先认真看一下数据文件内容。
请用右键选择文本编辑工具打开它，它们的内容看起来像下面这个样子：
![iris_training.csv](http://upload-images.jianshu.io/upload_images/4324074-879f8a80164d8709.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![iris_test.csv](http://upload-images.jianshu.io/upload_images/4324074-98fc40247b305ec9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

每个文件的第一行包含两个数字，第一个数字是说这个文件中有多少行数据，每一行代表一朵花。training有120朵，test有30朵。

第二个数字都是4，表示每朵花有几个【特征futures】数据。从前面的鸢尾花案例分析文章中我们知道，测量了花萼的长度、花萼的宽度、花瓣的长度、花瓣的宽度这4个数据，所以这里都是4。（但实际上，对于计算机来说，数据的名称一点也不重要，不是吗？）

第一行还包含了三个英文单词，就是鸢尾花的三个类型山鸢尾花Setosa、变色鸢尾花Versicolor、韦尔吉尼娅鸢尾花Virginica。

下面是很多很多的数字行。每一行有5个数字，逗号分割。前面4个对应花萼花瓣4个特征futrues。

每行数字最后一个都是0、1或2，这里的意思是0代表Setosa，1代表Versicolor，2代表Virginica。012这个顺序和第一行最后三个单词是对应的。这就是植物学家鉴定之后给每朵花写上的【标签label】

--
####安装软件
首先确保Python和Tensorflow已经被正确安装。具体请参考[Python-Tensorflow-最简安装教程](https://www.jianshu.com/p/2aeed4cee9c6)。
然后用IDLE从菜单【文件File-新文件New file】创建新文件，保存到桌面iris文件夹下命名iris.py，然后把下载的两个数据文件也拷贝到iris文件夹下。

保存后右键选择打开方式，IDLE打开，然后粘贴以下代码并保存：
```
import pandas as pd
import tensorflow as tf
```
然后在命令行工具内执行以下命令，MacOS：
```
python3 ~/desktop/iris/iris.py
```
Windows：
```
python3 desktop/iris/iris.py
```
正常情况会提示错误ImportError: No module named pandas。缺少pandas这个模块，下面我们安装它。

使用下面命令安装：
```
pip3 install pandas
```
如果遇到问题请尝试用管理员运行（Windows）或前面加sudo执行，下同。
如果进度非常缓慢卡住，请尝试添加--trusted-host国内镜像地址，多试几次，命令比如
```
pip3 --trusted-host http://mirrors.aliyun.com/pypi/simple/ install pandas
```
--

####加载数据
首先把数据文件的路径处理成可以使用的train_path和test_path。
然后使用pandas模块的read_csv方法把数据读进来，又使用pop方法把4个特征数据和Species数据拆分成_x和_y。这样命名的原因是我们之前介绍过的函数表示：
![](http://upload-images.jianshu.io/upload_images/4324074-183c5f35a8fe9c0c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

iris.py的代码如下：
```
import os
import pandas as pd
import tensorflow as tf

FUTURES = ['SepalLength', 'SepalWidth','PetalLength', 'PetalWidth', 'Species']
SPECIES = ['Setosa', 'Versicolor', 'Virginica']

dir_path = os.path.dirname(os.path.realpath(__file__))
train_path=os.path.join(dir_path,'iris_training.csv')
test_path=os.path.join(dir_path,'iris_test.csv')

train = pd.read_csv(train_path, names=FUTURES, header=0)
train_x, train_y = train, train.pop('Species')

test = pd.read_csv(test_path, names=FUTURES, header=0)
test_x, test_y = test, test.pop('Species')

feature_columns = []
for key in train_x.keys():
    feature_columns.append(tf.feature_column.numeric_column(key=key))

print(test_x)
```
保存到桌面文件夹iris/iris.py,和两个数据文件放在一起，我们使用python3命令运行它，MacOS终端命令
```
python3 ~/desktop/iris/iris.py
```
Windows命令提示符
```
python3 desktop/iris/iris.py
```
运行结果如下：
![](http://upload-images.jianshu.io/upload_images/4324074-58043d538c454c6b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
如果将最后一行代码改为print(test_y)则会只输出每朵花的类型0、1或2

如果将最后一行代码改为print(feature_columns)我们会看到输出类似下面的数据：
![](http://upload-images.jianshu.io/upload_images/4324074-e4a631e9d22e5983.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
暂时我们不需要深究它的含义，只要留意到它与花朵的4个特征相对应，表示了每个特征的数据类型都是32位浮点小数tf.float32。

--
####设定估算器（分类器）
我们直接使用tensorflow提供的估算器来从花朵数据推测分类规则。tf.estimator里面包含了很多估算器，这里我们使用深层神经网络分类器DNNClassifier(Deep Neural Network Classifier)。
去除最后一行，在最后添加新的内容:
```
classifier = tf.estimator.DNNClassifier(
    feature_columns=feature_columns,
    hidden_units=[10, 10],
    n_classes=3)

```
>这里的hidden_units是用来设定深层神经网络分类器的复杂程度的，n_classes对应我们三种花朵类型。

####训练模型
接下来我们就可以灌输数据给我们的估算器，让它自动训练，寻找其中的分类规律，也就是我们真正需要的分类函数，也称之为模型。

继续添加新的代码：
```
def train_input_fn(features, labels, batch_size):
    dataset = tf.data.Dataset.from_tensor_slices((dict(features), labels))
    dataset = dataset.shuffle(1000).repeat().batch(batch_size)
    return dataset.make_one_shot_iterator().get_next()

tf.logging.set_verbosity(tf.logging.INFO)
batch_size=100
classifier.train(input_fn=lambda:train_input_fn(train_x, train_y,batch_size),steps=1000)
```
>首先我们定义了“喂食函数”train_input_fn，用来将4个特征数据features和植物学家分类结果labels组合在一起，然后又用把这些花的顺序搅乱shuffle一下，这样以后每次我们进行训练都可能得到不同的结果。
然后，我们设定日志logging输入训练进度信息，稍后如果你觉得它太烦人可以把INFO改为WARN，只输出警告信息。
接着我们就启动了分类器的train训练。这里面的100和1000稍后你可以任意调节尝试不同结果。

重新运行iris.py，可以看到输出了很多行类似的信息，这说明训练正常运行了：
![](http://upload-images.jianshu.io/upload_images/4324074-81f2a94d80fb4b90.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

--
####评估模型
上面我们把训练数据“喂食”给分类器进行训练，当然计算机也就从数据中猜出了三种花分类的依据，也就是我们训练得到的模型。
但我们并不知道这个“训练”出来的模型是否正确，为了考验一下它，我们把test测试数据交给它，让计算机用这个模型来预测这些test花的分类，然后我们把预测得到的分类和植物学家为test花标注的分类进行对比，如果模型预测的都正确，我就说这个模型的精确度accuracy是100%。

继续添加以下代码：
```
def eval_input_fn(features, labels, batch_size):
    features=dict(features)
    inputs=(features,labels)
    dataset = tf.data.Dataset.from_tensor_slices(inputs)
    dataset = dataset.batch(batch_size)
    return dataset.make_one_shot_iterator().get_next()

eval_result = classifier.evaluate(
    input_fn=lambda:eval_input_fn(test_x, test_y,batch_size))

print(eval_result)
```
>分类器的evaluate方法是用来评估模型的精确度的，它同样需要一个“喂食函数”eval_input_fn把需要预测的特征值和应该得到的结果label值处理一下。

我们再次运行，最后一行得到类似下面的结果,我们看到accuracy能保持在0.9以上：
![](http://upload-images.jianshu.io/upload_images/4324074-b3838a016c207b3f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

如果我们调整神经网络的层级设置hidden_units，或者训练的设置batch_size=100或steps=1000，我们就有可能得到精确度更高或更低的结果。

####应用模型
回到我们最初要解决的问题，也就是当女朋友把她的鸢尾花测量数据交给我们的时候，我们可以让训练出来的人工智能模型来自动对这朵花进行分类，由于精度超过90%，所以我们有超过九成的把握可以认为这个分类就是正确的。

继续添加以下代码：
```
for i in range(0,100):
    print('\nPlease enter features: SepalLength,SepalWidth,PetalLength,PetalWidth')
    a,b,c,d = map(float, input().split(',')) 
    predict_x = {
        'SepalLength': [a],
        'SepalWidth': [b],
        'PetalLength': [c],
        'PetalWidth': [d],
    }
    predictions = classifier.predict(
            input_fn=lambda:eval_input_fn(predict_x,
                                            labels=[0],
                                            batch_size=batch_size))

    for pred_dict in predictions:
        class_id = pred_dict['class_ids'][0]
        probability = pred_dict['probabilities'][class_id]
        print(SPECIES[class_id],100 * probability)
                                      
```
>这段程序可以重复对100朵新花做分类。我们每次需要按照SepalLength,SepalWidth,PetalLength,PetalWidth的顺序把花朵的测量结果输进去，然后只要回车，人工智能训练出来的模型就会告诉我们这朵花是什么类型（并标注了有多大可能是这个类型），如下图所示测量数据是6.1，2.3，5.1，0.2的花朵有99.94%的可能是变色鸢尾花Versicolor。

![](http://upload-images.jianshu.io/upload_images/4324074-6175e42bd461329d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

--
####结语
通过这个经典案例，我们使用Tensorflow训练了第一个机器学习模型，虽然它只能根据已测量的数据做简单的分类预测，但是整个学习过程和代码流程却是完备的。

回顾一下整个流程：
1. #####了解数据集：特征值futures和标记值label
1.  #####加载数据集：训练数据training和测试数据test
1. #####设定估算器estimator：深层神经网络分类器DNNClassifier
1. #####训练模型：喂食函数train_input_fn和训练方法train
1. #####评估训练出来的模型：喂食函数eval_input_fn和评估方法evaluate
1. #####应用模型进行预测：classifier.predict

>文章中的代码主要参考了Tensorflow的官方示例，Github地址https://github.com/tensorflow/models/blob/master/samples/core/get_started
我对代码进行了大幅度的精简和改进，目的是让代码更少更易懂而不是使代码更严谨，如有错误之处请专业人士指正。

下面是以上代码的完整版，带有更多注释，仅供学习者参考理解，强烈提示不要一味照抄照搬，思路才是最重要的。更多关于神经网络的信息可以参考Tensorflow官网，我后续也会发布一些自己的学习经验。

```
import os
import pandas as pd
import tensorflow as tf

FUTURES = ['SepalLength', 'SepalWidth','PetalLength', 'PetalWidth', 'Species']
SPECIES = ['Setosa', 'Versicolor', 'Virginica']

#格式化数据文件的目录地址
dir_path = os.path.dirname(os.path.realpath(__file__))
train_path=os.path.join(dir_path,'iris_training.csv')
test_path=os.path.join(dir_path,'iris_test.csv')

#载入训练数据
train = pd.read_csv(train_path, names=FUTURES, header=0)
train_x, train_y = train, train.pop('Species')

#载入测试数据
test = pd.read_csv(test_path, names=FUTURES, header=0)
test_x, test_y = test, test.pop('Species')

#设定特征值的名称
feature_columns = []
for key in train_x.keys():
    feature_columns.append(tf.feature_column.numeric_column(key=key))

#选定估算器：深层神经网络分类器  
classifier = tf.estimator.DNNClassifier(
    feature_columns=feature_columns,
    hidden_units=[10, 10],
    n_classes=3)

#针对训练的喂食函数
def train_input_fn(features, labels, batch_size):
    dataset = tf.data.Dataset.from_tensor_slices((dict(features), labels))
    dataset = dataset.shuffle(1000).repeat().batch(batch_size) #每次随机调整数据顺序
    return dataset.make_one_shot_iterator().get_next()

#设定仅输出警告提示，可改为INFO
tf.logging.set_verbosity(tf.logging.WARN)

#开始训练模型！
batch_size=100
classifier.train(input_fn=lambda:train_input_fn(train_x, train_y,batch_size),steps=1000)

#针对测试的喂食函数
def eval_input_fn(features, labels, batch_size):
    features=dict(features)
    inputs=(features,labels)
    dataset = tf.data.Dataset.from_tensor_slices(inputs)
    dataset = dataset.batch(batch_size)
    return dataset.make_one_shot_iterator().get_next()

#评估我们训练出来的模型质量
eval_result = classifier.evaluate(
    input_fn=lambda:eval_input_fn(test_x, test_y,batch_size))

print(eval_result)

#支持100次循环对新数据进行分类预测
for i in range(0,100):
    print('\nPlease enter features: SepalLength,SepalWidth,PetalLength,PetalWidth')
    a,b,c,d = map(float, input().split(',')) #捕获用户输入的数字
    predict_x = {
        'SepalLength': [a],
        'SepalWidth': [b],
        'PetalLength': [c],
        'PetalWidth': [d],
    }
    
    #进行预测
    predictions = classifier.predict(
            input_fn=lambda:eval_input_fn(predict_x,
                                            labels=[0],
                                            batch_size=batch_size))

    #预测结果是数组，尽管实际我们只有一个
    for pred_dict in predictions:
        class_id = pred_dict['class_ids'][0]
        probability = pred_dict['probabilities'][class_id]
        print(SPECIES[class_id],100 * probability)
```

以上代码文件实在不成功可以从百度云盘下载
[iris.py](https://pan.baidu.com/s/1aPG6gU2K9AbN5uW2M22SGQ)
提取密码: 8dt3

>如果遇到ValueError: features should be a dictionary of "Tensor"s. Given type..错误，很可能是您的tensorflow版本太低，可以尝试直接命令行运行python3命令，然后输入下面命令查看版本是否低于1.5。建议直接升级到最新或重新安装，参照[Python-Tensorflow-最简安装教程](https://www.jianshu.com/p/2aeed4cee9c6)
感谢读者[人来丰](https://www.jianshu.com/u/a9140d7c0ca2)提醒。

```
>>> import tensorflow as tf
>>> print(tf.__version__)
```

---
###探索人工智能的新边界
如果您发现文章错误，请不吝留言指正；
如果您觉得有用，请点喜欢；
如果您觉得很有用，感谢转发~
---
END





















