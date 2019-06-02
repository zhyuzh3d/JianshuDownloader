####准备工作
[我已经把相关文件放到百度云，点这里下载](https://pan.baidu.com/s/1i66z0pv)
提取密码 im6s
![](http://upload-images.jianshu.io/upload_images/4324074-6cf94c94d9e60ffd.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

如果希望使用最新文件，请参照下面内容中的文字链接

####python安装
[进入官方下载页面了解详情](https://www.python.org/downloads/release/python-364/)
[直接下载安装程序 [Windows x86-64 executable installer](https://www.python.org/ftp/python/3.6.4/python-3.6.4-amd64.exe)
（windows7或更高， 64位系统）](https://www.python.org/ftp/python/3.6.4/python-3.6.4-amd64.exe)
下载后双击安装程序，勾选添加系统路径选项
![](http://upload-images.jianshu.io/upload_images/4324074-63f267a1daea5f9b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


点击默认安装即可
![](http://upload-images.jianshu.io/upload_images/4324074-1d9207f0af74cc43.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

[可选] 最后点击禁用路径长度限制
![](http://upload-images.jianshu.io/upload_images/4324074-372fcbe9da39df51.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


安装成功后会在windows程序列表里面出现
![](http://upload-images.jianshu.io/upload_images/4324074-acbcf1510a406fc2.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

点击IDLE就打开了Python编辑环境shell，可以在这里直接输入命令，回车运行。
![image.png](http://upload-images.jianshu.io/upload_images/4324074-eb9db592ac8503b0.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
```python
print('Hi,python!');
```

也可以从shell的File菜单新建文件编写更加复杂的命令，保存到桌面，名称a.py文件。
![](http://upload-images.jianshu.io/upload_images/4324074-131088add436245a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

在桌面双击a.py文件就能运行（黑色窗口一闪而过）。如果需要编辑修改，右键点击选择Edit with IDLE。
打开windows的命令提示符工具中用命令运行a.py，这样可以看到正常输出字符。

![](http://upload-images.jianshu.io/upload_images/4324074-e9819ef5cd1a0077.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
>你可以在程序列表里面找到命令提示符工具（cmd.exe），Win10可以直接搜索到。必要的话百度一下。

> cd desktop是进入桌面。如果把a.py放在了其他文件夹，也可以用cd命令进入，比如cd projects。cd ..命令是退出当前文件夹，进入上一级文件夹。进入D盘不需要cd，直接输入D：，然后回车就可以。

最后，在命令提示符里面测试python命令的环境路径是否添加成功
![](http://upload-images.jianshu.io/upload_images/4324074-1d99e9aeb3f8418d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
>可以直接关闭命令提示符工具，或者输入exit()退出python命令

####Tensorflow安装
[点这里查看官方安装指南](https://www.tensorflow.org/install/install_windows)
在命令提示符窗口中输入
```
pip3 install --upgrade tensorflow
```
![](http://upload-images.jianshu.io/upload_images/4324074-396a48fa59df208c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

>pip3命令是python特有的安装和管理第三方模块的命令。tensorflow只是python的一个功能模块。

>下载过程可能很慢，十几分钟或更多，如果进度卡住了可以按几下回车试试看。

[也可以从这里下载tensorflow-1.6.0-cp36-cp36m-win_amd64.whl](https://pypi.python.org/pypi/tensorflow),下载后从命令提示符窗口进入到下载文件存放的文件夹，执行
```
pip3 install tensorflow-1.6.0-cp36-cp36m-win_amd64.whl
```
然后自动会下载安装tensorflow必须的其他模块，比如 wheel, six, protobuf, termcolor, gast, astor, grpcio, numpy, html5lib, bleach, werkzeug, markdown, tensorboard, absl-py, tensorflow等等。

####验证安装
把刚才桌面上的a.py右键Edit with IDLE打开，改为以下代码
```
import tensorflow as tf
import os
os.environ['TF_CPP_MIN_LOG_LEVEL']= '2'
hello = tf.constant('Hello, TensorFlow!')
sess = tf.Session()
print(sess.run(hello))
```
然后在命令提示符窗口进入到desktop，执行a.py。如果输出Hello, TensorFlow就表示成功了！
![](http://upload-images.jianshu.io/upload_images/4324074-fb43018db48a2388.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

---
###探索人工智能的新边界
如果您发现文章错误，请不吝留言指正；
如果您觉得有用，请点喜欢；
如果您觉得很有用，感谢转发~
---
END







