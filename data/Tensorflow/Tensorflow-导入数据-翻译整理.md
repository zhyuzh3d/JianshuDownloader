tf.data可以创建复杂的数据输入流水线，实现图像、文字的导入。
tf.data产生两个新的抽象类：
* tf.data. Dataset,数据集，多个元素组成的队列，每个元素包含一个或多个张量。有两种方式创建Dataset对象：
  * 从张量创建，比如```tf.data.Dataset.from_tensor_slices((dict(train_x), train_y))```。
  * 从另外的数据集创建，比如```dataset.shuffle(1000).repeat().batch(batch_size)```
* tf.data.Iterator,从数据集中提取元素，Iterator.get_next()产生下一个元素。Iterator.initializer方法可以使用不同的数据集不同的参数进行初始化。

---
####基本原理
构建数据输入流：
* 定义数据源，```tf.data.Dataset.from_tensors(tensors)```或```tf.data.Dataset.from_tensor_slices(tensors)```,或者使用```tf.data.TFRecordDataset```读取本地的TFRecord格式文件。
* 变换数据集，例如使用```Dataset.map(map_func)```的方法对每个张量元素执行操作。
* 提取数据，```tf.data.Iterator```,使用``` Iterator.initializer```重新初始化数据，使用```Iterator.get_next()```获取下一个tensor张量。

1. ######数据集结构
  Dataset必须包含多个同类元素elements，每个元素包含一个或多个tensor称为组件components，每个组件的构成：
  * ```tf.Dtype```表示数据类
  * ```tf. TensorShape```表示数据形状
  * ```Dataset.output_types```,```Dataset.output_shapes```用来查看以上两个属性
 示例代码：
```
import tensorflow as tf

tensor=tf.random_uniform([4, 10])
with tf.Session() as session:
    print(session.run([tensor]))

dataset1 = tf.data.Dataset.from_tensor_slices(tensor)
print(dataset1.output_types)  # ==> "tf.float32"
print(dataset1.output_shapes)  # ==> "(10,)"

dataset2 = tf.data.Dataset.from_tensor_slices(
   (tf.random_uniform([4]),
    tf.random_uniform([4, 100], maxval=100, dtype=tf.int32)))
print(dataset2.output_types)  # ==> "(tf.float32, tf.int32)"
print(dataset2.output_shapes)  # ==> "((), (100,))"

dataset3 = tf.data.Dataset.zip((dataset1, dataset2))
print(dataset3.output_types)  # ==> (tf.float32, (tf.float32, tf.int32))
print(dataset3.output_shapes)  # ==> "(10, ((), (100,)))"
```

```tf.random_uniform([4,10])```产生的是一个4行10列的0~1随机数字，类似
```
[array([[0.8139155 , 0.00317001, 0.1536988, ..., 0.625741  ],
       [0.00984228, 0.88505733, 0.44980478, ..., 0.30504322],
       [0.10747015, 0.639518  , 0.6030766 , ..., 0.5297921 ],
       [0.48373353, 0.7960038 , 0.666453,..., 0.7486484 ]],
```
使用字典标记字段名，dataset的dtype和shape可以是个字典：
```
import tensorflow as tf
dataset = tf.data.Dataset.from_tensor_slices(
   {"a": tf.random_uniform([4]),
    "b": tf.random_uniform([4, 100], maxval=10, dtype=tf.int32)})
print(dataset.output_types)  # ==> "{'a': tf.float32, 'b': tf.int32}"
print(dataset.output_shapes)  # ==> "{'a': (), 'b': (100,)}"
```

对数据集进行处理，```Dataset.map(), Dataset.flat_map(), and Dataset.filter()```,它们可以对数据集的每个元素进行处理，元素的结构决定函数的参数。

2. ######创建迭代器
数据集自带创建各种迭代器的方法，迭代器分类：
* one-shot,
* initializable,
* reinitializable, and
* feedable.

one-shot不需要初始化，尤其适合estimator使用。
```
import tensorflow as tf

dataset = tf.data.Dataset.range(100) #生成0~99共100个元素的数据集
iterator = dataset.make_one_shot_iterator()
next_element = iterator.get_next()

with tf.Session() as sess:
    for i in range(100):
      v = sess.run(next_element)
      print(v)

#输出0,1,2,3,4...,99
```

