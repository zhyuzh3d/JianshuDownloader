欢迎关注我的专栏( つ•̀ω•́)つ[【人工智能通识】](https://www.jianshu.com/c/e9a7b7b7024d)
[【汇总】2019年4月专题](https://www.jianshu.com/p/e1afed853866)

---

如何在3D场景中正常显示中文汉字？

![](imgs/4324074-6c62bd2ef503880b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


之前曾经在这个文章里面记录了Aframe的文字实现方法：
[软件技术-WebVR-AFrame文字的实现](https://www.jianshu.com/p/ac92a4e0bf84)

这里主要是记录结合React使用的情况。

基于上一篇文章的项目，[软件技术-React-Aframe网站开发](https://www.jianshu.com/p/dfdf1fd9b52b)。

修改用于实现每个按钮的元素`component/linkBox.js`文件做了一些改进，以下是修改后的代码：

```
import React from "react";
import ReactDOM from "react-dom";
import h from "react-hyperscript"
import 'aframe';
import 'aframe-text-geometry-component';
import 'aframe-html-shader';

let gen = (position, size, clr, txt, href, label, labelId) => {
    return h('a-entity', {
        position,
        scale: '' + size + ' ' + size + ' ' + size,
        href,
    }, [
        h('a-entity', {
            geometry: "primitive: plane",
            position: "0 -0.75 0",
            scale: "0.25 0.25 0.25",
            material: "shader:html;\
            target:#" + labelId + ";\
            transparent:true;\
            ratio:height;\
            fps:1;"
        }),
        h('a-box', {
            material: "side:double;color:" + clr + ";\
            blending:additive;\
            opacity:0.2,\
            metalness:0.8",
        }),
        h('a-box', {
            id: 'tar',
            class: 'clickable',
            material: "side:double;color:" + clr + ";\
            blending:additive;\
            opacity:0.2,\
            metalness:0.8",
            scale: '1.2 1.2 1.2'
        }),
        h('a-entity', {
            material: 'metalness: 0.85;color:' + clr,
            position: "-0.4 -0.08 0",
            'text-geometry': "value:" + txt.toUpperCase() + "; \
            font: #optimerBoldFont;\
            height:0.1;\
            size:0.2;\
            curveSegments:1"
        }),
    ])
}

function createLabelDom(labelId, label,color) {
    //添加html标签元素
    let dom = document.getElementById('aframeTextLabels');
    if (!dom) {
        dom = document.createElement("div");
        dom.setAttribute("id", "aframeTextLabels")
        document.getElementsByTagName("body")[0].appendChild(dom)
    }
    let labelDom = document.createElement("div");
    labelDom.setAttribute("id", labelId);
    labelDom.innerHTML = label
    labelDom.style.position = 'absolute';
    labelDom.style['z-index'] = '-100';
    labelDom.style.color = color;
    labelDom.style['font-size'] = '100px';
    labelDom.style['font-weight'] = 'bold';
    dom.appendChild(labelDom)
}

export default class myComponent extends React.Component {
    constructor(props) {
        super(props);
        this['labelId'] = ('label' + Math.random()).replace('.', '')
        this.state = {
            use: false
        };
    }

    componentDidMount() {
        setTimeout(() => {            
            createLabelDom(this['labelId'], this.props.label || this.props.text,this.props.color)
            this.setState({
                use: true
            });
            this.render()
            
            //添加点击功能
            let rdom = ReactDOM.findDOMNode(this);
            let tarEl = rdom.querySelector('#tar');
            tarEl.addEventListener('click', function () {
                location = rdom.getAttribute('href')
            });            
        }, 1000);
    }
    render() {
        return this.state.use ? gen(this.props.position,
            this.props.size,
            this.props.color,
            this.props.text,
            this.props.href,
            this.props.label,
            this['labelId'],
        ) : null
    }
}
```

主要有几个地方注意：

- 引入了`aframe-html-shader`，它可以将一个普通的html元素变为一个图片，然后再贴到Aframe的3D场景中的模型上，并且能同步，就是说原来的html元素改变的时候，3D场景上的贴图会自动改变。
> [npm上的aframe-html-shader官方说明地址点这里](https://www.npmjs.com/package/aframe-html-shader)

- 增加了单独的`function createLabelDom(labelId, label)`函数用于创建一个标准的html元素，但是注意这里的`labelId`，我们将依靠这个`id`将html元素和3D元素绑定到一起，所以，这个`id`应该是唯一的。

- 在`constructor(props)`React元素实例的初始化构建方法中我们增加了`this['labelId'] = ('label' + Math.random()).replace('.', '')`,我们用随机数生成唯一性的`id`，注意这里一定要去掉随机数的小数点，因为`<div id='xxx'`这里的`xxx`是不能包含小数点和特殊字符的。

- 我们在`componentDidMount`React元素加载完成方法中增加了`createLabelDom(this['labelId'], this.props.label || this.props.text)`，这里使用了上面创建的`this['labelId']`，`this.props.label || this.props.text`表示如果有label就用label，没有就用text。注意这里使用了`setTimeout`延迟添加，这样的好处是可以避免初始页面的时候html文字闪现。

- 在最上面的`let gen = (position, size, clr, txt, href, label, labelId)`方法中我们增加了`labelId`参数，需要注意的是我们把新的文字放在了第一个` h('a-entity', {geometry: "primitive: plane",...`，这里是表示html元素转换的图片贴在一个plane平面物体上，下面的`material: "shader:html;\target:#" + labelId + ";\`实现了`aframe-html-shader`插件的启用和`labelId`的绑定。这里之所以放在第一个是防止被方盒`a-box`遮挡，一旦遮挡即使方盒透明也看不到文字，这应该是个bug。

- 另外一个问题是在浏览器的控制台总会不断地输出警告`aframe-master.js:50449 THREE.Math: .nearestPowerOfTwo() has been renamed to .floorPowerOfTwo().`，这是由于`aframe-html-shader`插件比较老，新的 `three.js`有些函数名改变了，而`aframe-html-shader`插件没有更新，我们可以自己手工找到`node_modules/aframe-html-shader`下面的js文件，搜索到两个`nearestPowerOfTwo`将它替换为`floorPowerOfTwo`就可以了。

![](imgs/4324074-949e319f1766b868.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

>Aframe的确制造了不少麻烦，有些时候想想还不如直接使用Three.js更自由些。但是考虑到开发效率，毕竟Aframe也提供了更多的方便之处。



---
欢迎关注我的专栏( つ•̀ω•́)つ[【人工智能通识】](https://www.jianshu.com/c/e9a7b7b7024d)

---
###每个人的智能新时代
如果您发现文章错误，请不吝留言指正；
如果您觉得有用，请点喜欢；
如果您觉得很有用，欢迎转载~
---
END