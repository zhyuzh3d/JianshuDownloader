[React+Electron桌面应用开发文章索引](https://www.jianshu.com/p/71c88b21ea48)


这一篇主要介绍如何快速搭建electron项目，开发属于自己的MacOS应用软件。是的，开发软件，只要你会基本的nodejs就可以。

![](imgs/4324074-c00a4da7d664c1e2.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

这里使用的是Brackets开发工具和git项目管理，以MacOS为主，windows用户也可以参考。

[brackets官网](http://brackets.io/)
[git官网](https://git-scm.com/)

---
## 创建项目
1. 在[github](https://github.com)创建新的仓库myproject，使用自动Readme初始化。
1. 在本机创建文件夹myproject。
1. 在brackets打开本机文件夹myproject，用brackets git插件，clone克隆github项目。
1. 任意修改一下readme.md文件(可以使用markdown插件实时预览)并保存，勾选modified项目，然后先commit提交到本地，然后再点push按钮提交到github，测试是否顺利。
1. 新建.gitignore文件，添加两行```node_modules```和```out```。让git不管理这两个文件夹。
1. 可选：为brackets安装Exclude Folders插件，隐藏接下来将要使用的node_modles文件夹。

---
## 下载安装Nodejs
1. 从[nodejs官网](https://nodejs.org/en/)下载稳定版Recommended安装包，安装。
1. 从brackets文件列表open terminal here打开终端，执行```node -v```回车，正常显示安装的nodejs版本，同样```npm -v```显示npm版本。
1. 添加npm国内资源镜像（淘宝提供）,终端运行命令```npm install -g cnpm --registry=https://registry.npm.taobao.org```,之后可以用cnpm命令代替npm，提高第三方模块的安装速度。


---
## 安装Electron
参照[官方说明](https://github.com/electron/electron)安装。

1. 执行终端命令```cnpm install electron --save-dev```安装electron，这将自动创建node_modules文件夹（brackets列表内已经隐藏），并下载很多很多文件到这里。
1. 修改package.json，增加start命令指向electron，设定入口为main.js，参照下面代码需要修改的部分代码
```
"main": "main.js",
  "scripts": {
    "start": "electron ."
  },
```

---
## 创建最简Electron项目

1. 创建main.js文件，添加下面的代码。 
1. 创建index.html文件，添加下面的代码。
1. 终端运行命令```npm start```,这时会弹出一个应用窗口（本质是一个浏览器），显示了hello electron文字（来自index.html页面）。

main.js
```
const {
    app,
    BrowserWindow
} = require('electron')
const path = require('path')
const url = require('url')

function createWindow() {
    //创建浏览器窗口
    win = new BrowserWindow({
        width: 800,
        height: 600
    })

    //让浏览器加载index.html
    win.loadURL(url.format({
        pathname: path.join(__dirname, 'index.html'),
        protocol: 'file:',
        slashes: true
    }))
}

//执行
app.on('ready', createWindow)
```

index.html
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

</html>

```

---
## 打包发布MacOS应用

1. 复制node_modules文件夹下electron/dist/Electron.app到项目下out文件夹里面。（之所以用out是上面再.gitignore里面我们让git忽略了这个文件夹）
1. 右键Electron.app显示包内容，进入到contents/Resources文件夹，新建一个app文件夹，这里就是放置所有页面的地方。
1. 把项目里面的package.json,main.js,index.html文件拷贝到app文件夹。
1. 然后你可以把Electron.app重命名任意名字，拷贝到任意地方，运行起来都是我们上面编写的效果。
1. 你可以从网上下载icns苹果系统专用的图标文件，覆盖Electron.app报内容里面contents/Resources内的electron.icns，然后Electron.app被复制到其他地方时候图标就会改变。

![](imgs/4324074-c00a4da7d664c1e2.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

[从easyicon下载icns图标](http://www.easyicon.net/)
[在线把png图片转为icns图标](http://www.easyicon.net/covert/)
[更加复杂的专业打包方法看这里](https://electronjs.org/docs/tutorial/application-distribution)
[推荐使用electron-forge打包工具](https://github.com/electron-userland/electron-forge)
[Windows下直接用nodejs改变exe文件图标最快速方法rcedit](https://www.npmjs.com/package/rcedit)

---
## 完善main.js

请把Electron.app当做一个Chrome浏览器看待。它同样可以打开多个窗口（不仅是标签页），也可以打开chrome的开发者工具。
阅读下面新的main.js代码，了解基本结构。

[阅读官方中文文档，了解更多内容](https://electronjs.org/docs)

```
const {
    app,
    BrowserWindow
} = require('electron')
const path = require('path')
const url = require('url')

// 保持一个对于 window 对象的全局引用，如果你不这样做，
// 当 JavaScript 对象被垃圾回收， window 会被自动地关闭
let win

function createWindow() {
    // 创建浏览器窗口。
    win = new BrowserWindow({
        width: 800,
        height: 600
    })

    // 然后加载应用的 index.html。
    win.loadURL(url.format({
        pathname: path.join(__dirname, 'index.html'),
        protocol: 'file:',
        slashes: true
    }))

    // 打开开发者工具。
    win.webContents.openDevTools()

    // 当 window 被关闭，这个事件会被触发。
    win.on('closed', () => {
        // 取消引用 window 对象，如果你的应用支持多窗口的话，
        // 通常会把多个 window 对象存放在一个数组里面，
        // 与此同时，你应该删除相应的元素。
        win = null
    })
}

// Electron 会在初始化后并准备
// 创建浏览器窗口时，调用这个函数。
// 部分 API 在 ready 事件触发后才能使用。
app.on('ready', createWindow)

// 当全部窗口关闭时退出。
app.on('window-all-closed', () => {
    // 在 macOS 上，除非用户用 Cmd + Q 确定地退出，
    // 否则绝大部分应用及其菜单栏会保持激活。
    if (process.platform !== 'darwin') {
        app.quit()
    }
})

app.on('activate', () => {
    // 在macOS上，当单击dock图标并且没有其他窗口打开时，
    // 通常在应用程序中重新创建一个窗口。
    if (win === null) {
        createWindow()
    }
})

// 在这个文件中，你可以续写应用剩下主进程代码。
// 也可以拆分成几个文件，然后用 require 导入。

```

---
###致力于让一切变得通俗易懂
如果您发现文章错误，请不吝留言指正；
如果您觉得有用，请点喜欢；
如果您觉得很有用，感谢转发~
---
END
