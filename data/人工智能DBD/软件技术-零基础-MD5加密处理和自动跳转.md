欢迎关注我的专栏( つ•̀ω•́)つ[【人工智能通识】](https://www.jianshu.com/c/e9a7b7b7024d)
[【汇总】2019年4月专题](https://www.jianshu.com/p/e1afed853866)

---
如何将用户的密码加密之后再存储？

![](imgs/4324074-0dd3b5f26f37ff19.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
[人工智能通识-2019年3月专题汇总](https://www.jianshu.com/p/72685b77cfff)

##MD5

加密的目的是保护用户的隐私，尤其是一些很敏感的密码，原则上这些密码的明文只能出现在用户电脑上，不能在网络上传输，更不能存储在网站服务器上。

MD5是一种不可逆的加密算法，就是说它可以把用户密码变为一串新字符，而原则上没有任何方法可以把这串新字符再变回去找到用户真实的密码。（但没有什么是绝对的，只是相对来说是这样）

MD5总是生成32个英文字符和字母混合的字符串。

##前端加密

实际上我们只需要在网页端将用户所有输入的密码都处理一下就可以了，不涉及后端服务器程序，因为用户密码到底是什么格式，对于服务器来说都是一样的存储、验证。


需要为前端相关页面`register.html，login.html，resetPw.html`都添加一个加密工具：
```
    <script src="https://cdn.bootcss.com/spark-md5/3.0.0/spark-md5.min.js"></script>
```
然后把所有向接口发送的Pw数据都用`SparkMD5.hash`代码包裹一下：
```
Pw: SparkMD5.hash($('#pw').val())
```
然后Golang服务端对Pw验证的正则表达式改为`^[0-9a-z]{32}$`，应该涉及到`login.go,register.go,resetPw.go`等多个文件。

然后把服务端数据库都删除，然后重新测试登录和注册、改密码和自动登录功能。

##注册和重置后自动登录

先做一个统一的创建新Token并写入Cookie的方法`ext/NewToken.go`，其代码如下：
```
package ext

import (
	"app/tool"
	"app/util"
	"context"
	"encoding/json"
	"net/http"
	"time"

	uuid "github.com/satori/go.uuid"
	"go.mongodb.org/mongo-driver/bson"
)

//NewToken 创建新token，返回一个基本的用户信息Token和Uid，用于用户手工登录注册和重置时候使用
func NewToken(w http.ResponseWriter, uids string) string {
	//创建token
	token, _ := uuid.NewV4()
	tokens := token.String()

	//删除旧的,创建新的
	coll := tool.MongoDBCLient.Database("myweb").Collection("token")
	du := bson.M{"Token": tokens, "Id": uids, "Ts": time.Now().Unix()}
	du2 := bson.M{"Id": uids}
	coll.DeleteMany(context.TODO(), du2)
	coll.InsertOne(context.TODO(), du)

	//返回对象
	data := map[string]string{
		"Token": tokens,
		"Uid":   uids}

	datas, err := json.Marshal(data)
	if err != nil {
		return ""
	}

	//返回id，写入Token和Uid
	util.SetCookie(w, "Uid", uids)
	util.SetCookie(w, "Token", tokens)
	return string(datas)
}
```
这个主要是为了将登录、注册和重置密码后所要做的同样工作统一在一起了。

然后我们就可以修改`login.go`简化很多：
```
	if u["Pw"] == ds.Pw {
		uids := u["_id"].(primitive.ObjectID).Hex()

		datas := ext.NewToken(w, uids)
		util.WWrite(w, 0, "登录成功", datas)
	} else {
		util.WWrite(w, 1, "邮箱与用户名不匹配", nil)
	}
	return
```
同样简化`register.go`:
```
	uids := res.InsertedID.(primitive.ObjectID).Hex()

	datas := ext.NewToken(w, uids)
	util.WWrite(w, 0, "注册成功。", datas)
	return
```

修改`resetPw.go`：
```
	//创建token，返回修改的账号
	var nu bson.M
	dbc.FindOne(context.TODO(), bson.M{"Email": ds.Email}).Decode(&nu)
	uids := nu["_id"]
	datas := ext.NewToken(w, uids.(string))
	util.WWrite(w, 0, "修改成功", datas)
	return
```

这样我们再登录、注册和重置之后都会更新Token，如果需要获取用户邮箱等信息，可以再执行`autoLogin`接口就可以了。


##自动跳转

比如说用户打开首页，然后会执行`autoLogin`，没通过，被我们跳转到登录页，然后用户登录成功，——这时候应该跳转回首页啊，怎么跳？
我们之前使用过`location = '/page/login.html'`实现跳转。

但是，当我们处于登录页的时候，登陆成功我们要跳回去，但我们怎么知道用户从哪里过来的呢？

所以在跳过来的时候就必须做好标记传递原来的页面地址过来。

首先在`index.html`中修改跳转链接：
```
location = '/page/login.html?ref='+location.pathname
```
这里的`location.pathname`就是页面地址。
然后在`login.html`页面中增加用来提取链接的工具
```
<script src="https://cdn.bootcss.com/jquery-url-parser/2.3.1/purl.min.js"></script>
```
登录成功后修改：
```
        $.post('/api/Login', JSON.stringify(data), function (res) {
            if (res['Code'] == 0) {
                //登录成功
                location = purl(location.href).param('ref') || "/"
            } else {
                alert(res['Msg'])
            }
        }, 'json')
```

这里`purl(location.href).param('ref')`表示提取刚才传过来的地址。双竖线表示如果没有传来地址那么就回`/`首页。

同时我们修改一下注册按钮链接，改为使用`script`跳转：
```
            <a onClick='goReg()' style="color:#CCC;cursor: pointer;">
                <h4>注册</h4>
            </a>
```
底部添加配套的代码：
```
    //注册链接动态跳转
    function goReg(){
        ref=purl(location.href).param('ref')
        fix=ref?('?ref='+ref):''
        location = '/page/register.html'+fix
    }
```
可以使用同样的方法添加`忘记密码`页面的链接跳转到`forgotPw.html`页面。也可以为`register.html`和`forgotPw.html`修改类似的成功跳转回去的功能。


##小结

前后从开始部署Golang到编写前端页面，然后前后端一起实现登录注册功能，这里总计用了15篇文章，基本上告一段落，后续还有很多内容，大家可以从Golang官方



---
欢迎关注我的专栏( つ•̀ω•́)つ[【人工智能通识】](https://www.jianshu.com/c/e9a7b7b7024d)

---
###每个人的智能新时代
如果您发现文章错误，请不吝留言指正；
如果您觉得有用，请点喜欢；
如果您觉得很有用，欢迎转载~
---
END