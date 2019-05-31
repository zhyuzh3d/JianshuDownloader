欢迎关注我的专栏( つ•̀ω•́)つ[【人工智能通识】](https://www.jianshu.com/c/e9a7b7b7024d)
[【汇总】2019年4月专题](https://www.jianshu.com/p/e1afed853866)

---

如何制作登录页面？如何从Mongo数据库中进行验证？

![](imgs/4324074-bf3fc5fcfa5816ab.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

上一篇文章[软件技术-零基础-Golang用MongoDB验证用户信息](https://www.jianshu.com/p/c270eddcfffa)
[人工智能通识-2019年3月专题汇总](https://www.jianshu.com/p/72685b77cfff)

##创建login.html

把我们原来的`login.html`文件复制一份重命名为`register.html`，因为登录和注册页面的代码很像，我们只要复制修改一下就可以重用了。

利用右下角的`Go Live`按钮启动实时预览，然后修改`login.html`页面。

- 首先，把原来简单的标题修改一下，增加跳转到`register.html`页面的链接：
```
<div class="row justify-content-center" style="margin-top:100px;margin-bottom:20px">
            <h4>登录</h4>
            <div style="width:24px"></div>
            <a href="register.html" style="color:#CCC"><h4>注册</h4></a>
        </div>
```
效果如下：
![](imgs/4324074-d5a47d7c7d28c05b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- 然后删掉用户协议的旋钮部分，下面这个代码删掉。
```
                <div class="form-check">
                    <input id='agree' onChange='checkBtn()' type="checkbox" class="form-check-input" id="exampleCheck1">
                    <label class="form-check-label" for="exampleCheck1">
                        <span>同意用户协议:</span>
                        <a href='agreement.html'>点击阅读</a>
                    </label>
                </div>
```
- 然后修改按钮的名称和动作名称，`regBtn`改为`loginBtn`，`sendRegPost`改为`sendLoginPost`。
```
<button id='loginBtn' onClick="sendRegPost()" class="btn btn-pr...
```
- 修改`script`中的函数名称，`sendRegPost`改为`sendLoginPost`，并修改请求路径变为`'/api/login'`，修改稿和是：
```
    function sendLoginPost() {
        var data = {
            Email: $('#email').val(),
            Pw: $('#pw').val(),
        }

        $.post('/api/login', JSON.stringify(data), function (res) {
            alert(res.Msg);
        }, 'json')
    }
```

- 修改`script`中的`checkBtn`方法，去掉对用户协议选项的检测。
```
    //检查按钮是否可以被开启
    function checkBtn() {
        var agree=$('#agree').is(':checked');
        var mail = $('#email').val();
        var pw = $('#pw').val();
        if (pwRe.test(pw) && mailRe.test(mail)) {
            $('#regBtn').removeAttr('disabled')
        } else {
            $('#regBtn').attr('disabled', 'true')
        }
    }
```

##创建login.go

同样我们复制`register.go`文件到路径`app/api/login/login.go`文件，然后修改它。

- 顶部第一行包名称改为`login`
```
package login
```
- 然后修改`HandleFunc`函数内容，用`FindOne`来读取用户的密码，和`ds.Pw`进行对比，如果一致则返回成功，否则返回不匹配提示。
```
//HandleFunc 注册接口处理函数
func HandleFunc(w http.ResponseWriter, r *http.Request) {
	ds := ReqDS{}
	json.NewDecoder(r.Body).Decode(&ds)

	// //访问数据集
	dbc := tools.MongoDBCLient.Database("myweb").Collection("user")

	//验证用户邮箱是否与用户名匹配
	var u bson.M
	dbc.FindOne(context.TODO(), bson.M{"Email": ds.Email}).Decode(&u)
	if u["Pw"] == ds.Pw {
		util.WWrite(w, 0, "登录成功", u["_id"])
	} else {
		util.WWrite(w, 1, "邮箱与用户名不匹配", nil)
	}
	return
}
```

- 切换到`app.go`，把我们的新`login.go`指定到对应的服务路径。
```
	//注册登录相关
	register.InitRun(tools)
	http.HandleFunc("/api/register", register.HandleFunc)
	login.InitRun(tools)
	http.HandleFunc("/api/login", login.HandleFunc)

```

然后重新`Run Code`,在浏览器中切换到`http://localhost:8088/page/login.html`,注意不是`Go Live`打开的页面。然后使用之前注册过的账号和密码尝试登陆，正常的话将显示成功。


##改进tools.go使用方式

对于每个服务接口都要`register.InitRun(tools)`这看起来并不方便。能否像使用`util`那样使用`tool`？也就是只要`import "app/tool"`就可以直接用`tool.MongoDBCLient`，怎么做？

- 首先我们要在`tool.go`中创建`MongoDBCLient`变量：
```
var MongoDBCLient *mongo.Client`
```
之前我们是依赖`InitRun`方法调用`initMongoDB()`来真的生成`MongoDBCLient`的，在`app.go`中我们还必须调用`tool.initRun()`才能呼叫成功。

实际上任何一个外部`go`文件被`import`的时候都会自动尝试运行`init()`函数，我们可以借用这个函数来自动生成`MongoDBCLient`，而不依赖手工呼叫：
```
//MongoDBCLient mongo数据库客户端，init中自动初始化
var MongoDBCLient *mongo.Client

func init() {
	MongoDBCLient = initMongoDB()
}

func initMongoDB() *mongo.Client {
...
```
这样看起来简化不少。

- 在`app.go`文件中我们删除`tool.InitRun()`代码，也去掉`register.InitRun`和`login.InitRun`代码。`app.go`中`main`函数内容：
```
func main() {
	//获取当前程序运行的目录
	dir, _ := os.Getwd()
	webDir := path.Join(dir, "/web")

	//设置文件服务
	http.Handle("/", http.FileServer(http.Dir(webDir)))

	//注册登录相关
	http.HandleFunc("/api/register", register.HandleFunc)
	http.HandleFunc("/api/login", login.HandleFunc)

	//启动服务
	fmt.Println("Server is running;CurrentDir is", dir)
	log.Fatal(http.ListenAndServe(":8088", nil))
}
```

- 简化`register.go`，先去掉`InitRun`相关代码，以下代码删除。
```
var tools = uds.Tools{}

//InitRun 初始化tools
func InitRun(t uds.Tools) {
	tools = t
}
```
然后把`dbc := tools.MongoDBCLient.Database...`一行改为`dbc := tool.MongoDBCLient.Database`，并在顶部添加导入：
```
import (
	"app/util"
	"app/tool"
```

- 修改login.go。类似上面，一样去掉`InitRun`相关，增加`import`，修改`dbc:=tools.M...`为`dcc:=tool.M...`。

- 去掉`udc.go`中的`Tools`结构，因为我们不再需要它了。

最后运行，结合网页测试注册和登录功能。


>虽然能够注册和登录，但是如果用假邮箱注册怎么办？用户忘记密码了怎么办？后续文章中我们继续扩展这些内容。

以下是主要文件的完整代码：

![](imgs/4324074-ffca54a15304a812.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)




`app.go`
```
package main

import (
	"app/api/login"
	"app/api/register"
	"fmt"
	"log"
	"net/http"
	"os"
	"path"
)

func main() {

	//获取当前程序运行的目录
	dir, _ := os.Getwd()
	webDir := path.Join(dir, "/web")

	//设置文件服务
	http.Handle("/", http.FileServer(http.Dir(webDir)))

	//API-注册登录相关
	http.HandleFunc("/api/register", register.HandleFunc)
	http.HandleFunc("/api/login", login.HandleFunc)

	//启动服务
	fmt.Println("Server is running;CurrentDir is", dir)
	log.Fatal(http.ListenAndServe(":8088", nil))

}
```


`uds.go`
```
package uds

//Respons 定义统一的返回格式
type Respons struct {
	Code int
	Msg  string
	Data interface{}
}
```

`tool.go`
```
package tool

import (
	"context"
	"time"

	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
	"go.mongodb.org/mongo-driver/mongo/readpref"
)

//MongoDBCLient mongo数据库客户端，init中自动初始化
var MongoDBCLient *mongo.Client

func init() {
	MongoDBCLient = initMongoDB()
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
`util.go`
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
`login.go`
```
package login

import (
	"app/tool"
	"app/util"
	"context"
	"encoding/json"
	"net/http"

	"go.mongodb.org/mongo-driver/bson"
)

//ReqDS 注册接口的请求数据格式
type ReqDS struct {
	Email string
	Pw    string
}

//HandleFunc 注册接口处理函数
func HandleFunc(w http.ResponseWriter, r *http.Request) {
	ds := ReqDS{}
	json.NewDecoder(r.Body).Decode(&ds)

	// //访问数据集
	dbc := tool.MongoDBCLient.Database("myweb").Collection("user")

	//验证用户邮箱是否与用户名匹配
	var u bson.M
	dbc.FindOne(context.TODO(), bson.M{"Email": ds.Email}).Decode(&u)
	if u["Pw"] == ds.Pw {
		util.WWrite(w, 0, "登录成功", u["_id"])
	} else {
		util.WWrite(w, 1, "邮箱与用户名不匹配", nil)
	}
	return
}
```

`register.go`
```
package register

import (
	"app/tool"
	"app/util"
	"context"
	"encoding/json"
	"net/http"
	"regexp"
	"time"

	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/bson/primitive"
)

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
	dbc := tool.MongoDBCLient.Database("myweb").Collection("user")
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

`register.html`
```
<!doctype html>
<html lang="zh-cmn-Hans">

<head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://cdn.bootcss.com/bootstrap/4.0.0/css/bootstrap.min.css"
        integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">

    <title>我的站点</title>
</head>

<body>
    <div class="container-fluid">
        <div class="row justify-content-center" style="margin-top:100px;margin-bottom:20px">
            <a href="login.html" style="color:#CCC">
                <h4>登录</h4>
            </a>
            <div style="width:24px"></div>
            <h4>注册</h4>
        </div>
        <div class="row justify-content-center">
            <div class="col-xs-10 col-sm-8 col-md-6 col-lg-4 col-xl-3">
                <div class="form-group">
                    <label for="exampleInputEmail1">邮箱：</label>
                    <input id='email' onkeyup="checkMail()" type="email" class="form-control"
                        aria-describedby="emailHelp" placeholder="请输入正确格式的邮箱">
                    <small id='mailTip' style="display:none;">请输入正确邮箱格式</small>
                </div>
                <div class="form-group">
                    <label for="exampleInputPassword1">密码：</label>
                    <input id='pw' onkeyup="checkPw()" type="password" class="form-control" placeholder="请输入6~18位密码">
                    <small id='pwTip' style="display:none">请输入6~18位数字字母或下划线</small>
                </div>
                <div class="form-check">
                    <input id='agree' onChange='checkBtn()' type="checkbox" class="form-check-input" id="exampleCheck1">
                    <label class="form-check-label" for="exampleCheck1">
                        <span>同意用户协议:</span>
                        <a href='agreement.html'>点击阅读</a>
                    </label>
                </div>
                <br>
                <button id='regBtn' onClick="sendRegPost()" class="btn btn-primary btn-block">注册</button>
            </div>
        </div>
    </div>

    <!-- Optional JavaScript -->
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
    <script src="https://cdn.bootcss.com/jquery/3.2.1/jquery.min.js"></script>
    <script src="https://cdn.bootcss.com/popper.js/1.12.9/umd/popper.min.js"></script>
    <script src="https://cdn.bootcss.com/bootstrap/4.0.0/js/bootstrap.min.js"></script>
</body>

<script type="text/javascript">
    function sendRegPost() {
        var data = {
            Email: $('#email').val(),
            Pw: $('#pw').val(),
        }

        $.post('/api/register', JSON.stringify(data), function (res) {
            alert(res.Msg);
        }, 'json')
    }

    var mailRe =
        /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;

    function checkMail() {
        var mail = $('#email').val();
        if (mailRe.test(mail) == false) {
            $('#mailTip').css('display', 'block')
            $('#email').removeClass('is-valid')
            $('#email').addClass('is-invalid')
        } else {
            $('#mailTip').css('display', 'none')
            $('#email').removeClass('is-invalid')
            $('#email').addClass('is-valid')
        }
        checkBtn()
    }


    var pwRe = /^[0-9a-zA-Z_@]{6,18}$/

    function checkPw() {
        var pw = $('#pw').val();
        if (pwRe.test(pw) == false) {
            $('#pwTip').css('display', 'block')
            $('#pw').removeClass('is-valid')
            $('#pw').addClass('is-invalid')
        } else {
            $('#pwTip').css('display', 'none')
            $('#pw').removeClass('is-invalid')
            $('#pw').addClass('is-valid')
        }
        checkBtn()
    }

    //检查按钮是否可以被开启
    function checkBtn() {
        var agree = $('#agree').is(':checked');
        var mail = $('#email').val();
        var pw = $('#pw').val();
        if (pwRe.test(pw) && mailRe.test(mail)&& agree)  {
            $('#regBtn').removeAttr('disabled')
        } else {
            $('#regBtn').attr('disabled', 'true')
        }
    }
</script>

</html>
```
`login.html`
```
<!doctype html>
<html lang="zh-cmn-Hans">

<head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://cdn.bootcss.com/bootstrap/4.0.0/css/bootstrap.min.css"
        integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">

    <title>我的站点</title>
</head>

<body>
    <div class="container-fluid">
        <div class="row justify-content-center" style="margin-top:100px;margin-bottom:20px">
            <h4>登录</h4>
            <div style="width:24px"></div>
            <a href="register.html" style="color:#CCC"><h4>注册</h4></a>
        </div>
        <div class="row justify-content-center">
            <div class="col-xs-10 col-sm-8 col-md-6 col-lg-4 col-xl-3">
                <div class="form-group">
                    <label for="exampleInputEmail1">邮箱：</label>
                    <input id='email' onkeyup="checkMail()" type="email" class="form-control"
                        aria-describedby="emailHelp" placeholder="请输入正确格式的邮箱">
                    <small id='mailTip' style="display:none;">请输入正确邮箱格式</small>
                </div>
                <div class="form-group">
                    <label for="exampleInputPassword1">密码：</label>
                    <input id='pw' onkeyup="checkPw()" type="password" class="form-control" placeholder="请输入6~18位密码">
                    <small id='pwTip' style="display:none">请输入6~18位数字字母或下划线</small>
                </div>
                <br>
                <button id='regBtn' onClick="sendLoginPost()" class="btn btn-primary btn-block">登录</button>
            </div>
        </div>
    </div>

    <!-- Optional JavaScript -->
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
    <script src="https://cdn.bootcss.com/jquery/3.2.1/jquery.min.js"></script>
    <script src="https://cdn.bootcss.com/popper.js/1.12.9/umd/popper.min.js"></script>
    <script src="https://cdn.bootcss.com/bootstrap/4.0.0/js/bootstrap.min.js"></script>
</body>

<script type="text/javascript">
    function sendLoginPost() {
        var data = {
            Email: $('#email').val(),
            Pw: $('#pw').val(),
        }

        $.post('/api/login', JSON.stringify(data), function (res) {
            alert(res.Msg);
        }, 'json')
    }

    var mailRe =
        /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;

    function checkMail() {
        var mail = $('#email').val();
        if (mailRe.test(mail) == false) {
            $('#mailTip').css('display', 'block')
            $('#email').removeClass('is-valid')
            $('#email').addClass('is-invalid')
        } else {
            $('#mailTip').css('display', 'none')
            $('#email').removeClass('is-invalid')
            $('#email').addClass('is-valid')
        }
        checkBtn()
    }


    var pwRe = /^[0-9a-zA-Z_@]{6,18}$/

    function checkPw() {
        var pw = $('#pw').val();
        if (pwRe.test(pw) == false) {
            $('#pwTip').css('display', 'block')
            $('#pw').removeClass('is-valid')
            $('#pw').addClass('is-invalid')
        } else {
            $('#pwTip').css('display', 'none')
            $('#pw').removeClass('is-invalid')
            $('#pw').addClass('is-valid')
        }
        checkBtn()
    }

    //检查按钮是否可以被开启
    function checkBtn() {
        var agree=$('#agree').is(':checked');
        var mail = $('#email').val();
        var pw = $('#pw').val();
        if (pwRe.test(pw) && mailRe.test(mail)) {
            $('#regBtn').removeAttr('disabled')
        } else {
            $('#regBtn').attr('disabled', 'true')
        }
    }
</script>

</html>
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