可初始化的initializable类型的迭代器需要初始化之后才能使用，但可以使用参数feed_dict，```sess.run(iterator.initializer, feed_dict={placeholder: 10})```
```
import tensorflow as tf
sess= tf.Session()

#创建一个站位符，和后面的feed_dict联合用来喂数据
max_v = tf.placeholder(tf.int64, shape=[]) 

#创建一个数据集，从max_v到max_v*2
dataset = tf.data.Dataset.range(max_v, max_v*2)
iterator = dataset.make_initializable_iterator()
next_element = iterator.get_next()

sess.run(iterator.initializer, feed_dict={max_v: 10}) #max_v必须和占位符一致
for i in range(3):
  value = sess.run(next_element)
  print('max_v=10',value)

sess.run(iterator.initializer, feed_dict={max_v: 100}) #max_v必须和占位符一致
for i in range(3):
  value = sess.run(next_element)
  print('max_v=100',value)
```
上面的代码输出
```
max_v=10 10
max_v=10 11
max_v=10 12
max_v=100 100
max_v=100 101
max_v=100 102
```
可重复初始化的reinitializable类型迭代器，可以使用多个不同的数据集进行初始化。比如创建一个训练输入管道故意把数据扰乱，再创建一个评价管道使用正常的数据集。不同数据集必须有完全相同的结构。
```
iterator =tf.data.Iterator.from_structure(dtypes,shapes)
next_element = iterator.get_next()
training_init_op =iterator.make_initializer(dataset)
```
下面是示例代码，会输出2遍10个train和5个validation。仅供演示，并没有什么实际作用。
```
import tensorflow as tf
sess=tf.Session()

training_dataset = tf.data.Dataset.range(10).map(
    lambda x: x + tf.random_uniform([], -10, 10, tf.int64))
validation_dataset = tf.data.Dataset.range(5)

iterator = tf.data.Iterator.from_structure(training_dataset.output_types,
                                           training_dataset.output_shapes)
next_element = iterator.get_next()

training_init_op = iterator.make_initializer(training_dataset)
validation_init_op = iterator.make_initializer(validation_dataset)

for _ in range(2): #两个周期
  sess.run(training_init_op)
  for _ in range(10):
    v = sess.run(next_element)
    print('train',v)

  sess.run(validation_init_op)
  for _ in range(5):
    v = sess.run(next_element)
    print('validation',v)
```
可喂食的的迭代器feedable，不直接由dataset生成，但它可以联合tf.placeholder一起为tf.Session.run每次呼叫切换不同的迭代器（由dataset生成），类似feed_dict的机制。
```
handle = tf.placeholder(tf.string, shape=[]) 
iterator = tf.data.Iterator.from_string_handle(handle, dtypes, shapes)
next_element = iterator.get_next()
...
training_iterator = training_dataset.make_one_shot_iterator()
training_handle = sess.run(training_iterator.string_handle())
...
sess.run(next_element, feed_dict={handle: training_handle})
```

示例代码,会输出3次10个train和5个validation。
```
import tensorflow as tf
sess=tf.Session()

#定义相同结构的数据集
training_dataset = tf.data.Dataset.range(0,10).map(
    lambda x: x + tf.random_uniform([], -10, 10, tf.int64)).repeat()
validation_dataset = tf.data.Dataset.range(100,200)

#feedable迭代器由placeholder及其结构设定
handle = tf.placeholder(tf.string, shape=[]) #这个handle名和下面的必须一致
iterator = tf.data.Iterator.from_string_handle(
    handle, training_dataset.output_types, training_dataset.output_shapes)
next_element = iterator.get_next()

#不同类型的迭代器
training_iterator = training_dataset.make_one_shot_iterator()
validation_iterator = validation_dataset.make_initializable_iterator()

#Iterator.string_handle()返回一个张量，可以用来喂食placeholder
training_handle = sess.run(training_iterator.string_handle())
validation_handle = sess.run(validation_iterator.string_handle())

for _ in range(3):
  for _ in range(10):
    v=sess.run(next_element, feed_dict={handle: training_handle})
    print('train',v)

  sess.run(validation_iterator.initializer)
  for _ in range(5):
    v=sess.run(next_element, feed_dict={handle: validation_handle})
    print('validation',v)
```

