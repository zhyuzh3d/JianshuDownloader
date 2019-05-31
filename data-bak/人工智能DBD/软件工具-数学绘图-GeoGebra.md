[人工智能通识-2019年3月专题汇总](https://www.jianshu.com/p/72685b77cfff)

![](imgs/4324074-32903abaf7b10b1e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

GeoGebra是专门用来绘制数学公式图形的软件，支持windows、macOS和linux，并且提供了网页在线直接使用的版本，支持多语言包括中文。

[官网在这里](https://www.geogebra.org/)
[经典绘图操作页面](https://www.geogebra.org/classic)
[官方教程页面](https://www.geogebra.org/a/14)

整体上操作都很简单，每个工具都会清晰的中文提示，虽然官方教程很多都是在Youtube上需要梯子才能看，但稍微摸索一下可以很快上手，下面以经典模式为准，随便记录几个操作。

![](imgs/4324074-a1862a0298282f7c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


##界面布局

- A 工具区。可以创建各种线、面、体、交叉线等造型。注意很多按钮点击会弹出更多子层按钮。
- B 运算区。在这里写公式函数。如下图可以点击左侧圆圈关闭某些图形和点的显示。
![](imgs/4324074-6dc4f7239ba81edd.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- C 绘图区。注意绘图区右上角的按钮，可以隐藏水平面甚至坐标轴，点击齿轮弹出丰富的设置选项，如下图所示。
![](imgs/4324074-bcbc0faff8f03358.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- C 绘图区。点击画面拖动可以旋转角度，但似乎无法平移。点击几何体，右键会弹出快速操作，可以删除，或者通过设置弹出右侧属性面板，修改填充颜色或边缘粗细。

![](imgs/4324074-6aa609587d1752dd.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- D 右上角工具。主要是撤销、重做和搜索。最右边一个相当于全部菜单，包含文件、编辑、视图、设置等各种功能。其中格局可以更改2D或3D绘图模式。你也可以在最底部登录注册用户。

![](imgs/4324074-04b9d17f09eb1294.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


##画一个球

- 右上角主菜单，格局，切换到3D绘图。
- 左侧计算区输入x\^2+y\^2+z\^2=10，绘图区就出现了一个球形。
![](imgs/4324074-d3a0861358fa0ae4.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- 当然也可以直接从工具栏中点击球按钮创建。

##可调节的球

继续上面的公式画球方法。
- 在下面输入m=1然后回车，得到一个滑竿。
- 点击滑竿自身进入编辑模式，设置最小值最大值和步长0.1。
![](imgs/4324074-6021e133e9452a8d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
- 同样创建n=1和k=1。
- 修改最初的公式为$(\frac{x}{m})^2+(\frac{y}{n})^2+(\frac{z}{k})^2=10$.
- 拉动m、n、k的滑竿就能改变球的形状。

![image.png](imgs/4324074-f448b366ff460128.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

##绘制相交线

- 从绘图区右上角按钮隐藏水平面。
- 从顶部工具栏创建一个三点平面。可以三个坐标轴上分别选一个点。

![](imgs/4324074-99fa729855a28f98.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- 从顶部工具栏创建相交线，点选球和平面。就会得到交叉线。

![](imgs/4324074-64c1914beaa8b9a2.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- 点选交叉线，右键创建c的平面图，就得到如下所示图像，三维绘图区中拖拽ABC点，右侧相交线会同步变化。

![](imgs/4324074-37e6e8ec55df19b3.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

##绘制旋转曲面

- 从右上角主菜单，新建文件。
- 计算区输入sin(x)+2。得到正弦曲线。

![](imgs/4324074-64ea0d1363d1fa07.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- 增加输入Surface(f,pi*2,xAxis)。得到旋转曲面。这里小括号中的f是指上面的f(x)=sin(x)+2曲线，pi*2是旋转360度，围绕x轴旋转。

![](imgs/4324074-0c1d5710b6240317.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

##限定区间旋转

- 绘图区齿轮，设置y轴向上。
![](imgs/4324074-b9cf92e0204e8cb4.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- 输入sqrt(),显示开根号，根号下输入10-x^2得到半圆。
 ![](imgs/4324074-0457e42b09f8a93e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- 修改为sqrt(10-x^2)，1<x<3得到一段弧线。

![](imgs/4324074-ecb315ec9ff462b0.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- 新增输入Surface(f,pi*2,yAxis)得到一段旋转的曲面

![](imgs/4324074-3e4f22585b9c442d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


##双向裁切和旋转

- 先画一个半球，sqrt(1-x^2-y^2)。
![](imgs/4324074-aefa98bccc09ee58.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- 再用Function方法对它进行裁切，Function(a,0,1,0,1)。a是上面的函数名，然后是x从0到1，y从0到1.

![](imgs/4324074-f7ea62c5c829fc7c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- 然后对这个函数进行旋转，Rotate(c,pi/4,zAxis)，绕z轴旋转45度。

![](imgs/4324074-4056a923527f00a4.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



##参数方程

- 使用参数方程画圆。Curve(5sin(t),5cos(t),t,0,π*2)

![](imgs/4324074-d181fb227928a21f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)





