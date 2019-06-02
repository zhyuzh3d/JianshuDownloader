>[点击这里进入**人工智能嘚吧嘚**目录，观看全部文章](https://www.jianshu.com/p/ff37dbc75edb)
---

其实很简单，把cell改为markdown，然后两个美元符号中间或者四个美元符号中间就可以撰写LaTeX公式了。
撰写之后shift+enter运行显示公式，双击公式返回编辑。

![](imgs/4324074-01364308f696180d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

单个美元符号开头结尾的公式只是字号小一些，其他没区别。


##常用符号语法说明
>简书目前也支持以下这些公式语法，你在写简书的时候也可以试试看`$$\sqrt{ x^{2}+\sqrt{y} }$$`，它可以显示如下$$\sqrt{ x^{2}+\sqrt{y} }$$

以下是一些常见的LaTeX公式符号规范：
- \frac{分母}{分子}
![](imgs/4324074-a470b2e6bb1ed24b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- \sqrt{被开方内容}，^{指数}
![](imgs/4324074-750b67267971787f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- \sqrt[n]表示n次方根，_{m}表示m下标
![](imgs/4324074-8f063c027dddfe0d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- \choose和\atop都是竖向排列，区别是有括号
![](imgs/4324074-06efc813a082fd40.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- \overrightarrow{a,b} 向量的顶上向右箭头，\overleftarrow{a,b} 向左
![](imgs/4324074-c0d56951f3cf5656.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- \overbrace和\underbrace表示上面或者下面大括号
![](imgs/4324074-955bc6e13e7bb84f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- \sum求和符号，\pi圆周率符号，\int积分符号，\prod乘积运算符号
![](imgs/4324074-00e8ae9289583c2a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- \,空格，\;中空格，\quad大空格，\qquad两个大空格
![](imgs/4324074-aad656de80e8065b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- \begin{matrix/bmatrix/Bmatrix}和\end{}配合表示矩阵，双斜杠\\\\表示换行，\begin{cases}可以配合&符号对齐。
![](imgs/4324074-efe4927e698a02c1.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

更多示例
```
$$
x_{(22)}^{(n)}\qquad
\frac{1}{1+\frac{1}{2}}\qquad
\sqrt{1+\sqrt[^p]{1+a^2}}\qquad
\int_1^\infty\qquad
\sum_{k=1}^n\frac{1}{k}\qquad
\int_a^b f(x)dx\qquad
\frac{\partial E_w}{\partial w}\qquad
\lim_{1\to\infty}\qquad
\lt \gt \le \ge \neq \not\lt \neq\qquad
\times \div \pm \mp x \cdot y\qquad
\cup \cap \setminus \subset \subseteq \subsetneq \supset \in \notin \emptyset \varnothing\qquad
\to \rightarrow \leftarrow \Rightarrow \Leftarrow \mapsto\qquad
\land \lor \lnot \forall \exists \top \bot \vdash \vDash\qquad
\star \ast \oplus \circ \bullet\qquad
\approx \sim \cong \equiv \prec\qquad
\infty \aleph \nabla \partial\qquad
\epsilon \varepsilon\qquad
\phi \varphi\qquad
\left \lbrace \sum_{i=0}^n i^2 = \frac{(n^2+n)(2n+1)}{6} \right\rbrace \qquad
\left( \sum_{k=\frac{1}{2}}^{N^2}\frac{1}{k} \right)\qquad
\left. \frac{\partial f(x, y)}{\partial x}\right|_{x=0}\qquad
\left\lbrace\begin{aligned}a\\a\\a\\\end{aligned}\right\rbrace \qquad
\left\lbrace\begin{aligned}
a_1x+b_1y+c_1z &=d_1+e_1 \\\ 
a_2x+b_2y &=d_2 \\\ 
a_3x+b_3y+c_3z &=d_3
\end{aligned}\right\rbrace \qquad
f(n)
\begin{cases}
n/2&if\;n>10\\
n+1&if\;n=10\\
\end{cases}\qquad
$$
```
![](imgs/4324074-61f9a4f091bf232a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

##附录
####希腊字母
![](imgs/4324074-4e56622a3e074f91.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

####注音符号
![](imgs/4324074-de5e9d47b6744b0b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

####二元关系
![](imgs/4324074-d647f8c79d08850f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

####二元运算
![](imgs/4324074-40acf7d1937e8a7e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

####大运算符
![](imgs/4324074-beada0799241ea86.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

####定界符
![](imgs/4324074-506f923f722d485c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

####大定界符
![](imgs/4324074-daaba7f56c115b76.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

####其他
![](imgs/4324074-69c43cff6b276be5.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


---
>[点击这里进入**人工智能DBD嘚吧嘚**目录，观看全部文章](https://www.jianshu.com/p/ff37dbc75edb)
---
###每个人的智能新时代
如果您发现文章错误，请不吝留言指正；
如果您觉得有用，请点喜欢；
如果您觉得很有用，欢迎转载~
---
END