3. ######提取迭代器的数据
```Iterator.get_next()```方法返回一个或多个张量对象，它们关联到迭代器的下一个元素，当这些张量被计算的时候，才会获取下一个元素的数据。```Iterator.get_next()```方法并不会立即运算，而是必须把返回的对象放到表达式里面，并且把表达式结果传递到tf.Session.run()中，才会被计算。
到达最后一个元素的时候再执行```Iterator.get_next()```会出错，```tf.errors.OutOfRangeError```,如果需要再使用，必须重新初始化。
示例代码
```
import tensorflow as tf
sess=tf.Session()

dataset = tf.data.Dataset.range(5)
iterator = dataset.make_initializable_iterator()
next_element = iterator.get_next() #获得张量对象
result = tf.add(next_element, next_element) #传入表达式

#将表达式结果传入run执行
sess.run(iterator.initializer)
print(sess.run(result))  # ==> "0"
print(sess.run(result))  # ==> "2"
print(sess.run(result))  # ==> "4"
print(sess.run(result))  # ==> "6"
print(sess.run(result))  # ==> "8"

try:
  sess.run(result)
except tf.errors.OutOfRangeError:
  print("End of dataset")  # ==> "End of dataset"
```

如果Dataset包含嵌套结构，```Iterator.get_next()```将返回同样结构的张量。示例代码：
```
import tensorflow as tf
sess=tf.Session()

dataset1 = tf.data.Dataset.from_tensor_slices(tf.random_uniform([4, 10]))
dataset2 = tf.data.Dataset.from_tensor_slices((tf.random_uniform([4]), tf.random_uniform([4, 100])))
dataset3 = tf.data.Dataset.zip((dataset1, dataset2))

iterator = dataset3.make_initializable_iterator()

sess.run(iterator.initializer)
next1, (next2, next3) = iterator.get_next()
ziped= iterator.get_next()
print('ziped',ziped);
print('next1',next1);
print('next2',next2);
print('next3',next3);
```
以上代码将输出,看到iterator.get_next()方法得到结果的结构和dataset设置的相同：
```
ziped (<tf.Tensor 'IteratorGetNext_1:0' shape=(10,) dtype=float32>, (<tf.Tensor 'IteratorGetNext_1:1' shape=() dtype=float32>, <tf.Tensor 'IteratorGetNext_1:2' shape=(100,) dtype=float32>))
next1 Tensor("IteratorGetNext:0", shape=(10,), dtype=float32)
next2 Tensor("IteratorGetNext:1", shape=(), dtype=float32)
next3 Tensor("IteratorGetNext:2", shape=(100,), dtype=float32)
```
---
####读取输入数据
1. ######使用Numpy数组
如果数据就在内存里，最简单的创建dataset的方法就是，用```Dataset.from_tensor_slices()```把它们转为张量。但是这将把数据完全嵌入到计算图graph中，消耗大量内存（最多2G）。
```
#仅供示意，请勿执行
with np.load("/var/data/training_data.npy") as data:
  features = data["features"]
  labels = data["labels"]
assert features.shape[0] == labels.shape[0] #确保数据形状一致
dataset = tf.data.Dataset.from_tensor_slices((features, labels))
```
利用placeholder占位符和feed_dict可以优化内存占用:
```
# 仅供示意，请勿执行
with np.load("/var/data/training_data.npy") as data:
  features = data["features"]
  labels = data["labels"]
assert features.shape[0] == labels.shape[0]

features_placeholder = tf.placeholder(features.dtype, features.shape)
labels_placeholder = tf.placeholder(labels.dtype, labels.shape)

dataset = tf.data.Dataset.from_tensor_slices((features_placeholder, labels_placeholder))
...对dataset进行其他操作...
dataset = ...
iterator = dataset.make_initializable_iterator()

sess.run(iterator.initializer, feed_dict={
                          features_placeholder: features,
                          labels_placeholder: labels})
```

