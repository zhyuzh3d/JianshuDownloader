鸢尾花分类案例可能是机器学习里面最经典的入门案例，新手可能都会遇到它，这篇文章纯粹从概念上进行分析，没有任何正式的代码，希望完全没有编程基础的人也能看懂。

####鸢尾花课题
我们要解决的问题如下
>已知鸢尾花iris分为三个不同的类型：山鸢尾花Setosa、变色鸢尾花Versicolor、韦尔吉尼娅鸢尾花Virginica，这个分类主要是依据鸢尾花的花萼长度、宽度和花瓣的长度、宽度四个指标（也可能还有其他参考）。我们并不知道具体的分类标准，但是植物学家已经为150朵不同的鸢尾花进行了分类鉴定，我们也可以对每一朵鸢尾花进行准确测量得到花萼花瓣的数据。

![三种鸢尾花类型](http://upload-images.jianshu.io/upload_images/4324074-7fe9843c5af010d0.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



>那么问题来了，你女朋友家的一株鸢尾花开花了,她测量了一下，花萼长宽花瓣长宽分别是3.1、2.3、1.2、0.5，然后她就问你：“我家这朵鸢尾花到底属于哪个分类？”

![植物学家给我们的数据表(前面50条都是山鸢尾花Setosa)](http://upload-images.jianshu.io/upload_images/4324074-dec7af17dd814a96.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

>表格说明：横行属于一朵花的数据
Dataset Order:数据集序号（没什么用）
Sepal length/width:花萼的长度/宽度数据
Petal length/width:花瓣的长度/宽度数据
Species：植物学家鉴定的花的类型

####难点在哪？
作为一个传统程序员，一定会很崩溃，因为我们不清楚具体的分类标准，也不能用类似下面这种条件判断解决问题：
```
if(SepalLength>4.1 && SepalLength<2.2 &&....) {
  return “Setosa”
}else(...){
  return “Versicolor”
}...
```
我们不知道是>4.1还是>4.2合适...我们必须从植物学家给我们的150条数据中找出规律。

事情并不那么容易，植物学家可能完全没有对花朵测量，完全凭感觉进行的鉴定，所以他的头脑里根本没有大于小于，根本没有if...else...

甚至我们都不能断定花萼长度这个特征是否可以用2个分界值分成大、中、小三个数据，因为植物学家在头脑里可能把花萼长度分成了特大、大、中、小、超小五个级别，他认为长度特大或中+花萼宽度中或小+花瓣宽度特特大或特大或大+花瓣长度小或超小的才是Setosa：
![假象的植物学家分类思路](http://upload-images.jianshu.io/upload_images/4324074-73f718270449d820.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


这就尴尬了。

####解决思路
我们必须要从这个逻辑深坑里跳出来，换个思考方式。

不要再想去寻找临界值的事情了！

我们需要的是一个方法函数，输入一朵新花的4个测量数据，这个方法就能返回三种分类中的一种。
![](http://upload-images.jianshu.io/upload_images/4324074-7d57e500997045dd.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
或者写作
![](http://upload-images.jianshu.io/upload_images/4324074-559939756d67d40c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
或者是这样的代码
```
function guess(rowData){
  string species;
    ...do something...
  return species
}
guess([2.1,3,4.2,0.3]); 
//输出Versicolor
```

幸运的是，研究机器学习的科学家已经为我们提供了一些成熟的算法，这些算法可以自动从我们150条数据中寻找规律，并自动为我们生成所需要的分类方法函数。

####机器学习
机器学习是如何分析数据并找到规律的？
某智商不高的机器学习科学家发明了最糟糕的分类方法，叫做random乱猜分类器：
```
function guess(rowData){
  string species;
  int n=random()%3; //随机数除以3的余数，0或1或2
  if(n==0){
    species="Virginica";
  }else if(n==1){
    species="Versicolor";
  }else if(n==2){
    species="Setosa";
  }
  return species
}
```
这是一个毫无技术含量的分类方法，但它形式上的确符合我们需要的预期。对于任何一朵新的鸢尾花，这个函数有33.3%猜对。（当然，如果植物学家也真是乱猜乱鉴定的，那么我们这个乱猜分类器就是最合适不过的，——虽然random不会与植物学家脑子吻合，但是任意其他办法也不会更有效了）

另外一个也比较容易理解的分类器是KNN最近邻分类方法，简单说就是把150朵花的数据记在本子上，当有人把新花的测量数据给我的时候，我们就计算新花数据和我们本子上拿朵花最接近，最接近的那朵花的分类就应该是新花的分类。

以上两个分类方法在我的这个文章里面都有详细介绍和正式代码实现，并且里面还有另外一个也能够读懂的确定树分类器的介绍。
[Scikit-learn-iris-macOS-案例-机器学习入门](https://www.jianshu.com/p/ea164546dc76)

Tensorflow使用更加复杂的神经网络分类器，可以处理比上面这种情况复杂几百几千倍的难题，比如图像识别、语音识别等。后续我们会一起慢慢深入到机器学习和人工智能的最内部去弄明白这一切。

---
###探索人工智能的新边界
如果您发现文章错误，请不吝留言指正；
如果您觉得有用，请点喜欢；
如果您觉得很有用，感谢转发~
---
END



















