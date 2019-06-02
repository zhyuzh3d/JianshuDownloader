####从五角星说起
谈到N角星，习惯性的我们会先想到五角星。你可能觉得应该这样绘制：
![](http://upload-images.jianshu.io/upload_images/4324074-a84a99955917efa9.gif?imageMogr2/auto-orient/strip)

代码也会相当的简洁：
![](http://upload-images.jianshu.io/upload_images/4324074-62aa03243f219684.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

####六角星和八角星
我们能用同样的方法画六角星吗？NO！五角星可以一笔画出来，笔画不重复，而六角星不行。
好吧，我们可以画两个颠倒的正三角形组成六角星：
![](http://upload-images.jianshu.io/upload_images/4324074-38db52bdbc1641a2.gif?imageMogr2/auto-orient/strip)
代码如下,有些命令使用了连写比如p.fd(300).rt(90);
![](http://upload-images.jianshu.io/upload_images/4324074-6d1b21d2f704b2ea.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


同样我们用2个正方形可以拼成八角星（代码请大家自己实现）
![](http://upload-images.jianshu.io/upload_images/4324074-35ba334d71aab30a.gif?imageMogr2/auto-orient/strip)

但是问题来了，七角星怎么办？

####化整为零
上面的各种方法都是试图用连贯的线把图画出来，就是从整体上来思考的方式。

大多数事物从整体上看都是很复杂的，难于掌握。我们必须想办法把它拆解成几个小部分，每个小部分相对就简单多了，甚至我们可以发现各个部分之间的关系。

就比如画画，如果我们想一下子画个人很难，但是我们可以分成头、身体、四肢分别去考虑就容易多了。这就是化整为零的思考方式。

####寻找重复单元
对于N角星，每个角就是一个单元，如下图所示
![](http://upload-images.jianshu.io/upload_images/4324074-58e1ecef0b571673.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
>注意最后的黄色箭头。每个单元的最终，我们把笔的方向回复到和开始的黑色箭头一样，这样我们才能继续后面的重复。

代码如下：
![](http://upload-images.jianshu.io/upload_images/4324074-a7f5a17a727ca2c6.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

运行结果如下
![](http://upload-images.jianshu.io/upload_images/4324074-5cf82fdea9735df5.gif?imageMogr2/auto-orient/strip)

####变身多角星
如果我们把上面的单元一行代码重复，我们只能得到锯齿
![](http://upload-images.jianshu.io/upload_images/4324074-3ab4cc7e27af71d7.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

N角星每个角都是不同方向的，所以在绘制每个单元之前，我们需要转一下角度，比如画5次，每次转360/5=72度，就得到了五角星
![](http://upload-images.jianshu.io/upload_images/4324074-ef33fb0c4f5ecc49.gif?imageMogr2/auto-orient/strip)

它的代码是这个样子的
![](http://upload-images.jianshu.io/upload_images/4324074-397f83c2e44f1a3e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

仔细观察这个五角星和我们最初那个五角星有什么不一样呢？

####思考题

虽然上面的方法画面上看起来画笔有些摇晃，但有什么要紧呢？最重要的是我们的思路变得一下子清晰了，而且这个算法具有很强的普遍性，比如只要改下数字就有下面这些图形了

![](http://upload-images.jianshu.io/upload_images/4324074-3f44243fbcc78465.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

你也试试看吧！

>这里的N角星都没有把中间的多边形画出来。计算多边形的边长是个棘手的问题，需要用到三角函数，在后面的文章中会提到具体实现方法。

---
###致力于让一切变得通俗易懂
如果您发现文章错误，请不吝留言指正；
如果您觉得有用，请点喜欢；
如果您觉得很有用，感谢转发~
---
END
