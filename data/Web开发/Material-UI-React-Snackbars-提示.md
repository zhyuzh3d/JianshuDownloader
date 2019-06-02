[React+Electron桌面应用开发文章索引](https://www.jianshu.com/p/71c88b21ea48)

这篇文章继续之前的文章。比起弹窗，底部弹出的小提示更加频繁，这次我们介绍如何创建小提示Snackbar。

![](imgs/4324074-04f51e4f404befb5.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

[MaterialUI官方给出了Snackbar实现案例](https://material-ui-next.com/demos/snackbars/)，也很繁琐，小提示本质上也是全局性的，但与弹窗略有区别的是，小提示可以同时出现多个。

这次我们还是想办法把它统一化。

---
##思路分析

snackbar的功能特征：

* 和弹窗一样，包含内容区（纯文字，或文字+按钮）和一个关闭按钮

* snackbar并不打断用户操作，大多时候会几秒后自动消失

* 所以可能有多个snackbar同时出现

* snackbar看上去也是全局性的功能，但实际应该是多个元素

* 在任意页面都可以创建snackbar

* snackbar都应该放在App的某个容器里面统一接管,添加或移除

* 我们需要一个快速创建snackbar的全局功能global.$addSnackbar(state)
---
##编写代码

创建Utitlies/MySnackbar.js。

实现思路是：
* 创建一个snackbars局部变量，用来存放所有实例，这样就可以跨越执行实例.setState({open:false})方法关闭snackbar。（参考xset的实现思路）

* 实现全局化的global.$closeMySnackBar通过id关闭特定snackbar方法

* 创建一个MySnackbar类，constructor构建函数里面把每个实例通过id添加到snackbars，以后就能使用snackbars[id]来获取

* MySnackbar类中render()通过style实现了snackbar的堆叠效果，通过覆盖onClose关闭方法实现autoHideDuration倒计时结束自动关闭

* MySnackbars类是所有snackbar界面dom的容器，全局化了global.$addMySnackbar方法用来添加新的snackbar

* id这个参数专门用来配合snackbars变量管理和获取创建的MySnackbar实例

```
/*
被加载时候componentDidMount添加全局方法：
$addSnackbar(state,id)，state格式请参照官方API说明,必须通过id才能自定义关闭snackbar的按钮
$closeMySnackBar(id)，关闭特定的snackbar
*/
import React from 'react'
import h from 'react-hyperscript'
import deepmerge from 'deepmerge'

import Button from 'material-ui/Button'
import Snackbar from 'material-ui/Snackbar'

let snackbars = {} //全部snackbar实例列表，关闭snackbar时候使用

//输出关闭特定snackbar的全局方法
global.$closeMySnackBar = (id) => {
    if (snackbars[id]) {
        snackbars[id].setState({
            open: false
        })
    }
}

/*
自动接收snackbar管理的类
能够自动计时关闭
*/
class MySnackbar extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            open: true
        }
    }

    componentDidMount() {
        if (this.props.id) {
            snackbars[this.props.id] = this
        }
    }

    render() {
        let props = deepmerge(this.props, {
            open: this.state.open,
            style: {
                display: 'block',
                position: 'relative',
                height: 56,
            },
            onClose: (event, reason) => {
                this.props.onClose && this.props.onClose()
                if (reason !== 'clickaway') this.setState({
                    open: false
                })
            },
        })
        return h(Snackbar, props)
    }
}

//App中所有snackbar的容器管理
class MySnackbars extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            list: []
        }
    }

    add(state, id) {
        console.log('xx', id)
        let newOne = h(MySnackbar, deepmerge(state, {
            open: true,
            id: id //关闭snackbar时候使用
        }))
        this.state.list.push(newOne)
        this.setState({
            list: this.state.list
        })
    }

    componentDidMount() {
        let that = this;
        global.$addMySnackbar = (state, id) => {
            that.add(state, id)
        }
    }

    render() {
        //嵌套两层div把所有snackbar固定在底部中间
        return h('div', {
            style: {
                bottom: 8,
                position: 'fixed',
                textAlign: 'center',
                width: '100%'
            }
        }, [
            h('div', {
                style: {
                    display: 'inline-block',
                }
            }, this.state.list)
        ])
    }
}

export default MySnackbars
```

---
##使用MySnackbars

首先我们还是在App.js中引入```import MySnackbar from '../Utilities/MySnackbars'```,并在render()中创建放置snackbars的容器
```
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
            h(MyDialog),
            h(MySnackbar),
        ]))
    }
```

然后我们就可以在其他页面中使用了，比如：
```
            h(Button, {
                onClick: () => {
                    let id = Math.random()
                    global.$addMySnackbar({
                        anchorOrigin: {
                            vertical: 'bottom',
                            horizontal: 'center',
                        },
                        autoHideDuration: 3000,
                        onClose: () => {
                            console.log('Home Page said:', that.state.title)
                        },
                        message: 'Hello from MySnackbar!',
                        action: [
                            h(Button, {
                                key: 'any',//必须要有这个，值任意
                                color: 'secondary',
                                onClick: () => {
                                    global.$closeMySnackBar(id)
                                    console.log('Home Page said:', that.state.title)
                                }
                            }, '关闭')
                        ],
                    }, id)
                }
            }, 'add snackbar'),
```
这生成一个按钮

![](imgs/4324074-3241e6192173be13.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

点击它弹出

![](imgs/4324074-e4e55a03e093e979.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

多次点击弹出多个
![](imgs/4324074-2032ac1e1e05643f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

点击紫色按钮可以关闭某个snackbar，或者超过3秒钟自动消失

---
###致力于让一切变得简单
如果您发现文章错误，请不吝留言指正；
如果您觉得有用，请点喜欢；
如果您觉得很有用，欢迎转载~
---
END






