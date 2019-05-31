>[点击这里进入**人工智能DBD嘚吧嘚**目录，观看全部文章](https://www.jianshu.com/p/ff37dbc75edb)
---

在电脑上开发的网页，有时候在手机上查看会变得奇怪甚至无法打开，微信公众号和小程序也经常有类似情况发生。
而手机上一旦出现错误，又不能像电脑浏览器那样打开开发者工具查找Bug，这是个问题。
如何能在手机上调试网页观看手机浏览器真实的控制台信息呢？

- 通过USB监视手机上的Chrome浏览器
- 通过微信开发者工具监视手机上的小程序
- 通过TBS监视手机上的微信公众号
- 通过vConsole调试

## 通过USB监视手机上的Chrome浏览器
在电脑端的Chrome浏览器中[打开这个链接chrome://inspect/#devices](chrome://inspect/#devices)，收藏它以后备用。
![](imgs/4324074-fac7a41779740166.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

这里显示了USB线连接的手机设备，如果手机上正打开着Chrome浏览器，那么手机浏览的页面也会列在下面，有时候不准确，但只要点击inspect按钮就能看到和手机同步的页面了。
> 感谢[雨露晨光_92a1](https://www.jianshu.com/u/f0f102f09eb3)提醒：如果遇到404错误，可能需要临时FanQiang才行，只要成功以后就不用FQ也可以用了。[FQ软件蓝灯点这里](https://github.com/getlantern/lantern)。


![](imgs/4324074-c24c917ba37b9f6e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

如果USB连了手机，但电脑Chrome的Device设备里面没有怎么办？
首先要确保手机已经开启了**开发者选项**，由于每个品牌不同型号手机打开开发者选项的方法不完全一样，你只能自己百度搜索自己的手机型号的打开方法。一般都是在**设置**里面不停连续点击**关于手机、版本号**诸如此类文字。成功开启后如下图所示，增加了**开发者选项**一栏。
![](imgs/4324074-3869920dd23767f7.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

然后进入开发者选项，打开里面的**USB调试**。

![](imgs/4324074-dff87e6523d9be3c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

这时候重新插拔USB线，电脑Chrome中应该就会出现设备名了，同时手机上会弹出提示，点击确定即可。
![](imgs/4324074-3a6c3f2e4d13c536.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

如果你仍然没有成功，那么在windows系统中你可能需要安装单独的Android设备驱动。
另外，还有可能你也需要安装ADB（Android Debug Bridge）。

## 通过微信开发者工具监视手机上的小程序

首先你应该已经安装了**微信开发者工具**，没有的话[从这里下载](https://developers.weixin.qq.com/miniprogram/dev/devtools/download.html)。

启动后选择**小程序项目**，如果没有APPID可以点击使用测试ID。
![](imgs/4324074-2124e878f67fbddf.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

然后点击**真机调试**显示二维码。
![](imgs/4324074-a423bc49c4d15be7.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

用微信扫描这个二维码，手机端打开小程序的同时，电脑上**真机调试**窗口也会同步显示调试控制台信息。
![](imgs/4324074-b9f0141ac710291e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

##通过TBS监视手机上的微信公众号

在早期的微信开发者工具中集成了公众号真机调试工具，后来版本升级莫名其妙的移除了，但腾讯也推出了另外一个更通用的调试工具TBS Studio腾讯浏览器服务工具。

[点击这里下载安装TBS Studio](https://x5.tencent.com/tbs/guide/debug/download.html)

安装完成后启动，手机USB连接电脑，**手机打开微信**，然后TBS中启动检测。注意，这也必须先开启手机的开发者选项和USB调试模式。

最后你可能需要设定微信内普通网页（公众号）或者小程序。
![](imgs/4324074-e2fae7736b9179e6.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
注意，如果普通网页设置遇到问题，可以尝试扫描小程序的二维码，或者下面这个二维码
![](imgs/4324074-9ec500f9b4bcf9b9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

然后在**信息**面板下的TBS setting中勾选以下选项。
![](imgs/4324074-46b6182f269d5a8f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![](imgs/4324074-cd92e39203917b50.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

成功之后，启动调试按钮可以点击，开启和Chrome调试工具类似的窗口。
![](imgs/4324074-75d4cb3346b70862.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

##使用vConsole开发调试工具

如果你在网页开发中使用了vConsole模块，那么可以在手机上网页显示绿色的vConsole按钮，点击即可在手机上打开开发调试控制台。
![](imgs/4324074-dea073e2cbaff21a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


公众号或者微信内部打开的网页链接，可以直接在手机上打开调试工具。方法是先访问这个[网址http://debugx5.qq.com/](http://debugx5.qq.com/)或者微信扫下面的二维码：
![](imgs/4324074-9ec500f9b4bcf9b9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
然后再**信息**标签下找到**打开vConsole**选项，勾选它。

![](imgs/4324074-46b6182f269d5a8f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![](imgs/4324074-8447901ecea71998.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

然后微信内打开网页之后，底部都会出现绿色的VConsole按钮，点击即可打开开发者控制台。

>[点击这里进入**人工智能DBD嘚吧嘚**目录，观看全部文章](https://www.jianshu.com/p/ff37dbc75edb)
---
###每个人的智能新时代
如果您发现文章错误，请不吝留言指正；
如果您觉得有用，请点喜欢；
如果您觉得很有用，欢迎转载~
---
END