2. ######使用TFRecord数据
TFRecord是简单的面向记录record-oriented的二进制数据格式；```tf.data.TFRecordDataset```让我们可以把单个或多个TFRecord文件作为输入管道的一部分。
```
#示意代码。一次性读取两个文件
filenames = ["/var/data/file1.tfrecord", "/var/data/file2.tfrecord"]
dataset = tf.data.TFRecordDataset(filenames)
```
结合```tf.placeholder和feed_dict```使用，分别喂食训练数据和验证数据：
```
#示意代码，请勿运行
filenames = tf.placeholder(tf.string, shape=[None])
dataset = tf.data.TFRecordDataset(filenames)
dataset = dataset.map(...)  # 将记录数据解析为张量.
dataset = dataset.repeat()  # 重复输入.
dataset = dataset.batch(32) #合并成批次
iterator = dataset.make_initializable_iterator() 

training_filenames = ["/var/data/file1.tfrecord", "/var/data/file2.tfrecord"]
sess.run(iterator.initializer, feed_dict={filenames: training_filenames})

validation_filenames = ["/var/data/validation1.tfrecord", ...]
sess.run(iterator.initializer, feed_dict={filenames: validation_filenames})
```
3. ######使用文本数据
使用```tf.data.TextLineDataset```可以从单个或多个文本文件中逐行的读取数据。
```
filenames = ["/var/data/file1.txt", "/var/data/file2.txt"]
dataset = tf.data.TextLineDataset(filenames)
```
当文本文件第一行包含标题栏信息的时候，我们使用```Dataset.skip()和Dataset.filter()```进行处理。为了对每个文件进行处理，可以使用```Dataset.flat_map()```为每个文件创建嵌套的数据集:
```
filenames = ["/var/data/file1.txt", "/var/data/file2.txt"]
dataset = tf.data.Dataset.from_tensor_slices(filenames)

dataset = dataset.flat_map(
    lambda filename: (
        tf.data.TextLineDataset(filename)
        .skip(1) #跳过第一行
        .filter(lambda line: tf.not_equal(tf.substr(line, 0, 1), "#")))) #忽略#注释行
```
---
####使用Dataset.map()处理数据
```Dataset.map(f)```处理数据中的每一个元素element，其中函数f(element) 需要返回一个新的元素element。

######解析tf.Example缓冲格式信息
输入管道从TFRecord格式文件提取```tf.train.Example```，每个```tf.train.Example```包含了单个或多个特征，然后输入管道把这些特征转为张量。
```
#将一个标量字符串example_proto转为1个标量字符串+1个标量整数，表示某图片的名称和标签
def _parse_function(example_proto):
  features = {"image": tf.FixedLenFeature((), tf.string, default_value=""),
              "label": tf.FixedLenFeature((), tf.int32, default_value=0)}
  parsed_features = tf.parse_single_example(example_proto, features)
  return parsed_features["image"], parsed_features["label"]

filenames = ["/var/data/file1.tfrecord", "/var/data/file2.tfrecord"]
dataset = tf.data.TFRecordDataset(filenames)
dataset = dataset.map(_parse_function)
```

######解码图片数据并重新设置大小
```
def _parse_function(filename, label):
  image_string = tf.read_file(filename) #读取图片
  image_decoded = tf.image.decode_image(image_string) #解码图片
  image_resized = tf.image.resize_images(image_decoded, [28, 28]) #统一大小
  return image_resized, label #返回特征和标签

filenames = tf.constant(["/var/data/image1.jpg", "/var/data/image2.jpg", ...])

# `labels[i]`对应 `filenames[i]`图片的标签.
labels = tf.constant([0, 37, ...])

dataset = tf.data.Dataset.from_tensor_slices((filenames, labels)) #参数结构与parse函数一致
dataset = dataset.map(_parse_function)
```

