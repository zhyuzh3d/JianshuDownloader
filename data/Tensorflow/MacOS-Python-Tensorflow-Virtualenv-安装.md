
--

#### 安装python

从官方网站下载并安装Python3.x最新版[https://www.python.org/downloads/mac-osx/](https://www.python.org/downloads/mac-osx/)

--

#### 安装pip

pip是python第三方包（扩展功能包）安装和管理工具，有了它我们可以安装各种扩展功能

终端执行下面的命令，安装pip

```
sudo easy_install pip
```
--

#### 安装virtualenv

Virtualenv是用来为每个项目创建单独的python虚拟运行环境，每个项目可以使用不同的第三方包，各个项目互不干扰

终端执行以下命令，用pip安装virtualenv
```
sudo pip install --upgrade virtualenv
```
--

#### 建立环境

创建python项目文件夹

```
mkdir ~/desktop/myapp
```
进入文件夹
```
cd ~/desktop/myapp
```
初始化虚拟运行环境
```
sudo virtualenv --system-site-packages -p python3 ./venv
```
说明：--system-site-packages表示为将这个项目单独安装第三方包，-p python3设定python的版本，./venv是虚拟环境相关文件放在这个文件夹内

--

#### 激活环境

终端运行以下命令
```
cd ~/desktop/myapp
source ./venv/bin/activate
```
说明：以后每次要运行python文件(.py文件)，都要先激活环境。source命令是执行activate文件。这句命令会改变终端的提示文字，变为(venv) xxx表示环境已经激活；以后如果要退出激活状态，直接运行deactivate命令

--

#### 安装tensorflow

tensorflow只是python的一个第三方包，可以在环境激活情况下用pip来安装它
```
pip3 install --upgrade tensorflow
```
说明：更多

--

#### 验证安装是否成功

打开应用程序中python文件夹内自带IDLE，command+n打开新窗口，粘贴以下代码

```
import tensorflow as tf
import os
os.environ['TF_CPP_MIN_LOG_LEVEL']= '2'
hello = tf.constant('Hello, TensorFlow!')
sess = tf.Session()
print(sess.run(hello))
```

另存到myapp文件夹内，命名a.py

说明：也可以使用任意文字编辑工具生产这个文件；也可以放到任意文件夹下任意名称，这里只是为了方便

--

#### 运行python代码

终端确保进入myapp，并已经激活环境（提示行以(venv)开头），否则请执行以下命令进行激活
```
cd ~/desktop/myapp
source ./venv/bin/activate
```
执行以下命令运行a.py文件
```
python a.py
```
如果正常输出了Hello, TensorFlow!或者b'Hello, TensorFlow!'就表示安装成功了！

--

#### 图表库matplotlib测试案例

进入激活环境，安装matplotlib
```
sudo pip install matplotlib
```
创建测试文件b.py，包含以下代码

```python
import tensorflow as tf
import numpy as np
import matplotlib.pylab as plt
# 使用TensorFlow 定义一个随机数构成的 2 * 20 的矩阵，并将其赋给变量 a
a = tf.random_normal([2, 20])
# a 是一个Tensor("random_normal:0", shape=(2, 20), dtype=float32) 对象
sess = tf.Session()
out = sess.run(a)
# 将数组中的元素分别赋值给 x、y
x, y = out
# 使用matplotlib.pylab 绘制一个散点图 x 对应横轴 y 对应竖轴
# 其实就是取出 x y 种索引相同的两个数后分别当做
横轴和竖轴显示成一个点
plt.scatter(x, y)
#显示绘制的图像
plt.show()
```
终端运行这个文件
```
python b.py
```

如果弹出一个图表窗口就表示成功了！

说明：如果出现RuntimeError: Python is not installed as a framework.类似错误，请新建一个文件保存为文件名matplotlibrc，放在桌面即可，文件内只包含一行命令
```
backend:TkAgg
```
然后在访达finder内前往~/.matplotlib，将文件matplotlibrc拷贝到这里，再重新运行python b.py就正常了。

--

提示：很多时候使用sodu命令可以解决permit相关授权错误（但个别情况会不能用），官方安装说明有几处没有强调这个；遇到提示错误要认真阅读，到网上搜索解决方案。

---
###探索人工智能的新边界
如果您发现文章错误，请不吝留言指正；
如果您觉得有用，请点喜欢；
如果您觉得很有用，感谢转发~
---
END
