网站开发尤其是前端页面站点开发，nodejs语言已经是必选，为了适应JavaScript的最新语法ES6/7标准，提升开发速度，一大堆辅助工具应运而生，而webpack可能是最佳选择。因为绝对多数情况，有它，就够了。

这篇文章将以最快的速度带领web开发新手进入标准开发流程。
以后有时间会慢慢整理Angular、Vue和React相关内容。

---
####准备工作
######安装nodejs
进入[nodejs官网](https://nodejs.org/en/)直接点击Download大按钮,下LTS稳定版。

######选一个开发工具
推荐[Brackets](http://brackets.io/),点进去直接下载安装。免费，支持win/mac。

---
####安装webpack
首先我们在桌面上建一个文件夹myweb作为项目,我们的网站文件都将放在这里。

启动系统命令行工具（windows下管理员权限运行命令提示符工具;mac下启动终端)，用cd命令进入桌面这个文件夹（下同，不再区分win/mac，必要时尝试mac终端命令前面加sudo）：
windows:
```shell
cd desktop/myweb/
```
然后用下面的命令把项目初始化一下，它会询问诸如项目名称、版本、作者之类信息，不用管，一路回车就好。最后在myweb生成一个package.json文件，它包含了所有nodejs需要的设置。
```
npm init
```
>npm是nodejs的第三方包（插件）管理工具，如果在下面使用的时候很慢，你可以参考[淘宝npm镜像](https://npm.taobao.org/)的使用说明部分，然后使用cnpm命令替换下面的npm命令

使用下面的命令安装webpack,install是安装，--save-dev是把插件名webpack记录到package.json文件中，只影响dev开发环境。可能需要一会时间，成功后可以看到myweb下面多了一个node_modules文件夹，以后所有的插件npm都会装在这里,同时package.json里面也多了webpack一行
```
npm install --save-dev webpack
```
---
####安装开发服务器dev-server
为了能够使用ES6/7新语法，又能够在老浏览器运行我们的代码，webpack可以把我们的新语法代码“编译”成老语法来运行。dev-server就是实时全自动化的编译工具。
```
npm install --save-dev webpack-dev-server 
npm install --save-dev webpack-cli
```
安装成功后，也会在node_modules里面多出文件，在package.json里面多出一行。

---
####设置参数
在myweb目录下创建webpack.config.js文件，内容如下：
```
const path = require('path');
module.exports = {
    entry: './src/index.js', //入口文件
    output: {
        filename: 'bundle.js', //编译后的文件
        path: path.resolve(__dirname, 'dist')
    },
    mode: 'development',
    devServer: {
        contentBase: path.join(__dirname, "dist"), //编译好的文件放在这里
        compress: true,
        port: 9000 //本地开发服务器端口
    }
};
```
然后打开package.json文件，修改其中的script一段,这将让我们使用npm几个新命令（小心标点，详细语法请百度json）:
```
    "scripts": {
        "start": "webpack --config webpack.config.js",
        "dev": "webpack-dev-server",
        "build": "webpack"
    },
```
---
####创建文件
创建myweb/dist/index.html文件，内容如下,注意引入了不存在的bundle.js文件:
```
<!doctype html>
<html>
<head>
    <title>myweb</title>
</head>
<body>
    <script src="bundle.js"></script>
</body>
</html>
```
创建myweb/src/index.js文件，内容如下，注意前面webpackage.json.js中的entry入口设置的就是它:
```
import $ from 'jquery';
$('body').append('Hello webpack!');
```
这时候我们的目录结构看起来像是（这里没显示node_modules文件夹）：
![](imgs/4324074-921c01f44c749e6c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

---
####安装缺失的插件库
上面的js里面我们使用了jquery插件，但我们并没有在html中使用<script ..../>标签引入它，而是js中使用了```import xxx from 'xxxx'```这么高级的语法，但是，没有终归是不行的，我们来安装它:
```
npm install --save-dev jquery
```
>更多插件请访问[NPM官方网站](https://www.npmjs.com/),除了你可能熟悉jqeury、bootstrap，那里近50万的插件供你install.
---
####启动实时服务器dev-server
一切就绪，我们执行下面的命令启动服务器:
```
npm run dev
```
>注意这里的dev，就是package.json中我们设置的```"dev": "webpack-dev-server"```,下面我们还会用到```"build": "webpack"```

如果没有出错，那么就成功了！注意其中的```http://localhost:9000/```这一行，复制它粘贴到浏览器里面就能打开我们的网页了，虽然只有一行Hello webpack！

![](imgs/4324074-f4ee07918550e3f6.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
>重新启动dev-server之前你必须先关闭它！关闭方法是按两次ctrl+c。如果端口9000不被释放就会出错```listen EADDRINUSE 127.0.0.1:9000```，如果出错我暂时建议你重启电脑...或者自行百度如何杀死进程。
---
####修改页面
打开index.html，把里面的Hello webpack！改为其他字符串，然后保存。

你会发现，浏览器内的页面自动刷新了！完全不需要手动去点任何按钮。这就是dev-server最美的地方。

---
####编译项目文件
刚才打开localhost显示的是本地页面，注意index.html页面中引用的bundle.js仍然不存在（实际上它只存在于dev-server的内存里面）。
没有bundle.js我们的index.html放到远程服务器上一定会出错找不到js文件。

运行下面的命令生成bundle.js文件
```
npm run build
```
成功之后就会看到dist/bundle.js了，你可以把dist文件夹都放到远程服务器上面，就能正常访问了。

---
CONGRATULATIONS！你已经迈出了Web开发的第一步！
END
