TF-Hub是一个分享可在用的机器学习模型的平台，尤其是预训练的模型pre-trained model。这个教程包含两部分：

####说明：使用TF-Hub训练一个文字分类器
我们将使用TF-Hub文字嵌入模型来训练一个简单的分类器达到合理的基准精度。然后我们分析预测结果，来确保我们的模型合理并提升精度。

####高级：迁移学习Transfor learning分析
我们使用不同的TF-Hub模型来对比评估器的精度，呈现迁移学习的优势和缺点。

----
##准备环境
安装必须的模块
```
pip3 install  tensorflow
pip3 install tensorflow-hub
pip3 install scipy
pip3 install seaborn
```
创建init.py文件，引入必要的模块
```
import tensorflow as tf
import tensorflow_hub as hub
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import re
import seaborn as sns
```
---
##数据

我们使用Large Movie Review Dataset大电影评论数据集，其中包含了25000个流行电影的评论用来做训练，25000个作为测试，每个样本都带有1~10标签表示评论的积极程度。我们希望通过训练，让模型能够根据评论的文字评估出这个评论认为电影是好电影还是差电影。

从文件目录读取数据的函数：
```
def load_directory_data(directory):
  data = {}
  data["sentence"] = [] #评论内容
  data["sentiment"] = [] #评价高低
  for file_path in os.listdir(directory):
    with tf.gfile.GFile(os.path.join(directory, file_path), "r") as f:
      data["sentence"].append(f.read())
      data["sentiment"].append(re.match("\d+_(\d+)\.txt", file_path).group(1))
  return pd.DataFrame.from_dict(data)
```

载入正面评价和负面评价，并洗牌的函数：
```
def load_dataset(directory):
  pos_df = load_directory_data(os.path.join(directory, "pos"))
  neg_df = load_directory_data(os.path.join(directory, "neg"))
  pos_df["polarity"] = 1 #好评
  neg_df["polarity"] = 0 #差评
  return pd.concat([pos_df, neg_df]).sample(frac=1).reset_index(drop=True)
```

启动载入：
```
tf.logging.set_verbosity(tf.logging.INFO) #减少冗余输出

dir_path = os.path.dirname(os.path.realpath(__file__))
train_path=os.path.join(dir_path,'aclImdb/train')
test_path=os.path.join(dir_path,'aclImdb/test')

train_df=load_dataset(train_path)
test_df =load_dataset(test_path)
train_df.head()
print(train_df)
```
命令行运行```python3 init.py```得到类似如下输出：
![](imgs/4324074-85afc8a3856f7ca7.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

其中最左侧是序号，英文句子是sentence，后面sentiment的评价打分1~10，最右边polarity是根据文件夹pos或neg确定的好评1或者差评0.

---
##模型

####输入函数Input function

```
#针对整个训练集进行训练，不限制训练周期
train_input_fn = tf.estimator.inputs.pandas_input_fn(
    train_df, train_df["polarity"], num_epochs=None, shuffle=True)

#使用整个训练集进行预测
predict_train_input_fn = tf.estimator.inputs.pandas_input_fn(
    train_df, train_df["polarity"], shuffle=False)
#使用测试集进行预测
predict_test_input_fn = tf.estimator.inputs.pandas_input_fn(
    test_df, test_df["polarity"], shuffle=False)
```
####特征列Feature columns

在这里我们把每个单词作为一个特征列来对待，然后对比电影评论来看每个单词被重复出现的次数作为特征值。
[请参照这篇文章Tensorflow-FeutureColumns-数据格式-机器学习](https://www.jianshu.com/p/fceb64c790f3)

这里我们使用TF-Hub提供的nnlm-en-dim 128模块。
* 这个模型使用成批的句子作为1维张量，用来输入。
* 这个模型能够自动对句子进行处理，比如去掉标点，使用空格划分等。
* 这个模型可以接受任何输入，即使没有出现过的奇怪单词。

```
embedded_text_feature_column = hub.text_embedding_column(
    key="sentence", 
    module_spec="https://tfhub.dev/google/nnlm-en-dim128/1")
```

####估算器Estimator
直接使用DNN分类器。
```
estimator = tf.estimator.DNNClassifier(
    hidden_units=[500, 100],
    feature_columns=[embedded_text_feature_column],
    n_classes=2,
    optimizer=tf.train.AdagradOptimizer(learning_rate=0.003))
```
####启动训练Training
```
estimator.train(input_fn=train_input_fn, steps=1000)
```
####执行预测Prediction
```
train_eval_result = estimator.evaluate(input_fn=predict_train_input_fn)
test_eval_result = estimator.evaluate(input_fn=predict_test_input_fn)

print "Training set accuracy: {accuracy}".format(**train_eval_result)
print "Test set accuracy: {accuracy}".format(**test_eval_result)
```





