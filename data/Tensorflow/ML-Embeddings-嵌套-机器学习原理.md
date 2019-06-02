什么是Embedding嵌套？

下面是谷歌官方定义：
一种分类特征，以连续值特征表示。通常，嵌套是指将高维度向量映射到低维度的空间。例如，您可以采用以下两种方式之一来表示英文句子中的单词：
*   表示成包含百万个元素（高维度）的[**稀疏向量**](https://developers.google.cn/machine-learning/glossary/#sparse_features)，其中所有元素都是整数。向量中的每个单元格都表示一个单独的英文单词，单元格中的值表示相应单词在句子中出现的次数。由于单个英文句子包含的单词不太可能超过 50 个，因此向量中几乎每个单元格都包含 0。少数非 0 的单元格中将包含一个非常小的整数（通常为 1），该整数表示相应单词在句子中出现的次数。
*   表示成包含数百个元素（低维度）的[**密集向量**](https://developers.google.cn/machine-learning/glossary/#dense_feature)，其中每个元素都包含一个介于 0 到 1 之间的浮点值。这就是一种嵌套。

>嵌套本质上是降维，是化稀疏为密集。

---
##嵌套的概念
嵌套是一种映射，将稀疏不连续的对象映射到实数向量。

比如下面是300维度的英语单词嵌套：
```
blue:  (0.01359, 0.00075997, 0.24608, ..., -0.2524, 1.0048, 0.06259)
blues:  (0.01396, 0.11887, -0.48963, ..., 0.033483, -0.10007, 0.1158)
orange:  (-0.24776, -0.12359, 0.20986, ..., 0.079717, 0.23865, -0.014213)
oranges:  (-0.35609, 0.21854, 0.080944, ..., -0.35413, 0.38511, -0.070976)
```
向量中的这些单独的维度并没有什么具体意义，它们是向量的位置、距离关系的整体图式表达，以便于机器学习使用。

嵌套对于机器学习的输入非常重要。分类器Classifier、神经网络Neura networks普遍工作于实数向量Real number vector。训练Train最好是基于密集向量dense vector，全部所有数值共同定义对象。但是，对于机器学习来说，很多重要的输入比如文本的单词，都没有自然的向量表现形式，嵌套函数就是这么一个标准且有效的函数，可以把稀疏离散discrete/sparse的对象变为连续的向量表示法。

嵌套也作为机器学习的输出值。由于嵌套将物体映射为向量，应用程序可以使用向量空间相似的方法，强健且灵活的估算物体之间的相似性。一个通用的用途就是发现最近邻对象。

比如上面的单词向量，下面是每个单词的三个最近邻单词，用角度来展示：
```
blue:  (red, 47.6°), (yellow, 51.9°), (purple, 52.4°)
blues:  (jazz, 53.3°), (folk, 59.1°), (bluegrass, 60.6°)
orange:  (yellow, 53.5°), (colored, 58.0°), (bright, 59.9°)
oranges:  (apples, 45.3°), (lemons, 48.3°), (mangoes, 50.4°)
```
最后一行数字告诉应用程序oranges和apples比较近似(分离45.3度），而和lemons，mangoes稍微区别大一些（48.3，50.4）。

---
##Tensorflow中的嵌套Embedding

为了创建单词的嵌套，我们首先把文本划分为单词，并为每个词汇指定一个整数张量。假设这已经完成，word_ids表示包含这些整数的向量。比如句子，I have a cat.被划分为['I','have','a','cat',',']，对应的word_ids张量是形状shape[5]，由5个整数组成，比如[32,177,4,23,16]。要把这些单词映射为向量，我们需要使用```tf.nn.embedding_lookup```来生成嵌套变量。
```
word_embeddings = tf.get_variable(“word_embeddings”,
    [vocabulary_size, embedding_size])
embedded_word_ids = tf.nn.embedding_lookup(word_embeddings, word_ids)
```
如上，张量embedded_word_ids的形状变为[5,embedding_size],包含了5个嵌套（密集矢量）对应每个单词。训练结束后，word_embeddings将包含所有词汇单词的嵌套。
```
#如果Embedding_size=3，那么embedded_word_ids可能是
[[0.438890,0.782233,0.52721],
 [0.645432,0.523233,0.62333],
 [0.412333,0.124522,0.67223],
 [0.145333,0.133422,0.67223],
 [0.988888,0.765556,0.13344],
]
```

嵌套可以被多种网络类型训练，各种损失函数和数据集。例如，一个使用卷积神经网络RNN依赖词库去预测某个单词后面的下一个单词，或者使用两个网络进行语言翻译。

---
##视觉化嵌套Visualizing Embeddings
Tensorboard中包含的嵌套投影器Embedding projector，它可以交互的显示嵌套，他可以从模型中读取嵌套并渲染到3D空间。


Embedding projector有三个面板：
* Data panel
* Projections panel
* Inspector panel

此处省去很多内容的翻译...

![](imgs/4324074-73605ee756c1cc7b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


![](imgs/4324074-7e47f07bd8a44b72.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

---
###探索人工智能的新边界
如果您发现文章错误，请不吝留言指正；
如果您觉得有用，请点喜欢；
如果您觉得很有用，感谢转发~
---
END







