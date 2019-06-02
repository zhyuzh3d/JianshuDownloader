利用scikit-learn工具和经典的iris鸢尾花分类案例快速上手机器学习

####准备工作
下载并安装python3.x
https://www.python.org/


终端安装pip和Virtualenv虚拟环境管理
```
sudo easy_install pip
sudo pip install --upgrade virtualenv 
```
创建项目文件夹
```
mkdir ~/desktop/myapp
```
初始化虚拟环境
```
sudo virtualenv --system-site-packages -p python3 ~/venv
```

激活虚拟环境
```shell
cd ~/desktop/myapp
source ./venv/bin/activate
```
>终端提示行前面出现(venv)字样


安装Numpy和Scipy,Scikit-learn
  ```
sudo pip install numpy scipy
pip install -U scikit-learn
```



*图表生产模块，可选安装homebrew https://brew.sh/*
```
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```
>homebrew安装遇到```fatal: unable to access 'https://github.com/Homebrew/homebrew/': SSL certificate problem```这主要是网络不稳定造成的。解决方案：用```sudo vim /etc/resolv.conf```打开设置，输入i进入插入模式，上下移动光标，增加粘贴一行```nameserver 8.8.8.8```或者```nameserver 114.114.114.114```然后esc退出插入模式，```:wq```保存退出，重新使用上面的命令。如果中途又失败，需要重新增加8.8.8.8，因为会被重置。


*图表生产模块，可选安装graphviz（需要翻墙）*
```
brew install graphviz
```
>遇到```The Command Line Tools header package must be installed on Mojave```错误,请按指示目录打开文件夹```/Library/Developer/CommandLineTools/Packages/```进行安装。

>[windows用户点这里下载安装graphviz](https://www.graphviz.org/)

--
####了解案例

Iris鸢尾花分类经典案例介绍
[点这里wiki地址查看详细](https://en.wikipedia.org/wiki/Iris_flower_data_set?utm_campaign=chrome_series_decisiontree_041416&utm_source=gdev&utm_medium=yt-annt)
这里鸢尾花数据集共有150条，每条数据中记录了每朵花的花萼长度、宽度以及花瓣长度、宽度这四个数据。
这些花被植物学家分成三种类型，前50条是setosa(山鸢尾花),中间50条是versicolor(变色鸢尾花)，最后三种是virginica(维吉尼亚鸢尾花)。

但是，计算机并不知道植物学家的分类标准(花萼多宽是山鸢尾花？花瓣多长是变色鸢尾花？)。我们的任务就是训练计算机根据这些数据推算出植物学家的分类标准(模型)，以便于以后对任何一朵鸢尾花数据都能自动判断出类型来。

--
####了解数据
应用程序python文件夹中的IDLE，command+n新建,然后save as存储到桌面myapp文件夹下命名iris.py,文件内容如下
```
from sklearn.datasets import load_iris
iris=load_iris()
print(iris.feature_names)
print(iris.target_names)
print(iris.data[0])
print(iris.target[0])
for i in range(len(iris.target)):
    print ( i,iris.target[i],iris.data[i],iris.target_names[iris.target[i]])
```

在终端进入项目文件夹并激活环境
```
cd ~/desktop/myapp
source ./venv/bin/activate
```
>前面提示出现(venv)字样

运行我们的代码
```
python iris.py
```
观察输出的各种数据，注意到data包含了四个长宽数字，target表示了属于第几种鸢尾花类型

--
####训练模型和测试模型
我们把第0朵、第50朵、第100朵的数据提取出来作为测试数据，其余的作为训练数据。
然后我们用训练数据培训我们的计算机，让它自动从数据中找出分类规律，也就是分类模型。
然后我们再用这个模型去评估这三朵花(由于没有参与训练，所以计算机并不知道它们是哪一种类型)，如果计算机评估出来的这三朵花类型与之前植物学家的看法一致，我们就认为计算机掌握了鸢尾花的分类方法(尽管我们从头到尾都不知道植物学家如何分类的，也不知道计算机是怎么分类的)。
修改代码如下
```
import numpy as np
from sklearn.datasets import load_iris
from sklearn import tree

iris=load_iris()
test_idx=[0,50,100] #三朵预留出来做测试的花

train_target=np.delete(iris.target,test_idx,0) #训练模型不包含三朵花
train_data=np.delete(iris.data,test_idx,0) #训练模型不包含三朵花

test_target=iris.target[test_idx]
test_data=iris.data[test_idx]

#用数据训练计算机
clf=tree.DecisionTreeClassifier()  #这里使用了决策树分类器
clf.fit(train_data,train_target)

print(test_target) #植物学家对三朵花分类的看法
print(clf.predict(test_data)) #计算机对三朵花分类的看法
```
在终端再次运行我们的代码
```
python iris.py
```
如果正常则输出
```
[0 1 2]
[0 1 2]
```
这表示计算机训练出来的模型和植物学家观点一致

--
####深入理解决策树

*请确保正确安装了graphviz模块*
在最后增加以下代码
```
from sklearn.externals.six import StringIO 
import graphviz 
dot_data = tree.export_graphviz(clf, out_file=None, 
                         feature_names=iris.feature_names,  
                         class_names=iris.target_names,  
                         filled=True, rounded=True,  
                         special_characters=True)  
graph = graphviz.Source(dot_data)  
graph.render("iris")
```
再次执行
```
sudo python iris.py
```
这次将会在桌面myapp文件夹内生成一个pdf文件，打开后类似下图，从图中我们可以看到计算机从147条数据中自动总结出来的分类规律。
![irisClassifierTree.png](http://upload-images.jianshu.io/upload_images/4324074-d5c98871ab13d104.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

---
###探索人工智能的新边界
如果您发现文章错误，请不吝留言指正；
如果您觉得有用，请点喜欢；
如果您觉得很有用，感谢转发~
---
END






