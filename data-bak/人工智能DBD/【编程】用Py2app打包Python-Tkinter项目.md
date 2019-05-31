欢迎关注我的专栏( つ•̀ω•́)つ[【人工智能通识】](https://www.jianshu.com/c/e9a7b7b7024d)
[【专题】Python-Tkinter项目编程入门](https://www.jianshu.com/p/0f5011b3d6bb)

---

##MacOS下打包Python应用

参照以下步骤将我们[上一篇](https://www.jianshu.com/p/a54a5eab7e17)编写的main.py文件打包成一个MacOS标准软件：

- `pip3 install py2app`命令进行安装py2app工具
- 从命令行用`cd xxx`进入到main.py文件所在的目录（可选）
- `py2applet --make-setup main.py`命令创建一个setup.py的打包脚本文件
- `python3 setup.py py2app -A`命令运行打包脚本，生成app文件

正常的话将会生成几个目录，最终软件在dist文件夹下面main.app：

![](imgs/4324074-8a0d85cbade87447.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

直接点击运行main.app可以打开。

如果遇到无法打开的问题，请尝试把build和dist文件夹以及setup.py删除，然后重新启动VSCode（或者把电脑也重启），然后重试，注意确认**文件目录要正确，不要在上层执行这些命令**。

##添加图标

你可以直接在[EasyIcon网站](https://www.easyicon.net/)下载icns格式的图标（不是所有图标都有这个格式可以下载），然后放到main.py一起，再打开setup.py文件，修改OPTIONS内容：
```
OPTIONS = {
    'iconfile':'icon.icns'
}
```
然后重新运行脚本`python3 setup.py py2app -A`，这样生成的main.app就是带有图标的软件了。

也可以使用命令的参数模式直接生成带有图标设置的setup文件：
```py2applet --make-setup main.py icon.icns```
这个命令会自动添加OPTION信息。

##Windows打包Python应用

以下内容仅供参考：
- `pip3 install pyinstaller`安装工具
- `pyinstaller /path/to/yourscript.py`生成安装包

更多内容请参照pyinstaller官方文档。



---
欢迎关注我的专栏( つ•̀ω•́)つ[【人工智能通识】](https://www.jianshu.com/c/e9a7b7b7024d)

---
###每个人的智能新时代
如果您发现文章错误，请不吝留言指正；
如果您觉得有用，请点喜欢；
如果您觉得很有用，欢迎转载~
---
END