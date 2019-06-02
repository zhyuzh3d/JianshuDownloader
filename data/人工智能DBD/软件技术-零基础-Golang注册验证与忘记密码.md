欢迎关注我的专栏( つ•̀ω•́)つ[【人工智能通识】](https://www.jianshu.com/c/e9a7b7b7024d)
[【汇总】2019年4月专题](https://www.jianshu.com/p/e1afed853866)

---

如何检查用户的验证码？如何编写忘记密码功能？

![](imgs/4324074-d0fbd1d4fdb3ad39.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

[人工智能通识-2019年3月专题汇总](https://www.jianshu.com/p/72685b77cfff)


##改进register.go

我们先在开头的数据结构中增加一个`Code`验证码字段：
```
type registerReqDS struct {
	Email string
	Pw    string
	Code  string
}
```
然后在下面的`Register`方法里面增加验证码格式的检查：
```
	codeRe, _ := regexp.Compile(`^[0-9]{6}$`)
	fmt.Println(ds.Code, reflect.TypeOf(ds.Code))
	if !codeRe.MatchString(ds.Code) {
		util.WWrite(w, 1, "验证码格式错误", nil)
		return
	}
```

后面检查用户邮箱是否存在之前，我们增加检查验证码`Code`和数据库`regVerify`中数据是否匹配的检查：
```
	//检查验证码是否正确
	dbcv := tool.MongoDBCLient.Database("myweb").Collection("regVerify")
	var v bson.M
	dbcv.FindOne(context.TODO(), bson.M{"Email": ds.Email}).Decode(&v)
	if v["Code"] == nil || v["Code"] != ds.Code {
		util.WWrite(w, 1, "验证码错误。", nil)
		return
	}
```
最后面我们可以顺带把用户注册时间戳也一起存入数据库：
```
	//写入数据库
	u := bson.M{"Email": ds.Email, "Pw": ds.Pw, "Ts": time.Now().Unix()}
```
然后保存并运行，利用邮箱中收到的验证码进行注册。

整个`regsiter.go`的完整代码如下，可以对照梳理一下思路：
```
package api

import (
	"app/tool"
	"app/util"
	"context"
	"encoding/json"
	"fmt"
	"net/http"
	"reflect"
	"regexp"
	"time"

	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/bson/primitive"
)

type registerReqDS struct {
	Email string
	Pw    string
	Code  string
}

//Register 注册接口处理函数
func Register(w http.ResponseWriter, r *http.Request) {
	ds := registerReqDS{}
	json.NewDecoder(r.Body).Decode(&ds)

	//格式检查
	pwRe, _ := regexp.Compile(`^[0-9a-zA-Z_@]{6,18}$`)
	if !pwRe.MatchString(ds.Pw) {
		util.WWrite(w, 1, "密码格式错误。", nil)
		return
	}

	codeRe, _ := regexp.Compile(`^[0-9]{6}$`)
	fmt.Println(ds.Code, reflect.TypeOf(ds.Code))
	if !codeRe.MatchString(ds.Code) {
		util.WWrite(w, 1, "验证码格式错误", nil)
		return
	}

	mailRe, _ := regexp.Compile(`^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$`)
	if !mailRe.MatchString(ds.Email) {
		util.WWrite(w, 1, "邮箱格式错误。", nil)
		return
	}

	//检查验证码是否正确
	dbcv := tool.MongoDBCLient.Database("myweb").Collection("regVerify")
	var v bson.M
	dbcv.FindOne(context.TODO(), bson.M{"Email": ds.Email}).Decode(&v)
	if v["Code"] == nil || v["Code"] != ds.Code {
		util.WWrite(w, 1, "验证码错误。", nil)
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
	u := bson.M{"Email": ds.Email, "Pw": ds.Pw, "Ts": time.Now().Unix()}
	res, err := dbc.InsertOne(ctx, u)
	if err != nil {
		util.WWrite(w, 1, "写入数据库失败。", nil)
		return
	}
	d := res.InsertedID.(primitive.ObjectID).Hex()
	util.WWrite(w, 0, "注册成功。", d)
	return
}
```

##忘记密码页面

如果用户忘记了密码怎么办？
我们实际上可以参照注册流程来思考。
复制`regsiter.html`文件成为`page/fogotPw.html`，修改它看起来这样：

![](imgs/4324074-13b5764d4d38f624.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

用户输入邮箱，点击发送验证码，然后只要能输入邮箱里面收到的正确验证码就可以重置密码了。

整个页面代码的变化主要有：
- 去掉了`用户协议`选项，在`checkBtn() `函数中也去掉了`agree`检测。
- 原来的`sendRegPost`方法改为`sendRstPwPost`方法，`'/api/Register'`也改为`'/api/ResetPw'`
- `sendVerify`方法中`'/api/SendRegVerifyMail'`改为`'/api/SendRstPwMail'`.

##增加sendRstPwMail.go

复制`sendRegVerifyMail.go`的内容成为`api/sendRstPwMail.go`文件，然后修改：
- 修改数据结构为` type sendRstPwReqDS struct`
- 修改函数名为`func SendRstPwReqDS`
- 修改`ds := sendRstPwReqDS{}`
- 修改数据集为`Database("myweb").Collection("rstPwVerify")`
- 修改发送邮件内容`SendMail(ds.Email, "您在www.myweb.com的重置码是:"+s, "来自Myweb的重置验证码")`
- 在邮箱格式检查之后，我们添加邮箱是否注册的检查：
```
	//检查邮箱是否已经注册，没注册不发送验证码
	dbcu := tool.MongoDBCLient.Database("myweb").Collection("user")
	count, _ := dbcu.CountDocuments(context.TODO(), bson.M{"Email": ds.Email})
	if count == 0 {
		util.WWrite(w, 1, "这个邮箱还没有注册。", nil)
		return
	}
```

然后再`app.go`中添加服务路径：
`http.HandleFunc("/api/SendRstPwMail", api.SendRstPwMail)`

然后运行代码，尝试访问页面`http://localhost:8088/page/resetPw.html`输入已经注册的邮箱，点击发送验证码按钮，成功后检查邮箱中的验证码。


##增加resetPw.go

复制`register.go`的内容成为`api/resetPw.go`文件，然后修改：
- 修改数据格式`type resetPwReqDS construt`和`ds := resetPwReqDS{}`
- 修改函数名`func ResetPw`
- 将原有验证码检查部分修改为`.Database("myweb").Collection("rstPwVerify")`
- 将后续部分修改为以下新内容：
```
	//更新数据库中的密码
	dbc := tool.MongoDBCLient.Database("myweb").Collection("user")
	filter := bson.M{"Email": ds.Email}
	up := bson.M{"$set": bson.M{"Pw": ds.Pw}}
	_, err := dbc.UpdateOne(context.TODO(), filter, up)
	if err != nil {
		util.WWrite(w, 1, "写入数据库失败。", nil)
		return
	}

	//返回修改的账号
	var nu bson.M
	dbc.FindOne(context.TODO(), bson.M{"Email": ds.Email}).Decode(&nu)
	util.WWrite(w, 0, "修改成功。", nu["_id"])
	return
```
这段代码注意几个内容：
- 我们使用了`UpdateOne`方法更新已有数据，
- 注意这里带有`$set`的格式表示要修改的内容`bson.M{"$set": bson.M{"Pw": ds.Pw}}`
- 重新使用了`FindOne`最后获取了用户的`_id`属性返回给用户，这在后续会使用到。

>虽然我们能够利用`login.html`页面登录，但是切换新页面之后我们怎么知道用户仍然处于登录状态呢？不能让用户每个页面都登录，在下一篇我们介绍如何利用cookie来实现用户的自动登录。



---
欢迎关注我的专栏( つ•̀ω•́)つ[【人工智能通识】](https://www.jianshu.com/c/e9a7b7b7024d)

---
###每个人的智能新时代
如果您发现文章错误，请不吝留言指正；
如果您觉得有用，请点喜欢；
如果您觉得很有用，欢迎转载~
---
END