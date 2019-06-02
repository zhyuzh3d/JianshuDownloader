很多官方的案例数据文件都可以利用Tensorflow自带的功能直接从官方服务器上拉取，比如拉取MNIST的4个数据文件：

```
import os
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

dir_path = os.path.dirname(os.path.realpath(__file__))
data_path=os.path.join(dir_path,'MNIST_data')
mnist = input_data.read_data_sets(data_path, one_hot=True)
```

把这几行代码保存，然后运行，就会开始从官方服务器下载文件，可能需要几分钟，下载好的文件被自动放在代码文件同目录下的MNIST_data文件夹下：

![](imgs/4324074-14476efeb9e0e440.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

如果你运行代码的时候遇到```SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed```错误，这是说没有安装SSL安全证书，目前3.6版本python不会自动安装这个证书了，需要我们手工安装，方法是：

请打开电脑的**应用程序-Python3.6**，然后双击运行**Install Certificates.command**文件，等待它成功完成：
![](imgs/4324074-285bea0468e7b3d7.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

一旦下载成功之后，如果再次运行代码并不会重复下载，可以放心使用。如果移动了文件夹，那么相应更换一下dir_path的设置就可以了。

---
###探索人工智能的新边界
如果您发现文章错误，请不吝留言指正；
如果您觉得有用，请点喜欢；
如果您觉得很有用，感谢转发~
---
END
