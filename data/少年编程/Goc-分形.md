分形Fractal是个几何图像学术语。我们知道，空间是用来研究物体位置形状的，时间是研究事物变化运动的，而分形则是研究事物形状的复杂程度的。
下面我们来用Goc绘制一些看似复杂实则规律简单的分形图像。
![](imgs/4324074-a6ad2d66c410e440.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

---
###康托三分集Cantor
1883年，德国数学家康托(G.Cantor)提出了如今广为人知的三分康托集，或称康托尔集。实际看起来就是下面这个样子：

![](imgs/4324074-da089adf271329e2.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

看上去很无聊，但是你发现规律了吗？
* 先把一条长线三等分，去掉中间一份；
* 再把剩下的两个1/3线段每条都三等分，去掉中间的；
* 再把剩下的每个小线段三等分，去掉中间的
* ...

不断的往复循环继续下去。
怎么用Goc实现呢？似乎不能用for循环，因为每次for循环都是一样的啊，而这个每次分段是看似相同，却每次的长度都不同。

要使用函数递归。

---
####递归
递归就是函数自己运行自己。
比如下面这个样子的
![](imgs/4324074-bce6d66a8a46ea70.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

看看就好，不要运行它，会死机的。因为a会被反复加1，无穷无尽，永不停止，计算机会傻傻的运算下去，然后呢就崩溃了。

我们改动一下，只有a小于1000才继续（在大于等于1000的时候就停止运算）：
![](imgs/4324074-a2ba2b24602d59f5.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

---
####绘制康托三分线段
因为动作是循环的，所以最关键就是编写三分再去掉中间这个算法：
![](imgs/4324074-84768175d3a6e03b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

运行后就能得到三分的两条断开的线。
![](imgs/4324074-55376a8758dcc9c6.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
注意draw函数其实是竖向画的，在main里面p.rt(90);把它整个右转变为水平方向。

这里只是画一次三分线，两个线段，但是我们注意到如果我们每次fd之后， 再用a/3重复draw函数，那么就可以画下面一级；所以我们需要把两个画线的p.fd(a)想办法用一个可以递归下去的函数替换掉。


接下来我们来看下面神奇的代码：
![](imgs/4324074-ca054f4aa2573c0b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

运行这个代码就得到了康托三分线段图：
![](imgs/4324074-9b397e5696eb612d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

我们来仔细分析这个代码：
fdAndRun函数很奇怪，小括号带了一个a参数，后面还有一个int (*draw)(float)，这也是个参数！它是一个函数参数，传递进来我们才能在下面draw(a/3);呼叫它。

要把函数作为一个参数传递，必须使用下面的格式
![](imgs/4324074-84216214bfe4aa34.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

我们要传递的draw函数是int draw(float a){...}，只有a一个参数，所以变为int (*draw)(float)传递进fdAndRun函数。

这样，我们就能在fdAndRun里面呼叫draw函数draw(a/3)；然后注意draw里面，原来两个画线的p.fd被替换成了fdAndRun前进或递归运行。

这样我们就形成了递归循环！
draw呼叫fdAndRun，fdAndRun再呼叫draw，两个函数互相呼叫不停，直到a不大于3，fdAndRun就不再呼叫draw了，也就停下来了。

注意fdAndRun里面的代码，
* 先fd把当前线画出来
* if如果大于3，那么准备下一级
* 因为上面画线已经移动了，所以bk回来
* 然后下移10
* 用三分之一长度a/3呼叫draw
* 向上移动10复位！这很重要！

---
####科赫曲线Koch
![](imgs/4324074-9353bfced9a2ff9b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

这条曲线是瑞典数学家海里格·冯·科赫（Niels Fabian Helge von Koch）在100多年前发现的。

我们把它的复杂度一层层降低
![](imgs/4324074-92acc57e3baec286.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![](imgs/4324074-cb804ab5c01426fa.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![](imgs/4324074-035a4a2c08cfee6d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

发现规律！每条线段不断递归成这个倒V字形就得到了最上面的复杂曲线！

看下面的代码，他可以生成最基础4条线的V造型：
![](imgs/4324074-4b33d29b5d146da3.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

然后我们来添加一个前进画线或者递归的fdOrRun函数，这次稍有不同，画线或者进入下一级（刚才三分线是画线并且进入下一级）：

![](imgs/4324074-5076d9223ace1b63.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

下面的雪花形状只是把它旋转并重复的结果：
![](imgs/4324074-70aaf3cf840dbfa9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
需要调整部分的代码：
![](imgs/4324074-caba56191cb1429f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

---
####谢尔宾斯基三角形Sierpinski triangle
![](imgs/4324074-3fa61b1fccb9d53a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


如果我们把它一步步简化下去就看到，其实是不断把三角形分为三个堆叠的内部三角形：
![](imgs/4324074-cafec612f968618b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![](imgs/4324074-7a2bf3033ca84d4f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![](imgs/4324074-b33e1c17554eea51.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![](imgs/4324074-65590a3066a1be88.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
下面是它的代码：
![](imgs/4324074-2d0b17be77804ef5.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
---
####分形树
![](imgs/4324074-067c5a4b67d7c576.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
看起来很复杂，但实际上只是一个Y字形分叉反复递归迭代而成的，圆点代表在这里生长下一级：
![](imgs/4324074-1f3b5cf812caecdd.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


它的实现代码是：
![](imgs/4324074-05e21697c96bc7b7.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
>在这里使用rand()方法获得随机的变化；
可以认为rand()是一个0到无穷大的数值，
rand%100表示它除以100的余数，就是0～100中的某个数字；
rand()%100/100.0就是一个1%～100%的小数，也就是0～1.0之间的小数，
rand()%100/100*10表示它再乘以10就是0～10.0之间的小数。

---
###摇曳的树枝
![](imgs/4324074-1e2f9eddd8d36c67.gif?imageMogr2/auto-orient/strip)


它的基本单元如下，五个圆圈表示在这里进入下一级。
![](imgs/4324074-42b9e91a18c6bbc0.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


它的代码如下：
```
//画一个小枝直线，或者进入下一级
int doOrRun(float a,float j,int b,int (*fn)(float,float,int)){
	if(a>30){
		fn(a,j,b);
	}else{
		p.fd(a).bk(a);
	}
}
//a竖直长度，jiao左右分开的度数，b左右摇摆的角度
int draw(float a,float jiao,int b){
	float x=0.8;
	float a2=a*0.4;
	float j=jiao*0.7;	

	p.rt(b).fd(a*0.35);
	p.rt(j).fd(a2);
	doOrRun(a2,j,b,draw);//左下生长点
	p.bk(a2).lt(j*2).fd(a2);
	doOrRun(a2,j,b,draw);//右下生长点
	p.bk(a2).rt(j);
	
	p.fd(a*0.65);
	doOrRun(a*0.8,j,b,draw);//中间顶部生长点，0.8使它更长
	p.rt(j).fd(a2);
	doOrRun(a2,j,b,draw);//左上生长点
	p.bk(a2).lt(j*2).fd(a2);
	doOrRun(a2,j,b,draw);//右上生长点
	p.bk(a2).rt(j);	
	
	p.bk(a).lt(b);//复位	
}

int main(){
	int b=0;
	for(int i=0;i<1000;i++){
		p.cls();
		p.move(0,-200);
		draw(100,60,sin(i/6.00)*20);
		wait(0.1);
	}
}
```
注意main函数里面，使用了```sin(i/6.00)*20```这个方法，它得到一个波浪起伏的循环数字，形状类似0，1，2，3，...18，19，20，19，18，17，...3，2，1，0，1，2，3... ...
你可以用下面的代码测试这个数字
```
int main()
{
	for(int i=0;i<100;i++){
		p.move(i*5,sin(i/6.0)*50);
		p.o(2);
	}
    return 0;
}
```
![](imgs/4324074-ab6ad8039c2fd97c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

---
###致力于让一切变得通俗易懂
如果您发现文章错误，请不吝留言指正；
如果您觉得有用，请点喜欢；
如果您觉得很有用，感谢转发~
---
END