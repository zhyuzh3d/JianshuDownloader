
这篇文章主要介绍tensorflow对数据的处理知识：特征列feature columns。

####特征列FeatureColumns
特征列是指一组数据的相关特征，包含了数据的相关类型和长度等信息。
在前面的[鸢尾花案例](https://www.jianshu.com/p/b86c020747f9)中，我们使用了下面的代码拼合特征列,你可以在iris项目中添加新的测试文件test.py并运行它观看输出效果：
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

#拼合特征列
feature_columns = []
for key in train_x.keys():
    feature_columns.append(tf.feature_column.numeric_column(key=key))

print(feature_columns);
```
以上代码输出如下内容（整理后）
```
[
    _NumericColumn(key='SepalLength', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=None),
    _NumericColumn(key='SepalWidth', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=None), 
    _NumericColumn(key='PetalLength', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=None), 
    _NumericColumn(key='PetalWidth', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=None)
]
```

feature_columns = []，它是一个列表，被添加append了多个包含了多个feature_column.numeric_column()方法生成的特征列，每个特征列包含五个字段：
* 关键字key，用来标识每一列的名称，避免混淆。
* 形状shape, 数据的形状，见下面。
* 默认值default_value。
* 数据类型dtype，默认是浮点小数tf.float32。
* 标准化函数normalizer_fn，可以对每个每行数据进行处理。

---
####形状shape

关于shape，比如shape=3表示[r,g,b]类型的三元列表，类似[0,100,255]。shape=[4,3]表示下图的4行3列的矩阵，类似[[1,0,0] [0,1,0] [0,0,1] [0,0,0]]。

![4x3矩阵：4行3列](http://upload-images.jianshu.io/upload_images/4324074-edc72e9647186757.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

> 在python中还有一类和方括号[]列表类似的数据格式：小括号元组()。元组基本上就是每个元素都不重复的列表。
但是这里就有一个问题，mylist=(3)这句话到底是生成(3)这样的元组呢，还是生成一个类似(x,y,z)有三个元素的元组呢？答案是后者！
如果需要生成只包含3这个数字的元组，你需要在3后面强加一个逗号：
mylist=(3,)

----
####转化过程

我们把这段for循环改一下，把train_x，train_x.keys()和key以及转化完毕的特征列column打印出来，仔细看看数据的变化过程：
```
feature_columns = []
print(train_x);
print(train_x.keys());
for key in train_x.keys():
    print(key);
    print(tf.feature_column.numeric_column(key=key));
    feature_columns.append(tf.feature_column.numeric_column(key=key))
```
它们的情况：
* iris_training.csv是我们的原始数据，如下，具体情况之前文章详细解说过：
```
120,4,setosa,versicolor,virginica
6.4,2.8,5.6,2.2,2
5.0,2.3,3.3,1.0,1
4.9,2.5,4.5,1.7,2
4.9,3.1,1.5,0.1,0
...
```
* train_x是pandas模块读取的csv数据，使用pd.read_csv()方法，得到的是120行乘以4列的数据表[120 rows x 4 columns]
```
     SepalLength  SepalWidth  PetalLength  PetalWidth
0            6.4         2.8          5.6         2.2
1            5.0         2.3          3.3         1.0
2            4.9         2.5          4.5         1.7
...
[120 rows x 4 columns]
```
* train_x.keys()包含了四个关键字和一个数据类型对象dtype
```
Index(['SepalLength', 'SepalWidth', 'PetalLength', 'PetalWidth'], dtype='object')
```
* key是关键字名称，numeric_column(key=key)得到的单个特征列和上面展示的一样
```
SepalLength
_NumericColumn(key='SepalLength', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=None)
```

---
####数据流程
在之前的[鸢尾花案例](https://www.jianshu.com/p/b86c020747f9)中，我们从csv读取数据，组织成为特征列feature_columns并编写了喂食数据的函数input_fn，然后利用特征列创建了qiu zh器中的深度神经网络分类器estimator.DNNClassifier，然后利用喂食函数input_fn把读取的数据喂食到DNNClassifier中进行训练、评估和预测。
![](http://upload-images.jianshu.io/upload_images/4324074-b22b62e746a1f662.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

---
####数值列numeric_column
我们在上面使用的就是数值列numeric_column，它的默认格式如下
```
numeric_column(
    key,
    shape=(1,),
    default_value=None,
    dtype=tf.float32,
    normalizer_fn=None
)
```
你可以用下面的代码测试：
```
import tensorflow as tf

price = {'price': [[1.], [2.], [3.], [4.]]}  # 4行样本

column = tf.feature_column.numeric_column('price', normalizer_fn=lambda x:x+2)
tensor = tf.feature_column.input_layer(price,[column])

with tf.Session() as session:
    print(session.run([tensor]))
```
将会输出以下内容，每个数值都被+2处理了:
```
[array([[3.],
       [4.],
       [5.],
       [6.]], dtype=float32)]
```

---
####分箱列Bucketized column
分箱是指把一个连续的数字范围分成几段，比如我们经常说的【80后，90后，00后，10后】这些就是把一个连续的年份（1980～现在2018）分成了4段，我们把这些年份分别写在39张卡片上，然后准备四个箱子，分别标上【0号箱80后】【1号箱90后】【2号箱00后】【3号箱10后】，卡片1980～1989放入【0号箱】，卡片1990～1999放入【1号箱】...
![](http://upload-images.jianshu.io/upload_images/4324074-0374bdbae0724744.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


为什么这样做？

在我们分箱之前，我们的用excel填写100个人的出生年代，那么会是
```
  years
0  1988
1  1999
2  2013
3  2004
...
```
如果我们要用这些数据分析90后的身高分布情况，那么这样的数据看起来就比较麻烦。而分箱后的数据就好多了，我们用0表示80后，1表示90后，2表示00后，3表示10后：
```
  years
0  0  #1988
1  1  #1999
2  3  #2013
3  2  #2004
...
```

我们继续更进一步，比起简单的数字，Tensorflow更喜欢列表类型，更善于从列表或矩阵中估算出变化规律。
共有4段年代，我们表示为包含4个元素的列表[y0,y1,y2,y3],80后第一个元素中招，标记为[1,0,0,0]；90后第二个元素中招，[0,1,0,0],以此类推，我们得到
```
0  [1,0,0,0]  #1988
1  [0,1,0,0]  #1999
2  [0,0,0,1]  #2013
3  [0,0,1,0]  #2004
```

在这个例子中，我们把1980～now年份用3个边界(1990，2000，2010)划为4段（假设我们的数据不存在早于1980出生的人），我们可以使用下面的代码进行测试:
```
import tensorflow as tf

years = {'years': [1999,2013,1987,2005]}  

years_fc = tf.feature_column.numeric_column('years')
column = tf.feature_column.bucketized_column(years_fc, [1990, 2000, 2010])

tensor = tf.feature_column.input_layer(years, [column])

with tf.Session() as session:
    print(session.run([tensor]))
```
运行得到下面的输出，可以看到每一个年份的列表对应的元素变成了1，而其他元素为0:
```
[array([[0., 1., 0., 0.],  #1999
       [0., 0., 0., 1.],  #2013
       [1., 0., 0., 0.],  #1987
       [0., 0., 1., 0.]],  #2005
       dtype=float32)]
```
>Bucketized也被称作分桶，在这里参考谷歌官方说法统一称为分箱。

---
####关于独热编码one-hot
顾名思义，在上面的列表中[0,1,0,0]中只有第二个元素为1，热起来了，其他元素都是0。所以叫独热。

可以这样说，如果某个特征有M种可能，而我们有三个数据[m1,m2,m3]，可以把它变成一个由0和1组成3xM的二维矩阵,类似下图：

![](imgs/4324074-2ea2a697eb1ea320.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


分箱特征栏Bucketized column就是把一维的普通列表变成了二维矩阵，升维了！

为什么会这样做？不是把数据复杂化了吗？
其实是把数据简化了，独热之后我们只剩下0或1，1只是代表一个位置，并不关注这一行具体代表什么含义。

######首先，升维往往能让数据直接的关系更加清楚，更易于找到规律。其次，也是更重要的，分箱之后可以让无序数据之间关系更加正确。

比如我们有三种商品分类，['服装','食品','化妆品']，如果我们只是把它转化为[0,1,2]，那么我们如果在几何空间中计算它们之间的距离关系，三个类别代表线段上的三个点，我们会得到服装距离食品是1-0=1，食品距离化妆品是2-1=1，而服装距离化妆品是2-0=2；计算机就会误以为化妆品和服装关系很远。但实际上这毫无依据，这种错误关系完全是由于我们的数据格式引发的。
![直线上两点间距离公式](imgs/4324074-3a758012b8e6823a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


再看分箱后的结果，三种类别变为服装[1,0,0],食品[0,1,0],化妆品[0,0,1],它们代表三维空间中的三个点，利用距离平方等于每个维度平方之和，我们得到它们三者之间的距离都是根号2，完全相等，没有任何偏倚。
![空间中两点间距离公式](imgs/4324074-2c6d4c66037045ae.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


---
####分类识别列Categorical identity column
很多数据都不是数字格式的，比如动物的类别“猫狗牛羊”、商品的类别“食品服装数码”、人的姓氏“张王李赵”...这些都是文字格式的。

######但是，Tensorflow只能处理数字。

我们必须把字符名称变为数字模式，或者说我们必须用数字来表示文字。
参照上面的分箱的方法，我们可以创建很多箱子表示各种动物，把每个种类动物名称写在卡片上，放到对应的箱子里。

假设我们有4种宠物分类：猫，狗，兔子，猪，对应列表[a1,a2,a3,a4]那么就有:
![宠物类别的独热编码](http://upload-images.jianshu.io/upload_images/4324074-83728f431eff5aea.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

语法格式
```
categorical_column_with_identity(
    key,
    num_buckets,
    default_value=None
)
```

测试代码
```
import tensorflow as tf

pets = {'pets': [2,3,0,1]}  #猫0，狗1，兔子2，猪3

column = tf.feature_column.categorical_column_with_identity(
    key='pets',
    num_buckets=4)

indicator = tf.feature_column.indicator_column(column)
tensor = tf.feature_column.input_layer(pets, [indicator])

with tf.Session() as session:
        print(session.run([tensor]))
```
运行输出结果
```
[array([[0., 0., 1., 0.], #兔子
       [0., 0., 0., 1.], #猪
       [1., 0., 0., 0.], #猫
       [0., 1., 0., 0.]], dtype=float32)] #狗
```

---

####分类词汇列Categorical vocabulary column
在上面的示例图中我们看到，必须手工在excel里面把cat、dog、rabbit、pig转为0123才行，能不能更快一些？
tf.feature_column.categorical_column_with_vocabulary_list这个方法就是将一个单词列表生成为分类词汇特征列的。

语法格式
```
categorical_column_with_vocabulary_list(
    key,
    vocabulary_list,
    dtype=None,
    default_value=-1,
    num_oov_buckets=0
)
```
>num_ovv_buckets，Out-Of-Vocabulary，如果数据里面的某个单词没有对应的箱子，比如出现了老鼠mouse，那么就会在【箱子总数4～num_ovv_buckets+ 箱子总数=7】，如果num_ovv=3,那么老鼠mouse会被标记为4～7中的某个数字，可能是5，也可能是4或6。num_ovv不可以是负数。

测试代码
```
import tensorflow as tf

pets = {'pets': ['rabbit','pig','dog','mouse','cat']}  

column = tf.feature_column.categorical_column_with_vocabulary_list(
    key='pets',
    vocabulary_list=['cat','dog','rabbit','pig'], 
    dtype=tf.string, 
    default_value=-1,
    num_oov_buckets=3)

indicator = tf.feature_column.indicator_column(column)
tensor = tf.feature_column.input_layer(pets, [indicator])

with tf.Session() as session:
    session.run(tf.global_variables_initializer())
    session.run(tf.tables_initializer())
    print(session.run([tensor]))
```
输出结果如下，注意到独热list 有7个元素，这是由于【猫狗兔子猪4个+num_oov_buckets】得到的。
```
[array([[0., 0., 1., 0., 0., 0., 0.], #'rabbit'
       [0., 0., 0., 1., 0., 0., 0.], #'pig'
       [0., 1., 0., 0., 0., 0., 0.], #'dog'
       [0., 0., 0., 0., 0., 1., 0.], #mouse
       [1., 0., 0., 0., 0., 0., 0.]], dtype=float32)] #'cat'
```

单词有些时候会比较多，这时候我们可以直接从文件中读取文字列表：
```
import os
import tensorflow as tf

pets = {'pets': ['rabbit','pig','dog','mouse','cat']}  

dir_path = os.path.dirname(os.path.realpath(__file__))
fc_path=os.path.join(dir_path,'pets_fc.txt')

column=tf.feature_column.categorical_column_with_vocabulary_file(
        key="pets",
        vocabulary_file=fc_path,
        num_oov_buckets=0)

indicator = tf.feature_column.indicator_column(column)
tensor = tf.feature_column.input_layer(pets, [indicator])

with tf.Session() as session:
    session.run(tf.global_variables_initializer())
    session.run(tf.tables_initializer())
    print(session.run([tensor]))
```
其中pets_fc.txt每行一个单词如：
```
cat
dog
rabbit
pig
```
管理员权限运行，得到以下结果，这次我们oov使用了0，并没有增加元素数量，但是也导致了mouse变成了全部是0的列表
```
[array([[0., 0., 1., 0.], #rabbit
       [0., 0., 0., 1.], #pig
       [0., 1., 0., 0.], #dog
       [0., 0., 0., 0.],#mosue
       [1., 0., 0., 0.]], dtype=float32)] #cat
```

---
####哈希栏Hashed Column
仍然是分箱，但是这一次我们更加关心“我希望有多少分类？”，也许我们有150个单词，但我们只希望分成100个分类，多下来50个的怎么处理？

取余数！101除以100余1，我们就把第101种单词也标记为1，和我们的第1种单词变成了同一类，如此类推，第102种和2种同属第2类,第103种和3种同属第3类...

我们把计算余数的操作写为%；那么第N个单词属于N%100类。
```
feature_id = hash(raw_feature) % hash_buckets_size
```
哈希列HashedColumn对于大数量的类别很有效（vocabulary的file模式也不错），尤其是语言文章处理，将文章分句切词之后，往往得到大数量的单词，每个单词作为一个类别，对于机器学习来说，更容易找到潜在的单词之间的语法关系。

但哈希也会带来一些问题。如下图所示，我们把厨房用具kitchenware和运动商品sports都标记成了分类12。这看起来是错误的，不过很多时候tensorflow还是能够利用其他的特征列把它们区分开。所以，为了有效减少内存和计算时间，可以这么做。
![](http://upload-images.jianshu.io/upload_images/4324074-ec3e1cf09da0d8c1.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

语法格式
```python
categorical_column_with_hash_bucket(
    key,
    hash_bucket_size,
    dtype=tf.string
)
```

测试代码
```
import tensorflow as tf

colors = {'colors': ['green','red','blue','yellow','pink','blue','red','indigo']}  

column = tf.feature_column.categorical_column_with_hash_bucket(
        key='colors',
        hash_bucket_size=5,
    )

indicator = tf.feature_column.indicator_column(column)
tensor = tf.feature_column.input_layer(colors, [indicator])

with tf.Session() as session:
    session.run(tf.global_variables_initializer())
    session.run(tf.tables_initializer())
    print(session.run([tensor]))
```
运行得到如下的输出,我们注意到red和blue转化后都是一样的，yellow，indigo，pink也都一样，这很糟糕。
```
[array([[0., 0., 0., 0., 1.],#green
       [1., 0., 0., 0., 0.],#red
       [1., 0., 0., 0., 0.],#blue
       [0., 1., 0., 0., 0.],#yellow
       [0., 1., 0., 0., 0.],#pink
       [1., 0., 0., 0., 0.],#blue
       [1., 0., 0., 0., 0.],#red
       [0., 1., 0., 0., 0.]], dtype=float32)]#indigo
```
将hash_bucket_size箱子数量设置为10，这个问题可以得到解决。箱子数量的旋转很重要，越大获得的分类结果越精确。


---

####交叉列Crossed column
交叉列可以把多个特征合并成为一个特征，比如把经度longitude、维度latitude两个特征合并为地理位置特征location。
如下图，我们把Atlanda城市范围的地图横向分成100区间，竖向分成100区间，总共分割成为10000块小区域。（也许接下来我们需要从数据分析出哪里是富人区哪里是穷人区）

![](http://upload-images.jianshu.io/upload_images/4324074-600c7b3412edbc11.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

测试代码如下：
```
import tensorflow as tf

featrues = {
        'longtitude': [19,61,30,9,45],
        'latitude': [45,40,72,81,24]
    }

longtitude = tf.feature_column.numeric_column('longtitude')
latitude = tf.feature_column.numeric_column('latitude')

longtitude_b_c = tf.feature_column.bucketized_column(longtitude, [33,66])
latitude_b_c  = tf.feature_column.bucketized_column(latitude,[33,66])

column = tf.feature_column.crossed_column([longtitude_b_c, latitude_b_c], 12)

indicator = tf.feature_column.indicator_column(column)
tensor = tf.feature_column.input_layer(featrues, [indicator])

with tf.Session() as session:
    session.run(tf.global_variables_initializer())
    session.run(tf.tables_initializer())
    print(session.run([tensor]))
```
上面的代码中进行了分箱操作，分成～33，33～66，66～三箱，运行得到下面输出
```
[array([[0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 1.],
       [0., 0., 0., 0., 0., 0., 0., 0., 0., 1., 0., 0.],
       [0., 0., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
       [0., 0., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
       [0., 0., 0., 0., 0., 1., 0., 0., 0., 0., 0., 0.]], dtype=float32)]
```

---
####指示列Indicator Columns和嵌入列Embeding Columns
我们在上面的代码中使用了很多次指示列命令
```
indicator = tf.feature_column.indicator_column(column)
tensor = tf.feature_column.input_layer(featrues, [indicator])
```
指示列并不直接操作数据，但它可以把各种分类特征列转化成为input_layer()方法接受的特征列。

当我们遇到成千上万个类别的时候，独热列表就会变的特别长[0,1,0,0,0,....0,0,0]。嵌入列可以解决这个问题，它不再限定每个元素必须是0或1，而可以是任何数字，从而使用更少的元素数表现数据。

如下图，我们最初的数据可能是4个单词比如dog、spoon、scissors、guitar，然后这些单词被分类特征列Categorical处理成为数字0、32、79、80，接下来我们可以使用指示列来处理成为独热的01列表（图中假设我们有81种单词分类），也可以按照嵌入Embeding列来处理成小数元素组成的3元素数列。

![分类列Categorical、指示列Indicator和嵌入列Embeding](http://upload-images.jianshu.io/upload_images/4324074-04d67ac63ac2a92d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

嵌入列中的小数只在train训练的时候自动计算生成，能够有效增加训练模型的效率和性能，同时又能便于机器学习从数据中发现潜在的新规律。

为什么嵌入Embeding的都是[0.421,0.399,0.512]这样的3元素列表，而不是4元5元？实际上有下面的参考算法：
![](http://upload-images.jianshu.io/upload_images/4324074-462cefec68b76339.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

嵌入列表的维数等于类别总数开4次方，也就是3的4次方等于81种类。
![](http://upload-images.jianshu.io/upload_images/4324074-aff625883bb1b18f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

嵌入列语法
```
embedding_column(
    categorical_column,
    dimension,
    combiner='mean',
    initializer=None,
    ckpt_to_load_from=None,
    tensor_name_in_ckpt=None,
    max_norm=None,
    trainable=True
)
```

> dimention维度，即每个列表元素数
combiner组合器，默认meam，在语言文字处理中选sqrtn可能更好
initializer初始器
tensor_name_in_ckpt可以从check point中恢复
ckpt_to_load_from恢复文件

示例代码
```
import tensorflow as tf

features = {'pets': ['dog','cat','rabbit','pig','mouse']}  

pets_f_c = tf.feature_column.categorical_column_with_vocabulary_list(
    'pets',
    ['cat','dog','rabbit','pig'], 
    dtype=tf.string, 
    default_value=-1)

column = tf.feature_column.embedding_column(pets_f_c, 3)
tensor = tf.feature_column.input_layer(features, [column])

with tf.Session() as session:
    session.run(tf.global_variables_initializer())
    session.run(tf.tables_initializer())

    print(session.run([tensor]))
```
运行得到输出,我们看到由于老鼠mouse没有对应的箱子，所以元素都为0
```
[array([[ 0.15651548, -0.620424  ,  0.41636208],
       [-1.0857592 ,  0.03593585,  0.20340031],
       [-0.6021426 , -0.48347804, -0.7165713 ],
       [-0.36875582,  0.4034163 , -1.0998975 ],
       [ 0.        ,  0.        ,  0.        ]], dtype=float32)]
```

---
####特征列和估算器Estimator
在鸢尾花的案例中，我们拼接多个数值特征列numeric column成为feature_columns列表
```
feature_columns = []
for key in train_x.keys():
    feature_columns.append(tf.feature_column.numeric_column(key=key))
```
然后利用特征列创建了深度神经网络分类器tf.estimator.DNNClassifier：
```
classifier = tf.estimator.DNNClassifier(
    feature_columns=feature_columns,
    hidden_units=[10, 10],
    n_classes=3,
    model_dir=models_path,
    config=ckpt_config) #
```
有了这个DNNClassifier我们就能对原始数据进行train、evaluate、pedict。
Tensorflow提供了多个评估器，但不是每种评估器都能够接收所有类型的特征列feature column。
* 线性分类器 linearClassifier和线性回归器linearRegressor，接收所有类型特征列；
* 深度神经网络分类器DNNClassifier和深度神经网络回归器DNNRegressor，仅接收密集特征列dense column,其他类型特征列必须用指示列indicatorColumn或嵌入列embedingColumn进行包裹
* 线性神经网络合成分类器linearDNNCombinedClassifier和线性神经网络合成回归器linearDNNCombinedRegressor：
  * linear_feature_columns参数接收所有类型特征列
  * dnn_feature_columns只接收密度特征列dense column

---
####分类列CategoricalColumn和密集列DenseColumn
上面介绍了Tensorflow用于生成特征列的9个方法（tf.feature_column...），每个方法最终都会得到分类列或者密集列：
![](http://upload-images.jianshu.io/upload_images/4324074-8bfbf778dc5a34c3.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

---
####权重分类列WeightedCategoricalColumn
默认的CategoricalColumn所有分类的权重都是一样的，没有轻重主次。而权重分类特征列则可以为每个分类设置权重。
语法格式
```
weighted_categorical_column(
    categorical_column,
    weight_feature_key,
    dtype=tf.float32
)
```
测试代码
```
import tensorflow as tf
from tensorflow.python.feature_column.feature_column import _LazyBuilder

features = {'color': [['R'], ['A'], ['G'], ['B'],['R']],
                  'weight': [[1.0], [5.0], [4.0], [8.0],[3.0]]}

color_f_c = tf.feature_column.categorical_column_with_vocabulary_list(
    'color', ['R', 'G', 'B','A'], dtype=tf.string, default_value=-1
)

column = tf.feature_column.weighted_categorical_column(color_f_c, 'weight')

indicator = tf.feature_column.indicator_column(column)
tensor = tf.feature_column.input_layer(features, [indicator])

with tf.Session() as session:
    session.run(tf.global_variables_initializer())
    session.run(tf.tables_initializer())
    print(session.run([tensor]))
```
运行之后得到下面输出，权重改变了独热模式，不仅包含0或1，还带有权重值
```
[array([[1., 0., 0., 0.],
       [0., 0., 0., 5.],
       [0., 4., 0., 0.],
       [0., 0., 8., 0.],
       [3., 0., 0., 0.]], dtype=float32)]
```

---
####线性模型LinearModel
对所有特征进行线性加权操作（数值和权重值相乘）。
语法格式
```
linear_model(
    features,
    feature_columns,
    units=1,
    sparse_combiner='sum',
    weight_collections=None,
    trainable=True
)
```
测试代码
```
import tensorflow as tf
from tensorflow.python.feature_column.feature_column import _LazyBuilder


def get_linear_model_bias():
    with tf.variable_scope('linear_model', reuse=True):
        return tf.get_variable('bias_weights')


def get_linear_model_column_var(column):
    return tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES,
                             'linear_model/' + column.name)[0]

featrues = {
        'price': [[1.0], [5.0], [10.0]],
        'color': [['R'], ['G'], ['B']]
    }

price_column = tf.feature_column.numeric_column('price')
color_column = tf.feature_column.categorical_column_with_vocabulary_list('color',
                                                                      ['R', 'G', 'B'])
prediction = tf.feature_column.linear_model(featrues, [price_column, color_column])

bias = get_linear_model_bias()
price_var = get_linear_model_column_var(price_column)
color_var = get_linear_model_column_var(color_column)

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    sess.run(tf.local_variables_initializer())
    sess.run(tf.tables_initializer())

    sess.run(bias.assign([7.0]))
    sess.run(price_var.assign([[10.0]]))
    sess.run(color_var.assign([[2.0], [2.0], [2.0]]))

    predication_result = sess.run([prediction])

    print(prediction)
    print(predication_result)
```
运行结果得到
```
[array([[ 19.],
       [ 59.],
       [109.]], dtype=float32)]
```

---

以上全部演示代码都可以[从百度网盘下载](https://pan.baidu.com/s/1QrU8rL1a-phwoPHp8-WtgQ)(提取密码:qdvx)

---
###探索人工智能的新边界
如果您发现文章错误，请不吝留言指正；
如果您觉得有用，请点喜欢；
如果您觉得很有用，感谢转发~
---
END


