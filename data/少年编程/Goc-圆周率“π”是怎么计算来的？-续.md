在[上一篇文章中](https://www.jianshu.com/p/00319ea12c18)我们使用了细分圆面积，然后数格子的方法计算得到圆周率π的近似值。但更科学的方法是使用π的展开式形式来计算。比如下面这个公式：

![](imgs/4324074-6d0cebbee94bfeb4.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

第一眼看到这个公式都会惊讶甚至怀疑，不过你可以用下面的Goc代码来验证这个事情，看看循环次数是否越多就越接近π的值：
```
int main(){
	float he=0;
	for(int i=1;i<1000;i+=2){
		he=he+1.0/(i*i);
	}
	float pi=sqrt(he*8); //sqrt是把括号里面的数字开平方，比如sqrt(16)就是4
	char str[10];
	gcvt(pi, 10, str);
	p << str;
}
```
>由于普通计算机数字精度问题，不能处理超大的数字，所以上面for循环不要使用太大的数字，请在3万以内测试。如果您有好的解决方案，烦请留言，万分感激！

但为什么会这样？

---
##从倒数勾股定理说起

还是从勾股定理开始：任意直角三角形，斜边c的平方等于两个直角边平方的和。

![](imgs/4324074-9259aae527042358.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![](imgs/4324074-14a793b501a0aeef.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

我们再看这个：
![](imgs/4324074-26d5920837a51623.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

对于直角三角形面积我们知道是两个直角边相乘再除以2，也就是(a*b)/2;但看这个倒下的直角三角形，如果我们把c当成底边，d是三角形的高，那么我们就知道整个三角形的面积是(c*d)/2。两个方法哪个才正确？当然都正确啦！

所以我们有：
![](imgs/4324074-0a83e26424c52f7d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

也就是：
![](imgs/4324074-d6ed851fbb075b58.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
然后：
![](imgs/4324074-1d04b251c8f44c53.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
两边都平方：
![](imgs/4324074-544972eb7f40bbdc.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
因为勾股定理c方又等于a方加b方：
![](imgs/4324074-7d37c4bc4b4d1025.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
也就是：
![](imgs/4324074-7a7c7069ba2f334a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

换个写法：
![](imgs/4324074-99163125d0987b79.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

也就是有：
![](imgs/4324074-03367c927977cece.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


终于到最后了~两数相加除以一个数，等于两数分别除以这个数再相加：
![](imgs/4324074-71f0ab59284a94de.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

这就是神奇的倒数勾股定理公式，三角形斜边上高的倒数，等于两个直角边倒数的和：
![](imgs/4324074-d8b1e025cdeae9cc.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![](imgs/4324074-c3354337f48aa6bc.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


---
##圆直径内接三角形

我们再来看另外一个和勾股定理没关系的事情，圆上任意一个点，连接直径两端，和直径一起围成的三角形，一定是个直角三角形。比如下图：
![](imgs/4324074-4fdb92dd7f758ea6.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

由于三角形内角和是180度，所以橙色和绿色两个三角形内角和加起来是360度，也就是两个黄色角和两个绿色角加中心的黑色半圆等于360度。

又因为虚线也是半径，c边分成左右两边也都是半径，所以这两个三角形都是等腰三角形，两个黄色角相等，两个绿色角相等，：
![](imgs/4324074-8946edd949eb5b8b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

两边都减半，就有
![](imgs/4324074-eef6fbd7517fa25d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
很明显，黄色角加绿色角就是90度，也就是恰好是红色直角位置。

这证明了，**圆上任意一点连接直径两端围成的三角形一定是直角三角形**。


---
##从第一个圆开始

好了，我们已经做好准备，下面就开始拿下开头的那个神奇公式：
![](imgs/4324074-7f433f41ba21792b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

先看下面这个：
![](imgs/4324074-477e9333e69b2c3c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


这里灰色大圆直径是黑色小圆的两倍。
首先根据我们证明的倒数勾股定理，我们有：

![](imgs/4324074-8645c68e8a48e08c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

a和b左右两边是对称的，所以有：
![](imgs/4324074-a899436a3a8a8243.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


假设我们的小黑圆周长是2，那么直径d是2/π；d的平方就是(2/π)的平方，倒数就是(π/2)的平方，就是：
![](imgs/4324074-6fbb87696502406e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
>注意，由于大圆直径是小圆直径的2倍，周长也是2倍。小黑圆周长是2，那么大圆周长是4，两个点之间的半圆长度是2。

---
##再看更大的圆
我们再看下图，外面增加一个4倍大的圆：

![](imgs/4324074-5952e180ebce8b8c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



注意粗橙色的三角形，是直径和圆上点组成的直角三角形！在这个粗橙色三角形内，b是斜边上的高！所以有：
![](imgs/4324074-b21059631a7a7aaf.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

结合上面的结论：
![](imgs/4324074-2b9bb7c23c4a37b8.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

我们得到：
![](imgs/4324074-a36610f561057891.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

>注意这里，四个橙色的圆点把整个大圆四等分。b2上面对着的最大圆的灰色周长，正好是整个大圆的1/8，也正好是小黑圆的一半，也就是1（小黑圆周长我们开始就设定是2），和中等圆的1/4相等。


---
##再看超大的圆

似乎规律还不明显，我们再看超大的圆：

![](imgs/4324074-5e4db76216f061bb.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

这个图上，根据倒数勾股定理，可以得到:
![](imgs/4324074-a672644d8b6ded61.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

我们再看a2的情况：
![](imgs/4324074-5fed5a74efcf9302.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


这个图很乱，我们只看粗线，橙色粗线a2，m和n代表绿色粗线，根据倒数勾股定理我们有：
![](imgs/4324074-c623b75b8bed2b2c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

好了，如果再继续下去我们可能会头晕了，但是我们可以换个思路来看。

---
##圆继续变大会怎样？

每次我们把圆增加1倍，都会产生下面的规律：
首先，圆上的点会一个分裂成为两个。最初1个黑色点，分裂成两个蓝色点，再分裂成4个橙色点，再分裂成为8个绿色点，继续下去就是16个。
![](imgs/4324074-b69a517246762d97.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

其次，我们最初的黑色点上到顶部，也就是小黑圆直径平方分之一，也被分解为两个蓝色点到顶部距离平方的倒数和。然后每个蓝色点到顶部距离的平方分之一，又被分解成两个橘色点到顶部距离的平方倒数和。然后每个橙色点到顶部的距离分之一，又被分解成两个绿色点到顶部距离的平方倒数和。

![](imgs/4324074-9ac591b9a9be7e53.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

从上图可以看出，我们最初的黑色竖线平方分之一，被分解成2条蓝线平方倒数和（2个点每个点有一条到顶部），然后分解成4个黄色点到顶部距离平方倒数和（图中只画了1个蓝点分裂的情况），又分解为8个绿色点到顶部距离平方倒数和（图中分两种情况画了2个点橙色点分裂的情况）...如下图所示：
![](imgs/4324074-8a65abe4763cfebb.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



再次，我们来注意上图这些线的长度，最初周长是2；然后周长翻倍变成4，有两个蓝色点，点之间隔半个圆长度是2；然后周长翻倍变成8，有4个橘色点，相邻点之间隔1/4圆，也就是弧长8/4=2；然后周长变16，点之间弧长16/8还是2;然后周长32，点之间弧长还是2...无论继续编号多少次，点之间的弧长永远是2！

最后，假设我们的圆无限大，比地球赤道还要大无限倍，会怎样？无限大的那个圆会在顶部变为一条直线！
![](imgs/4324074-9bf7da9fb873e022.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
然后呢？前面图中我们画的蓝色-橙色-绿色-红色线最终都重叠在这条直线上！
这又怎样？记得我们上面的计算的黑色小线段平方倒数和吗？
![](imgs/4324074-7ac0e1bfbcbd465a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

我们把黑色点到0的距离平方倒数(π平方除以4)，无限分解，最终分解成无限多个紫色点到0的长度平方倒数和！
这就有：
![](imgs/4324074-4faf52ddcc7086d6.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

我们再把负数的一半去掉，那么左边就变为π平方除以8：
![](imgs/4324074-0c791eb481e7d545.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


大功告成！

>可能你已经注意到，对于无限大圆，顶部的点都在直线上，但我们忽略了底下对面圆上的点，没有画出它们连过来的线。这是因为对于无限大圆，底下的点在无限远处，无限远的倒数平方和近乎是0，对我们的计算没有影响。当然如果我们计算100倍大的圆时候，下面的点会有影响的，这会让我们计算得到的π值小那么一丁点，微乎其微，如果我们真的希望更精确，那么不应该纠缠于损失的这么一点，而是使用更大的圆（比如10000倍）来进行计算，圆越大，损失越小，圆无限大的时候，我们就得到了最好的π数值。——当然，无限是不可能实现的，所以无论如何，这个算法得到的π总是比实际小那么一丢丢。

---


##小结
圆周率π的展开式很多，可以百度搜索到。这些展开式基本都是微积分计算得到的，这种形式的展开式形式也称为微积分的泰勒展开式。

这篇文章主要是利用几何极限的方法对它进行证明，也不是最好的证明方法，但可以让初中数学水平就能理解。

圆周率π的神奇故事还有很多，就像是数学世界的一个万能钥匙，可以打开一扇又一扇大门，希望大家一起来探索！

---
###致力于让一切变得通俗易懂
如果您发现文章错误，请不吝留言指正；
如果您觉得有用，请点喜欢；
如果您觉得很有用，感谢转发~
---
END


