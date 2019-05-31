欢迎关注我的专栏( つ•̀ω•́)つ[【人工智能通识】](https://www.jianshu.com/c/e9a7b7b7024d)
[【汇总】2019年4月专题](https://www.jianshu.com/p/e1afed853866)

---

Webpack是目前最流行的Web开发模块化管理工具，这是一篇最基础的上手教程，包含了VSCode和Github项目设置。

![](imgs/4324074-3f6ed1e369455f17.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
[人工智能通识-2019年3月专题汇总](https://www.jianshu.com/p/72685b77cfff)


##前提工作

- 首先,你需要安装VSCode(Visual Studio Code)，这可以说是当今最流行的Web开发编码工具，它是开源免费的，由微软进行更新维护。

[点击这里进入微软官方站点下载VSCode](https://code.visualstudio.com/)

![](imgs/4324074-d9e154a6decf2a82.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- 其次，你需要安装Git，然后在Github创建仓库Repository（我创建的是`GoCraft`仓库）,然后在电脑上创建本地项目文件夹（我创建的是同名`GoCraft`文件夹），然后进入这个文件夹`git init`初始化本地Git仓库，然后`git remote add origin https://username:password@github.com/...`关联到远程的Github仓库，创建新文件如`index.html`，测试成功推送到本地Git和远程Github仓库。

[具体完整的操作说明可以参照这个文章](https://www.jianshu.com/p/bf37a3fdf480)

- 最后，你需要安装`node.js`。这是Web开发人员必备工具，它本来是用作后端开发的，但实际上前端的项目组织管理都离不开它，尤其是它包含的`npm`管理命令，稍后我们要一直用到。

[点击这里进入Node.js官方站点下载LTS稳定版安装](https://nodejs.org/en/)

##初始化项目

进入你存放所有网页的文件夹（我的是`GoCraft/cli`)，然后执行`npm init -y`，这个`npm`命令是`node.js`安装包提供的。

这个命令为我们快速设置项目的信息，都写在`package.json`文件中。`-y`是自动设置，如果没有它你就需要输入很多内容或敲很多回车。

![](imgs/4324074-3d857cb6be897264.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

注意这里的`main："index.js"`，表示入口文件是`index.js`，它是所有代码的起始点。

##安装webpack

webpack是用来管理各种web文件之间的关系的，能够有效地把各种js文件组织在一起，是当前最常用的模块化开发管理工具。

![](imgs/4324074-1fcfe522f4649486.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

安装命令：
`npm install webpack --save-dev`
`npm install webpack-cli --save-dev`

这里的`--save-dev`是指把安装信息记录保存到开发环境设置中，建议所有安装都带着这个参数执行。`webpack-cli`是webpack的一个配套命令工具，稍后会用到它。

>如果你安装比较慢，建议你先用管理员权限（苹果电脑下加sudo）安装淘宝的npm镜像：`npm install -g cnpm --registry=https://registry.npm.taobao.org`，然后再用`cnpm`代替`npm`来执行`cnpm install webpack --save-dev`和`cnpm install webpack-cli --save-dev`

##设置Git忽略文件夹

安装webpack的时候会导致Git出现数千个文件更改标记，这是因为在`node_modules`文件夹下产生数千个文件，而这些文件没必要放到Git仓库或者Github仓库中去，所以我们需要及时设置，让Git排除
`node_modules`文件夹。

在整个项目下(`GoCraft`目录而不是`cli`目录）下创建`.gitignore`文件，然后文件内添加要忽略的文件夹，这里只有一行:
```
cli/node_modules/
```
然后保存，退出Code重新启动，这时候就会看到Git需要提交的文件变成了很少的两三个。

##创建index.html和index.js

作为浏览器的入口页面`index.html`是必不可少的，而作为`main`代码的入口页面`index.js`也是必不可少的。实际上网站的运行顺序是：

$浏览器打开index.html \to index.js \to 更多.js模块文件和其他文件$

我们创建`dist/index.html`文件：
```
<!doctype html>
<html>
  <head>
    <title>Getting Started</title>
  </head>
  <body>
    <script src="main.js"></script>
  </body>
</html>
```
在这里我们引入一个还不存在的本地文件`main.js`，稍后它将由webpack根据`index.js`生成。

然后我们创建`src`文件夹下的`src/index.js`：
```
function component() {
    let element = document.createElement('div');
    element.innerHTML = "Hello World!"
    return element;
}
document.body.appendChild(component());
```

然后我们需要修改一下`package.json`文件，添加一行`"private": true,`，去掉`"main": "index.js",`一行，这样将自动生成`main.js`而不会直接使用`index.js`。完整内容变为：
```
{
  "name": "cli",
  "version": "1.0.0",
  "description": "",
  "private": true,
  "scripts": {
    "test": "echo \"Error: no test specified\" && exit 1"
  },
  "keywords": [],
  "author": "",
  "license": "ISC",
  "devDependencies": {
    "webpack": "^4.29.6",
    "webpack-cli": "^3.3.0"
  }
}
```
注意`devDependencies`开发依赖包，这个内容就是我们之前`--save-dev`产生的记录。

##使用第三方包

安装第三方工具，这里我们使用`lodash.js`这个工具进行测试，它提供了一些列常用小功能。
`cnpm install --save lodash`
这个命令将把`lodash`安装到`node_modules`文件夹中待用。`--save`表示记录到生产环境（所以没有带`-dev`)

修改一下`index.js`使用我们的`lodash`：
```
import _ from 'lodash';
function component() {
    let element = document.createElement('div');
    element.innerHTML = _.join(['Hello', 'webpack'], ' ');
    return element;
}
document.body.appendChild(component());
```
注意`import xx from "XXX"`就是从`node_modules`文件夹包含的第三方工具中调用功能，并且将这个功能重命名为`xxx`。所以下面直接使用了` _.join`功能。

然后执行`npx webpack`命令，这个命令将自动分析`src/index.js`，找到里面所有`import`导入的`js`模块文件，以及这些模块文件又可能导入的另外的模块文件，把这所有文件打包成`dist/main.js`,供`index.html`使用。

>如果`npx webpack`命令遇到错误`cannot find module...`，那么可以尝试重新用标准`npm`命令(而不是`cnpm`命令)安装，注意要使用管理员模式或者加sudo开始：
`npm install webpack --save-dev`
`npm install webpack-cli --save-dev`
`npm install --save lodash`

成功后生成的文件结构类似：

![](imgs/4324074-af6786de42668b64.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

如果在浏览器手工打开`index.html`文件查看，将看到`Hello webpack！`字样。

##自定义模块

创建`cli/utils/hello.js`文件，内容如下：
```
export default function hello() {
    alert("I am hello module.")
}
```
然后在`index.js`中导入并使用它：
```
import _ from 'lodash';
import hello from './utils/hello';
function component() {
    let element = document.createElement('div');
    element.innerHTML = _.join(['Hello', 'webpack'], ' ');
    hello()
    return element;
}
document.body.appendChild(component());
```
再次执行`npx webpack`，然后打开`index.html`，正常就可以看到来自自定义模块的弹窗。

##webpack.config.js设置文件

一般情况下webpack不需要额外设置，但可以在用项目根目录下创建`webpack.config.js`文件进行更多设置，例如：
```
const path = require('path');

module.exports = {
  entry: './src/index.js',
  output: {
    filename: 'main.js',
    path: path.resolve(__dirname, 'dist')
  }
};
```
这里，`entry: './src/index.js'`指定了入口`js`文件，而`ouput`指定了`npx webpack`命令输出文件`main.js`的位置。

##npx webpack和npm run build

我们可以通过修改`package.json`，用`npm run build`替换掉`npx webpack`命令(虽然这好像没啥意义)：
```
{
  "name": "cli",
  "version": "1.0.0",
  "description": "",
  "private": true,
  "scripts": {
    "test": "echo \"Error: no test specified\" && exit 1",
    "build": "webpack"
  },
  "keywords": [],
  "author": "",
  "license": "ISC",
  "devDependencies": {
    "webpack": "^4.29.6",
    "webpack-cli": "^3.3.0"
  },
  "dependencies": {
    "lodash": "^4.17.11",
    "resolve-cwd": "^2.0.0",
    "resolve-from": "^4.0.0"
  }
}
```
然后我们运行`npm run build`也能打包生成`dist/main.js`文件。


##最终目录
最终目录结构看起来像这个样子：

![](imgs/4324074-058e7e05fc5c06a2.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

你可以从我的Github项目中访问到完整代码：

[点这里打开webpack-demo代码仓库](https://github.com/zhyuzh3d/webpack-demo)


> 更多扩展内容：关于如何在打包`main.js`的时候支持ES6/7语法，你需要在`webpack.conf.js`安装和配置相应的`loader`工具。关于如何实现保存文件时候自动打包，你需要安装和配置`webpack-dev-server`。具体内容在这里暂时不扩展了。




---
欢迎关注我的专栏( つ•̀ω•́)つ[【人工智能通识】](https://www.jianshu.com/c/e9a7b7b7024d)

---
###每个人的智能新时代
如果您发现文章错误，请不吝留言指正；
如果您觉得有用，请点喜欢；
如果您觉得很有用，欢迎转载~
---
END