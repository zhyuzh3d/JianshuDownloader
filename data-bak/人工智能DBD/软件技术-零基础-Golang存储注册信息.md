欢迎关注我的专栏( つ•̀ω•́)つ[【人工智能通识】](https://www.jianshu.com/c/e9a7b7b7024d)

---

如何把用户网页端发来的邮箱和密码存储到MongoDB数据库？

![](imgs/4324074-c95311d55fe6aeb1.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

上一篇文章[软件技术-零基础-MangoDB数据库存储](https://www.jianshu.com/p/6a556f7be793)
[人工智能通识-2019年3月专题汇总](https://www.jianshu.com/p/72685b77cfff)


##安装Mongo数据库Golang驱动

从Golang连接到MongoDB需要使用一个模块`mongo-go-driver`。
这是一个开源工具，[更多信息参见这里](https://github.com/mongodb/mongo-go-driver/)，你可以从这里Download zip然后解压到`src/go.mongodb.org/mongo-driver`文件夹下然后`go install go.mongodb.org/mongo-driver/mongo`。
[也可以从百度盘下载压缩包然后解压](https://pan.baidu.com/s/1Utftt3QNSowL-PO4i7PseQ)  密码:hi9q

如果有梯子的话可以直接使用下面的命令安装:
```
go get go.mongodb.org/mongo-driver/mongo
```

##通用数据结构uds.go

我们在`login.go`中创建了很多数据`struct`结构，同样，我们也可以把一些通用的数据结构放到单独的文件中，其他代码调用它就可以了。

创建`src/app/uds/`文件夹，uds表示`uniform data struct`统一的数据结构，当然名称是随意取的。它的代码如下：

```
package uds

import "go.mongodb.org/mongo-driver/mongo"

//Tools 定义返回对象
type Tools struct {
	MongoDBCLient *mongo.Client
}
```
这里只包含了一个数据结构`Tools`，它有一个字段`MongoDBCLient`，是个mango数据库的客户端对象的指针`*mongo.Client`。
指针`*`可以看做是一个内存里面的标记，比如我们把`mongo.Client`这个复杂对象放在了内存的某个地方，那么我们就在这个地方放一个标记，这个标记就是指针，代表了这个复杂对象。

`uds.go`定义了通用工具集`Tools`的数据结构，如果我们哪里要使用工具集就可以引入这个`uds.go`。

##工具集tool.go

因为我们几乎会在每个数据地址服务（API接口）中用到MongoDB，比如存储用户的留言，读取用户的好友列表等等，所以类似`login.go`这样的代码会有很多，而在每个代码中都编写MongoDB驱动显然是不合理的，最好是编写一次，然后在每个代码中都能拿来使用。

这种为其他多个代码文件提供支持的代码我们叫做工具（tool或者utility）。

创建`src/app/tool`文件夹，然后里面创建`tool.go`文件：

```
package tool

import (
	"app/uds"
	"context"
	"time"

	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
	"go.mongodb.org/mongo-driver/mongo/readpref"
)

//InitRun 初始化
func InitRun() uds.Tools {
	rtn := uds.Tools{}
	rtn.MongoDBCLient = initMongoDB()
	return rtn
}

//initMongoDB 初始化工具集
func initMongoDB() *mongo.Client {
	//连接服务
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	client, err := mongo.Connect(ctx, options.Client().ApplyURI("mongodb://localhost:27017"))
	defer cancel()

	if err != nil {
		panic(err)
	}

	//检测连接是否成功
	ctx, cancel = context.WithTimeout(context.Background(), 2*time.Second)
	err = client.Ping(ctx, readpref.Primary())
	defer cancel()
	if err != nil {
		panic(err)
	}

	return client
}
```
需要注意这几点：
- 顶部导入了我们刚才创建的通用数据结构`uds.go`。
- 创建了一个`func InitRun() uds.Tools`初始化运行函数，它返回的结果是一个`
uds.Tools`结构，由小字开头的内容函数`initMongoDB `生成。init还记得上面`uds.go`中那个指向MongoDB客户端的指针吗？
- 重点是`initMongoDB`函数，主要是` client, err :=mongo.Connect(ctx, options.Client().ApplyURI("mongodb://localhost:27017"))`这句，是它连接到了MongoDB数据库，并生成了`client`客户端。
- `func initMongoDB() *mongo.Client`注意这个函数返回的是个客户端指针`*mongo.Client`
- `context.WithTimeout`计时函数需要和`defer cancel()`联合使用。
- `panic(err)`这是在遇到异常错误的时候抛出信息，后续我们会统一处理各种异常情况。

##改名login.go为register.go并修改app.go

都准备好了，我们可以改进`login.go`文件了。首先我们还是把它改名为`register.go`和服务地址名一致。因为我觉得代码有些多，如果把注册和登录的服务都放在这一个文件并不科学，所以还是为每个接口单独做文件。

这样就是`src/api/register/register.go`文件。改名之后先修改`app.go`文件：
- `import`里的`login`要改为`"app/api/register"`。
- `main`里面添加`tools := tool.InitRun()`,先初始化工具集。
- `http.HandleFunc...`改为然后行，把`tools`通过`InitRun`传进`register.go`：
```
register.InitRun(tools)
http.HandleFunc("/api/register", register.HandleFunc)
```
修改后的`app.go`完整如下：
```
package main

import (
	"app/api/register"
	"app/tool"
	"log"
	"net/http"
	"os"
	"path"
)

func main() {

	//初始化自定义工具集
	tools := tool.InitRun()

	//获取当前程序运行的目录
	dir, _ := os.Getwd()
	webDir := path.Join(dir, "/web")

	//设置文件服务
	http.Handle("/", http.FileServer(http.Dir(webDir)))

	//注册登录相关
	register.InitRun(tools)
	http.HandleFunc("/api/register", register.HandleFunc)

	//启动服务
	log.Fatal(http.ListenAndServe(":8088", nil))

}
```

##修改register.go

然后我们再修改`register.go`文件：
- 把第一行改为`package register`与文件名一致。
- 增加以下代码，实现`InitRun`函数，接收从`app.go`传入的`tools`：
```
var tools = uds.Tools{}

//InitRun 初始化tools
func InitRun(t uds.Tools) {
	tools = t
}
```
这样我们在外部文件`app.go`执行`register.InitRun(tools)`的时候，外面传进来的`tools`就会变为内部可以使用的`tools`。

##存储用户注册信息

我们继续修改`register.go`文件，修改原来的`func Register`为`func HandleFunc`和`app.go`中使用的一致，然后在里面添加代码：
```
ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
dbc := tools.MongoDBCLient.Database("myweb").Collection("user")
res, err := dbc.InsertOne(ctx, bson.M{"Email": ds.Email, "Pw": ds.Pw})
defer cancel()
```
- `dbc`表示`database collection`，还记得在设置MongoDB Compass的时候有个`collection name`我们设置为`user`吗？和这里是对应的。数据库Database包含很多数据集Collection，每个数据集里面可以存储无限多个数据。
- `dbc.InsertOne(ctx, bson.M{"Email": ds.Email, "Pw": ds.Pw})`，这是向数据集dbc中插入一个M数据对象，包含我们接收到的`Email、Pw`。

统一修改后的`register.go`文件是这样的：
```
package register

import (
	"app/uds"
	"context"
	"encoding/json"
	"net/http"
	"regexp"
	"time"

	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/bson/primitive"
)

var tools = uds.Tools{}

//InitRun 初始化tools
func InitRun(t uds.Tools) {
	tools = t
}

//RespDS 返回的数据格式
type RespDS struct {
	Err  int
	Msg  string
	Data struct {
		Token string
	}
}

//ReqDS 注册接口的请求数据格式
type ReqDS struct {
	Email string
	Pw    string
}

//HandleFunc 注册接口处理函数
func HandleFunc(w http.ResponseWriter, r *http.Request) {
	ds := ReqDS{}
	json.NewDecoder(r.Body).Decode(&ds)

	mailRe, _ := regexp.Compile(`^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$`)
	pwRe, _ := regexp.Compile(`^[0-9a-zA-Z_@]{6,18}$`)

	resp := RespDS{Err: 0, Msg: "注册成功！"}

	if !pwRe.MatchString(ds.Pw) {
		resp = RespDS{Err: 1, Msg: "密码格式错误！"}
	}
	if !mailRe.MatchString(ds.Email) {
		resp = RespDS{Err: 1, Msg: "邮箱格式错误！"}
	}

	//写入数据库
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	dbc := tools.MongoDBCLient.Database("myweb").Collection("user")
	res, err := dbc.InsertOne(ctx, bson.M{"Email": ds.Email, "Pw": ds.Pw})
	defer cancel()

	if err != nil {
		resp = RespDS{Err: 1, Msg: "写入数据库失败."}
	}

	resp.Data.Token = res.InsertedID.(primitive.ObjectID).Hex()

	dt, _ := json.Marshal(resp)
	w.Write([]byte(string(dt)))
}
```
这里我们使用了更统一的`RespDS`返回的数据结构和`ReqDS`接收的数据结构命名，注意在`RespDS`中包含了`Data`数据字段，其中包含一个`Token`字段，后面我们会重点使用到它。
在底部使用了`resp.Data.Token = res.InsertedID.(primitive.ObjectID).Hex()`这句话把插入MongoDB之后得到的ID信息放入了`Token`里面，一会儿可以在网页上看到它。

好了，保存，然后`Stop Code Run`再切换到`app.go`执行右键`Run Code`，服务启动后在网页上输入正式的邮箱和密码，然后提交，就可以看到MongoDB Compass中增加了新的数据（可能你需要先点local再切换回来以便于刷新数据显示）。

![](imgs/4324074-36e1718e7622794e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


到这里的项目结构是这样的：
![](imgs/4324074-3bf0b8e8a55452ec.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


> 到这里我们已经实现了用户注册信息的存储，但用户可以重复提交产生很多重复数据，而且我们还没有实现登录以及自动登录，后续文章会继续介绍相关内容。



---
欢迎关注我的专栏( つ•̀ω•́)つ[【人工智能通识】](https://www.jianshu.com/c/e9a7b7b7024d)

---
###每个人的智能新时代
如果您发现文章错误，请不吝留言指正；
如果您觉得有用，请点喜欢；
如果您觉得很有用，欢迎转载~
---
END


