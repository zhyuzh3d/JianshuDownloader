欢迎关注我的专栏( つ•̀ω•́)つ[【人工智能通识】](https://www.jianshu.com/c/e9a7b7b7024d)
[【汇总】2019年4月专题](https://www.jianshu.com/p/e1afed853866)

---


![](imgs/4324074-2eddb23a066d5848.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


##Three.js

Three.js是一款用于网页3D效果的框架，它可以在网页内实现非常炫酷的效果。
[官方网站点此进入](https://threejs.org/)

Three.js官网包含了很多效果惊人的3D网站。


![](imgs/4324074-e05bdd146fcce503.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

##Aframe.js

Aframe.js是一款开源的网页3DVR技术解决方案，开源用html标记的方法快速搭建具有3DVR功能的网站页面。

[官方网站点此进入](https://aframe.io/)

##快速上手Aframe.js

- 首先，需要引入`script`脚本(或者从文末下载到本地使用)：
```
    <script src="https://aframe.io/releases/0.9.0/aframe.min.js"></script>
```
- 然后需要在`body`中添加场景单元`a-scene`标记:
```
    <a-scene></a-scene>
```
- 然后再向场景里面添加一个盒子`a-box`：
```
    <a-scene>
        <a-box color="red"></a-box>
    </a-scene>
```
这时候预览页面，你需要用鼠标按住向下旋转视角，在下面就能看到一个红色矩形。
![](imgs/4324074-4f86af6861d75548.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- 因为默认情况的摄像机是在原点人的高度位置（0，1.6，0）的。你可以添加一个摄像机`a-camera`标记，用`position`属性来移动它：
```
    <a-scene>
        <a-box color="red"></a-box>
        <a-entity>
            <a-camera position="0 0 5"></a-camera>
        </a-entity>
    </a-scene>
```
![](imgs/4324074-ced5cb9e35e6298e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- 我们复制几个`box`，移动一下位置，也可以添加一个球体`a-sphere`：
```
    <a-scene>
        <a-box color="red" position="2 0  0"></a-box>
        <a-sphere color="green" radius="1"></a-sphere>
        <a-box color="blue" position="-2 0  0"></a-box>
        <a-entity>
            <a-camera position="0 0 3"></a-camera>
        </a-entity>
    </a-scene>
```
![](imgs/4324074-17f361187f149add.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- 默认情况会有一个照亮整个世界的环境光和一个来自左上方模拟太阳的灯光，我们可以手工添加一个灯光`a-light`，这时候默认两个灯光就会自动关闭：
```
    <a-scene>
        <a-box color="white" position="2 0  0"></a-box>
        <a-sphere color="white" radius="1"></a-sphere>
        <a-box color="white" position="-2 0  0"></a-box>
        <a-entity>
            <a-camera position="0 0 3"></a-camera>
        </a-entity>
        <a-light type="point" position="2 5 3"  distance="20" color="#FFCC00" intensity="1"></a-light>
        <a-light type="ambient" position="2 5 3"  color="#00CCFF" intensity="0.6"></a-light>
    </a-scene>
```
![](imgs/4324074-4b99d01a8210f8a3.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- 这时候可能很难理解灯光和物体之间的关系，你可以按快捷`ctrl+alt+i`打开Aframe的监视器来查看，它看起来很像是一个三维软件的界面，左键按住拖拽旋转，右键按住拖拽移动，滚轮放缩。
![](imgs/4324074-e30770a343c35cd7.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


- 我们添加一个灰色的天空`a-sky`，再给几何体添加一些材质`material`属性。
```
    <a-scene>
        <a-sky color="gray"></a-sky>
        <a-box position="2 0  0" material="color:red;opacity:0.3;side:double"></a-box>
        <a-sphere  radius="1" material="metalness:0.65;color:white"></a-sphere>
        <a-box color="#CCC" position="-2 0  0" material="color:green;opacity:0.3;side:double;blending:additive"></a-box>
        <a-entity>
            <a-camera position="0 0 3"></a-camera>
        </a-entity>
        <a-light type="point" position="2 8 5"  distance="20" color="#FFCC00" intensity="1.5"></a-light>
        <a-light type="ambient"  color="#00CCFF" intensity="0.6"></a-light>
    </a-scene>
```
在这里`opacity`指透明，`metalness`指金属性质，影响高光强度和大小，`blending`表示混合模式，加亮或减暗，如果需要发光则要`emissiveIntensity:100;emissive:red;`联合使用。

![](imgs/4324074-0e7c692c62593e24.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

##Aframe.js中的文字

Aframe.js中的文字有三种实现形式：
- 3D立体文字。需要结合`aframe-text-geometry-component.js`然后在`text-geometry`属性设置使用，[官方说明点这里](https://www.npmjs.com/package/aframe-text-geometry-component)
- 使用SDF图像文字格式，这也是默认的文字属性text即可实现。它是把可能用到的文字打包成一个图片，然后在3D里面拼接图片中的文字使用，可以[参考这个示例文件](https://a-frobot.github.io/aframe/examples/test/text/sizes.html)。
- 实时元素图片文字。它是把网页div元素实时截图再放到3D场景里面，需要`aframe-html-shader.js`并在`material`属性中指定`shader:html;target:#label-1;`才能使用，这里的`#target`是指要转成图片的元素id。


![](imgs/4324074-14be2c81b1117453.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

[上图的页面可以参考这个链接](http://syc.10knet.com/)

下面是它的代码：
```
<!DOCTYPE html>
<!-- saved from url=(0052)https://aframe.io/aframe/examples/showcase/anime-UI/ -->
<html class="a-fullscreen">

<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <title>HourCode</title>
    <script src="/js/aframe-master.min.js"></script>
    <script src="/js/aframe-text-geometry-component.min.js"></script>
    <script src="/js/aframe-html-shader.min.js"></script>
    </style>

<body>




    <a-scene renderer="colorManagement: true;" inspector="" keyboard-shortcuts="" screenshot="" vr-mode-ui="">
        <!-- 素材 -->
        <a-assets>
            <a-asset-item id="optimerBoldFont" src="/font/optimer_bold.typeface.json"></a-asset-item>
            <a-asset-item id="engine" src="/3d/engine.glb"></a-asset-item>
            <a-mixin id="image" geometry="height: 2; width: 2"></a-mixin>
            <a-mixin id="toggleAnimation" animation="property: visible; from: false; to: true; dur: 1" visible="false">
            </a-mixin>
            <audio id="blip1" src="/sound/321103__nsstudios__blip1.wav"></audio>
            <audio id="blip2" src="/sound/321104__nsstudios__blip2.wav"></audio>
        </a-assets>

        <!-- 背景环境模型 -->
        <a-entity position="0 0 -3">
            <a-gltf-model src="#engine" rotation="90 0 0" scale="18 18 18" gltf-model=""></a-gltf-model>
        </a-entity>

        <!-- 菜单 -->
        <a-entity position="-4 0 -6" scale="2 2 2" rotation="0 0 0">
            <a-box id="Train" material="opacity:0.3;side: double;metalness: 0.85;blending:additive" class="clickable"
                color="pink"></a-box>
            <a-box id="Train" scale="1.25 1.25 1.25"
                material="opacity:0.3;side: double;metalness: 0.85;blending:additive" class="clickable" color="pink">
            </a-box>
            <a-entity material="metalness: 0.85;;color:#ff88ff" position="-0.4 -0.08 0"
                text-geometry="value:SHOW; font: #optimerBoldFont;height:0.1;size:0.2" color="#333333"></a-entity>
            <a-entity scale="8 8 8" position="0 1.2 0" text="color: #ffccff; font:dejavu; align: center;value: SHOW">
            </a-entity>
        </a-entity>

        <a-entity position="0 0 -6" scale="2 2 2" rotation="0 0 0">
            <a-box id="Train" material="opacity:0.3;side: double;metalness: 0.85;blending:additive" class="clickable"
                color="blue"></a-box>
            <a-box id="Train" scale="1.25 1.25 1.25"
                material="opacity:0.3;side: double;metalness: 0.85;blending:additive" class="clickable" color="blue">
            </a-box>
            <a-entity material="metalness: 0.85;;color:#88ff88" position="-0.4 -0.08 0"
                text-geometry="value:TRAIN; font: #optimerBoldFont;height:0.1;size:0.2" color="#333333"></a-entity>
            <a-entity scale="8 8 8" position="0 1.2 0" text="color: #ccccff; font:dejavu; align: center;value: TRAIN">
            </a-entity>
        </a-entity>

        <a-entity position="4 0 -6" scale="2 2 2" rotation="0 0 0">
            <a-box id="Train" material="opacity:0.3;side: double;metalness: 0.85;blending:additive" class="clickable"
                color="green"></a-box>
            <a-box id="Train" scale="1.25 1.25 1.25"
                material="opacity:0.3;side: double;metalness: 0.85;blending:additive" class="clickable" color="green">
            </a-box>
            <a-entity material="metalness: 0.85;color:#88ff88" position="-0.4 -0.08 0"
                text-geometry="value:LEARN; font: #optimerBoldFont;height:0.1;size:0.2"></a-entity>
            <a-entity scale="8 8 8" position="0 1.2 0" text="color: #ccffcc; font:dejavu; align: center;value: LEARN">
            </a-entity>
        </a-entity>


        <!-- 标签文字 -->

        <div id='labels' style="display:none">
            <div id="label-1" style="position: absolute;color: #ffaaff;font-size: 100px;font-weight: bold">表演台</div>
            <div id="label-2" style="position: absolute;color: #aaaaff;font-size: 100px;font-weight: bold">训练场</div>
            <div id="label-3" style="position: absolute;color: #aaffaa;font-size: 100px;font-weight: bold">学习营</div>
        </div>

        <a-entity>
            <a-entity geometry="primitive: plane" position="-4 -2 -6" scale="0.5 0.5 0.5"
                material="shader:html;target:#label-1;transparent:true;ratio:height;fps:1;"> </a-entity>
            <a-entity geometry="primitive: plane" position="0 -2 -6" scale="0.5 0.5 0.5"
                material="shader:html;target:#label-2;transparent:true;ratio:height;fps:1;side:double;"> </a-entity>
            <a-entity geometry="primitive: plane" position="4 -2 -6" scale="0.5 0.5 0.5"
                material="shader:html;target:#label-3;transparent:true;ratio:height;fps:1;side:double;"> </a-entity>
        </a-entity>


        <!-- 摄像机 -->
        <a-entity position="0 0 0" rotation="0 0 0">
            <a-camera position="0 0 0" near="0.1" camera="" rotation="" look-controls="" wasd-controls=""></a-camera>
        </a-entity>

        <!-- 灯光 -->
        <a-light id="left" type="point" color="#ff00ec" distance="10" decay="1" position="-2 2 -4" intensity="10"
            animation="property: light.intensity; from: 0; to: 10; delay: 500; dur: 500" light=""></a-light>

        <a-light id="right" type="point" color="#ffff00" distance="20" decay="4" position="4 0 -8" intensity="16"
            animation="property: light.intensity; from: 0; to: 20; delay: 500; dur: 500" light=""></a-light>

        <a-light id="top" type="point" color="#00a0ff" distance="10" decay="2" position="0 2 -10" intensity="10"
            animation="property: light.intensity; from: 0; to: 10; delay: 500; dur: 500" light=""></a-light>

        <a-light id="bot" type="point" color="#3fff00" distance="10" decay="2" position="-2 -5 -10" intensity="10"
            animation="property: light.intensity; from: 0; to: 10; delay: 500; dur: 500" light=""></a-light>

        <a-light id="farright" type="point" color="#ff4400" distance="14" decay="6" position="-5 4 -12" intensity="1"
            animation="property: light.intensity; from: 0; to: 10; delay: 500; dur: 500" light=""></a-light>

        <a-light id="farleft" type="point" color="#0000ff" distance="20" decay="6" position="5 0 -12" intensity="2"
            animation="property: light.intensity; from: 0; to: 10; delay: 500; dur: 500" light=""></a-light>

        <a-light id="env" type="point" color="#00aaff" distance="20" decay="6" position="0 0 0" intensity="10"
            animation="property: light.intensity; from: 0; to: 10; delay: 500; dur: 500" light=""></a-light>
        <!-- <a-light type="ambient" intensity="1" color="#00" light=""></a-light> -->

        <!-- 启动声效 -->
        <a-entity sound="autoplay: true; src: #blip1"></a-entity>
        <a-entity sound="autoplay: true; src: #blip2"></a-entity>

    </a-scene>


    <audio controls="controls" style="display: none;"></audio>
</body>

<script>
    var tmr=setInterval(function(){
        if (document.querySelector("canvas")){
            setTimeout(()=>{
                document.querySelector("#labels").style.display="block"
            },1500)
            clearInterval(tmr)
        }
    },100)
</script>

</html>
```

>你可以访问页面链接http://syc.10knet.com/然后另存为本地页面，以此来获得全部相关的素材资源和js文件。


---
欢迎关注我的专栏( つ•̀ω•́)つ[【人工智能通识】](https://www.jianshu.com/c/e9a7b7b7024d)

---
###每个人的智能新时代
如果您发现文章错误，请不吝留言指正；
如果您觉得有用，请点喜欢；
如果您觉得很有用，欢迎转载~
---
END