[React+Electron桌面应用开发文章索引](https://www.jianshu.com/p/71c88b21ea48)


继续上一篇[**React+Electron项目快速搭建**](https://www.jianshu.com/p/c2a7c56bc472)，这篇介绍如何在React下使用MaterialUI界面框架，实现谷歌MaterialDesign界面设计风格。

[**MaterialUI官方网站**](https://material-ui-next.com/getting-started/installation/)

---
##安装MaterialUI
```shell
cnpm install material-ui@next --save-dev
cnpm install @material-ui/icons --save-dev
```
这里@next使用了最新的版本，也可以去掉就会使用稳定版。

---
##测试MaterialUI

修改index.js，创建一个MD按钮元素，点击可以产生漂亮的水波效果。
```
import React from 'react';
import ReactDOM from 'react-dom';
import h from 'react-hyperscript';

import Button from 'material-ui/Button';

function App() {
    return h(Button, {
        variant: 'raised',
        color: 'primary',
        children:'BUTTON',
    })
}

ReactDOM.render(h(App), document.getElementById('root'));
```
>这里使用了hyperscript语法格式h(tagname,attrsObj),相当于创建了一个DOM
```<Button variant="raised" color="primary">BUTTON</Button>```


![](imgs/4324074-7cb21b225a160c6e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

>关于Button的更多设置,请[参考官方文档](https://material-ui-next.com/api/button/)


---
##组织页面文件结构

我们把整个整个站点分为四层：
1. APP应用层，提供一些全站通用功能，控制整个界面，它负责载入页面和切换页面。相当于简单的路由功能。
1. Pages页面层，实现不同的页面，它负责把页面划分成不同的区块（如顶部导航栏+主体内容区或左侧导航栏+主题内容区+右侧功能区），并且管理各个区块的切换和显示，同时为下一层各个单元之间通信实现接口。跨区块的业务逻辑在这里实现。
1. Blocks区块层，实现每个区块的独立布局和相应功能，能够接收上级页面层传来的参数并作出相应。主要的业务逻辑都在这里实现。
1. Units单元层，区块层的更小的界面单位。实现更加细节的业务功能。
1. Symbols元件层，只实现UI样式和动画交互等，不实现业务逻辑。（这里主要使用MaterialUI的组件）
1. Utilities工具组，一些通用函数，非界面相关，但可以在任意层级中调用这些工具。

基于以上思路，我们在src下分别创建五个文件夹App、Pages、Blocks、Units、Symbols、Utilities。（brackets是按照文件夹名称排列的，顺序并不代表层级）

![](imgs/4324074-f0d25e340f76fab7.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

---
##实现App应用层

修改src/index.js文件,使它读取并显示src/App/App.js生成的内容:
```js
import React from 'react'
import ReactDOM from 'react-dom'
import h from 'react-hyperscript'

import App from './App/App'

ReactDOM.render(h(App), document.getElementById('root'))
```

新建src/App/App.js文件，暂时仅生成最简单的文字:
```js
import {
    Component
} from 'react'
import h from 'react-hyperscript'

class App extends Component {
    render() {
        return h('h1', 'Hello MaterialUI!')
    }
}
export default App
```

顺利的话这时候页面已经自动刷新显示了Hello MaterialUI！文字。
>更多关于React的component组件的创建请[参考官方文档](https://reactjs.org/docs/state-and-lifecycle.html),官方标准使用的是JSX语法，而我的文章中改为使用hyperscript就是大家在这里一直看到的```h(tagNameOrComponent,attrObj,[children])```方法

---
##实现Page页面层

首先创建一个欢迎页文件src/Pages/WelcomePage/WelcomePage.js，内容如下：
```
import {
    Component
} from 'react'
import h from 'react-hyperscript'

class WelcomePage extends Component {
    render() {
        return h('h1','Welcome to my website!')
    }
}

export default WelcomePage
```
然后我们创建一个设置文件，用于管理全部页面，src/App/_pages.js内容如下：
```
import WelcomePage from '../Pages/WelcomePage/WelcomePage'
const pages = {
    WelcomePage,
}

export default pages
```

最后，我们修改一下App.js，调用页面设置，并显示Welcome页面。
```
import {
    Component
} from 'react'
import h from 'react-hyperscript'
import Pages from './_pages'

class App extends Component {
    constructor(props) {
        super(props)
        this.state = {
            curPage: Pages.WelcomePage,
        }
    }

    render() {
        let that = this
        return h(that.state.curPage)
    }
}

export default App
```
>在这里使用了constructor方法来初始化class类，创建了state状态对象用来管理界面上的各种不同状态属性。

这时候浏览器内显示了欢迎页：
![](imgs/4324074-fba3cbf9dd293b3f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

Block区块层和Units单元层、Symbols元件层的实现原理与这个类似，Utilities工具层是不同的。在后面的文章中会逐步介绍。

---
##增加自定义CSS样式

我们可以创建自己的CSS样式，然后引入到App、Page或其他元素中，这里以App为例。

首先创建文件src/App/_styles.js。注意，我们使用js(而不是css)来更加自由的创建css样式类。
```
const styles = theme => ({
    app: {
        background:'#FAFAFA',
        '-webkit-font-smoothing': 'antialiased',
    },
})
export default styles
```

修改App.js引入这个_style并使用它：
```js
import {
    Component
} from 'react'
import h from 'react-hyperscript'
import {
    MuiThemeProvider,
    withStyles
} from 'material-ui/styles'
import PropTypes from 'prop-types'

import Pages from './_pages'
import Style from './_style'

class App extends Component {
    constructor(props) {
        super(props)
        this.state = {
            curPage: Pages.WelcomePage,
        }
    }

    render() {
        let that = this
        const css = this.props.classes
        
        return h('div', {
            style: {
                marginTop:'100px',
            },
            className:css.app,
        }, [h(that.state.curPage)])
    }
}

App.propTypes = {
    classes: PropTypes.object.isRequired,
}
export default withStyles(Style)(App)
```
注意开头代码import引入了withStyles和PropTypes两个模块，尾部代码```withStyles(Style)(App)```把样式style注入到App中。在render()的return部分，我们在curPage外层嵌套了一层div，并使用style给它添加了自定义css样式，并使用了css.app调用了_style.js里面定义的样式类。得到结果如下，可以看到css.app产生的灰色背景，以及直接style产生的marginTop上边距：

![](imgs/4324074-59db6a31733c917c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

>再次强调，这个模式不限于App，可以在任何Page、Unit使用。
---
##自定义主题

我们可能需要MaterialUI的默认设置（颜色、圆角、字体大小等）进行一些自定义，这可以在App层方便的设置。

首先我们为Welcome.js增加一个按钮，以便于我们观察效果
```
import {
    Component
} from 'react'
import h from 'react-hyperscript'

import Button from 'material-ui/Button';

class WelcomePage extends Component {
    render() {
        return h(Button, {
            color: 'primary',
            variant:'raised',
        }, 'Welcome to my website!')
    }
}

export default WelcomePage
```
默认情况它看起来这样(去掉了上面添加的style效果)：

![](imgs/4324074-e1a4594fc6bd1e3b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

>关于Button的更多设置,请[参考官方文档](https://material-ui-next.com/api/button/)

我们在App层创建一个主题src/App/_theme.js,去掉按钮的圆角和阴影：
```
import { createMuiTheme } from 'material-ui/styles';
import teal from 'material-ui/colors/teal';
import pink from 'material-ui/colors/pink';
import red from 'material-ui/colors/red';

const Theme = createMuiTheme({
    palette: {
        primary: teal,
        accent: pink,
        error: red,
    },
    overrides: {
        MuiButton: {
            root: {
                borderRadius: 0,
                boxShadow: 'none',
            },
            raised: {
                borderRadius: 0,
                boxShadow: 'none',
            },
        },
    },
});

export default Theme;
```


然后我们在App.js中使用它，将影响全站所有的页面、区块等：
```
import {
    Component
} from 'react'
import h from 'react-hyperscript'
import {
    MuiThemeProvider,
    withStyles
} from 'material-ui/styles'
import PropTypes from 'prop-types'
import Grid from 'material-ui/Grid';

import Pages from './_pages'
import Style from './_style'
import Theme from './_theme'

class App extends Component {
    constructor(props) {
        super(props)
        this.state = {
            curPage: Pages.WelcomePage,
        }
    }

    render() {
        let that = this
        const css = this.props.classes
        
        return h(MuiThemeProvider, {
            theme: Theme,
        }, h(Grid, {
            container: true,
            spacing: 0,
            className: css.app,
        }, [h(that.state.curPage)]))
    }
}

App.propTypes = {
    classes: PropTypes.object.isRequired,
}
export default withStyles(Style)(App)
```
>这里我们使用了h(MuiThemeProvider)在外层嵌套了主体管理对象，它将对所有内部的页面产生效果。同时我们使用了Grid网格来更容易的实现布局。

![](imgs/4324074-a47d9b9f381364be.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

请注意到按钮颜色、圆角和阴影的变化。

我们在App文件夹增加了_theme.js,_style.js,_pages.js等设置文件，一般我们还会增加一个_config.js文件用来保存其他更多的统一设定。下面是项目的文件结构：
![](imgs/4324074-588722a669df3eee.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

---
##结语

到这里，我们搭建了最基本的网站结构文件结构，并引入了界面解决方案。可以说，对于一个前端站点架构，我们已经完成了一半。

另一半就是，在安心写代码之前，我们还需要实现各个页面的跳转、各个区块的状态切换管理等复杂的控制，以及页面之间、区块之间、页面和区块之间、甚至单元和区块之间的数据传递。

不用担心，我们后面的文章中会以最简单的方式实现这些：路由和数据穿越。

---
###致力于让一切变得通俗易懂
如果您发现文章错误，请不吝留言指正；
如果您觉得有用，请点喜欢；
如果您觉得很有用，欢迎转载~
---
END





