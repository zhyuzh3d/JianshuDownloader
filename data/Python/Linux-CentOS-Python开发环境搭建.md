### CentOS安装Python
1. CentOS已经自带安装了2.x版本,先尝试`python`命令检查已安装的版本.如果你使用rpm、yum或deb命令安装过，请使用相对命令查询。
1. 复制安装文件链接。在https://www.python.org/ftp/python/ 进入对应的文件夹，选择`Python-3.x.0.tgz`右键复制链接
1. 在centOS下载tgz安装文件。使用`wget https://www.python.org/ftp/python/3.7.0/Python-3.7.0.tgz`，这里的链接请使用上一步复制的地址
1. 安装必要的其他软件包。使用`yum install gcc openssl-devel bzip2-devel libffi libffi-devel`进行安装
1. 解压安装文件。`tar xzf Python-3.7.0.tgz`。
1. 编译前准备。`cd Python-3.7.0`进入文件夹，执行`./configure --enable-optimizations`
1. 进行安装。可能需要一点时间，`make altinstall`
1. 检查是否安装成功。`python3.7 -V`，成功应该输出版本号。运行`python -V`显示原有的python版本号。

### CentOS修改命令别名
1. 安装位置。你可以在`\usr\local\bin`文件夹下看到已安装的python3.7
1. 修改命令别名。`update-alternatives --install /usr/bin/python3 python3 /usr/local/bin/python3.7 0`,最后0表示优先级。
1. 删除别名关联。`update-alternatives --remove python3 /usr/local/bin/python3.7`

### 使用virtualenv管理项目
1. 安装。`pip3 install virtualenv`,这里的pip3可能需要使用`update-alternatives --install`方法添加别名，目标文件在`/usr/local/bin/pip3.7`
1. 创建项目环境。`virtualenv env`,这将自动创建env文件夹。
1. 激活当前环境。`source env/bin/activate`
1. 退出激活状态。`deactivate`
1. 更多请参照virtualenv的官方说明或网络教程。

### Ubuntu安装Python
1. ubuntu16.04自带了Python2.7和3.5.
1. 你可以使用类似CentOS的源码安装方式进行安装
1. 也可以使用apt-get命令进行安装。基本命令如下：
```
$ sudo add-apt-repository ppa:deadsnakes/ppa
$ sudo apt update
$ sudo apt install python3.6
```
更多内容请参照网络教程。