######使用```tf.py_func()```应用任意Python逻辑
尽必要时候，在```Dataset.map(f)```中使用```tf.py_func()```.
```
import cv2
# 使用自定义的OpenCV函数代替 `tf.read_file()`读取图片
def _read_py_function(filename, label):
  image_decoded = cv2.imread(filename.decode(), cv2.IMREAD_GRAYSCALE)
  return image_decoded, label

# 使用tf方法把图片调整到统一尺寸
def _resize_function(image_decoded, label):
  image_decoded.set_shape([None, None, None])
  image_resized = tf.image.resize_images(image_decoded, [28, 28])
  return image_resized, label

filenames = ["/var/data/image1.jpg", "/var/data/image2.jpg", ...]
labels = [0, 37, 29, 1, ...]

dataset = tf.data.Dataset.from_tensor_slices((filenames, labels))
dataset = dataset.map(
    lambda filename, label: tuple(tf.py_func( #返回2元素的元组
        _read_py_function, [filename, label], [tf.uint8, label.dtype])))
dataset = dataset.map(_resize_function)
```
---
####将数据集元素分批次Batching

######简单分批处理
最简单的分批方法是使用```Dataset.batch()```把n个连续元素组成一个新元素,要求每个旧元素结构必须相同。

以下示例代码把4个数字分批处理。
```
import tensorflow as tf
sess=tf.Session()

inc_dataset = tf.data.Dataset.range(100)
dec_dataset = tf.data.Dataset.range(0, -100, -1)
batched_dataset = tf.data.Dataset.zip((inc_dataset, dec_dataset))
batched_dataset = dataset.batch(4)

iterator = batched_dataset.make_one_shot_iterator()
next_element = iterator.get_next()

print(sess.run(next_element))  # ==> ([0, 1, 2,   3],   [ 0, -1,  -2,  -3])
print(sess.run(next_element))  # ==> ([4, 5, 6,   7],   [-4, -5,  -6,  -7])
print(sess.run(next_element))  # ==> ([8, 9, 10, 11],   [-8, -9, -10, -11])
```
######带有填充的分批
对于长度不同的张量可以使用```Dataset.padded_batch()```填充分批.
```
dataset = tf.data.Dataset.range(100)
dataset = dataset.map(lambda x: tf.fill([tf.cast(x, tf.int32)], x))
dataset = dataset.padded_batch(4, padded_shapes=[None])

iterator = dataset.make_one_shot_iterator()
next_element = iterator.get_next()

print(sess.run(next_element))  # ==> [[0, 0, 0], [1, 0, 0], [2, 2, 0], [3, 3, 3]]
print(sess.run(next_element))  # ==> [[4, 4, 4, 4, 0, 0, 0],
                               #      [5, 5, 5, 5, 5, 0, 0],
                               #      [6, 6, 6, 6, 6, 6, 0],
                               #      [7, 7, 7, 7, 7, 7, 7]]
```
```tf.fill([x,y],n)```方法形成x行y列都是n的列表,比如tf.fill([2,3],9):
```
[9 9 9]
[9 9 9]
```
```tf.cast(x,dtype)```是对张量x进行数据格式转化，比如从```tf.float32```转为```tf.int32```，在这里转为整数才能使用。
以上代码中```dataset = dataset.map(lambda x: tf.fill([tf.cast(x, tf.int32)], x))```得到的是
```
[]
[1]
[2 2]
[3 3 3]
[4 4 4 4]
[5 5 5 5 5]
[6 6 6 6 6 6]
[7 7 7 7 7 7 7]
[8 8 8 8 8 8 8 8]
```
然后```dataset.padded_batch(4, padded_shapes=[None])```把每4个元素分为一个批次，并填充0处理，得到
```
[[0 0 0]
 [1 0 0]
 [2 2 0]
 [3 3 3]]
[[4 4 4 4 0 0 0]
 [5 5 5 5 5 0 0]
 [6 6 6 6 6 6 0]
 [7 7 7 7 7 7 7]]
[[ 8  8  8  8  8  8  8  8  0  0  0]
 [ 9  9  9  9  9  9  9  9  9  0  0]
 [10 10 10 10 10 10 10 10 10 10  0]
 [11 11 11 11 11 11 11 11 11 11 11]]
```

---
####训练流程

######处理多个周期epochs
Dataset有两种方法创建周期

1. 使用```Dataset.repeat(n)```
重复n次，如果为空则无限重复下去：
```
filenames = ["/var/data/file1.tfrecord", "/var/data/file2.tfrecord"]
dataset = tf.data.TFRecordDataset(filenames)
dataset = dataset.map(...)
dataset = dataset.repeat(10) #重复10次
dataset = dataset.batch(32)
```

