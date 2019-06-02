[React+Electron桌面应用开发文章索引](https://www.jianshu.com/p/71c88b21ea48)


继续上一篇[Electron项目快速搭建](https://www.jianshu.com/p/2d1e60d909e9),这篇文章介绍如何使用Reactjs创建页面框架。

---
##安装和配置webpack

请参考上一篇文章进行：
```
cnpm install --save-dev webpack
cnpm install --save-dev webpack-dev-server 
cnpm install --save-dev webpack-cli
```
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
}
```
打开package.json文件，修改其中的script一段,这将让我们使用npm几个新命令
```
"scripts": {
    "electron": "electron .",
    "start": "webpack --config webpack.config.js",
    "dev": "webpack-dev-server",
    "build": "webpack"
  },
```
新建dist文件夹，新增index.html文件，引入了不存在的bundle.js文件。
```
 <!DOCTYPE html>
<html>

<head>
    <meta charset="UTF-8">
    <title>Hello World!</title>
</head>

<body>    
    <h1>Hello Electron!</h1>
</body>

<script type="text/javascript" src="bundle.js"></script>
</html>
```
新建src文件夹，创建index.js文件
```
document.write('<h2>Hello webpack!</h2>')
```
现在目录结构看起来这样(暂时有两个index.html)：
![](imgs/4324074-5fe49fd3d9c7b522.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

---
##测试页面

我们启动webpack的开发服务器dev-server
```
npm run dev
```
>启动之后按ctrl+C关闭(close)。
>如果错误的使用ctrl+Z或其他方式退出，将导致服务器在后台运行而没有关闭，macOS下可以使用```ps -ef|grep node```中找到刚才运行的dev-server一行，注意它前面比较大的数字编号，然后使用```kill -9 XXXXX```关闭它（XXXXX为数字编号）
```

应该能看到成功信息，用浏览器打开http://localhost:9031/可以看到Hello webpack。
我们看到的是dist/index.html的内容。

打开main.js修改electron默认的启动页面路径为我们的开发服务器端口localhost:9000
```js
win.loadURL(url.format({
        //pathname: path.join(__dirname, 'dist/index.html'),
        //protocol: 'file:',
        pathname: ('localhost:9000'),
        protocol: 'http:',
        slashes: true
    }))
```
新开一个命令行终端窗口，运行
```
npm run electron
```
electron窗口启动后显示hello webpack！表示我们已经成功切换到webpack服务器页面。这时候可以删除外面的index.html了。

---
##安装Reactjs

```
cnpm install react --save-dev
cnpm install react react-dom --save-dev
cnpm install react-hyperscript --save-dev
```
>安装hyperscript是为了快速生成reactDom元素，这里不使用费解的jsx文件。

修改index.html文件增加react的入口元素root
 ```
<!DOCTYPE html>
<html>

<head>
    <meta charset="UTF-8">
    <title>Hello World!</title>
</head>

<body>
    <h1>Hello Electron!</h1>
    <div id="root"></div>
</body>

<script type="text/javascript" src="bundle.js"></script>

</html>

```

修改index.js文件
```js
import React from 'react';
import ReactDOM from 'react-dom';
import h from 'react-hyperscript';

document.write('<h2>Hello webpack!</h2>')

ReactDOM.render(h('h1','Hello React!'), document.getElementById('root'));
```
这时候electron窗口应该已经自动更新显示了Hello React！你也可以手动ctrl+R刷新页面（它就是个浏览器，下图中底部显示了开发工具）,到这里就表示React可以正常使用了。
![](imgs/4324074-bf54801855d31fe9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


---
###致力于让一切变得通俗易懂
如果您发现文章错误，请不吝留言指正；
如果您觉得有用，请点喜欢；
如果您觉得很有用，欢迎转载~
---
END












