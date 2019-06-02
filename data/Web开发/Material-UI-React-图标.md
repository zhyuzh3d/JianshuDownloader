[React+Electron桌面应用开发文章索引](https://www.jianshu.com/p/71c88b21ea48)

这篇文章继续之前的文章，介绍如何添加图标元素。

---
##SVG图标
从[官方实例](https://material-ui-next.com/style/icons/)中我们得到，只要引入```import SvgIcon from 'material-ui/SvgIcon'```，然后render()中增加下面的代码就可以生成一个SVG主页图标
```
            h(SvgIcon, {
                color: "primary"
            }, [
                h('path', {
                    d: 'M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z'
                })
            ]),
```

![SVG图标](imgs/4324074-16187daf57eac741.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

>这里使用了path标记，[规范文档看这里](https://www.w3schools.com/graphics/svg_path.asp)

如何得到各种图标的d后面的长串值？我们可以从很多网站下载到svg格式文件。
[Material Icons 900+图标](https://material.io/icons/)
[IconFont阿里图标库 200W+图标](http://iconfont.cn/)

打开svg文件看起来像这个样子:
```
<svg fill="#000000" height="24" viewBox="0 0 24 24" width="24" xmlns="http://www.w3.org/2000/svg">
    <path d="M0 0h24v24H0z" fill="none"/>
    <path d="M19 3h-4.18C14.4 1.84 13.3 1 12 1c-1.3 0-2.4.84-2.82 2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-7 0c.55 0 1 .45 1 1s-.45 1-1 1-1-.45-1-1 .45-1 1-1zm0 4c1.66 0 3 1.34 3 3s-1.34 3-3 3-3-1.34-3-3 1.34-3 3-3zm6 12H6v-1.4c0-2 4-3.1 6-3.1s6 1.1 6 3.1V19z"/>
</svg>
```
我们只需要第二行path中引号中M19...的部分。
为了统一使用，我们把所有图标的d值都放入一个文件Utilities/Myicons.js，在需要的时候引用它：
```
import h from 'react-hyperscript'
import SvgIcon from 'material-ui/SvgIcon'

const icon = (iconName, props) => {
    return h(SvgIcon, props, [
        h('path', {
            d: datas[iconName] || ''
        })
    ])
}

const datas = {
    'favorite': 'M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z',
    'favorite border': 'M16.5 3c-1.74 0-3.41.81-4.5 2.09C10.91 3.81 9.24 3 7.5 3 4.42 3 2 5.42 2 8.5c0 3.78 3.4 6.86 8.55 11.54L12 21.35l1.45-1.32C18.6 15.36 22 12.28 22 8.5 22 5.42 19.58 3 16.5 3zm-4.4 15.55l-.1.1-.1-.1C7.14 14.24 4 11.39 4 8.5 4 6.5 5.5 5 7.5 5c1.54 0 3.04.99 3.57 2.36h1.87C13.46 5.99 14.96 5 16.5 5c2 0 3.5 1.5 3.5 3.5 0 2.89-3.14 5.74-7.9 10.05z',
}

const MyIcons = {
    icon,
    datas,
}

export default MyIcons
```
在这里我们还添加了icon函数快速生成图标```icon(iconName,props)```，这样我们在任意页面中引入```import MyIcons from '../../Utilities/MyIcons'```，然后render()中添加下面代码就可以生成图标了：

```
            h('h1', this.state.title),
            MyIcons.icon('favorite', {
                color: 'primary'
            }),
            MyIcons.icon('favorite border', {
                color: 'primary'
            }),
```
![SVG数据图标](imgs/4324074-08e8cb9d7cfe4cd6.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

---
##MaterialDesign图标

可以从网上下载到几乎所有希望的SVG图标，也可以使用PS等画图软件来制作新的SVG图标。SVG可以任意变色，我们把图标都整合到一起也更加精简。但SVG使用起来确实不方便。

其实可以直接引入MaterialDesign的900+图标的，比如引入闹钟图标```import AccessAlarmIcon from '@material-ui/icons/AccessAlarm'```,[全部图标名称看这里](https://material.io/icons/)

然后使用它:
```
            h(AccessAlarmIcon, {
                color: 'primary'
            }),
```

---
##其他图标

####FontAwasome

[FontAwasome 600+字体图标](http://www.fontawesome.com.cn/faicons/)

这也是网页开发者常用的另外一套图标。参照它的教程可以使用，先要在index.html中引用css文件```...font-awesome.min.css```，其他页面元素才能使用```class:'fa fa-heart'```。它有自己的变色方法，并不能直接使用'primary'这个值。
我建议还是下载FontAwasome单个图标的svg文件，参照我们上面的方法使用。

[从这里可以点击进入FontAwasome的SVG下载页面](https://fontawesome.com/icons?d=gallery)

####图片图标

我们经常使用设计精美的图片作为图标，你可以直接把图片放在dist/imgs文件夹下面，然后像使用图片那样使用它，注意这里src路径开始不需要添加点或斜杠：
```
            h('img', {
                src: 'icons/heart-red.png'
            }),
```
要知道，图片是不能通过代码直接变色的。

---
###致力于让一切变得简单
如果您发现文章错误，请不吝留言指正；
如果您觉得有用，请点喜欢；
如果您觉得很有用，欢迎转载~
---
END
