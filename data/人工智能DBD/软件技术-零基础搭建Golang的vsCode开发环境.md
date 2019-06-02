欢迎关注我的专栏( つ•̀ω•́)つ[【人工智能通识】](https://www.jianshu.com/c/e9a7b7b7024d)

---

Golang可能是所有编程语言中最优美的一个，它速度快，语法简洁，原生的完美支持多线程编程。

![](imgs/4324074-70790ea7778d5b69.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
[人工智能通识-2019年3月专题汇总](https://www.jianshu.com/p/72685b77cfff)


##Golang的卸载

如果你已经安装过Golang，那么在安装新版本之前最好先卸载干净旧版本。新用户请跳过。

**首先**，是删除Go文件夹，linux和macOS在`/usr/local/go`文件夹，windows在`c:\Go`。

macOS下你可以用管理员权限运行这个命令进行删除。
`sudo rm -rvf /usr/local/go/`
> -rvf: r循环删除文件夹内文件；v输出删除的文件名；f强制删除不提示

**然后**，从你的系统环境变量设置中移除Go的bin文件目录行。

macOS下你需要移除`/etc/paths.d/go`文件；windows在控制面板-系统-高级标签卡-环境变量按钮。

**最后**，如果你曾经设置过其他相关变量也要删除并使其，比如macOS中`.bash_profile`的`GoOPATH`字段行，然后执行`source ~/.bash_profile`使其生效。

**附加**，如果你觉得旧的相关目录不再需要也可以删除，比如用户名文件夹下的go文件夹（如果你的项目不在这里的话）。

##Golang的安装

![](imgs/4324074-b1c859fe4a175255.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

**首先**,安装基本程序。到官方下载对应系统的文件包，[点这里进入](https://golang.org/dl/)。

>[没有梯子的你可以从这里百度盘下载](https://pan.baidu.com/s/1FOYue7T8KEe_vUC6jeG8oQ)  ,密码:vkze。

解压，安装。

**其次**，设定**GOPATH环境变量**。默认Golang的工作空间是在`$HOME/go`（macOS和Linux）或者`%用户名%\go`目录，如果你需要修改的话，可以手工修改。

macOS打开`$HOME/.bash_profile`文件（隐藏文件），添加一行`export GOPATH=$HOME/Desktop/Golang`这样会指向桌面的Golang文件夹，要使其生效需要执行`source ~/.bash_profile`。

> mac下显示隐藏文件，如果系统是新版本macOS Sierra，那么直接在访达中command+shift+.(英文句号）即可进行切换。其他版本请百度搜索。

windows下从控制面板-系统-高级选项卡-环境变量，手工添加即可。

**最后**，检查是否成功。方法就是写一个`hello.go`文件编译运行它。

在你的工作空间文件夹内创建`src/hello/`文件夹，再用任何文本编辑工具创建一个`hello.go`文件，打开添加以下内容。（如果你不知道怎么做可以先看下面的VSCode部分）

```
package main

import "fmt"

func main() {
	fmt.Printf("hello, world\n")
}
```
然后打开命令行工具（windows）或终端（mac），利用上一层`cd ..`和进入下一层`cd $HOME/go/src/hello`命令进入到当前文件夹下，执行`go build`进行编译，这会在文件夹下产生一个新的可执行文件。然后执行`./hello`运行这个可执行文件，将看到输出`hello world`,表示安装成功。

更简单的办法是不编译，直接运行，`go run hello.go`。

##VSCode

Visual Studio Code是微软推出的一款免费开源编程工具，如果你需要使用Golang和其他语言一起，那么Code是最合适的。如果你只使用Golang而不使用其他语言，那么可以使用专门编写Golang的LiteIDE工具，实际上它更加简单好用。当然还有其他一些编程工具可选，但都不推荐。

![](imgs/4324074-6427727eb81bc733.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

直接官网下载解压安装即可。[点这里进入官网](https://code.visualstudio.com/)

然后从File/open打开你的工作空间文件夹，双击hello.go文件打开它，你也可以在左侧文件列表点中hello文件夹右键创建新文件。
![](imgs/4324074-9b3c9391d2926209.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

这时候注意窗口右下角的提升，Analysis Tools Missing表明对当前的Golang文件不能进行分析。我们点击它，弹出提示，再点击Install按钮进行安装。

![](imgs/4324074-249c7b8674bba880.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

这时候会弹出一个面板，显示有好几个插件都要安装。
![](imgs/4324074-a45f928efb3255ec.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

等好一会，很可能都还是失败，这是由于我们的墙太厚了。

![](imgs/4324074-a18925ba76ed9da8.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

从错误列表中可以看到主要是`golang.org/x/tools...`这个地址是在墙外的，我们可以单独下载它。[点击这里进入官方的仓库](https://github.com/golang/tools)

然后Download Zip。
![](imgs/4324074-1533f8cebb66da24.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

下载后解压，放到你的工作空间文件夹`$GOPATH/src/golang.org/x/tools`下面。然后回到VSCode中，随便修改一下hello.go文件，然后再保存，右下角就会弹出提示，再次点击Install按钮就可以成功安装了。

这个安装可能有些慢，着急的话你可以直接在终端进入到`$GOPATH`目录运行类似下面的命令进行安装：
```
go install github.com/mdempsky/gocode
go install github.com/ramya-rao-a/go-outline
go install github.com/acroca/go-symbols
go install golang.org/x/tools/cmd/guru
go install golang.org/x/tools/cmd/gorename
go install github.com/stamblerre/gocode
go install github.com/sqs/goreturns
go install golang.org/x/lint/golint
go install github.com/ianthehat/godef
```
最后两个会失败，因为它们需要单独获取。[在这里同样方法下载zip](https://github.com/golang/lint)然后也解压后放在`.../x/lint/`目录下。然后再执行`go install golang.org/x/lint/golint`即可成功。

对于`godef`也是，我们可以看到它的报错：
![](imgs/4324074-a9be76d92b0b76f7.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

同样我们到[https://github.com/ianthehat/godef](https://github.com/ianthehat/godef)下载ZIP，解压放到 `/src/github.com/ianthehat/godef`下,然后再运行。也可以control或command+shift+P打开命令工具，输入`Go: Install/Update Tools`再选择`godef`然后确定开始安装。

这里是我的src文件夹压缩包，[你可以下载使用](https://pan.baidu.com/s/1FOYue7T8KEe_vUC6jeG8oQ)  ,密码:vkze。

另外，你还需要安装Code Runner用来快速编译和运行代码。方法是左侧点击扩展Extensions按钮，然后搜索code runner。

![](imgs/4324074-a4a7b3fd10be8d00.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

安装之后可以在代码页面上的右键菜单多出一个Run Code命令，点击可以直接运行代码，底部面板的OUTPUT内将出现`hello world`字符。此外在窗口右上角也会多出一个三角的播放按钮，同样可以编译运行当前代码文件。

![](imgs/4324074-ffb994cfd5f16ac0.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


>由于Golang是谷歌创建的，所有由于某种未墙的原因，配置Golang还是很麻烦的，可能你需要常备梯子才行。


---
欢迎关注我的专栏( つ•̀ω•́)つ[【人工智能通识】](https://www.jianshu.com/c/e9a7b7b7024d)

---
###每个人的智能新时代
如果您发现文章错误，请不吝留言指正；
如果您觉得有用，请点喜欢；
如果您觉得很有用，欢迎转载~
---
END