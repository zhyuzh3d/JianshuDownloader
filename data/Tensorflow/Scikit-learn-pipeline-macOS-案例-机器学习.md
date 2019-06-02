通过案例深入认识分类器和机器学习流程。

####分类器函数

机器学习可以自动从众多数据中归纳出分类器函数，这个函数接收新的一条数据作为输入参数x，然后返回一个结果y(即此条数据所对应的分类类别).
![image.png](http://upload-images.jianshu.io/upload_images/4324074-d7fcac69c5b97a99.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

>Features：特征值，足以用来区分类别的若干属性值，用来输入给机器进行学习的数据。如鸢尾花案例中的花萼长宽、花瓣长宽。
>Label：标签，我们希望机器学习输出的结果(我们需要手工为训练数据和测试数据打标签)，如鸢尾花案例中经过训练后计算机能够针对任意鸢尾朵数据评估出所属类型。

####准备工作

可以继续使用前一篇文章的项目，如果没有请参照它的准备工作部分
[Scikit-learn-iris-macOS-案例-机器学习入门](https://www.jianshu.com/p/ea164546dc76)

需要下载安装Python 3.x;
需要从终端安装Pip、Virtualenv并创建项目和初始化、激活虚拟环境
```
sudo easy_install pip
sudo pip install --upgrade virtualenv 
mkdir ~/desktop/myapp
sudo virtualenv --system-site-packages -p python3 ~/venv
cd ~/desktop/myapp
source ./venv/bin/activate
```
>终端提示行前面出现(venv)字样

需要从终端安装Numpy和Scipy,Scikit-learn等第三方模块
```
sudo pip install numpy scipy
pip install -U scikit-learn
```


####训练分类器流程
创建iris2.py文件，包含以下内容
```
#导入数据集（在这里共计150条）
from sklearn import datasets
iris=datasets.load_iris()

#特征和标签
X=iris.data
y=iris.target

#将数据划分为训练数据和测试数据，测试数据占一半即0.5（75条）
from sklearn.cross_validation import train_test_split
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.5)

#创建分类器classifier-决策树分类器DecisionTreeClassifier
from sklearn import tree
my_classifier=tree.DecisionTreeClassifier()

#训练数据
my_classifier.fit(X_train,y_train)

#使用训练好的分类器模型进行预测实验
predictions=my_classifier.predict(X_test)

#预测结果应该和y_test基本一致
print(predictions) 
print(y_test)
```
确保终端进入激活环境，以(venv)开头，如果没有请执行以下命令
```
cd ~/desktop/myapp
source ./venv/bin/activate
```
然后执行我们的python代码
```
python iris2.py
```
仔细观看输出的两个数组是否完全相同，一般情况应该有不同

####计算模型的精确度
在尾部增加以下代码
```
#计算精确度
from sklearn.metrics import accuracy_score
print(accuracy_score(y_test,predictions))
```
输出的结果大概是0.9x，即我们训练的分类器在百分之九十多的情况下都能作出正确的分类。
>由于测试数据和训练数据的划分是随机的，所以每次结果可能略有不同。

####邻近分类器
注释掉创建分类器的两行代码，更换新的分类器
```
#from sklearn import tree
#my_classifier=tree.DecisionTreeClassifier()
from sklearn.neighbors import KNeighborsClassifier
my_classifier=KNeighborsClassifier()
```
再次运行，观察输出的精确度。可能提高也可能降低。

####深入理解分类器
分类器就如同下图中的虚线，将红绿两种类型的点分开。
我们可以使用一个函数表示这个直线y=mx+b,那么寻找这条直线的过程就是计算m和b的值。
机器学习就是从训练数据中自动归类寻找到这样的m、b的值(当然机器学习的实际情况比这要复杂很多，可能是条曲线，甚至是个曲面，可能复杂到人类难于理解的地步)
![image.png](http://upload-images.jianshu.io/upload_images/4324074-a99e168b2668ae54.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

---
###探索人工智能的新边界
如果您发现文章错误，请不吝留言指正；
如果您觉得有用，请点喜欢；
如果您觉得很有用，感谢转发~
---
END



