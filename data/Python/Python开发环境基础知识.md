### Python的安装
* 官网https://www.python.org/
* 直接在官方网站下载对应系统的安装包，支持macOS、windows、linux等系统
* 下载后直接安装，windows下需要右键使用管理员权限运行。推荐使用默认安装和默认文件路径
* 安装成功后在命令行工具输入`python`后可以显示python的版本等信息，输入`exit()`退出。
* windows下可能需要系统环境变量，可在设置中搜索“环境变量”或“系统变量”，确保python的路径和实际安装的目录一致

### Python的版本
* 两个主流版本2.x和3.x，两个版本的语法差别很大，3.x版本的代码不能再2.x下正常运行，相反也是
* 推荐使用3.x，如果需要兼容旧有2.x项目，则需要使用2.x版本
* 如果同时安装了2.x和3.x，那么`python3`命令用于3.x，`python`命令用于2.x。如果只安装了3.x，那么这两个命令通用
* 可以使用第三方功能模块virtualenv来为每个项目配置不同的版本使用，virtualenv的安装需要使用下面介绍的pip命令
* 也可以为每个项目创建不同的docker虚拟容器来解决版本冲突问题

### 第三方模块
* 编程不需要自己动手编写项目需要的每个功能，很多常用功能都早已被开发出来模块化，你可以直接拿来使用
* 自己动手重复编写已经成熟的功能模块，是浪费时间的，我们成为“重复造轮子”
* 模块（module）有些时候也被称为库（lib）
* 已有模块分两类，一是Python官方已经整合自带模块，其余是需要单独安装的第三方发布的模块
* Python自带pip命令，在命令行工具中可以使用`pip install xxx`来安装xxx模块，`pip list`显示所有已安装的模块
* 使用`pip --help`命令显示更多帮助命令
* 如果同时安装了Python2.x和3.x，那么`pip3`命令用于3.x，`pip`命令用于2.x。如果只安装了3.x，那么这两个命令通用
* 第三方模块也会有不同版本冲突问题，同样可以使用virtualenv或docker来解决

### 开发工具（IDE）
* 中大型项目开发推荐使用pycharm或eclipse。pycharm专用于python编程，eclipse适用于更多编程语言，但需要安装插件pyDev才能更好的支持python
* python自带了IDEL编程工具，但功能不多，适合执行简单命令或少量代码测试
* 数据分析、数据科学等对编程工具要求不高的工作可以使用jupyter notebook，它可以用pip命令安装
* 其他编辑器如sublime、brackets、atom也可以用来编写python程序

### Anaconda
* Anaconda是一个知名的python发行版，它集成了python和上百个科学计算相关模块集合在一起，下载后一次性安装全部。
* Anaconda包含了jupyter notebook工具，包含了numpy、pandas、scikit-learn等科学计算模块。
* Anaconda提供了一个和pip命令功能相近的命令`conda`，可以`conda install`安装模块
* `conda create -n python36 python=3.6`可以创建指定python版本的环境，`activate python36`激活，`deactivate`退出





