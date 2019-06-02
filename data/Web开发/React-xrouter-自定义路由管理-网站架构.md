[React+Electron桌面应用开发文章索引](https://www.jianshu.com/p/71c88b21ea48)


这一节我们将继续[上一篇文章Material-UI-React-Electron-项目文件结构](https://www.jianshu.com/p/bd05ff5632ad)来完成一个网站的前端结构。

---
##什么是路由？

1.  ####网站是文件夹和文件

  - 站点是是一个文件夹，包含了多层嵌套的众多文件。

  - 有的文件表示一个页面page，比如index.html表示首页，usercenter.html表示用户中心页面。

  - 有的文件表示页面的某个区块（如导航栏、留言列表等），有的表示更小的单元（如留言列表的一个单元、商品列表的一个单元甚至是一个按钮）。

  - **我们把它们都称之为元素component**。

2. ####网站是互相链接的系统

- **站点是一个错错综复杂相互链接的系统，各个元素之间的跳转切换我们称之为路由**。

- 用户通过点击，可以从一个页面跳转到另一个页面，比如点击进入商品详情页面。

- 用户通过点击，可以把一个区块的内容变为另外不同的内容，比如点击评价按钮，把当前显示的商品参数内容变为用户留言列表。

- 用户可以通过点击，改变一个元素的自身状态或者其他元素的状态，比如留言列表的下一页，单个留言的已读未读切换。

- 如果我们在页面外层嵌套一个盒子，那么对于这个盒子来说，页面也是一个区块。如果我们把页面当做一个对象，它包含的每个区块都对应一个字段，类似```{top:navBar,left:tabList,right:details}```，那么我们也可以把切换区块当做切换页面对象的状态state。

- **我们只要能够通过点击按钮来实现改变元素component的state就可以实现自由的链接跳转**。

- **网站的交互就是切换元素或改变元素的状态**


3. ####比状态更多的问题

- 这里还有两个问题，对于网站来说，用户是通过地址栏来访问的，打开是```http://163.com```，然后到```http://163.com/news/133424.html```这样的地址，每个地址对应不同的html文件。

- 问题1：**我们的跳转如果通过切换component来实现，那么就和地址栏无关，用户都无法收藏我们站点的当前页面，即使收藏了也打不开期望的页面，因为我们的地址栏只有一个```http://localhost:9000```或者正式域名```http://www.mysite.com```**。

- 问题2：对electron的桌面App，似乎不存在地址栏导航的收藏问题，但是第二个问题也无法绕过，那就是我们如何实现页面的个性化和数据恢复？

- 最简单的情况，我们在loginPage元素内实现了用户登录，然后跳转到userCenterPage用户中心页面，我们如何知道用户是谁？这个情况的常规解决方案有几种，比如说地址栏增加参数变为```http://mysite.com/usercenter.html?userid=61731```表示用户id是61731，或者通过服务器向浏览器的cookies内写入一个用户的token标记类似UDS839028390DJSFDSFH893这么一个奇怪的字符对应用户61731。

- 我们切换元素state的方法和地址无关，和cookie也无关。当用户登录进入用中心页面时候我们不知道是谁，不知道该显示谁的内容；当用户管理浏览器再打开的时候我们也不知道他有没有登录，只能让他重新登录。这很糟糕！

- 每个站点的cookie都是保存在浏览器内部的，有很多限制，比如不能存储太多内容，每次访问这些内容都会被发送到服务端，内容多了就造成多余的传输数据。

---
##我们的任务

把上面的分析综合成以下三条任务：

1. #####建立路由机制，实现元素自身的切换和元素状态的切换。
1. #####建立浏览器地址同步机制，使我们的切换能与地址互相配合。
1. #####建立数据恢复机制，使元素重新出现时能够自动恢复之前的状态。

听起来着很复杂，但下面将用三个文件不到200行代码来实现这些功能。
* XStore.js，用来保存数和读取据任意对象
* XSet.js，用来改变任意component元素对象的state状态
* XRouter.js，用来同步元素状态的切换和地址栏的关系

---
##保存与读取数据XStore.js

安装模块：
* deepmerge,它可以把{a:1}和{b:1}合并成为{a:1,b:1}。
```shell
cnpm install deepmerge --save-dev
```
[deepmerge模块官方说明](https://www.npmjs.com/package/deepmerge)

创建一个utilities/XStore.js文件，我们使用浏览器的本地存储localStorage来存储任意数据，[localStorage相关文档说明看这里](http://www.w3school.com.cn/html5/html_5_webstorage.asp)。

下面是XStore.js的代码：
```js
/*
利用本地存储JSON结构的数据，分为单独的targetKey避免整个ls读取压力
获取存储的数据store('key','subkey')；
存储,与原来数据合并store('key',{'subkey':11})；
获取整个对象store('key')；
清理store('key')或store('key',null)；
设空子属性store('key',{'subkey':null})；
*/
import merge from 'deepmerge';
const store = (targetKey, objOrKey) => {
    let lsdata, res
    
    if (!targetKey || targetKey.constructor !== String) {
        console.error('Xstore:store:targetKey must be a string.')
        return res
    }

    if (objOrKey === null) {
        localStorage.removeItem(targetKey) //清理targetKey
        return
    } else if (objOrKey === undefined) {
        lsdata = localStorage.getItem(targetKey)
        res = lsdata ? JSON.parse(lsdata) : undefined //获取targetKey值
        return res
    }

    lsdata = localStorage.getItem(targetKey)
    res = lsdata ? JSON.parse(lsdata) : undefined

    if (objOrKey && objOrKey.constructor === String) {
        res = res ? res[objOrKey] : undefined //获取targetKey.subkey值
    } else {
        res = merge(res || {}, objOrKey || {})
        localStorage.setItem(targetKey, JSON.stringify(res)) //合并存储targetKey值
    };
    return res
}

const XStore = {
    store,
}
export default XStore
```

这30行代码借助LocalStorage.setItem和getItem实现了如何存储一个对象、如何读取一个对象以及对子属性的操作（请仔细阅读注释掉的说明文字）。

---
##改变任意元素的状态XSet.js

React的元素component中，```this.setState(object)```方法可以改变自身的```this.state```中的数据。

但是React并不支持我们去胡乱的修改任意元素的state数据，但这里我们不管这些，我们希望能获取到任意的component元素并执行```component.setState(obj)```。这样我们就可以把需要动态更换的页面放在App元素的state.currentPageName里面，只要用```App.setState({currentPageName:'HomePage'})```，改变这个数据就能实现换页了。

我们的思路是：
1. 对于需要被切换状态组件，当它加载到页面的时候，把它添加到我们的components列表中
1. 同样当它要从页面上移除的时候，再把它从我们的components列表中移除
1. 这样，我们就可以任何时候从components列表中获取某个元素，进而使用它的setState()方法

这对应了三个方法：
1. use(),将它加入到管理列表
1. free(),将它从管理列表移除
1. set(),执行它的setState方法

下面是utilities/XSet.js文件的代码:
```
import {
    Component
} from 'react'

/*
接管全部components实例
每个实例对应一个XSetId，这里不考虑同一类的多个重复实例
重复的实例应该利用props.XSetId进行区别处理
*/
let components = {}

/*
初始化一个元素,components[key]=component
应该在componentWillUnmount方法中调用
必须经过初始化才能使用xset
key注册键名，默认使用key->XSetId->元素类名
return 实际使用的key或失败undefined
*/
const use = (component, key) => {
    if (!(component instanceof Component)) {
        console.error('Xset:init:componet format err.')
        return
    }

    key = key ? key : (component.props.XSetId ? component.props.XSetId : component.constructor.name)

    if (key.constructor !== String) {
        console.error('Xset:init:key must be a string.')
        return
    }

    components[key] = component
    return key
}

/*
释放一个元素，从components中移除,不再接收xset
应该在componentWillUnmount中调用
如果是元素，删除对应的key
如果是key，删除key
return true或失败undefined
*/
const free = (componentOrKey, index = -1) => {
    if (!componentOrKey) {
        console.error('Xset:free:componentOrKey can not be undefined.')
        return
    }
    if (componentOrKey instanceof Component) {
        for (let key in components) {
            if (components[key] == componentOrKey) {
                delete components[key]
            }
        }
    } else if (componentOrKey.constructor == String) {
        delete components[componentOrKey]
    } else {
        console.error('Xset:free:componentOrKey must be a component or a string.')
        return
    }

    return true
}

/*
根据key跨元素setState
执行components[key].setState(state)
return true或失败undefined
*/
const set = (key, state) => {
    if (!key || key.constructor != String) {
        console.error('Xset:xset:key must be a string:' + key + '.')
        return
    }

    if (!components[key] || !(components[key] instanceof Component)) {
        console.warn('Xset:xset:component does not exist on ' + key + '.')
        return
    }

    components[key].setState(state)
    return true
}

const XSet = {
    use,
    free,
    set,
    getComponents: () => {
        return components
    }
}
export default XSet
```

---
##实现路由跳转功能XRouter.js

通常情况下，都是页面之间的跳转，比如从home.html跳转到usercenter.html;用户收藏的也是页面比如.../usercenter.html，也或者收藏某个页面的特定内容比如.../news.html?articleId=87822这样的链接。

由于我们实际上只有一个对外公开的html页面，也就是index.html，所以我们只能在？参数上面做文章。比如我们可以约定...?pageName=userCenter表示我们需要切换App的currentPageName到userCenter状态，展示用户中心页面内容。

但.?pageName=newsPage还不够，我们需要后面的articleId=87822，或者需要更多的数据跟在后面。我们把所有跟在后面的数据打包，统一放在pageState={articleId:87822,...}里面,虽然地址栏看起来比较长但毕竟有效（比如```...?pageName=newsPage&pageState={articleId:87822,...}```）。

首先我们安装两个模块：
```
cnpm install history --save-dev
cnpm install urlparser --save-dev

```
[history模块用于管理地址栏前进后退历史，官方说明](https://www.npmjs.com/package/history)
[urlparser模块用于从地址栏中解析出数据对象，官方说明](https://www.npmjs.com/package/urlparser)

我们的思路是：
* 监听地址栏变化，只要它一改变，我们就从地址栏中分析得到pageName和对应的pageState，然后去XSet设置App.setState(obj)方法去改变currentPageName和其他state数据
* 点击按钮时候把要切换到的新页面名称指定到地址栏pageName，把要设置的状态数据指定到pageState
* 就这么简单！

下面是utilities/XRouter.js文件的代码:
```
/*
利用xset和xstore实现路由
*/
import createHistory from 'history/createBrowserHistory'
import deepmerge from 'deepmerge'
import urlParser from 'urlparser'

import XStore from './XStore'
import XSet from './XSet'

/*
监听所有动作地址栏动作，根据地址里面的XSetPath变量跳转页面
依赖于App元素的state.currentPageName
当history被push的时候就会被激活
*/
let history = createHistory({
    basename: '',
})
history.listen((location, action, state) => {
    let urlObj = urlParser.parse(window.location.href)
    let pageName = urlObj.query ? urlObj.query.params['XSetPageName'] : undefined
    let urlState = urlObj.query ? urlObj.query.params['XSetPageState'] : undefined
    urlState = JSON.parse(decodeURIComponent(urlState))
    let appState = deepmerge({
        currentPageName: pageName
    }, urlState)
    XSet.set('App', appState)
})

/*
正式的切换元素的函数。
history.push推入历史，被上面的函数监听到激活上面的监听
如果pageName为空，那么尝试从地址栏中取得pageName和urlState
*/
const changePage = (pageName, urlState) => {
    let urlObj = urlParser.parse(window.location.href)
    if (!pageName) {
        pageName = urlObj.query ? urlObj.query.params['XSetPageName'] : undefined
        let urlStateStr = urlObj.query ? urlObj.query.params['XSetPageState'] : undefined
        urlStateStr = decodeURIComponent(urlStateStr)
        if (urlStateStr != 'undefined') {
            urlState = JSON.parse(urlStateStr)
        }
    }

    if (pageName) {
        let stateStr = encodeURIComponent(JSON.stringify(urlState || {}))
        history.push('?XSetPageName=' + pageName + '&XSetPageState=' + stateStr)
    }
}

const XRouter = {
    changePage,
    prevPage: history.goBack,
    nextPage: history.goForward,
    use: XSet.use,
    free: XSet.free,
    getComponents: XSet.getComponents,
    store: XStore.store,

}
export default XRouter
```
---
##把路由引入到App.js

从上面的代码已经看到，XRouter.js实际上已经把XSet和XRestore都整合在一起了。所以我们只要引入它就可以了。

下面是引入Xrouter.js后的App.js，注意这里，我们用global.XRouter把它全局化了，好处就是在App之后任何其他文件中都能自由使用它。



```
import React from 'react'
import {
    Component
} from 'react'
import h from 'react-hyperscript'
import {
    MuiThemeProvider,
    withStyles
} from 'material-ui/styles'
import PropTypes from 'prop-types'

import Grid from 'material-ui/Grid'
import Button from 'material-ui/Button'

import Pages from './_pages'
import Style from './_style'
import Theme from './_theme'
import Config from './_config'

import XRouter from '../Utilities/XRouter'

global.XRouter = XRouter //输出到全局

class App extends Component {
    constructor(props) {
        super(props)
        this.state = {
            currentPageName: 'WelcomePage',
            randNumber: Math.random(),
        }
    }

    componentDidMount() {
        global.XRouter.use(this)
        global.XRouter.changePage()
    }

    componentWillUnmount() {
        global.XRouter.free(this)
    }

    render() {
        let that = this
        const css = this.props.classes

        return h(MuiThemeProvider, {
            theme: Theme,
        }, h(Grid, {
            container: false,
            className: css.app,
        }, [
            h(Pages[this.state.currentPageName]),
            h('h5', this.state.randNumber)
        ]))
    }
}

App.propTypes = {
    classes: PropTypes.object.isRequired,
}
export default withStyles(Style)(App)
```
>同时注意componentDidMount元素加载和componentWillUnmount元素卸载两个函数中的内容，我们使用use注册这个App元素，使用free卸载它， global.XRouter.changePage()自动根据当前的地址栏切换不同的页面及状态。


---
##测试我们的路由

先看一下文件结构：

![](imgs/4324074-815ca7b68615f5f0.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

首先我们注意一下src/App/_pages.js，如上面的代码，它被App.js引入了，并且在底部代码使用了```h(Pages[this.state.currentPageName])```，下面是_pages.js的代码：
```
import WelcomePage from '../Pages/WelcomePage/WelcomePage'
import HomePage from '../Pages/HomePage/HomePage'

const Pages = {
    WelcomePage,
    HomePage,
}
export default Pages
```
实际上，它应该包含可能被App切换的所有页面，这里只引入了WelcomePage和HomePage两个页面做示范。

我们再看src/Pages下面的这两个页面文件，下面是WelcomePage.js
```
import {
    Component
} from 'react'
import h from 'react-hyperscript'

import Button from 'material-ui/Button';

class Page extends Component {
    constructor(props) {
        super(props)
        this.state = {
            title: 'WelcomePage',
        }
    }

    render() {
        return h('div', [
            h('h1', this.state.title),
            h(Button, {
                color: 'primary',
                variant: 'raised',
                onClick: () => {
                    global.XRouter.changePage('HomePage', {
                        randNumber:Math.random(),
                    })
                },
            }, 'go home')
        ])
    }
}

Page.constructor = (props) => {
    Page.constructor(props)

}
export default Page
```
上面的render()方法包含了一个按钮和一个div，onClick函数使用了XRouter的changePage切换页面，并附上了{randNumber:Math.random()}一个新的随机数，这个randNumber和App.js中的state里的randomNumber是同一个，它将改变App.state.randomNumber数值。

同样的，下面是HomePage.js的代码:
```
import {
    Component
} from 'react'
import h from 'react-hyperscript'

import Button from 'material-ui/Button';

class Page extends Component {
    constructor(props) {
        super(props)
        this.state = {
            title: 'HomePage',
        }
    }

    render() {
        return h('div', [
            h('h1', this.state.title),
            h(Button, {
                color: 'primary',
                variant: 'raised',
                onClick: () => {
                    global.XRouter.changePage('WelcomePage', {
                        randNumber:Math.random(),
                    })
                },
            }, 'go welcome')
        ])
    }
}

Page.constructor = (props) => {
    Page.constructor(props)

}
export default Page

```
这些都完成后，我们看下效果,最初是这个样子的，注意地址栏：
![](imgs/4324074-bb937d8b76085db7.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

点击GO HOME按钮后是这样的，正确的跳转到HomePage页面,同样注意常常的地址栏:
![](imgs/4324074-78cdc0fadcaa975c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

点击GO WELCOME按钮回到WelcomPage，注意地址栏的变化：
![](imgs/4324074-6fb4dab75acdebf9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

再点击GO HOME按钮，又回到Home页面，但下面的随机小数变了，地址栏也变动了：
![](imgs/4324074-6af8d4665ac79808.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

关键的事情来了！收藏这个页面，关掉再打开，注意，它能正常显示HomePage，并且**那个随机数字并没有变**！因为这个数字是保存在地址栏那长串数字里面的。

在这个例子中，我们把App.state.randNumber保存在地址栏中并自动恢复它。是的，我们实际并没有用到XSet。XSet是个更加强大的工具，它不仅适用于页面，也适用于任何区块、单元、元件等任意元素。你可以在任意元素componentWillUnmount卸载的时候将它的任意state保存下来，然后在componentDidMount元素显示的时候再把保存的state数据取出来，用setState更新，**这可以让页面晚期恢复到用户上次离开时候的样子**。

---
##结语

最近连续的几篇文章是基于一个小测试项目进行的。[GitHub项目地址](https://github.com/zhyuzh3d/dataMagic)，你可以下载这个项目到本地，然后从命令行进入目录执行```cnpm install```安装全部需要的模块。但我推荐你根据这些教程从头一点点了解它的搭建过程和思路。

---
###致力于让一切变得通俗易懂
如果您发现文章错误，请不吝留言指正；
如果您觉得有用，请点喜欢；
如果您觉得很有用，欢迎转载~
---
END



