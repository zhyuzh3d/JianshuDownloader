欢迎关注我的专栏( つ•̀ω•́)つ[【人工智能通识】](https://www.jianshu.com/c/e9a7b7b7024d)

---
用户注册功能是网站的必要功能，也是其他功能的基础和前提。

![](imgs/4324074-30e7e7167f7bb6cf.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

上一篇文章[软件技术-零基础编写响应式页面](https://www.jianshu.com/p/d87f60409f84)
[人工智能通识-2019年3月专题汇总](https://www.jianshu.com/p/72685b77cfff)



##发送数据

编写好页面效果了，还要实现提交按钮功能，当用户点击提交按钮的时候就把邮箱和密码信息发送给服务器。

- 发送到哪里，定个目标，比如发给`http://localhost:8080//api/register`这个地方。
- 发送什么数据？要获取到输入框中用户打字的内容，可以用` $('#email').val()`的方法通过元素id名`email`获得输入框内容。
- 怎么发送？使用`$.post(target,data,successFunction)`方法。

综合上面三点，我们再代码最后增加以下部分：
```
...
...
</body>

<script type="text/javascript">
    function sendRegPost() {
        var data = {
            Email: $('#email').val(),
            Pw: $('#pw').val(),
        }
        $.post('/api/register?g=99', JSON.stringify(data), function (res) {
            alert(res.Email + ':' + res.Pw);
        }, 'json')
    }
</script>

</html>
```
这时候我们刷新`http://localhost:8080/page/login.html`页面后点击按钮并没有反应，因为服务器还没编写能够处理`/api/register`请求的代码。

我们可以在浏览器中**右键-检查**，切换到`console`控制台看到404报错：
![](imgs/4324074-ea3811d8c3ebb8f6.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


##接收数据

我们将把登录和注册相关的功能都放在`login.go`里面，为了整齐，我们把整个`login`文件夹放到`api`文件夹下，文件结构如下：
![](imgs/4324074-da8722dd79ac2621.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

修改`app.go`文件使之路径合适：
```
package main

import (
	"app/api/login"
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

	//注册登录相关
	http.HandleFunc("/api/register", login.Register)

	//启动服务
	log.Fatal(http.ListenAndServe(":8088", nil))

}
```
注意这里的`import`路径是`app/api/login`，并且下面的`http.HandleFunc("/api/register", login.Register)`把注册指向了`login.go`中的`Register`方法，我们立即去补充它：
```
package login

import (
	"encoding/json"
	"net/http"
)

//RegisterDS is DS
type RegisterDS struct {
	Email string
	Pw    string
}

//Register is the api handler function
func Register(w http.ResponseWriter, r *http.Request) {
	ds := RegisterDS{}
	json.NewDecoder(r.Body).Decode(&ds)
	dt, _ := json.Marshal(ds)
	w.Write([]byte(string(dt)))
}
```
注意这里我们创建了和网页上`script`中数据相同的结构`struct`，它也包含两个字段`Email、Pw`。
- 在下面的`Register`函数中我们创建了一个数据`ds:= RegisterDS{}`，这个数据是空的。
- 然后我们利用`json`的转换功能，把用户发来请求`r *http.Request`中的数据`r.Body`转化填充到`&ds`中，这样我们实际上`ds`就变为了一个`{Email:xxx,Pw:xxx}`的对象，我们可以使用`ds.Email`获得用户输入的邮箱。
- 最后，我们又用`Marshal`方法把`ds`转化为json对象`dt`,再用`w.Write`方法把它送回给用户。

虽然这看起来什么也没做，就像把用户发过来的快递拆开，然后又原封不动的寄了回去，但这只是个实验，足以证明我们可以对快递盒子中的数据做任何处理。

保存然后`Run Code`执行`app.go`文件。顺利启动没有异常的话然后到浏览器中随便输入一些什么，点击注册提交按钮，就会弹出输入的邮箱和密码，注意这个邮箱和密码其实是从服务器发送过来的而不是从输入框直接获得的。

![](imgs/4324074-69b5f619809985e9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

##输入格式的验证

上面的代码我们并没有对用户的输入进行验证，如果用户胡乱输入字符当做邮箱怎么办？如果用户密码只输了一个a怎么办？

首先我们要明确，验证有两遍，既要在用户键入字符的时候验证，也要在服务器Golang收到代码的时候验证，因为万一网络上半路被黑客篡改了就不安全了。

网页端的验证，修改`login.html`代码。我们先在两个输入框下面添加两行小字提示用户格式不对，默认不显示这些小字，同时为`input`添加`onkeyup`按键弹起时候执行的动作：
```
<input id='email' onkeyup="checkMail()" type="email" class="form-control" ...>
<small id='mailTip' style="display:none;">请输入正确邮箱格式</small>
```
然后我们再底部的`script`部分补上这个`checkMail()`代码：
```
    function sendRegPost() {
        var data = {
            Email: $('#email').val(),
            Pw: $('#pw').val(),
        }

        $.post('/api/register?g=99', JSON.stringify(data), function (res) {
            //alert(res.Email + ':' + res.Pw);
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
    }
```
注意以下几个内容：
- `var mailRe= /^(([^<>()[\]\\....`这种语法叫做**正则表达式**，专门用来检测字符串格式的，如果`mailRe.test(mail) == false`就代表不能通过它的测试，不符合邮箱的基本语法格式。
- `$('#mailTip').css('display', 'none')`，其中`display:none`就是不显示，而`display:block`就是正常显示。
- `$('#email').removeClass('is-valid')`，其中`removeClass`就是移除某种样式效果，而`addClass`则是增加效果；`valid`表示格式正确（绿色框），`invalid`是不正确（红色框）。

同样我们也为密码输入框添加：
```
<input id='pw' onkeyup="checkPw()" type="password" class="form-control" placeholder="请输入6~18位密码">
<small id='pwTip' style="display:none">请输入6~18位数字字母或下划线</small>
```
添加script：
```
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
}
```
完整运行的效果如下：

![](imgs/4324074-8c50b449dd725331.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

##服务端数据验证

服务器上面我们也要对用户发送过来的邮箱和密码进行验证。
```
package login

import (
	"encoding/json"
	"net/http"
	"regexp"
)

//Resp 返回的数据格式
type RespDS struct {
	Err  int
	Msg  string
	Data map[string]string
}

//RegisterDS 注册接口的请求数据格式
type RegisterDS struct {
	Email string
	Pw    string
}

//Register 注册接口处理函数
func Register(w http.ResponseWriter, r *http.Request) {
	ds := RegisterDS{}
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

	dt, _ := json.Marshal(resp)
	w.Write([]byte(string(dt)))
}
```
注意以下几点：
- 新增了`RespDS`数据结构，包含三个字段，`Err`错误代码，0表示没有错误；`Msg`附加信息说明，成功或者错误的描述；`Data`数据，如果有更多数据需要传送给用户就都放在这里。
- `mailRe,pwRe`这两个正则表达式完全参照了`login.html`里面的内容。
- `resp`是`RespDS`结构，默认是成功的，但如果邮箱格式不对或者密码格式不对都会改变为错误。

运行起来之后，就可以从网页上提交注册请求了，如果格式错误则会被服务器返回信息。
要查看到这个错误信息，可以修改`login.html`中的`$.post`里面接受到服务器数据之后的方法，比如弹出提示：
```
 function sendRegPost() {
        var data = {
            Email: $('#email').val(),
            Pw: $('#pw').val(),
        }

        $.post('/api/register?g=99', JSON.stringify(data), function (res) {
            alert(res.Msg);
        }, 'json')
    }
```

##网页限制提交

网页上虽然我们增加了提示，而且会使用`valid`进行变色，但其实用户还是可以直接提交的错误格式信息的，我们可以对提交按钮加以限制，只有在`mail，pw`格式都正确的情况下才使提交按钮可以点击。

修改`login.html`的部分代码,先写一个用来检测是否可以提交的函数：
```
//检查按钮是否可以被开启
function checkBtn() {
    var agree=$('#agree').is(':checked');
    var mail = $('#email').val();
    var pw = $('#pw').val();
    if (pwRe.test(pw) && mailRe.test(mail) && agree) {
        $('#regBtn').removeAttr('disabled')
    } else {
        $('#regBtn').attr('disabled', 'true')
    }
}
```
注意这里是利用`attr('disabled', 'true')`禁用按钮，利用`removeAttr('disabled')`开启按钮的。
然后把这个`chekBtn`放到每次邮箱或密码改变的时候都执行：
```
function checkMail() {
...
    checkBtn()
}
```
```
function checkPw() {
...
    checkBtn()
}
```

另外注意到我们除了检测邮箱和密码格式之外，我们还检测了是否同意用户协议的按钮`var agree=$('#agree').is(':checked')`，所以我们要修改对应的元素：`<input id='agree' onChange='checkBtn()' type="checkbox" ...>`,给它命名并且改变的时候`onChange`检测是否可以打开提交按钮。

这时候再页面上测试就会发现必须邮箱和密码格式正确并且勾选了同意按钮，提交按钮才能被使用。

![](imgs/4324074-74786c2afdef793c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

下面是三个文件的完整代码供大家参考。
第一个网页login.html：
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
            <h4>注册页面</h4>
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

        $.post('/api/register?g=99', JSON.stringify(data), function (res) {
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
        if (pwRe.test(pw) && mailRe.test(mail) && agree) {
            $('#regBtn').removeAttr('disabled')
        } else {
            $('#regBtn').attr('disabled', 'true')
        }
    }
</script>

</html>
```
第二个Golang的入口文件：
```
package main

import (
	"app/api/login"
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

	//注册登录相关
	http.HandleFunc("/api/register", login.Register)

	//启动服务
	log.Fatal(http.ListenAndServe(":8088", nil))

}
```
第三个Golang处理register请求的文件：
```
package login

import (
	"encoding/json"
	"net/http"
	"regexp"
)

//Resp 返回的数据格式
type RespDS struct {
	Err  int
	Msg  string
	Data map[string]string
}

//RegisterDS 注册接口的请求数据格式
type RegisterDS struct {
	Email string
	Pw    string
}

//Register 注册接口处理函数
func Register(w http.ResponseWriter, r *http.Request) {
	ds := RegisterDS{}
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

	dt, _ := json.Marshal(resp)
	w.Write([]byte(string(dt)))
}
```



>我们初步实现了看上去不错的登录页面，而且能够和Golang服务器软件通信了，但Golang还不能保存用户数据，也还不能对用户邮箱是否真实进行验证，后续我们会继续把它完善起来，制作具有专业水平的网站。




---
欢迎关注我的专栏( つ•̀ω•́)つ[【人工智能通识】](https://www.jianshu.com/c/e9a7b7b7024d)

---
###每个人的智能新时代
如果您发现文章错误，请不吝留言指正；
如果您觉得有用，请点喜欢；
如果您觉得很有用，欢迎转载~
---
END