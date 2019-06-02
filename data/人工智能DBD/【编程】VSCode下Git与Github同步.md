欢迎关注我的专栏( つ•̀ω•́)つ[【人工智能通识】](https://www.jianshu.com/c/e9a7b7b7024d)

---

在VSCode下如何连接本地Git和远程Github项目。
![](imgs/4324074-84fb90397318deb2.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

之前写过一篇比较啰嗦的版本[VSCode同步推送Github](https://www.jianshu.com/p/bf37a3fdf480)，新手请参考。这里是简化版本并进行了一些完善。

##预先准备
已经安装了VSCode、Git并注册了Github账号，并清楚如何创建Github项目。
如果是第一次接触这些，请参照之前的那个文章。

##设置Git
- Code主菜单-终端-新建终端，打开命令行。
- `git init`初始化，自动新增.git隐藏文件夹。
- 如果搞错了，用`rm -rf .git`命令或手工直接删除文件夹就可以。
- `git config --global user.name "zhyuzh"`,配置用户名任意。
- `git config --global user.email "zhyuzh3d@hotmail.com"`,配置邮箱任意。

##关联Github项目
- `git remote add origin https://username:password@github.com/zhyuzh3d/goWeb.git`，设置Git的远程地址。
- 如果搞错了，修改命令是`git remote set-url origin https://username:password@github.com/zhyuzh3d/goWeb.git`。
- 如果搞错了可以用`git remote remove origin`删除设置,或者手工修改.git/config文件。
- 如果要拉取远程项目(从Github复制到本地)，使用命令`git pull origin master`。


##将修改内容推送到Github
- 先推到本地Git，方法是直接在左侧源代码管理面板的输入框输入任意记录，然后ctrl+回车。
- 再推送到远程Github,方法是同样从左侧源代码管理面板的菜单-推送到...

>如果遇到问题就删除本地项目文件夹重新来。



---
欢迎关注我的专栏( つ•̀ω•́)つ[【人工智能通识】](https://www.jianshu.com/c/e9a7b7b7024d)

---
###每个人的智能新时代
如果您发现文章错误，请不吝留言指正；
如果您觉得有用，请点喜欢；
如果您觉得很有用，欢迎转载~
---
END