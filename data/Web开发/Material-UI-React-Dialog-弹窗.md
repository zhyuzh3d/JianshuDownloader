[React+Electron桌面应用开发文章索引](https://www.jianshu.com/p/71c88b21ea48)

这篇文章继续之前的文章，介绍如何创建弹窗。

[MaterialUI官方给出了Dialog各种实现案例](https://material-ui-next.com/demos/dialogs/)，但都很繁琐。因为弹窗经常被使用，所以我们需要极其简单的实现。

---
##弹窗思路

模态弹窗必须打断用户当前流程，用户必须做出选择或操作。同时显示的模态弹窗最多1个，不能重叠。

所以，弹窗不像是一个界面元素，而更像一个全局功能，任何按钮可以直接呼叫它，让它显示出来。

弹窗分为几类：
* 警告窗，用户只能点确定关闭
* 确认窗：用户可以点确定或者取消
* 选择窗：用户可以从弹出的列表中选择一个
* 输入窗：用户可以输入一个或多个文字信息
* 内容窗：弹窗内可以显示更加复杂的内容和操作

我们把用户操作分为两类：
* 窗口自身的打开和关闭
* 窗口内容的选择和输入

我们再分析打开和关闭的实现细节：
* 把弹窗放在App.js里面实现，然后global全局化它
* 窗口打开，需要一个全局函数显示窗口,比如global.showDialog()
* 窗口关闭，需要触发一个设定的函数，所以打开时候要带一个函数作为参数onClose(confirmOrCancel)
* 窗口确认或取消两个按钮的名称可能改变，比如“是的，我同意”和“不，请取消”,所以还要增加两个参数confirmLabel,cancelLabel
* 取消按钮还可以不显示，所以还要有一个参数useCancelButton
* 窗口关闭的时候我们要清理以上信息，还要清楚内容，避免干扰下一次弹窗

尽管内部的交互可能更加复杂，但实现很简单，因为我们可以在窗口打开时候增加一个children参数，把整个内容区填进去就可以。


---
##编写MyDialog.js

我们创建Utitlies/MyDialog.js。

这里输出了一个标准元素，当它被App的render使用的时候，会创造两个全局的方法用来显示和隐藏窗口。

一个默认的状态defaultState用来初始化和清空窗口的全部设置，包含了我们上面提到的各种参数。实际上大部分默认值都写在了render()函数里面。

```
/*
被加载时候componentDidMount添加全局方法：
$showMyDialog(state)，state格式请参照下面defaultState对象
$showMyDialog()
*/
import React from 'react'
import h from 'react-hyperscript'
import PropTypes from 'prop-types'
import deepmerge from 'deepmerge'


import Button from 'material-ui/Button'
import Dialog, {
    DialogTitle,
    DialogContent,
    DialogActions,
} from 'material-ui/Dialog'

const defaultState = {
    open: false, //窗口是否显示
    title: '', //标题
    content: '', //文字内容，优先使用
    children: [], //替换整个内容区，其次使用
    onClose: (confirmOrCancle) => {}, //关闭时执行的函数
    confirmLabel: '', //确认按钮上的文字
    cancelLabel: '', //取消按钮上的文字
    useCancelButton: true, //是否显示取消按钮
}

class MyDialog extends React.Component {
    constructor(props) {
        super(props)
        this.state = defaultState
    }

    show(state) {
        this.setState(deepmerge(state, {
            open: true
        }))
    }

    hide() {
        this.setState(deepmerge(defaultState, {
            open: false
        }))
    }

    componentDidMount() {
        let that = this;
        global.$showMyDialog = (state) => {
            that.show(state)
        }
        global.$hideMyDialog = () => {
            that.hide()
        }
    }

    render() {
        return h(Dialog, {
            open: this.state.open || false,
        }, [
            h(DialogTitle, {
                style: {
                    minWidth: '200px',
                }
            }, this.state.title || '弹窗标题'),
            h(DialogContent, {}, this.state.children || [
                h(DialogContentText, this.state.content || '弹窗提示文字')
            ]),
            h(DialogActions, [
                h(Button, {
                    onClick: () => {
                        this.setState({
                            open: false
                        })
                        this.state.onClose && this.state.onClose(true)
                    }
                }, this.state.confirmLabel || '确认'),
                this.state.useCancelButton && h(Button, {
                    onClick: () => {
                        this.setState({
                            open: false
                        })
                        this.state.onClose && this.state.onClose(false)
                    }
                }, this.state.cancelLabel || '取消')
            ])

        ])
    }
}

export default MyDialog
```

>使用||在字段未定义的使用默认值，使用&&避免if判断的啰嗦语法

---
##使用MyDialog

比起官方案例，MyDialog并不简单，但这是一劳永逸的做法，我们看一下具体使用。

首先，我们要在顶级的App.js中加载```import MyDialog from '../Utilities/MyDialog'```。

然后在render()的最后使用它，这样$showMyDialog和$hideMyDialog就被添加到global全局了：
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
        ]))
    }
```
好了，现在就绪了，我们可以在任意页面中使用，比如在HomePage.js的render()中直接使用它（因为App.js最先已经把$showMyDialog和$hideMyDialog全局化了，所以不需要再加载MyDialog模块了）：
```
            h(Button, {
                onClick: () => {
                    global.$showMyDialog({
                        onClose: (ok) => {
                            console.log('MyDialog said:',ok)
                        },
                        children: [h(Button, {
                            onClick: () => {
                                global.$hideMyDialog()
                                console.log('Home Page said:',that.state.title)
                            }
                        }, 'close dialog')]
                    })
                }
            }, 'open dialog'),
```

这里我们在页面上创建了open dialog按钮。
![](imgs/4324074-bd4c2c52c9d311f8.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

点击按钮将打开一个弹窗。
![](imgs/4324074-03d0c0ffeefd9d4a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

而弹窗内我们没有使用简单的文字内容content字段，而是使用了children向弹窗内添加了一个按钮close dialog，点击它会通过自身的onClick事件关闭弹窗，同时输出HomePage的state.title，而不是MyDialog的state。

如果点击下面的确认或取消按钮，则会调用onClose方法输出true或flase，我们可以利用这个知道用户点击了哪个按钮。

---
###致力于让一切变得简单
如果您发现文章错误，请不吝留言指正；
如果您觉得有用，请点喜欢；
如果您觉得很有用，欢迎转载~
---
END

