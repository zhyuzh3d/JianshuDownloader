####Python安装
下载最新版本安装程序
[点这里进入官方下载页面
然后选择对应的 Mac/Windows ...installer](https://www.python.org/downloads/release/python-364/)

下载后直接安装，Windows用户注意勾选【Add Python.. to path】

打开命令行工具（Windows的命令提示符工具，MacOS的终端，下同）。
尝试执行python3 -V命令和pip3 -V命令检查是否安装成功。
![](http://upload-images.jianshu.io/upload_images/4324074-86b5986f6e3cc7cb.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

####安装Tensorflow
Windows右键命令行工具，以管理员身份运行，执行以下代码：
```
pip3 install -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com tensorflow
```
Mac下直终端接运行以下代码然后输入管理员密码：
```
sudo pip3  --trusted-host http://mirrors.aliyun.com/pypi/simple/ install --upgrade tensorflow
```
这需要一段时间，安装完成后，从应用程序列表找到Python文件夹下的IDLE，打开它，输入import tensorflow as tf回车，如果没有提示错误就表示安装成功。
![](http://upload-images.jianshu.io/upload_images/4324074-2a44784390615e55.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

>如果经常timeout出错，可以安装命令增加```--default-timeout=100```来增加超时设置，比如```pip --default-timeout=100 install -U Pillow```

>命令中的```http://mirrors.aliyun.com/pypi/simple/ ```也可以换为以下任意一个地址
```http://pypi.douban.com/```
```http://pypi.hustunique.com/```
```http://pypi.sdutlinux.org/```
```https://pypi.tuna.tsinghua.edu.cn/simple/```

>把阿里云镜像作为pip默认安装源，依次执行命令
```cd ~```
```mkdir .pip```
```cd .pip```
然后执行下面命令直接在命令行新建并打开conf文件
```sudo vi ~/.pip/pip.conf```
然后直接粘贴下面一行
```[global] index-url = http://mirrors.aliyun.com/pypi/simple/ [install] trusted-host=mirrors.aliyun.com```
然后输入冒号再输入wq保存并退出```:wq```，或者```:q!```放弃保存
好了，修改配置完成


---
###探索人工智能的新边界
如果您发现文章错误，请不吝留言指正；
如果您觉得有用，请点喜欢；
如果您觉得很有用，感谢转发~
---
END



 