[神经网络文章索引](https://www.jianshu.com/p/7fb9edd69a3d)

---
##准备工作
前面两篇介绍了神经网络的结构，**神经网络包括一个输入层，多个隐藏层，一个输出层，神经元就是存储的激活值**：
![神经网络包括一个输入层，多个隐藏层，一个输出层](imgs/4324074-57990ebdc13d5e0a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

还介绍了每个神经元激活值的算法，**神经元激活值是前一层每个神经元乘以权重再求和，然后加偏置，再Sigmoid**：
![神经元激活值是前一层所有神经元乘以权重再求和，然后加偏置，再Sigmoid](imgs/4324074-440a5fff01a0755b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

以及每次尝试为神经网络设置13002个权重激活值之后，表示我们的这些待定值离成功还有多远的代价值cost的算法，**神经网络的代价值是输出结果减去期望结果，然后平方求和**：
![神经网络的代价值是输出结果减去期望结果，然后平方求和](imgs/4324074-440c05dd42522817.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

**把13002个待定值看做多维空间的维度（坐标轴向），把Cost看作是这个多维空间的海拔高度，那么我们的目标就是找到这个多维空间Cost最低点对应的坐标值。梯度下降方法能让我们找到当前位置下降最快的方向，我们沿着这个方向（路径）一直下去就能找到最低点。**多维空间难于想象，我们从三维空间可以看到：
![2个待定值xy和1个代价值形成的三维空间，梯度下降就是寻找最低点](imgs/4324074-c99521f92029e8cb.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

**负梯度是这个点上向下变化最快曲线的斜率，一个表示多维方向的向量，只要在现有的13002个待定值向量上叠加这个负梯度，就是我们下一步的位置。**
![image.png](imgs/4324074-92f267d2a6ba2dac.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

这一篇我们将介绍如何使用微分思想和反向传播方法找这个负梯度。

---
##极简情况

我们假设输入层只有一个像素（代表一个神经元），隐藏层层也是每层只有一个神经元，输出层也只有一个神经元而且就是十个之中我们需要点亮的那个，我们期望它的激活值是1.0.

在下图中，a表示激活值，a<sup>(L)</sup>和a<sup>(L-1)</sup>表示倒数最后两层的神经元，这里L只是上标，不是乘方运算符。y表示我们期望的结果，就是点亮1.0，z表示未经激活函数计算的原始激活值。
>L层就是输出层。y那我们期望得到的，y这层是不存在的。

![代价值算法示意](imgs/4324074-b382926519bac60d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

C<sub>0</sub>表示某一次计算的Cost值（因为反复调整，会计算很多次的）。
那么C<sub>0</sub>就等于最后一层每个神经元和目标层对应神经元相减的平方，在这里只有一个神经元，就是**(a<sup>(L)</sup>-y)<sup>2</sup>**

我们设定a神经元从前面层计算得到的值为z<sup>(L)</sup>，那么**a<sup>(L)</sup>=σ(z<sup>(L)</sup>)**,这里的σ读音['sɪɡmə]，就是指Sigmoid或者RELU。

计算值z<sup>(L)</sup>等于前一层每个神经元乘以权重，求和，再加偏置，**z<sup>(L)</sup>=w<sup>(L)</sup>a<sup>(L-1)</sup>+b<sup>(L)</sup>**，这里的w<sup>(L)</sup>是指0.48-0.66两个神经元之间的连线，也就是a<sup>(L)</sup>相对于a<sup>(L-1)</sup>的权重。b<sup>(L)</sup>是a<sup>(L)</sup>自身的偏置值。

---
##变量关系
我们集中关注最后两层的神经元。

从计算式**z<sup>(L)</sup>=w<sup>(L)</sup>a<sup>(L-1)</sup>+b<sup>(L)</sup>**中可以知道最后一层的计算值z<sup>(L)</sup>受到w<sup>(L)</sup>、a<sup>(L-1)</sup>、b<sup>(L)</sup>三个数值的直接影响。

同样，z<sup>(L)</sup>又会通过Sigmoid函数直接影响到a<sup>(L)</sup>。

a<sup>(L)</sup>和期望值y一起影响到最终的代价Cost数值C<sub>0</sub>。

如图左侧树形结构展示了这些关系。当然，如果我们继续往前一层推进，那么还可以把a<sup>(L-1)</sup>进行拆分。

![神经元各种变量对Cost的影响关系](imgs/4324074-7e762991d745a13d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

这个树形结构展示了各个变量对最终Cost代价值的影响。

---
##用微分思考

微分是一个神秘的极限值，微分不能孤立出现，必须是相对的，也就是必须要有因变量和自变量，只有一个量的微分没有意义。

微分表示了自变量对因变量的影响程度，在曲线某个点上，因变量除以自变量，dy/dx就是斜率，这条斜线清楚地表示了这个点上自变量将导致因变量变化多快，斜率越陡峭变化越快。

而我们现在要研究的就是w<sup>L</sup>、z<sup>L</sup>等各个变量对我们最终Cost的影响，如果我们知道哪个变量影响多一些，我们就可以反过来调整它，让我们下坡更快，也就是更快的达到最低点，让输出结果更快的接近y值1.0。

这样我们找梯度的问题就转换为求解每个待定的权重和偏置值相对于Cost的偏导了。

---
##链式法则

回到刚才的树形结构：

![神经元各种变量对Cost的影响关系](imgs/4324074-7e762991d745a13d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

我们先关注w<sup>(L)</sup>对C<sub>0</sub>的影响，也就是偏微分∂C<sub>0</sub>/w<sup>(L)</sup>。

>∂表示偏微分的符号，德尔塔δ的古写法，可以读‘偏’，或英文partial['pɑrʃəl] derivative[dɪ'rɪvətɪv]

从树形结构我们注意到，C<sub>0</sub>受w<sup>(L)</sup>影响的程度，可以分解成三层影响程度的乘积：
* z<sup>(L)</sup>受w<sup>(L)</sup>影响的程度
* a<sup>(L)</sup>受z<sup>(L)</sup>影响的程度
* C<sub>0</sub>受a<sup>(L)</sup>影响的程度。

![image.png](imgs/4324074-d1348dd71ef4bee1.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

这样将偏微分一层层链式相乘就是链式法则，我们只要分别求出三个偏微分就解决了问题。
![链式法则](imgs/4324074-de15374b251741f8.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


---
##偏微分求解

第一，因为有
![](imgs/4324074-506a2c1f999854f8.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
由于f(x)=x<sup>2</sup>的导数f'(x)=2x（可以根据导数定义公式推出）,x相当于上面的a<sup>(L)</sup>-y，我们得到
![](imgs/4324074-c62f25c0080a5d0f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

第二，因为有
![](imgs/4324074-3f83a2a8011465fa.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
这里的西格玛σ表示Sigmoid或者RELU，不确定，我们不进行具体求解

![](imgs/4324074-c8c21434e7b138d6.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

第三，因为有
![](imgs/4324074-488376df52948dbc.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
从f(x)=mx+n的导数是f'(x)=m得到：
![](imgs/4324074-9dacd54cad763ca6.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

将它们链式到一起就是：
![](imgs/4324074-457c999fbd3581de.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

---
##扩展到更多样本情况

我们上面谈到的只是一个训练样本时 w<sup>(L)</sup>这个权重的情况，实际上我们有n张训练图片，那么我们就对Cost求和再取平均数。
![](imgs/4324074-20e0fe19ccbe6c37.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
>Σ求和符号，k从Σ底下数字0开始，到上面n-1结束，共n个，类似于编程里面的for循环相加。

---
##扩展到更多维度更多层

但是这也只是我们需要的13003维空间曲面的梯度中一个权重维度，这个梯度是个13002维向量才对，也就是我们实际上最后需要：
![最终梯度包含了13002个权重和偏置](imgs/4324074-56d0ee30bfdc77d9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

我们用相似的方法可以得到梯度的某个偏置维度值：
![](imgs/4324074-56eddbc97a334aaa.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

由于
![](imgs/4324074-ebae5c44ed74a639.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
所以链式第一项∂z<sup>(L)</sup>和∂b<sup>(L)</sup>直接加法相关，∂z<sup>(L)</sup>/∂b<sup>(L)</sup>是1，我们可以直接舍弃第一项，也就有
![](imgs/4324074-cf624a5de8e6ea45.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

我们再来扩展到向前一层的神经元a<sup>(L-1)</sup>对Cost的影响：
![](imgs/4324074-5dd18a2dc464eeeb.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


总结在一起，继续延伸下去可以适用于任意多个隐藏层：
![image.png](imgs/4324074-b489b422ab8a830d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

---
##扩展到更多神经元
不要高兴太早，我们现在面对的只是每层都只有一个神经元的情况：
![](imgs/4324074-00d04629c2256b8a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

而实际是：
![](imgs/4324074-1d8cdb24fdfa94ea.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

我们继续扩展，用a上标L表示所在层，下标数字来表示每个神经元：
![](imgs/4324074-f84bd5811e9b1357.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

我们用下标k表示上一层的某个神经元，下标j表示下一层的某个神经元，y下标表示期望输出的某个神经元：
![](imgs/4324074-7422f320394d7c90.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

那么就有Cost是j从0到L层神经元减1，每个神经元激活值a减去对应的期望神经元结果的平方，然后累计起来：
![](imgs/4324074-85b2af8897b3ad5e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

像之前一样推导，得到适用于每层多个神经元的算法：
![](imgs/4324074-528c7d7a000bb3b9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

进一步得到更适用的神经元激活值的偏导数算式：
![](imgs/4324074-dc1b3e2818ab300f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

这样我们就可以一层一层向前推演下去：
![](imgs/4324074-b56b019cc8da5e4a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

经过这样的算法，多维曲面的梯度的每个维度（对应13002个权重和偏置），然后把这个梯度叠加到原来的13002个权重和偏置上去，重新计算，就会产生新的Cost，然后再反向计算回去，调整新的权重和偏置，以此往复，直到最后13002个权重和偏置产生的运算结果最接近我们的期望结果。
![](imgs/4324074-a7ea9217bce4020f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

---
##随机梯度下降Stochastic Graident Desent
实际上，每次运算梯度并不是使用全部几万张样例图片的，因为那样运算量还是太大了，近似的方法是随机取几百张（**小批次Mini-Batches**）样例进行运算，这就好像你并不会检测周边每0.1角度的下坡幅度，而是随机的转身100次，检测每次正前方的下坡幅度，然后取最陡峭的就好了。

这样看起来有些像醉酒的人晃来晃去跌跌撞撞的下山，但至少他走的很快，最后也能下山去（下图右）。
![image.png](imgs/4324074-b95e31641b03320c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

这种思路就叫做随机梯度下降。

---
##全篇小结

神经网络的算法思路是这样的：

* 神经网络就是很多神经元一层一层的编织起来
* 神经元的激活值依赖于前一层所有神经元的激活值，以及对应的权重和偏置
* 我们期望有那么一组权重和偏置搭配在一起恰恰好
* 恰恰好可以把输入的数据转换成我们期望的输出数据
* 机器学习就是用暴力求解这组恰恰好的待定值的过程
* 纯暴力是不够的，还要讲方法，讲思路
* 把已经明确的样例数据灌入神经网络，流过神经网络
* 把输出的糟糕结果和期望结果进行对比，得出代价值
* 代价值表示了我们距离成功还有多远
* 知道多远还不够，我们还需要找到前进的方向，就是梯度
* 梯度就是不断从代价值往前反推，一路求偏导
* 神经网络倒流，帮我们找到梯度
* 把负梯度叠加到现有的待定值组合中，得到新的待定值组合
* 用新的待定值组合，再次灌入样例数据，再次评估代价值，如此往复
* 样例数据太多，我们可以使用随机梯度下降减少运算量
* That's all!

---
###让知识变得简单
如果您发现文章错误，请不吝留言指正；
如果您觉得有用，请点喜欢；
如果您觉得很有用，感谢转发~
---
END