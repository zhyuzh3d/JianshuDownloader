欢迎关注我的专栏( つ•̀ω•́)つ[【人工智能通识】](https://www.jianshu.com/c/e9a7b7b7024d)
[【汇总】2019年4月专题](https://www.jianshu.com/p/e1afed853866)

---

如何用Golang自动向用户邮箱发送验证码？

![](imgs/4324074-1848e5cd82d6e68e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

[人工智能通识-2019年3月专题汇总](https://www.jianshu.com/p/72685b77cfff)

##SMTP

Simple Mail Transfer Protocol，SMTP简单邮件传输协议，它是在网络传输电子邮件的常用标准。

我们的Golang可以通过SMTP方式调用右键服务商（比如Hotmail）的发邮件功能，替我们自动发邮件。

##查看hotmail的SMTP设置

首先需要注册一个hotmail邮箱。

[点这里注册Hotmail/Outlook邮箱](https://hotmail.com)

注册成功之后，右上角点齿轮弹出设置搜索，输入`pop`，点击进入**POP和IMAP**设置。

![](imgs/4324074-a373721fdb1aa533.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

然后开启POP选项，注意下面的SMTP设置。

![](imgs/4324074-de673782cfe573a8.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

##Golang的net/smtp

Golang提供了一个基本的SMTP发邮件模块，可以导入它`import 	"net/smtp"`。

[点这里看smtp的详细说明](https://golang.org/pkg/net/smtp/)

它的基本流程是：
- 用`smtp.SendMail`方法发送邮件，它需要几个参数`addr string, a Auth, from string, to []string, msg []byte`,分别是addr发送服务器名称（带端口），Auth用户授权（用户名和密码），发件人邮箱from，目标收件人邮箱to，发送的内容msg字符串字节形式。
-  `smtp.PlainAuth`可以生成这样用户授权（用户名和密码）。
- msg需要拼接，一般包含`From,To,Subject(标题),Content-Type(文字类型),邮件文字`。

一般情况直接使用Golang的这个设置就可以了，但是Hotmail目前已经不再支持`PlainAuth`的认证模式，所以就要做单独的处理。

##改名tool.go新增mail.go

在Golang里面，文件夹就是`import`的包名package，比如我们导入`app/tool`其实就是导入了`tool`文件夹下所有的`.go`文件，这些文件都必须以`package tool`开头，每个文件里的首字母大写的变量或者函数都会被放到`tool.Xxx`这样的二级命令里，并且如果文件里面有`init`函数也会被自动运行。

所以`tool.go`文件换成`mongo.go`也不会产生任何影响。那么我们就把它改名。

然后我们创建新的`app/tool/mail.go`文件，代码如下：
```
package tool

import (
	"net/smtp"
)

const umail string = "zhyuzhnd@hotmail.com"
const upw string = "zhyuzh3d"
const host string = "smtp.office365.com:587"

type loginAuth struct {
	username, password string
}

func genLoginAuth(username, password string) smtp.Auth {
	return &loginAuth{username, password}
}

func (a *loginAuth) Start(server *smtp.ServerInfo) (string, []byte, error) {
	return "LOGIN", []byte(a.username), nil
}

func (a *loginAuth) Next(fromServer []byte, more bool) ([]byte, error) {
	if more {
		switch string(fromServer) {
		case "Username:":
			return []byte(a.username), nil
		case "Password:":
			return []byte(a.password), nil
		}
	}
	return nil, nil
}

//SendMail 发送邮件
func SendMail(target string, body string, subject string) error {
	auth := genLoginAuth(umail, upw)

	contentType := "Content-Type: text/plain" + "; charset=UTF-8"
	msg := []byte("To: " + target +
		"\r\nFrom: " + umail +
		"\r\nSubject: " + subject +
		"\r\n" + contentType + "\r\n\r\n" +
		body)
	err := smtp.SendMail(host, auth, umail, []string{target}, msg)
	if err != nil {
		return err
	}
	return nil
}
```

这个代码看上去挺乱，但不必太理会它的意思，只要注意以下几点：
- 这个是针对借用hotmail邮箱来发送邮件的。简单说就是我们的Golang呼叫hotmail邮箱，模拟用户名和密码登录，模拟发邮件。
- 这个代码并不完全适用于其他的邮箱（QQ邮箱或者Gmail或者网易邮箱等），可以参考[官方这个说明文档](https://golang.org/pkg/net/smtp/#SendMail)了解一下，其实可能只有Hotmail邮箱才这么麻烦。
- 顶部的几个常量中的`umai,upw`不要使用我的，你需要自己去注册Hotmail邮箱用你自己的密码，**小心不要把你常用的密码上传到Github！一定不要！一定不要！一定不要！**。
- 注意这个发送邮件函数`SendMail(target string, body string, subject string) error`包含了三个参数，target发送目标邮箱，body是发送的文字内容，subject是邮件的标题。


##重新组织所有api

同样，我们也把`api/login/login.go`和`api/register/register.go`移动到`api`文件夹下面，把空的`register`文件夹和`login`文件夹删除。

这样我们可以在`app.go`中只导入一个`src/api`就可以了，并修改下面的服务接口设置：
```
	//API-注册登录相关
	http.HandleFunc("/api/register", api.Register)
	http.HandleFunc("/api/login", api.Login)
```

然后我们还要修改`login.go`中：
- 第一行改为`package api`
- 修改`struct ReqDS`结构改名为`struct loginReqDS`，并对应修改下面的`ds := loginReqDS{}`。
- 将`HandleFunc`改名为`Login`与`app.go`中设置的一致。

同样修改`register.go`:
- 第一行改为`package api`
- 修改`struct ReqDS`结构改名为`struct registerReqDS`，并对应修改下面的`ds := registerReqDS{}`。
- 将`HandleFunc`改名为`Register`与`app.go`中设置的一致。


然后测试运行，检查已有的旧功能是否正常。


##修改注册页面register.html

我们在页面上增加验证码界面元素：
```
                <div class="form-group">
                    <label for="exampleInputPassword1">邮箱验证码：</label>
                    <div class="row">
                        <div class="col-7">
                            <input id='verify' onkeyup="checkVerify()"  class="form-control"
                                placeholder="请输入6位验证码">
                        </div>
                        <div class="col-5">
                            <button id='sendVerify' onClick="sendVerify()"
                                class="btn btn-success btn-block">发送验证码</button>
                        </div>
                    </div>
                    <small id='verifyTip' style="display:none">请输入6位数字验证码</small>
                </div>
```
利用`Go Live`查看效果大致是：
![](imgs/4324074-ed201f60b21798a8.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

然后我们再修改下面的`script`部分，增加检查验证码格式的`checkVerify`和发送验证码邮件的`sendVerify`方法。

`checkVerify`部分：
```
    //检查验证码格式是否正确
    var verifyRe = /^[0-9]{6}$/

    function checkVerify() {
        var ver = $('#verify').val();
        if (verifyRe.test(ver) == false) {
            $('#verifyTip').css('display', 'block')
            $('#verify').removeClass('is-valid')
            $('#verify').addClass('is-invalid')
        } else {
            $('#verifyTip').css('display', 'none')
            $('#verify').removeClass('is-invalid')
            $('#verify').addClass('is-valid')
        }
        checkBtn()
    }
```
`sendVerify`部分：
```
    //发送验证邮件
    function sendVerify() {
        var data = {
            Email: $('#email').val(),
        }

        $.post('/api/sendRegVerifyMail', JSON.stringify(data), function (res) {
            alert(res.Msg);
        }, 'json')
    }
```
此外，我们还要修改`checkBtn`检测提交按钮的函数中应该加入验证码格式是否正确的检查：
```
//检查按钮是否可以被开启
    function checkBtn() {
        var agree = $('#agree').is(':checked');
        var mail = $('#email').val();
        var pw = $('#pw').val();
        var ver = $('#verify').val();
        if (pwRe.test(pw) && mailRe.test(mail) && verifyRe.test(ver) && agree) {
            $('#regBtn').removeAttr('disabled')
        } else {
            $('#regBtn').attr('disabled', 'true')
        }
    }
```

最后我们还要限制**发送验证按钮**只能在邮箱格式正确的时候才被启用，所以先在界面代码加入`disabled`禁止`...class="btn btn-success btn-block" disabled="true">发送验证码</button>`，然后在`checkMail`中对它进行开启或关闭：
```
    //检查邮箱的输入格式
    function checkMail() {
        var mail = $('#email').val();
        if (mailRe.test(mail) == false) {
            $('#mailTip').css('display', 'block')
            $('#email').removeClass('is-valid')
            $('#email').addClass('is-invalid')
            $('#sendVerify').attr('disabled', 'true')
        } else {
            $('#mailTip').css('display', 'none')
            $('#email').removeClass('is-invalid')
            $('#email').addClass('is-valid')
            $('#sendVerify').removeAttr('disabled')
        }
        checkBtn()
    }
```

##增加sendRegVerifyMail.go

对应页面上的`sendVerify`方法的`$.post('/api/sendRegVerifyMail',...`，我们在Golang服务器上也应该增加对应的服务接口。

创建`api/sendRegVerifyMail.go`，其内容如下(我们已经拥有一个能发送邮件的`tool.SendMail`方法)：
```
package api

import (
	"app/tool"
	"app/util"
	"context"
	"encoding/json"
	"fmt"
	"math/rand"
	"net/http"
	"regexp"
	"strconv"
	"time"

	"go.mongodb.org/mongo-driver/bson"
)

type sendRegVerifyMailReqDS struct {
	Email string
}

//SendRegVerifyMail 注册接口处理函数
func SendRegVerifyMail(w http.ResponseWriter, r *http.Request) {
	ds := sendRegVerifyMailReqDS{}
	json.NewDecoder(r.Body).Decode(&ds)

	mailRe, _ := regexp.Compile(`^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$`)
	if !mailRe.MatchString(ds.Email) {
		util.WWrite(w, 1, "邮箱格式错误。", nil)
		return
	}

	//检查是否存在，如果已经存在且时间小于1分钟就就不再发送
	dbc := tool.MongoDBCLient.Database("myweb").Collection("regVerify")
	var u bson.M
	dbc.FindOne(context.TODO(), bson.M{"Email": ds.Email}).Decode(&u)
	now := time.Now().Unix()
	if u["Ts"] != nil && now-u["Ts"].(int64) < 60 {
		util.WWrite(w, 1, "请不要重复发送邮件。", nil)
		return
	}

	//生成随机6位数，并发送
	code := rand.Intn(899999) + 100000
	s := strconv.Itoa(code)
	err := tool.SendMail(ds.Email, "您在www.myweb.com的注册码是:"+s, "来自Myweb的注册验证码")
	if err != nil {
		util.WWrite(w, 1, "发送邮件失败。", nil)
		fmt.Println(err)
		return
	}

	//删除原有数据，创建新数据
	dbc.DeleteOne(context.TODO(), bson.M{"Email": ds.Email})
	dt := bson.M{"Code": s, "Email": ds.Email, "Ts": now}
	_, err = dbc.InsertOne(context.TODO(), dt)
	if err != nil {
		util.WWrite(w, 1, "写入数据库出错。", nil)
		fmt.Println(err)
	} else {
		util.WWrite(w, 0, "发送成功，请检查邮箱。", nil)
	}
	return
}
```
注意其中的几点：
- 首先我们检查了邮箱格式，格式不对直接返回。
- 然后我们坚持数据集`regVerify`中是否已经存在这个邮箱的数据，而且还检测这个数据的`Ts`，它是timestamp时间戳，它记录了上一次发送邮件的时间，如果这个时间到现在`now`不到60秒，那么就提示不要重复发邮件。
- 生成100000~999999的六位数，并利`tool.SendMail`用发送邮件，三个参数，发给谁，内容是什么，标题是什么。
- 尝试删除原有数据`DeleteOne`然后插入新的数据`InsertOne`，注意这里的`Ts`时间戳数字被存储了。

写好这个文件，别忘了在`app.go`中添加服务路径：
```
http.HandleFunc("/api/sendRegVerifyMail", api.SendRegVerifyMail)
```


##关于Hotmail邮箱

你必须要注册一个Hotmail邮箱才能借用它来发送邮件。

![](imgs/4324074-e8d723b8ab8391f4.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

注册之后修改你`mail.go`里面的`const umail`和`cosnt upw`。

启动`app.go`之后尝试在注册页面上输入邮箱，然后点击发送验证码按钮，很可能会没有反应，Golang的输出上会出错，这是正常的，请在网页里检查你新注册的Hotmail邮箱，会收到一封提示邮件，这是要求你绑定手机号，绑定之后才可以正常发邮件。

在Hotmail网站绑定好手机之后，重新启动`app.go`，注册页中输入邮箱点击发送按钮，稍后能弹出`发送成功，请检查邮箱。`提示，如果连续点击则会提示`请不要重复发送邮件`。然后检查邮件，在垃圾邮件里面可以找到自己发送的内容：
![](imgs/4324074-8b692825e2ad4127.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


> 注意Hotmail对这种用Golang的`smtp.SendMail`发送邮件的方式有限制，官方说法是每天不超过100封，但实际上可能十几封之后就被禁止发送了，需要你重新进入邮箱激活才能用，也可能今天就用不了了...遇到这个情况没有什么好办法，只能再去注册一个新邮箱测试了。

##在`register.html`中限制发送按钮

我们也可以在网页代码中限定用户每次点击发送按钮之后都冻结3秒，避免用户不小心连续点两下。
```
    //发送验证邮件
    function sendVerify() {
        var data = {
            Email: $('#email').val(),
        }

        $.post('/api/sendRegVerifyMail', JSON.stringify(data), function (res) {
            alert(res.Msg);
        }, 'json')
        $('#sendVerify').attr('disabled', 'true')
        setTimeout(() => {
            $('#sendVerify').removeAttr('disabled')
        }, 3000);        
    }
```
好了，差不多的时候可以切换到左侧的版本管理面板，输入框写点什么，然后Ctril+回车提交代码到Git，然后再从小菜单推送到Github。
![](imgs/4324074-2f40c31509b3bd12.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

>如果弹出username和mail的提示，请切换到终端输入下面的命令(用户名和邮箱任意):
```
git config --global user.name "zhyuzh"
git config --global user.email "zhyuzh3d@hotmail.com"
```



##几点补充

- 正常开发中都会使用专业的**邮件推送服务**，比如可以购买使用[阿里云的邮件推送服务](https://cn.aliyun.com/product/directmail)，但你首先需要有个已经备案的域名，购买域名只要几十块第一年，但备案就需要再花至少几十块买个ECS云服务器，而且备案一般都要一两周才能完成...当然最后邮件推送服务也是要花钱的。所以，如果你计划成为一名正式开发者，这些都是不可少的。
- 另外一个快一些的办法是改用**手机号码注册+短信验证**，阿里云提供了[很划算的短信套餐](https://cn.aliyun.com/product/sms)，你以后可以考虑学习使用这个。

> 虽然我们基本上完成了注册功能，但还没有提供修改密码相关的功能，登录功能也不完善，稍后的文章我们会继续这些内容。







---
欢迎关注我的专栏( つ•̀ω•́)つ[【人工智能通识】](https://www.jianshu.com/c/e9a7b7b7024d)

---
###每个人的智能新时代
如果您发现文章错误，请不吝留言指正；
如果您觉得有用，请点喜欢；
如果您觉得很有用，欢迎转载~
---
END