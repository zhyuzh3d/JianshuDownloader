欢迎关注我的专栏( つ•̀ω•́)つ[【人工智能通识】](https://www.jianshu.com/c/e9a7b7b7024d)

---
如何避免用户重复注册？如何验证用户登录成功？

![](imgs/4324074-6ccc3df18dc95fa5.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

上一篇文章[软件技术-零基础-Golang存储注册信息](https://www.jianshu.com/p/dafde95f6db6)
[人工智能通识-2019年3月专题汇总](https://www.jianshu.com/p/72685b77cfff)


##检查重复邮箱

如果用户的邮箱已经存在于MongoDB数据库中了，那么我们应该不要重复写入数据，并且告诉用户**您已经注册过了**。

用下面的代码检测用户邮箱是否已经存在，修改`register.go`的`HandleFunc`部分：

```
	//访问数据集
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	dbc := tools.MongoDBCLient.Database("myweb").Collection("user")
	defer cancel()

	//验证用户邮箱是否存在
	count, err := dbc.CountDocuments(context.TODO(), bson.M{"Email": ds.Email})
	if err != nil {
		resp = RespDS{Err: 1, Msg: "读取数据库失败。"}
	}
	if count >1 {
		resp = RespDS{Err: 1, Msg: "邮箱已经存在。"}
	}

	//写入数据库
	res, err := dbc.InsertOne(ctx, bson.M{"Email": ds.Email, "Pw": ds.Pw})
	if err != nil {
		resp = RespDS{Err: 1, Msg: "写入数据库失败."}
	}
	resp.Data.Token = res.InsertedID.(primitive.ObjectID).Hex()
```
注意这几个地方：
- `CountDocuments`是查找存在几个符合条件的，如果存在超过0个就表示已经至少有一个重名邮箱了。
- `bson.M{"Email": ds.Email}`我们是搜索符合这个条件的用户，也就是重名用户。

如果这时候保存并切换到`app.go`运行代码，从网页上提交注册，仍然会导致重复写入数据库，这是因为我们并没有阻止下面的代码执行。

仔细回顾我们的`register.go`文件的`HandleFunc`方法的流程：
![](imgs/4324074-c05978fb03755d57.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

三次检查，不管检查是否通过，都不会停止。而我们知道，任何一次检查不通过，都应该直接向用户返回结果，完全没必要再做后面的检查了。

所以我们期望的是这样的流程（注意橙色的捷径）：
![](imgs/4324074-d6ebd91b061b306e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


##实用功能util.go

我们来改进整个注册流程。
流程`HanleFunc`里最后负责返回响应数据的是这两句：
```
	dt, _ := json.Marshal(resp)
	w.Write([]byte(string(dt)))
```

虽然只有两句，但是因为以后也会很经常的使用，所以很不方便。我们采用类似`tools.go`的办法把这些常用的方法提炼到一个新的`/src/app/util/util.go`(utility实用功能)中去,作为一个单独的`WWrite`(WebWrite)函数：

```
package util

import (
	"app/uds"
	"encoding/json"
	"net/http"
)

//WWrite 向用户返回信息,返回resp和一个错误信息
func WWrite(w http.ResponseWriter, code int, msg string, data interface{}) (uds.Respons, error) {
	resp := uds.Respons{Code: code, Msg: msg, Data: data}
	var err error
	dt, err1 := json.Marshal(resp)
	if err1 != nil {
		err = err1
	}
	_, err2 := w.Write([]byte(string(dt)))
	if err2 != nil {
		err = err2
	}
	return resp, err
}
```
注意这几个地方：
- 我们调用了统一数据格式`app/uds`。
- 这个`WWrite`我们使用了多个参数`(w http.ResponseWriter, code int, msg string, data interface{})`，也返回了多个（2个）值`(uds.Respons, error)`,这和最后的`return resp, err`是一致的。
- 我们用这些参数拼合成了一个标准的返回给用户的数据格式`resp := uds.Respons{Code: code, Msg: msg, Data: data}`

这个`uds.Respons`是什么样的？下面是完整的`uds.go`：
```
package uds

import "go.mongodb.org/mongo-driver/mongo"

//Tools 定义返回对象
type Tools struct {
	MongoDBCLient *mongo.Client
}

//Respons 定义统一的返回格式
type Respons struct {
	Code int
	Msg  string
	Data interface{}
}
```

>`util.go`和`tool.go`有什么区别？都是提供通用工具啊。但我习惯把简单的、不用初始化的轻量工具放在`util.go`里面，而把那些复杂的需要初始化`InitRun`的工具放在`tool.go`里面，以后工具多了，其实还需要进步一细分处理。这只是对功能的分割规划，并非是必须的。
应该控制每个代码文件不要太多，三五百行还能忍一下看懂，两三千行代码看到就头晕了，以后改动和维护也会很烦。

##改进register.go

有了`util.go`实用功能我们就可以方便的调用它了，不仅可以替换掉`register.go`中最后两句，而且可以把数据结构`RespDS`和很多`resp = RespDS{Err: 1, Msg: "读取数据库失败。"}`类似的语句简化掉，因为`WWrite`可以自动组装成标准的`Respons`结构并返回。

下面是修改后的完整`register.go`：
```
package register

import (
	"app/uds"
	"app/util"
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

//ReqDS 注册接口的请求数据格式
type ReqDS struct {
	Email string `bson:"Email"`
	Pw    string
}

//HandleFunc 注册接口处理函数
func HandleFunc(w http.ResponseWriter, r *http.Request) {
	ds := ReqDS{}
	json.NewDecoder(r.Body).Decode(&ds)

	mailRe, _ := regexp.Compile(`^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$`)
	pwRe, _ := regexp.Compile(`^[0-9a-zA-Z_@]{6,18}$`)

	if !pwRe.MatchString(ds.Pw) {
		util.WWrite(w, 1, "密码格式错误。", nil)
		return
	}
	if !mailRe.MatchString(ds.Email) {
		util.WWrite(w, 1, "邮箱格式错误。", nil)
		return
	}

	//访问数据集
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	dbc := tools.MongoDBCLient.Database("myweb").Collection("user")
	defer cancel()

	//验证用户邮箱是否存在
	count, err := dbc.CountDocuments(context.TODO(), bson.M{"Email": ds.Email})
	if err != nil {
		util.WWrite(w, 1, "读取数据库失败。", nil)
		return
	}
	if count > 0 {
		util.WWrite(w, 1, "邮箱已存在。", nil)
		return
	}

	//写入数据库
	res, err := dbc.InsertOne(ctx, bson.M{"Email": ds.Email, "Pw": ds.Pw})
	if err != nil {
		util.WWrite(w, 1, "写入数据库失败。", nil)
		return
	}
	d := res.InsertedID.(primitive.ObjectID).Hex()
	util.WWrite(w, 0, "注册成功。", d)
	return
}
```

注意这里有很多的`return`，它表示快速结束当前函数`HandleFunc`，后面的代码不会被运行。
另外这里也做了很多` if err != nil {`错误检测，避免在出现异常时候没有反应。
这个代码虽然感觉变多了，但实际运行的顺序却更合理了，如果用户输错了邮箱格式，其实只会运行到`util.WWrite(w, 1, "邮箱格式错误。", nil)`这一行，后面一大片都不会被运行，所以速度快了很多。

**代码多未必运行的更慢，反之亦然**。


## 更多扩展内容： 
- 如果我们需要把`FindOne`得到用户信息提取出来，比如说想知道这个邮箱的密码是什么，可以创建一个`var u bson.M`对象，然后把读取的信息填充进去`dbc.FindOne(context.TODO(), bson.M{"Email": ds.Email}).Decode(&b)`然后就可以使用`b["Pw"]`来读取了:
```
	ctx, _ := context.WithTimeout(context.Background(), 5*time.Second)
	var result bson.M
	err := collection.FindOne(ctx, bson.M{"Name": "a"}).Decode(&result)
	if err != nil {
		log.Fatal(err)
	}
```
- 可以使用`Find`来查找不限数量的符合条件的数据，如果条件也不限制可以使用空的`bson.M`来做参数:`cur, err := collection.Find(ctx, bson.M{})`,但如果要使用它读取到的内容就麻烦一些：
```
	ctx, _ = context.WithTimeout(context.Background(), 30*time.Second)
	cur, err := collection.Find(ctx, bson.M{"Name": "a"})
	if err != nil {
		log.Fatal(err)
	}
	defer cur.Close(ctx)
	for cur.Next(ctx) {
		var result bson.M
		err := cur.Decode(&result)
		if err != nil {
			log.Fatal(err)
		}
		fmt.Println(result, "-->", result["Value"])
	}
```
- 如果我们只是想知道有多少条符合要求的信息，那么我们可以使用`CountDocuments`方法：
```
	ctx, _ = context.WithTimeout(context.Background(), 30*time.Second)
	c, _ := collection.CountDocuments(ctx, bson.M{})
	fmt.Println("Count", c)
```

>到这里为止，我们还是在做注册功能（虽然我们的网页叫`login.html`。。。），下一篇我们正式做登录，从数据库来检查当前用户是否输对了邮箱和密码。

---
欢迎关注我的专栏( つ•̀ω•́)つ[【人工智能通识】](https://www.jianshu.com/c/e9a7b7b7024d)

---
###每个人的智能新时代
如果您发现文章错误，请不吝留言指正；
如果您觉得有用，请点喜欢；
如果您觉得很有用，欢迎转载~
---
END