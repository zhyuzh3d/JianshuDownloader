欢迎关注我的专栏( つ•̀ω•́)つ[【人工智能通识】](https://www.jianshu.com/c/e9a7b7b7024d)

---
当用户请求一个网页的时候，如何让服务器把网页文件发送给用户？

![](imgs/4324074-574be171ee64b2dc.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

上一篇文章：[软件技术-零基础编写Web页面](https://www.jianshu.com/p/a72c0a9c23a6)
[人工智能通识-2019年3月专题汇总](https://www.jianshu.com/p/72685b77cfff)


##文件服务器

首先我们要知道，用户在浏览器中看到的页面其实就是一个`.html`文件，就是我们上一篇文章时候撰写的`<html><head><body>...`代码。

但我们最初用Golang写的服务器只是简单返回`Hello world!`字符串，而不是文件。所以，正确的做法是：

**让Golang读取硬盘上的文件内容，然后发送给用户。**

这就是文件服务器要干的事情，你要`login.html`页面，我就给你`login.html`文件。

在Golang里面，已经提供了快速建立文件服务的功能，就是`http.FileServer`方法，但是首先要知道我们的`web`文件夹放在哪里。


##获取当前文件路径

在Golang里面，可以用`os.Getwd()`获取当前Golang服务软件运行时候所在的目录，我们在`app.go`主入口文件中添加下面的代码来检测当前的目录(在这里我去除了原有的`http.Handle("/")`，因为我们要用文件服务替代它）：
```
package main

import (
	"app/login"
	"log"
	"net/http"
	"os"
	"path"
)

func main() {
	//获取当前程序运行的目录
	dir, _ := os.Getwd()
	fmt.Println(dir)

	//设置login数据服务
	http.HandleFunc("/login", login.HandleFunc)

	//启动服务
	log.Fatal(http.ListenAndServe(":8080", nil))
}
```
首先注意`:=`的用法，这是创建一个新名称，比如`dir:="haha"`就是说我们创建一个新名称叫做`dir`，它代表字符串`"haha"`。
然后注意`dir,_:=os.Getwd()`这个用法，因为后面`os.Getwd()`其实是两个东西，所以等号左边也要是两个。比如下面这个代码会输出`3,4`：
```
a, b := 3, 4
fmt.Println(a, b)
```
最后注意`dir,_`这里的下划线，这是因为如果我们创建了一个新名称（也叫变量）但是如果没有使用这个变量，Golang就会报错。比如上面我们创建了`a、b`也`Println`了两个所以没事，如果只`Println(a)`那就会因为`b`是创建了但没使用而报错。

上面整个代码运行之后会输出当前项目的文件夹路径，也就是`$GOPATH`路径。

##添加文件服务
修改`app.go`成如下代码：
```
package main

import (
	"app/login"
	"fmt"
	"log"
	"net/http"
	"os"
	"path"
)

func main() {

	a, b := 3, 4
	fmt.Println(a, b)

	//获取当前程序运行的目录
	dir, _ := os.Getwd()
	webDir := path.Join(dir, "/web")

	//设置文件服务
	http.Handle("/", http.FileServer(http.Dir(webDir)))

	//设置login数据服务
	http.HandleFunc("/login", login.HandleFunc)

	//启动服务
	log.Fatal(http.ListenAndServe(":8080", nil))

}
```
注意这里的`path.Join(dir, "/web")`是把当前文件夹也就是`$GOPATH`拼接到我们的`/web`文件夹下，我的文件夹结构如下图（`web`文件夹被我移动到了项目目录下而不是之前的`app`文件夹里面）：

![](imgs/4324074-26a93b7100af73be.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

注意`http.FileServer(http.Dir(webDir))`这句就是最关键的创建文件服务的方法。

然后我们打开浏览器，浏览`http://localhost:8080/`就可以打开首页(斜杠默认打开`index.html`)，点击链接就可以跳转到`http://localhost:8080/page/login.html`页面。

![](imgs/4324074-785275ed33dcfd2c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

注意这时候已经和`Live Server`毫无关系，我们这时看网站的方式和用户看我们网站的方式一模一样。

当我们修改`index.html`的标签代码的时候，这个`http://localhost:8080/page/login.html`当然是不会自动刷新的，但只要我们按一下刷新按钮（或者Ctrl+R）就能更新，而不需要`Stop Code Run`再`Run Code`重启。

>Golang的`FileServer`文件服务非常的简单好用，但实际有时候还不够强大，在真实的企业应用中一般不会使用Golang来编写文件服务，而是直接使用现成的文件服务软件比如Nginx来用。这里我们作为初学者教程，本着尽可能简化的想法会一直使用`FileServer`来做，除非后面它真的不够用为止。

##小结

到这里我们知道Golang编写服务端软件，主要给用户提供两种东西：
- 文件，主要是`html`文件给用户。
- 字符串数据，比如之前的`Hello world`和`Please Login or Register.`。

对于文件，我们只要`FileServer`就能把整个文件夹都向用户开放。但是对于字符串数据，我们就要单独写`.go`文件才行。

为什么要提供字符串数据呢？有两个原因：
1. 有时候用户想和服务器对话，但又不是要看网页，比如说用户登录的时候，就想问服务器我输入的密码和账号对吗？这就是要数据（"对"或者"错")而不是要网页，当然还有讨论群留言，只是想把留言发给服务器，而不是要网页。
1. 企业里现代的网页编写方法往往是布局和数据分离的，用户想看商品列表页面，服务器就先把预先做好的空的（没有商品）页面`html`文件发送给用户，但这是空的啥都没有怎么看啊？不要急，这个空页面会自动向服务器再要商品数据，服务器就又把数据发送给网页，网页接收到数据之后再填充到浏览器里面给用户看，说起来好像挺麻烦，但其实十分之一秒都不要就能完成这个流程。

**空网页模板+数据填充**，这个模式在行业里已经成为主流，所以我们接下来也会沿着这个思路进行开发。

>下一篇我们将介绍如何开发真正的用户注册功能。


---
欢迎关注我的专栏( つ•̀ω•́)つ[【人工智能通识】](https://www.jianshu.com/c/e9a7b7b7024d)

---
###每个人的智能新时代
如果您发现文章错误，请不吝留言指正；
如果您觉得有用，请点喜欢；
如果您觉得很有用，欢迎转载~
---
END