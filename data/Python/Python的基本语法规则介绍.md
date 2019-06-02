>以下以python3.x为参照



### 交互式编程
* 直接在命令行工具下输入`python3`然后回车，可以看到python的版本信息等
* 在命令提示符号`>>`后输入`print('hello world!')`然后回车，可以看到输出`hello world!`
* 输入`exit()`退出
* `python -h`显示命令的帮助

### 脚本式编程
* 在.py脚本文件中编写代码，然后用`python`命令运行这个脚本文件
* 创建一个app.py文件，包含`print('hello world!')`,保存.
* 在命令行用`cd xxx`进入app.py所在文件夹,执行`python3 app.py`回车，可以看到输出`hello world!`
* 在windows系统中app.py可以被直接运行，但在Linux或MacOS中需要以下处理：
* 修改app.py文件为

```
#!/usr/bin/python
print('hello!')
```
* 执行命令，授予app.py可运行权限，`chmod a+x app.py`
* 使用`./app.py`命令运行，输出`hello world!`，注意这里`./`不可省略

### 标识符
* 标识符是用来指代某个数据或对象、方法的符号，简单理解就是名称
* 在 Python 中，所有标识符可以包括英文、数字以及下划线(_)，但不能以数字开头。
* Python 中的标识符是区分大小写的。
* 以下划线开头的标识符是有特殊意义的。以单下划线开头 _foo 的代表不能直接访问的类属性，需通过类提供的接口进行访问，不能用 from xxx import * 而导入；
* 以双下划线开头的 __foo 代表类的私有成员；以双下划线开头和结尾的 __foo__ 代表 Python 里特殊方法专用的标识，如 __init__() 代表类的构造函数。
* Python 可以同一行显示多条语句，方法是用分号 ; 分开，如:`print(1);print(2)`输出1和2

### 保留字
* 保留字是Python官方保留使用的单词，不能用作常数或变数，或任何其他标识符名称。
* 保留字只包含小写字母保留字如下：
* and exec not assert finally or break for pass class from print continue global 
* raise def if return del import try elif in while else is with except lambda yield

### 行和缩进
* Python 的代码块不使用大括号 {} 来控制类，函数以及其他逻辑判断。python 最具特色的就是用缩进来写模块。
* 缩进的空白数量是可变的，但是所有代码块语句必须包含相同的缩进空白数量，这个必须严格执行。
* 不要使用以下格式的代码，因为两个层级相同的print使用了不同的右缩进，第一个用tab键第二个用空格:

```
if True:
    print "True"
else:
  print "False"
```

### 多行语句
* 我们可以使用斜杠（ \）将一行的语句分为多行显示，如下代码输出abc：

```
s = 'a' + \
    'b' + \
    'c'
print(s)
```
* 语句中包含 [], {} 或 () 括号就不需要使用多行连接符。如下实例：

```
days = ['Monday', 'Tuesday', 'Wednesday',
        'Thursday', 'Friday']
```

### 引号
* Python 可以使用引号( ' )、双引号( " )、三引号( ''' 或 """ ) 来表示字符串，引号的开始与结束必须的相同类型的。
* 三引号可以由多行组成，编写多行文本的快捷语法，常用于文档字符串，在文件的特定地点，被当做注释。

```
a = 'abc'
b = "这是一个句子。"
c = """这是一个段落。
包含了多个语句"""
```
* 可以使用单引号包裹双引号，也可以相反，但不能直接用单引号包裹单引号，或双引号包裹双引号,斜杠\加单引号或双引号直接输出引号，不影响其他：

```
s1="he said 'OK!'"
s2='he write that:"tom said \"OK!\""'
print(s1)
print(s2)
```
以上代码输出
```
he said 'OK!'
he write that:"tom said "OK!""
```

### 注释
* 每一行#后面的行将不被运行，视为注释
* 多行注释可以使用三个单引号或三个双引号包裹注释内容

```
#!/usr/bin/python
#-*- coding: UTF-8 -*-
#文件名：app.py

#这是一个注释
print("Hello, Python!");  #第二个注释

'''
这是多行的
注释
'''
```

### 空行
* 空行并不是Python语法的一部分。书写时不插入空行，Python解释器运行也不会出错。
* 空行的作用在于分隔两段不同功能或含义的代码，便于日后代码的维护或重构。

### 等待用户输入
* `a=input('请输入:')`程序将暂停等待用户输入，并把输入内容赋值到a

### 同一行显示多条语句
* 可以用分号分开多个语句在同一行连续运行，例如`print(1);print(2)`,但不推荐这种写法

### 输出
* 使用`print('a','b')`输连续多个字符串
* 使用`a=100;print('A%d' % a)`输出数字变量，得到`A100`输出
* 使用`b='XX';print('B%s' % b)`输出字符串变量，得到`BXX`输出

### 代码块
* 同样缩进的连续代码被视为一个代码块，具有同样的语义范围

```
a=100
if True:
    a=99
    print('in:',a)
print('out:',a)
```
以上代码输出,因为第四行和第三行在一个代码块，而第五行和第一第二行在同一代码块
```
in: 99
out: 99
```
