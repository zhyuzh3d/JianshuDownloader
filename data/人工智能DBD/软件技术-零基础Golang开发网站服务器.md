欢迎关注我的专栏( つ•̀ω•́)つ[【人工智能通识】](https://www.jianshu.com/c/e9a7b7b7024d)

---

如何开始一个最简单的Golang项目？

![](imgs/4324074-4182ae82e86c4435.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

上一篇文章：[搭建Golang的vsCode开发环境](https://www.jianshu.com/p/4a3b9863577b)
[人工智能通识-2019年3月专题汇总](https://www.jianshu.com/p/72685b77cfff)


##项目结构

在`$GOPATH`目录下一般都要有两个文件夹：
- 存放编译结果的bin,
- 存放代码文件的src。

![](imgs/4324074-fef23c1b17c7a17b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

而`src`文件夹又一般会包含两类代码文件
- `go get`和`go install`安装的别人的代码，根据来源不同分为`github.com`和`golang.org`两个文件夹；
- 自己手写的代码，放在任意名字的文件夹，比如`app`文件夹。

我们编写的程序肯定要从某个代码文件开始，我们可以在自己的文件夹下创建`app.go`或者叫`main.go`都可以。

##Hello World

打开`app.go`撰写下面内容：

```
package main

import (
	"fmt"
)

func main() {
	fmt.Println("Hello world!")
}
```
这三段代码的意思是：
- 这个代码文件是首要文件main；
- 我要导入`fmt`模块；
- 从`main`开始运行，先打印一个`Hello world!`

当你Ctrl+S保存的时候代码会自动被格式化，如果出错的话某些代码可能会消失，下面的PROBLEMS问题面板也会有说明。

然后右键可以`Run code`运行代码，在下面的OUTPUT输出面板可以看到`Hello world!`字样。

##最简服务器程序

我们知道，浏览一个网站的时候都要有服务器上运行的软件才行，我们告诉服务器要访问的网址(URL)，服务器软件就会把对应的内容发送到我们的浏览器上。

下面的代码可以搭建一个最简单的网站服务器（实际你只要复制粘贴`main`中的内容，而`import`中的内容会自动补全）：
```
package main

import (
	"fmt"
	"html"
	"log"
	"net/http"
)

func main() {
	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprintf(w, "Hello, URL is %q", html.EscapeString(r.URL.Path))
	})
	log.Fatal(http.ListenAndServe(":8080", nil))
}
```

`http`是用来创建服务器的功能模块，`main`函数中的代码意思是：
- `http.HandleFunc`是设定对访问地址URL（比如`http://www.baidu.com/search`）的怎么做出反应的方法；
- `fmt.Fprintf...`是说要返回给用户浏览器的内容，这里是`Hello,URL is...`，而这里的`%q`就是后面`html.Esca...`的内容，其实就是URL的路径名。
- 最后`http.ListenAndServe`就是在8080端口启动服务监听，如果启动失败的话`log.Fatal`会在OUTPUT提示错误。

右键运行代码，在OUTPUT会提示`[running]...`表示服务软件开始运行，你可以访问自己的网站啦！怎么访问呢？打开浏览器，输入这个地址`http://localhost:8080/hello`就可以看到结果，当然如果你输入`http://localhost:8080/nihao`就会看到`Hello, URL is "/nihao"`。

> 如果发生意外，可以在OUTPUT面板右击，找到`Stop Code Run`停止后再重新`Code Run`运行。

![](imgs/4324074-ac665819476b8e78.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

##自定义模块

我们的网站对所有的访问地址URL都是一样的处理，这不行。我们需要为每个URL使用不同的规则。

我们的确可以在`main`里面写很多`http.HandleFunc("/", func(...`，但那样`main`里面就会很长，也许有几百几千行还要多，这样会很乱。

如果我们能把每个URL响应规则写在单独的模块文件里面，那就清爽了。

我们再`src`下建个`login`文件夹，里面建一个`login.go`文件,如下图所示：
![](imgs/4324074-9cb8795066bea823.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

然后我们编写`login.go`这个模块文件内容：
```
package login

import (
	"fmt"
	"net/http"
)

//HandleFunc is the handler function
func HandleFunc(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, "Please Login or Regiter.")
}
```
注意两个事情：
- 第一行是`package login`表示这是`login`模块（`app.go`中叫`main`是因为那是起始文件)。
- `func HandleFunc(...`是从`app.go`那边抄来的，注意`HandleFunc`如果写成`handleFunc`就错了，这个模块就没用了。务必要首字母大写。这个方法我们只是返回一个`"Please Login or Regiter."`欢迎登录或注册文字。

写好了`login`模块，我们就可以在`app.go`中使用它了：
```
package main

import (
	"app/login"
	"fmt"
	"html"
	"log"
	"net/http"
)

func main() {
	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprintf(w, "Hello, URL is %q", html.EscapeString(r.URL.Path))
	})
	http.HandleFunc("/login", login.HandleFunc)

	log.Fatal(http.ListenAndServe(":8080", nil))
}
```
这里我们增加了两个地方：
- `import`中增加了`app/login`，导入我们自己写的模块；
- `main`中增加了`http.HandleFunc("/login", login.HandleFunc)`设定当用户要求访问`/login`的时候我们就用自定义的`login.HandleFunc`返回给他那个`"Please Login or Regiter."`。

好了，OUTPUT面板`Stop Code Run`然后代码上右击`Code Run`，正常`[Running]`之后打开浏览器，尝试访问`http://localhost:8080/login`可以看到服务器返回的提示，如果你访问其他页面，仍然会被`http.HandleFunc("/", func(...`接收并返回原来的信息。

![](imgs/4324074-373e00f302f8aaad.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

##结尾

如果你希望脱离VSCode运行自己编写的这个服务器软件，首先要在VSCode里面`Stop Code Run`，然后在命令行中利用`cd ..`命令进入到`src`的上层文件夹（即`$GOPATH`文件夹），然后执行`go install app`就会把app文件编译成为可以单独执行的文件，位于`bin`文件夹下。

然后你就可以把这个`app`可执行文件双击或者拖拽到命令行工具中运行它。注意在MacOS下你需要使用`Ctrl+C`来终止正在运行中的`app`可执行文件。如果总是提示`Port Already in use`，实在不行就重启电脑吧。

我们只是一个简单的开始，实际上每个URL的处理并不会这么简单，往往还要分析用户数据，检查他是谁，做一些固定的额外处理，然后读取我们的数据库，为他组装内容，或者读取特定的网页返回给他，步骤很多而且情况都很不一样。在后续的文章中我会逐渐和大家一起学习。







---
欢迎关注我的专栏( つ•̀ω•́)つ[【人工智能通识】](https://www.jianshu.com/c/e9a7b7b7024d)

---
###每个人的智能新时代
如果您发现文章错误，请不吝留言指正；
如果您觉得有用，请点喜欢；
如果您觉得很有用，欢迎转载~
---
END