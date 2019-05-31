>[点击这里进入**人工智能嘚吧嘚**目录，观看全部文章](https://www.jianshu.com/p/ff37dbc75edb)
---

LaTex['leɪ.teks]是一种语法，可以帮助简书作者快速插入复杂的数学公式或表格。

##对齐
使用\begin{align}和&符号来对齐,两个&&右对齐
```
$$
\begin{align}
&前提1：P\rightarrow Q\\
&前提2：P\\
&结论： Q\\
&&前提1：P\rightarrow Q\\
&&前提2：P\\
&&结论： Q\\
\end{align}
$$
```
$$
\begin{align}
&前提1：P\rightarrow Q\\
&前提2：P\\
&结论： Q\\
&&前提1：P\rightarrow Q\\
&&前提2：P\\
&&结论： Q\\
\end{align}
$$

##行内和行间

用单个美元符号开头和结尾，可以直接在文字段落中插入公式，称之为**内联公式或行内公式**。
比如$f(x)=x^3$这样的效果代码是:
```LaTex
比如$f(x)=x^3$这样的效果代码是
```
两个美元符号开头和结尾，将单独一行显示，称之为**行间公式**，比如下面公式的代码是：
$$f(x)=\frac{a+b}{c}$$
```
$$f(x)=\frac{a+b}{c}$$
```
公式内换行使用两个反斜杠，比如下面公式代码是：
$$
f(x)=\frac{a+b-a}{c}\\
=\frac{b}{c}
$$
```
$$
f(x)=\frac{a+b-a}{c}\\
=\frac{b}{c}
$$
```
上面是行内模式，高度被压缩了，下面是行间不被压缩的情况。
$$\sum_{k=1}^n\frac{1}{k}$$
换行对齐使用\begin{split}和\end{split},每行双反斜杠结尾，需要对齐的等号改为=&加空格,如果换行但连续的内容使用&加空格开头：
$$
\begin{split}
x=& a+b+c+d\\
& +f+e\\
=& b+c\\
=&d
\end{split}
$$

```
$$
\begin{split}
x=& a+b+c+d\\
& +f+e\\
=& b+c\\
=&d
\end{split}
$$
```
##使用空格

LaTex中的空格会被忽略，必须使用特定的标识，`\;`中空格，`\quad`大空格，`\qquad`两个大空格
$$
A\; B\quad C\qquad D
$$


##上标和下标

使用^表示上标或乘方，使用_表示下标数字。比如`$a^{12}$`即$a^{12}$，`$a_{x+y}$`即$a_{x+y}$，注意大括号的使用，`$a^12$`将被显示成$a^12$。
>在简书中，不使用LaTex，直接使用两个`^`夹住也能实现上标，比如`a^3+2^`即a^3+2^的。同样使用两个波浪号（键盘1左边那个）也能实现下标，比如`a~x+y~`即a~x+y~。注意不要使用`~~双波浪~~`即~~双波浪~~。

##常用顶部标记
- $a'$即`$a'$`
- $a''$即``$a''``
- $\hat{a}$即` $\hat{a}$`
- $\overline{aaa}$即`$\overline{aaa}$`
- $\acute{a}$即`$\acute{a}$`
- $\check{a}$即`$\check{a}$`
- $\grave{a}$即`$\grave{a}$`
- $\ddot{u}$即`$\ddot{u}$`
- $\vec{a}$即`$\vec{a}$`
- $\widehat{AAA}$即`$\widehat{AAA}$`
- $\dot{a}$即`$\dot{a}$`
- $\tilde{a}$即`$\tilde{a}$`
- $\ddddot{a}$即`$\ddddot{a}$`
- $\mathring{a}$即`$\mathring{a}$`
- $\widetilde{AAA}$即`$\widetilde{AAA}$`

##矩阵和条件对齐
使用`\begin{matrix/bmatrix/Bmatrix}`结合换行表示矩阵，其v表示竖线，b表示添加方括号，B表示大括号，p表示圆括号，如:
$$
\begin{split}
& \begin{vmatrix}
x,y,z\\
m,n,k\\
u,w,v\\
\end{vmatrix} \qquad
& \begin{matrix}
a,b,c\\
d,e,f \\
\end{matrix}\qquad
&\begin{bmatrix}
1,3,4\\
5,6,7\\
8,9,0 \\
\end{bmatrix} \qquad
&\begin{Bmatrix}
1,\frac{a}{b},4\\
5,6,\sqrt[p]{xy} \\
\sum_{n=3}^{0},9,0\\
\end{Bmatrix}
\end{split}
$$

```
$$
\begin{split}
& \begin{vmatrix}
x,y,z\\
m,n,k\\
u,w,v\\
\end{vmatrix} \qquad
& \begin{matrix}
a,b,c\\
d,e,f \\
\end{matrix}\\
&\begin{bmatrix}
1,3,4\\
5,6,7\\
8,9,0 \\
\end{bmatrix} \qquad
&\begin{Bmatrix}
1,\frac{a}{b},4\\
5,6,\sqrt[p]{xy} \\
\sum_{n=3}^{0},9,0\\
\end{Bmatrix}
\end{split}
$$
```
条件分支对齐使用`\begin{cases}`，可以结合&符号对齐，例如

$$
f(x) =  \begin{cases}
x+y \qquad & x>0\\
x-y^2+24 \qquad & x<=0
\end{cases}
$$

```
$$
f(x) =  \begin{cases}
x+y \qquad & x>0\\
x-y^2+24 \qquad & x<=0
\end{cases}
$$
```

##公式编号
简书中似乎有很多编号语法并不支持，测试成功的方法是在行后添加`\tag{1.1}`类似的手工编号,字体看上去都很小。

$$
\begin{eqnarray*}
x^n+y^n &=& z^n \tag{1.4} \\
x+y &=& z \tag{1.5}
\end{eqnarray*}
$$
$$
\begin{split}
a=b
\end{split}\tag{2}
$$
```
$$
\begin{eqnarray*}
x^n+y^n &=& z^n \tag{1.4} \\
x+y &=& z \tag{1.5}
\end{eqnarray*}
$$
$$
\begin{split}
a=b
\end{split}\tag{2}
$$
```


##常用数学运算符号

- **基本运算**符号，乘号`$\times$`即$\times$；正负号`$\pm$`即$\pm$；`$\div$`即$\div$;竖线`$\mid$`即$\mid$;点乘号`$\cdot$`即$\cdot$;克罗内克积`$\bigotimes$`$\bigotimes$;异或符号`$\bigoplus$`$\bigoplus$;N元乘积`$\prod$`$\prod$；N元余积`$\coprod$`$\coprod$

- 无穷`$\infty$`$\infty$;梯度`$\nabla$`$\nabla$;

- **分数**形式`\frac{分子}{分母}`,比如`$f(x)=\frac{a^2+2ab+b^2}{ab}$`即$f(x)=\frac{a^2+2ab+b^2}{ab}$。

- **求和**符号使用`\sum_{下标}^{上标}`,可以理解上标和下标结合使用的情况，例如`$\sum_{n=3}^{12}$`即$\sum_{n=3}^{12}$

- **根号**使用`\sqrt[方根]{根号下内容}}`表示`\sqrt[n]{1+\sqrt[^m]{1+a^2}}`即$\sqrt[n]{1+\sqrt[m]{1+a^2}}$

- **积分符号**用`$\int$`表示,例如`\int_{3}^{12}=f(t)dt`即$\int_{3}^{12}=f(t)dt$

更多符号图：
![](imgs/4324074-d9f56d5189686d82.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



##更多符号
![](imgs/4324074-61a1907796d015eb.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![](imgs/4324074-565e60672e9e3113.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![](imgs/4324074-c3973ea91db27768.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![](imgs/4324074-62c490a213610b8d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![](imgs/4324074-2a58950ae0d385b1.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![](imgs/4324074-e204550d412db4ef.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![](imgs/4324074-902b9e8fc5105943.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![](imgs/4324074-fb33fc7fbfbdddcd.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)





##更多资源
[官方文档](https://www.latex-project.org/help/documentation/)
[维基教程](https://zh.wikibooks.org/wiki/LaTeX)

---
>[点击这里进入**人工智能DBD嘚吧嘚**目录，观看全部文章](https://www.jianshu.com/p/ff37dbc75edb)
---
###每个人的智能新时代
如果您发现文章错误，请不吝留言指正；
如果您觉得有用，请点喜欢；
如果您觉得很有用，欢迎转载~
---
END