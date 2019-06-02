欢迎关注我的专栏( つ•̀ω•́)つ[【人工智能通识】](https://www.jianshu.com/c/e9a7b7b7024d)
[【专题】简书下载器：Python-Tkinter项目编程入门](https://www.jianshu.com/p/0f5011b3d6bb)

---

最近遇到的问题，Python中使用Tkinter，但一运行就花屏系统崩溃注销。

问题出在MacOS系统升级和默认的Python版本（3.6.x)不兼容，重新到Python官网下载安装包安装，然后更改默认的`python`命令指向。

即使安装了新版本的python,但默认的`python`命令很可能仍然指向老版本（我的老版本是3.6.x,新版本是3.7.3)，如果不修改的话，还用`python xxx.py`运行仍然会花屏崩溃。

先在【访达-前往-前往文件夹】输入`/usr/local/bin/`,然后查看下面是否有最新版本的python应用文件，比如python3.7，如果有那么就可以用下面的命令把默认的`python`命令指向最新的3.7了：
```
echo "alias python=/usr/local/bin/python3.7" >> ~/.bashrc
echo "source ~/.bashrc" >> ~/.bash_profile
source  ~/.bashrc
python -V
```
这里第一句是向.bashrc文件添加python命令的指向；第二句是确保.bashrc以后会自动被调用（加入到.bash_profile文件中的列表都会在终端启动时候调用）；第三句是先调用一下，以确保当前终端生效；最后一句是输出当前python命令对应的版本号。

>如果你在系统的终端工具中运行上面的代码，又在VSCode中使用python命令，那么很可能仍然是使用的老版本命令，因为VSCode里面的终端也是独立的，你必须重启VSCode或者在VSCode里面执行`source  ~/.bashrc`才有效。

最后应该会输出python命令对应的版本号（我的是3.7.3)，然后再次执行`python xxx.py`将会切换到新版本环境下运行，可以正常使用Tkinter了。

>注意，对于之前用py2app打包生成好的app文件仍然会花屏，只能重新打包。关于如何将python文件打包成独立app，请参考这个文章：[MacOS下打包Python应用](https://www.jianshu.com/p/5ad62b355c07)。对于最新的macOS系统可能有兼容性问题，仍然会花屏，暂时似乎无解。

上面介绍的修改.bashrc文件的方法虽然有效，但也有一些隐患，更多内容请参照这个英文教程：[The right and wrong way to set Python 3 as default on MacOS](https://opensource.com/article/19/5/python-3-default-macos)


>附带，正常情况这些是不需要使用的。
tck/tk的安装：
查看当前的tck/tk版本
`python -m tkinter`
[这里下载最新版本](https://tcl.tk/software/tcltk/)
安装命令(分别安装tcl和tk，只第一行不同):
```
tar -zvxf tk8.6.9.1-src.tar.gz
cd tk8.6.9
cd macosx
./configure
make
sudo make install
```

---
欢迎关注我的专栏( つ•̀ω•́)つ[【人工智能通识】](https://www.jianshu.com/c/e9a7b7b7024d)

---
###每个人的智能新时代
如果您发现文章错误，请不吝留言指正；
如果您觉得有用，请点喜欢；
如果您觉得很有用，欢迎转载~
---
END