2. 无限循环并捕获异常
为了避免无限重复到达结尾时候产生的异常，可以做如下处理
```
filenames = ["/var/data/file1.tfrecord", "/var/data/file2.tfrecord"]
dataset = tf.data.TFRecordDataset(filenames)
dataset = dataset.map(...)
dataset = dataset.batch(32)
iterator = dataset.make_initializable_iterator()
next_element = iterator.get_next()

# 100个周期
for _ in range(100):
  sess.run(iterator.initializer)
  while True:
    try:
      sess.run(next_element)
    except tf.errors.OutOfRangeError:
      break
  #在这里执行其他的代码
```

######随机顺序调整
```Dataset.shuffle(n)```将元素填充到n个缓冲，然后再随机提取处理，示意代码
```
filenames = ["/var/data/file1.tfrecord", "/var/data/file2.tfrecord"]
dataset = tf.data.TFRecordDataset(filenames)
dataset = dataset.map(...)
dataset = dataset.shuffle(buffer_size=10000)
dataset = dataset.batch(32)
dataset = dataset.repeat()
```

######使用高级API接口
```tf.train.MonitoredTrainingSession```简化了分布式运算设置，当运算完成时候通过```tf.errors.OutOfRangeError```得知，推荐结合```Dataset.make_one_shot_iterator()```迭代器使用：
```
filenames = ["/var/data/file1.tfrecord", "/var/data/file2.tfrecord"]
dataset = tf.data.TFRecordDataset(filenames)
dataset = dataset.map(...)
dataset = dataset.shuffle(buffer_size=10000)
dataset = dataset.batch(32)
dataset = dataset.repeat(num_epochs)
iterator = dataset.make_one_shot_iterator()

next_example, next_label = iterator.get_next()
loss = model_function(next_example, next_label)

training_op = tf.train.AdagradOptimizer(...).minimize(loss)

with tf.train.MonitoredTrainingSession(...) as sess:
  while not sess.should_stop():
    sess.run(training_op)
```
结合Estimator一起使用的示例代码:
```
def dataset_input_fn():
  filenames = ["/var/data/file1.tfrecord", "/var/data/file2.tfrecord"]
  dataset = tf.data.TFRecordDataset(filenames)

  def parser(record):
    keys_to_features = {
        "image_data": tf.FixedLenFeature((), tf.string, default_value=""),
        "date_time": tf.FixedLenFeature((), tf.int64, default_value=""),
        "label": tf.FixedLenFeature((), tf.int64,
                                    default_value=tf.zeros([], dtype=tf.int64)),
    }
    parsed = tf.parse_single_example(record, keys_to_features)

    image = tf.image.decode_jpeg(parsed["image_data"])
    image = tf.reshape(image, [299, 299, 1])
    label = tf.cast(parsed["label"], tf.int32)

    return {"image_data": image, "date_time": parsed["date_time"]}, label

  dataset = dataset.map(parser)
  dataset = dataset.shuffle(buffer_size=10000)
  dataset = dataset.batch(32)
  dataset = dataset.repeat(num_epochs)
  iterator = dataset.make_one_shot_iterator()

  features, labels = iterator.get_next()
  return features, labels
```
---
####小结
* #####导入数据集的基本机制
  * 数据集Dataset
     * 同类元素elements
       * 张量组件components
         * dtype
         * shape
  * 迭代器iterator
    * one-shot
    * initializable
    * reinitializable
    * feedable
  * 从迭代器获取元素get_next()
* #####读取数据
  * Numpy arrays
  * TFRecord
  * Text
* #####使用Dataset.map处理数据
  * tf.Example协议缓冲
  * 解码图像
  * 自定义tf.py_func()
* #####数据元素分批
  * Dataset.batch()
  * Dataset. padded_batch()
* #####训练流程
  * 多个周期epochs，Dataset.repeat()
  * 随机洗牌Dataset.shuffle()
  * 使用高级接口tf.train.MonitoredTrainingSession

---
###探索人工智能的新边界
如果您发现文章错误，请不吝留言指正；
如果您觉得有用，请点喜欢；
如果您觉得很有用，感谢转发~
---
END


