欢迎关注我的专栏( つ•̀ω•́)つ[【人工智能通识】](https://www.jianshu.com/c/e9a7b7b7024d)
[【汇总】2019年4月专题](https://www.jianshu.com/p/e1afed853866)

---

这篇文章介绍如何使用VSCode快速初始化一个基于React.js的Web项目，React.js是当前最主流的Web开发框架之一,另一个是Vue.js。

![](imgs/4324074-c0453634d39af7ca.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

##前提工作

首先我们需要安装(或确认已安装)：
- VSCode
- Git
- Nodejs

然后我们需要：
- 创建项目文件夹（GoCraft）；
- 初始化本地Git仓库`git init`；
- 在Github网站创建对应的无初始化的仓库(GoCraft)；
- 设置Github远程仓库`git remote add ...`；
- 创建`cli`文件夹，进入并初始化`npm init`
- 创建`.gitignore`文件忽略掉`cli/node_modules`文件夹；

以上步骤可以[参考这个文章](https://www.jianshu.com/p/65c5c3c22b88)的前半段内容完成。

##创建index文件

我们创建两个文件`cli/dist/index.html`和``cli/src/index.js`内容分别如下：
```
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta name="theme-color" content="#000000">
    <title>React-MD-Aframe</title>
    <script src="main.js"></script>
  </head>
  <body>
    <h1>Hello World!!</h1>
    <div id="root"></div>
  </body>
</html>
```
```
(function () {
    console.log("Hello!");
}());
```

##安装和配置Webpack

使用下面的命令安装(管理员或sudo)：
`npm install --save-dev webpack webpack-cli webpack-dev-server`
可能会要几分钟，也可能会出现一些错误，但只要最后正常完成即可：

![](imgs/4324074-545c90c7d4e57ede.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

为我们的`package.json`增加两个脚本命令(注意行尾的逗号)：
```
  "scripts": {
    "test": "echo \"Error: no test specified\" && exit 1",
    "start": "webpack --config webpack.config.js",
    "build": "webpack",
    "dev": "webpack-dev-server --open --hot"
  },
```

创建`cli/webpack.config.js`:
```
const path = require('path');
module.exports = {
    entry: path.join(__dirname, "src/index.js"), //入口文件
    output: {
        filename: 'main.js', //编译后的文件
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

然后我们执行`npm run build`可以生成文件，执行`npm run dev`可以启动开发服，这会自动打开页面`http://localhost:9000/`显示`Hello world!`文字。

>注意，要停止`dev`服务，可以按Ctrl+C快捷键。建议新开单独的命令行终端来执行别的命令，而不必每次都停止它。

打开页面的控制台`Console`，这时候我们在VSCode里面修改`src/index.js`文件，例如改为`console.log("Hello world!!");`，浏览器页面控制台内将自动刷新输出新的内容。


##使用Webpack的Html插件

如果我们修改`dist/index.html`文件，页面不会自动刷新。而且直接把`index.html`这个源码文件放在`dist`下面也并不合适。

安装`html-webpack-plugin`插件(管理员或sudo)：
`npm install --save-dev html-webpack-plugin`

然后我们修改`webpack.config.js`文件内容，开头增加`HtmlWebpackPlugin`并结尾增加`plugin`内容：
```
const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');
module.exports = {
    entry: path.join(__dirname, "src/index.js"), //入口文件
    output: {
        filename: 'main.js', //编译后的文件
        path: path.resolve(__dirname, 'dist')
    },
    mode: 'development',
    devServer: {
        contentBase: path.join(__dirname, "dist"), //编译好的文件放在这里
        compress: true,
        port: 9000 //本地开发服务器端口
    },
    plugins: [
        new HtmlWebpackPlugin({
            template: path.join(__dirname, 'src', 'index.html')
        })
    ]
}
```
然后我们把`dist/index.html`移动到`src/index.html`，并把里面的`<script type="text/javascript" src="main.js"></script>`删除，因为我们的插件会自动补充这个内容。

重启`npm run dev`服务。修改`src/index.html`内容，页面将自动刷新变化。

##安装React

使用下面命令安装：
`sudo npm install --save react react-dom`

修改`src/index.js`：
```
import React from "react";
import ReactDOM from "react-dom";

let HelloWorld = () => {
  return <h1>Hello React!</h1>
}

ReactDOM.render(
  <HelloWorld/>,
  document.getElementById("root")
);
```
保存时候浏览器控制台会出错，这是由于webpack还不知道怎么处理React这种html标记和js语句混用的情况。

##安装和配置Babel

Babel可以告诉webpack该如何做。使用下面的语句安装：
`sudo npm install --save-dev @babel/core @babel/node @babel/preset-env @babel/preset-react babel-loader`

在项目目录下创建`cli/.babelrc`文件，内容：
```
{
    "presets": [
        "@babel/env",
        "@babel/react"
    ]
}
```
然后再`webpack.config.js`中添加新的`module.rules`内容，指定`.js`格式文件都由`babel-loader`来处理，而且不处理`node_modules`文件夹内容：
```
    module: {
        rules: [{
            test: /\.m?js$/,
            exclude: /(node_modules|bower_components)/,
            use: 'babel-loader',
        }]
    },
    plugins: [
        new HtmlWebpackPlugin({
    ...
```
然后重新启动`npm run dev`，可以看到能够正常编译，出现`Hello Reac!`文字。

##CSS载入器

安装特殊的css文件处理器：
`sudo npm install --save-dev style-loader css-loader sass-loader node-sass`

创建一个`src/index.scss`文件：
```
body {
  div#root{
    background-color: #222;
    color: #8EE4AF;
  }
}
```
在`src/index.js`中导入它，开头增加一行：
```
import "index.scss";
```
这时候页面控制台编译失败。我们修改`webpack.config.js`,增加样式的载入器内容：
```
    module: {
        rules: [{
                test: /\.(js|jsx)$/,
                exclude: /node_modules/,
                use: ['babel-loader']
            },
            {
                test: /\.(css|scss)$/,
                use: [
                    "style-loader",
                    "css-loader",
                    "sass-loader"
                ]
            }
        ]
    },
```
重新启动`npm run dev`，可以看到`Hello React!`背景变黑色，文字变绿色。

##文件载入器

用下面命令安装：
`npm install --save-dev file-loader @babel/plugin-proposal-class-properties`

修改`webpack.config.js`，增加文件载入器内容：
```
    module: {
        rules: [{
                test: /\.(js|jsx)$/,
                exclude: /node_modules/,
                use: ['babel-loader']
            },
            {
                test: /\.(css|scss)$/,
                use: [
                    "style-loader",
                    "css-loader",
                    "sass-loader"
                ]
            },
            {
                test: /\.(jpg|jpeg|png|gif|mp3|svg)$/,
                loaders: ['file-loader']
            }
        ]
    },
```
然后将`.babelrc`文件修改为：
```
{
  "presets": [
    "@babel/env",
    "@babel/react"
  ],
  "plugins": [
    "@babel/plugin-proposal-class-properties"
  ]
}
```

>到这里为止，可以作为基本的React+webpack项目初始化使用。你可以在Github上获取以上代码：[react-webpack-base](https://github.com/zhyuzh3d/react-webpack-base)

##Material Design

安装核心元件及可选元件（下面只包含了SVG图标）：
`npm install @material-ui/core  --save-dev`
`npm install @material-ui/icons  --save-dev`

安装好了之后就可以在页面上直接在`index.js`中导入并使用：
```
import React from "react";
import ReactDOM from "react-dom";
import Button from '@material-ui/core/Button';

import "index.scss";

let HelloWorld = () => {
  return <h1>Hello React!!</h1>
}

let HelloBtn=()=>{
  return <Button variant="contained" color="secondary">Hello,MaterialDesign!</Button>
}

ReactDOM.render(
  <div><HelloWorld/><HelloBtn/></div>,
  document.getElementById("root")
);
```
产生如下的效果：
![image.png](imgs/4324074-b8007a7d6e7ac242.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

[关于更多Material-UI的内容可以参考这里](https://material-ui.com/getting-started/usage/)。

[更多关于Material-UI和React的技术可以参考这个文章](https://www.jianshu.com/p/71c88b21ea48)

[关于更多官方Material-Design的设计可以参考这里](https://material.io/)。


##react-hyperscript

尽管React官方更加支持html和js混用的jsx格式，但是我很讨厌它。推荐大家可以结合react-hyperscript来实现完全js的界面编写。

安装命令：
`npm install react-hyperscript  --save-dev`

直接在`index.js`中使用：
```javaScript
import React from "react";
import ReactDOM from "react-dom";
import Button from '@material-ui/core/Button';
import h from "react-hyperscript"

import "index.scss";

let HelloWorld = () => {
  return h('h1', 'Hello React')
}

let HelloBtn = () => {
  return h(Button, {
    variant: 'contained',
    color: 'primary',
  }, 'Hello,MaterialDesign!')
}

ReactDOM.render(
  h('div', [
    h(HelloWorld),
    h(HelloBtn)
  ]),
  document.getElementById("root")
);
```
这样的代码虽然看起来多了几行，但更加清楚整齐，而且自动格式化之后也不会出错。

##Aframe

最简单的接入方法是直接安装导入使用：
`npm install aframe --save-dev`

在`index.js`改为：
```
import React from "react";
import ReactDOM from "react-dom";
import h from "react-hyperscript"
import 'aframe';

import "index.scss";

let Box=()=>{
  return h('a-box',{color:'red',position:'0 0 -4'})
}

ReactDOM.render(
  h('a-scene',{background:'color:#CCC'},[
    h(Box)
  ]),
  document.getElementById("root")
);
```
这个方法问题也很多，只能用于组装场景，而不能检测场景内物体的事件，所以主要还是得使用aframe自身的编程规范。

[最终代码可以参考Github的项目这里](https://github.com/zhyuzh3d/GoCraft)

关于如何检测aframe元素的点击事件，稍后我们继续学习。


---
欢迎关注我的专栏( つ•̀ω•́)つ[【人工智能通识】](https://www.jianshu.com/c/e9a7b7b7024d)

---
###每个人的智能新时代
如果您发现文章错误，请不吝留言指正；
如果您觉得有用，请点喜欢；
如果您觉得很有用，欢迎转载~
---
END