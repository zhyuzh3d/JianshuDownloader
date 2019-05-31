欢迎关注我的专栏( つ•̀ω•́)つ[【人工智能通识】](https://www.jianshu.com/c/e9a7b7b7024d)
[【汇总】2019年4月专题](https://www.jianshu.com/p/e1afed853866)

---

如何实现用户自动登录？

![](imgs/4324074-7507959110a7d103.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

上一篇文章，[软件技术-零基础-Golang注册验证与忘记密码](https://www.jianshu.com/p/c326f14e6221)
[人工智能通识-2019年3月专题汇总](https://www.jianshu.com/p/72685b77cfff)


##Cookie

浏览器其实可以帮助网站记录我们浏览的信息，包括用户名，密码，或者上一次滚动页面的位置，或者任何网站开发者希望记录的信息。

这些信息其实就是很多小文件，浏览器为每个网站配一个小文件，用来记录用户浏览信息，而到底要记录什么，则由网站的开发者来决定。

这些小文件有个可爱的名字，就叫做Cookie小甜饼。


##Token

如果当用户第一次登录成功的时候，我们就把用户名和密码放在Cookie里面，然后每次页面打开都自动用`script`执行`post`登录，这样可以吗？

可以的。但把用户密码放在Cookie里面很不安全，随便谁获得了这个电脑都能从网页里查看到Cookie，所以你绝对不希望网站开发者把你的银行卡密码放在Cookie里面。

![](imgs/4324074-647ad076cc3d42cf.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

另外一个方法就比较好些。
当用户登录成功的时候，我们用Golang为用户生成一个特殊的额唯一数字令牌Token，然后把这个数字Token放在Cookie里面，当用户把这个数字发送给Golang服务器程序的时候，我们再用这个数字找到对应的用户名和密码，这样我们就知道他又回来了。
这样的数字我们之前在代码里使用过，比如注册和找回密码时候返回的那个`_id`数字。

但还有一个问题，这个`id`是数据库`user`里面固定的数字，如果用户在新的电脑上重新用密码登录了，那么旧电脑和新电脑的Token就一样的，而且能同时登录，用户只能跑回去旧电脑注销才可以清除，以防止其他人冒用。——这很糟糕。
如果用户每次手工密码登录，我们就为他生成一个新的Token，问题就解决了。

##UUID

通用唯一识别码（英语：Universally Unique Identifier，UUID），是用于计算机体系中以识别信息数目的一个128位标识符，还有相关的术语：全局唯一标识符（GUID）。
通俗说就是有个程序不断生产字符串（或数字），每次生产的数字都不同，永远不会相同。

我们需要为每次用户手工登录创建一个独一无二的UUID。

我们使用下面的命令安装能够生产`uuid`的模块：
```
go get github.com/satori/go.uuid
go install github.com/satori/go.uuid
```
用法很简单，`a, _ := uuid.NewV4()`就能得到一串`547d9f4b-05bd-4dc2-89d1-bab1c0f6ecd8`这样的代码。

##改进login.go写入Cookie

改进后的`func Login`函数代码如下：
```
//Login 注册接口处理函数
func Login(w http.ResponseWriter, r *http.Request) {
	ds := loginReqDS{}
	json.NewDecoder(r.Body).Decode(&ds)

	// //访问数据集
	dbc := tool.MongoDBCLient.Database("myweb").Collection("user")

	//验证用户邮箱是否与用户名匹配
	var u bson.M
	dbc.FindOne(context.TODO(), bson.M{"Email": ds.Email}).Decode(&u)
	if u["Pw"] == ds.Pw {
		//创建token并写入数据库
		uid, _ := uuid.NewV4()
		uids := uid.String()
		ctoken := tool.MongoDBCLient.Database("myweb").Collection("token")
		du := bson.M{"Token": uids, "Id": u["_id"], "Ts": time.Now().Unix()}
		ctoken.InsertOne(context.TODO(), du)

		//返回id，并将token写入cookie
		expire := time.Now().AddDate(0, 1, 0)
		c := http.Cookie{
			Name:     "Token",
			Path:     "/",
			Value:    uids,
			HttpOnly: true,
			Expires:  expire,
		}
		w.Header().Set("Set-Cookie", c.String())
		util.WWrite(w, 0, "登录成功", u["_id"])
	} else {
		util.WWrite(w, 1, "邮箱与用户名不匹配", nil)
	}

	return
}
```
注意几点：
- 我们把`token`和`_id`的对应关系存储在`token`数据集里面了。
- 使用`http.Cookie`创建要存储的数据，`HttpOnly`是限定只能用Golang服务器端修改，不能用网页的`script`修改。
- Cookie必须注意`Path`路径和`Expires`过期时间的设置，否则可能导致只在`/api`路径下有效（实际这只是个接口，真实浏览器并没有这个路径，所以导致Cookie刷新后就会消失）。
- 使用`w.Header().Set`设置`Cookie`。
- 设置Cookie和返回信息数据没有关系。

##分离SetCookie.go

写入Cookie这个还是比较啰嗦的，因为以后会一直使用，我们把它单独出来放到util里面`util/SetCookie.go`，内容如下：
```
package util

import (
	"net/http"
	"time"
)

//SetCookie 设置Cookie，默认1月/路径
func SetCookie(w http.ResponseWriter, k string, v string) {
	exp := time.Now().AddDate(0, 1, 0)
	path := "/"
	SetCookieExt(w, k, v, exp, path, 0)
}

//DelCookie 删除Cookie，MaxAge=-1
func DelCookie(w http.ResponseWriter, k string) {
	exp := time.Now()
	path := "/"
	SetCookieExt(w, k, "", exp, path, -1)
}

//SetCookieExt 设置Cookie扩展版
func SetCookieExt(w http.ResponseWriter, k string, v string, exp time.Time, path string, max int) {
	c := http.Cookie{
		Name:     k,
		Path:     path,
		Value:    v,
		HttpOnly: true,
		Expires:  exp,
		MaxAge:   max,
	}
	http.SetCookie(w, &c)
}
```
注意以下几点：
- 由于Golang不支持函数的参数默认值（每个值必须设置），所以我们做了三个函数，一个简化版`func SetCookie`的只有3个参数，另一个用来删除Cookie的`DelCookie`只有2个参数，还有一个扩展版`SetCookieExt`有5个参数。
- 删除一个Cookie只要把它的`MaxAge`设置为小于0。虽然你仍然可以在浏览器中看到这个Cookie，但是由于已经过期，所以读取出来是nil空的，等于不存在。
- `http.SetCookie(w, &c)`可以叠加多个Cookie，而`w.Header().Set("Set-Cookie", c.String())`只会执行最后一个Cookie。

然后我们就可以修改`login.go`中的代码：
```
//Login 注册接口处理函数
func Login(w http.ResponseWriter, r *http.Request) {
	ds := loginReqDS{}
	json.NewDecoder(r.Body).Decode(&ds)

	// //访问数据集
	dbc := tool.MongoDBCLient.Database("myweb").Collection("user")

	//验证用户邮箱是否与用户名匹配
	var u bson.M
	dbc.FindOne(context.TODO(), bson.M{"Email": ds.Email}).Decode(&u)
	if u["Pw"] == ds.Pw {
		uid := u["_id"].(primitive.ObjectID).Hex()

		//创建token并写入数据库
		token, _ := uuid.NewV4()
		tokens := token.String()
		ctoken := tool.MongoDBCLient.Database("myweb").Collection("token")
		du := bson.M{"Token": tokens, "Id": u["_id"], "Ts": time.Now().Unix()}
		ctoken.InsertOne(context.TODO(), du)

		//返回id，写入Token和Uid
		util.SetCookie(w, "Token", tokens)
		util.SetCookie(w, "Uid", uid)

		util.WWrite(w, 0, "登录成功", u["_id"])
	} else {
		util.WWrite(w, 1, "邮箱与用户名不匹配", nil)
	}

	return
}
```
注意这里我们写入了两个Cookie：`Token`和`Uid`。
其中`uid`（userId）使用`uid := u["_id"].(primitive.ObjectID).Hex()`把从数据库中读取的内容转成了字符`string`。

运行代码，在页面上登录之后就可以看到新增了两个Cookie：
[图片上传失败...(image-f37ea6-1554260822526)]


##中间件MiddleWare.go

在`app.go`中，我们使用了文件服务，`http.Handle("/", http.FileServer(http.Dir(webDir))`把所有没明确指出处理服务的路径都指向了文件服务。（`api/...`都是明确指出处理服务的）。

如果我们能够在用户每次打开新页面`.html`的时候就自动检测他是否已经登录过，那么以后处理就容易很多。

我们目前的文件路径处理是：
$$用户请求 \to FileServer文件服务处理$$
中间加一个事情，我们叫它中间件，就变为:
$$用户请求 \to 中间件MiddleWare处理 \to  FileServer文件服务处理$$

我们先修改`app.go`：
```
	//文件服务器和中间件
	fileHandler := http.FileServer(http.Dir(webDir))
	http.Handle("/", ext.MiddleWare(fileHandler))
```
这里我们给原来的`fileHandler`加了一层外套`ext.MiddleWare(fileHandler)`。然后我们来看`app/ext/MiddleWare.go`，代码如下：
```
package ext

import (
	"app/tool"
	"app/util"
	"context"
	"net/http"
	"regexp"

	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/bson/primitive"
)

//MiddleWare 文件服务中间件
func MiddleWare(h http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {

		//仅对.html文件处理
		htmlRe, _ := regexp.Compile(`^.+\.html[\?]*.*$`)
		if !htmlRe.MatchString(r.URL.String()) {
			h.ServeHTTP(w, r)
			return
		}

		//获取Token
		token, _ := r.Cookie("Token")
		if token == nil {
			util.DelCookie(w, "Uid")
			h.ServeHTTP(w, r)
			return
		}
		tv := token.Value
		if tv == "" {
			util.DelCookie(w, "Uid")
			h.ServeHTTP(w, r)
			return
		}

		//如果token匹配就向Cookie添加"Uid"
		ctoken := tool.MongoDBCLient.Database("myweb").Collection("token")
		var t bson.M
		ctoken.FindOne(context.TODO(), bson.M{"Token": tv}).Decode(&t)
		uid := t["Id"]
		if uid != nil {
			uids := uid.(primitive.ObjectID).Hex()
			util.SetCookie(w, "Uid", uids)
		} else {
			util.DelCookie(w, "Uid")
		}

		//文件服务
		h.ServeHTTP(w, r)
	})
}
```
注意几点：
- 我们的这个`func MiddleWare(h http.Handler) http.Handler `可以看得出，进来的参数是`h http.Handler`,返回的也是`http.Handler`,就是说吃进来的和吐出来的是一样类型。这样我们在`app.go`里面才能确保`fileHandler`和`ext.MiddleWare(fileHandler)`类型一样不会错。
- 我们使用了正则表达式```regexp.Compile(`^.+\.html[\?]*.*$`)```来判断是否是`.html`文件。只对`.html`文件页面做自动登录处理。
- 读取Cookie的代码是`r.Cookie("Token")`，但要取得它的`.Value`才能用。
- 仅对检测到匹配的`Token`的时候增加写入`Uid`，对于未检测到或者不匹配的就删除掉`Uid`。


##添加autoLogin.go

我们来增加一个自动登录的接口`api/autoLogin.go`，每个需要自动登录检查的页面都可以调用这个地址，如果成功就返回用户的邮箱信息，如果失败就跳转到`login.html`页面。

```
package api

import (
	"app/tool"
	"app/util"
	"context"
	"encoding/json"
	"net/http"

	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/bson/primitive"
)

type autoLoginReqDS struct {
	Email string
}

//AutoLogin 注册接口处理函数
func AutoLogin(w http.ResponseWriter, r *http.Request) {
	ds := autoLoginReqDS{}
	json.NewDecoder(r.Body).Decode(&ds)

	//直接信任Cookie中的Uid
	uid, _ := r.Cookie("Uid")

	//没登录返回空
	if uid == nil || uid.Value == "" {
		util.WWrite(w, 1, "自动登录失败。", nil)
		return
	}

	//登录成功返回对象
	var u bson.M
	coll := tool.MongoDBCLient.Database("myweb").Collection("user")
	idobj, err := primitive.ObjectIDFromHex(uid.Value)
	if err != nil {
		util.WWrite(w, 1, "自动登录Cookie.Uid异常。", nil)
		return
	}
	coll.FindOne(context.TODO(), bson.M{"_id": idobj}).Decode(&u)

	data := map[string]string{
		"Email": u["Email"].(string),
		"Uid":   uid.Value}
	datas, err := json.Marshal(data)
	if err != nil {
		util.WWrite(w, 1, "自动登录数据库内容异常。", nil)
		return
	}

	util.WWrite(w, 0, "自动登录成功。", string(datas))
	return
}
```
这个代码没有很特别的地方，注意最后我们利用`json.Mashal`返回了较复杂一些的数据，稍后我们会在页面上读取这个内容。

##改进MiddleWare.go

在上面的自动登录`autoLogin.go`中我们直接信任了Cookie里面的`Uid`。然而原则上前端网页带来的信息都是不可靠的，可以被伪造的。所以最好我们也应该在`autoLogin`处理之前最好也用中间件验证一下这个Cookie里面的`Uid`是否可靠。

我们改进`MiddleWare.go`：
```
package ext

import (
	"app/tool"
	"app/util"
	"context"
	"net/http"
	"regexp"

	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/bson/primitive"
)

//MiddleWare 文件服务中间件
func MiddleWare(h http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {

		//仅对.html文件处理
		htmlRe, _ := regexp.Compile(`^.+\.html[\?]*.*$`)
		if !htmlRe.MatchString(r.URL.String()) {
			h.ServeHTTP(w, r)
			return
		}

		//检查Cookie中的Uid是否合法
		loginCheck(w, r)
		//文件服务
		h.ServeHTTP(w, r)
	})
}

//MiddleWareAPI API中间件:检查Uid和Token的合理性
func MiddleWareAPI(next http.HandlerFunc) http.HandlerFunc {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		//检查Cookie中的Uid是否合法
		loginCheck(w, r)
		//API服务
		next(w, r)
	})
}

//loginCheck 检查Cookie中的Uid是否合法
func loginCheck(w http.ResponseWriter, r *http.Request) {
	//获取Token
	token, _ := r.Cookie("Token")
	if token == nil {
		util.DelCookie(w, "Uid")
		return
	}
	tv := token.Value
	if tv == "" {
		util.DelCookie(w, "Uid")
		return
	}

	//如果token匹配就向Cookie添加"Uid"
	ctoken := tool.MongoDBCLient.Database("myweb").Collection("token")
	var t bson.M
	ctoken.FindOne(context.TODO(), bson.M{"Token": tv}).Decode(&t)
	uid := t["Id"]
	if uid != nil {
		uids := uid.(primitive.ObjectID).Hex()
		util.SetCookie(w, "Uid", uids)
	} else {
		util.DelCookie(w, "Uid")
	}
}
```
注意几点：
- 我们把验证用户登录的方法单独拉出来变为`loginCheck`。
- 我们再原有文件处理中间件的基础上新增了`API`版本`MiddleWareAPI`。
- `MiddleWareAPI`其实比较简单，它吃`http.HandlerFunc`，也返回`http.HandlerFunc`，只是中间我们插入了`loginCheck(w,r)`。

然后我们终于可以到`app.go`设置服务路径了：
```
	http.HandleFunc("/api/AutoLogin", ext.MiddleWareAPI(api.AutoLogin))
```


##改进index.html

我们来改一下index.html，让首页尝试自动登录，如果登录失败就跳转到登录页面,下面是index.html的完整代码：
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
    <div class="row justify-content-center" style="margin-top:100px;margin-bottom:20px">
        <h4>~欢迎您来到我的网站~</h4>
    </div>
    <div class="row justify-content-center">
        <div id='uEmail'>正在为您登录</div>
    </div>

    <!-- Optional JavaScript -->
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
    <script src="https://cdn.bootcss.com/jquery/3.2.1/jquery.min.js"></script>
    <script src="https://cdn.bootcss.com/popper.js/1.12.9/umd/popper.min.js"></script>
    <script src="https://cdn.bootcss.com/bootstrap/4.0.0/js/bootstrap.min.js"></script>
</body>

<script type="text/javascript">
    function autoLogin() {
        $.post('/api/AutoLogin', function (res) {
            obj = JSON.parse(res.Data);
            if (obj && obj['Email']) {
                $('#uEmail').html(obj['Email'])
            }else{
                $('#uEmail').html("自动登录失败，正在为您跳转...")
                setTimeout(() => {
                    location='/page/login.html'
                }, 1000);
            }
        }, 'json')
    }
    autoLogin()
</script>

</html>
```
注意以下几点：
- 我们在结尾自动执行了`autologin()`
- 因为Golang传过来的都是string，所以我们`obj = JSON.parse(res.Data)`把string转为对象，这样就可以`obj['Email']`获取数据了。
- 使用`location='/page/login.html'`方法跳转页面。
- 使用`setTimeout(() => {...}, 1000)`延迟1秒再跳转。

好了，可以运行测试了，正常的话如果还没登录（或者把Cookie删掉了），那么首页就会为你跳转到登录页面，正常登陆之后，再回到首页就可以看到自己的邮箱了：
![](imgs/4324074-923e90c84e36b422.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


##小结
- Cookie就是浏览器为每个网站的开发者准备的用于记录用户信息的小文件。可以用Golang直接操作Cookie。
- Token是我们在用户每次手工登录时候创建的唯一字符串，和用户的Uid是对应的，也对应到数据库中的条目。注意可能多个Token对应一个Uid，但不可能多个Uid对应同一个Token。
- 中间件概念可以让我们为多个路径处理服务插入同一个处理程序，比如我们为每个.html文件服务都插入了验证Cookie中Token和Uid的功能，同样我们也为`api/Autologin`路径插入了这个验证，如果需要的话任何一个api处理都可以先加上这个验证以确保Uid可靠性。
- 别忘了提及到Git再提交到Github。

> 虽然还有一些链接没有添加，但似乎登录注册功能基本完成了。但还有一个严重缺陷，那就是我们一直把用户的密码反复的明文传输，如果被坏人中间截获了就不好了，当然，你的网站数据库中直接明明白白记录着这些重要的密码，本身就是非常不负责的，下一篇我们介绍如何解决这个缺陷。





---
欢迎关注我的专栏( つ•̀ω•́)つ[【人工智能通识】](https://www.jianshu.com/c/e9a7b7b7024d)

---
###每个人的智能新时代
如果您发现文章错误，请不吝留言指正；
如果您觉得有用，请点喜欢；
如果您觉得很有用，欢迎转载~
---
END