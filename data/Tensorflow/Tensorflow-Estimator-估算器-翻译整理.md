因为没有找到官方对estimator的翻译，这里暂时称作估算器，待以后改正。

---
估算器是tf重要的高级接口high level api，被设计用来简化机器学习程序的。

估算器有tf自带的预制pre-made估算器，也支持用户自己编写创建自定义custom估算器。

估算器可以被灌入数据执行训练train，可以对训练的模型进行评价evaluate，可以使用训练好的模型进行预测predict。

######通过估算器操作模型
---
####估算器优势
* 可以本地或分布式服务器上运行基于估算器的模型，而无需更改，甚至是CPU、GPU、TPU上运行。
* 估算器简化了模型开发者之间共享方式。
* 可以利用估算器凭直觉的简单创建模型。
* 估算器本身就是基于tf.layers，自定义起来更简单。
* 估算器直接创建graph图，从而无需手工创建。
* 估算器创建了一个安全的分布式训练循环，你可以：
  * 建造graph图
  * 初始化变量
  * 开始队列
  * 控制处理异常
  * 创建checkpoint检查点文件，从失败中恢复
  * 将summary总结保存到tensorboard信息板

当使用估算器编写应用的时候，必须把数据输入流程data input pipline单独出来，这可以使流程简化。

---
####预制估算器Pre-made Estimator
估算器为你管理着graph图和session会话，你无需手工管理它们。
利用估算器可以很容易的更换不同的算法，比如DNNClassifier等。

使用预制估算器的应用结构：
1. ######编写数据导入函数，比如导入训练数据的函数和导入测试数据的函数。这样的函数应该返回：
  * 特征字典dict:{特征名：张量Tensor或稀疏张量SpareTensor}
  * 标签张量Tensor，包含标签labels
```
#针对训练的喂食函数
def train_input_fn(features, labels, batch_size):
    dataset = tf.data.Dataset.from_tensor_slices((dict(features), labels))
    dataset = dataset.shuffle(1000).repeat().batch(batch_size) 
    features_result, labels_result = dataset.make_one_shot_iterator().get_next() 
    print(features_result, labels_result)
    return dataset.make_one_shot_iterator().get_next()
```
得到features_result, labels_result打印结果是：
```
#features_result 特征字典
{
  'SepalLength': <tf.Tensor 'IteratorGetNext:2' shape=(?,) dtype=float64>, 
  'SepalWidth': <tf.Tensor 'IteratorGetNext:3' shape=(?,) dtype=float64>, 
  'PetalLength': <tf.Tensor 'IteratorGetNext:0' shape=(?,) dtype=float64>, 
  'PetalWidth': <tf.Tensor 'IteratorGetNext:1' shape=(?,) dtype=float64>
}
#labels_result 标签列
Tensor("IteratorGetNext:4", shape=(?,), dtype=int64, device=/device:CPU:0)
```

2. ######定义特征列，tf.feature_column定义了特征的名称、数据类型和预处理方法。
```
# 两个数值型特征列
population = tf.feature_column.numeric_column('population')
crime_rate = tf.feature_column.numeric_column('crime_rate')
# 数值型特征列指定了规则化函数。每个数值将被减去100
median_education = tf.feature_column.numeric_column('median_education',
                    normalizer_fn='lambda x: x - 100')
```
3. ######实例化预制估算器
```
# 实例化，传入特征列列表[fc1,fc2,fc3]
estimator = tf.estimator.Estimator.LinearClassifier(
    feature_columns=[population, crime_rate, median_education],
    )
```
4. ######调用train，evaluate，predict函数
```
# my_training_set是第一步编写的输入函数，这里它并没有带参数输入原始数据
estimator.train(input_fn=my_training_set, steps=2000)
```
  
预制估算器实现了计算图graph运算的最佳方法，无论是单机运算还是群集运算
，也实现全局统计的最佳方法。自定义估算器则要手工实现这些。

---
####自定义估算器Custom Estimator
无论是预制还是自定义的估算器，核心都是model_fn函数，它将实现创建图graph和训练、评价、预测方法。

---
####建议流程
1. 如果有合适的预制估算器，先使用它作为基础
1. 使用预制估算器创建和测试你的模型，包括模型的完整性和可靠性
1. 如果有其他可选的预制估算器，实验哪一个是最好的
1. 可以的话，进一步自定义改进你的估算器

---
###探索人工智能的新边界
如果您发现文章错误，请不吝留言指正；
如果您觉得有用，请点喜欢；
如果您觉得很有用，感谢转发~
---
END


