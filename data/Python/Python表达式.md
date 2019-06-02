### 数学转换
* 其一为复数，则另一个自动转为复数
* 其一为浮点，则另一个自动转为浮点
* 两者都是整数，不做转换

### 表达式
* 运算符和操作数一起构成表达式
* 操作数可以使用标识符表示，如`a=3;b=2;c=a*b`
* 表达式是python程序最常见的代码

### 三元表达式
* value_of_true if condition else value_of_false
    * `n='a' if 10>4 else 'b'`n结果是'a'
    * `c=10/3;n=100 if c>5 else 0`,结果a是0
* (value_of_false,value_of_true)[condition]
    * `n=(100,0)[10>3]`结果n是100
    * `c=10/3;n=(100,0)[c>5]`结果n是0

### BNF巴科斯范式说明
* 这是一种定义语法规则的语法,在Python官方文档及本文以下都使用此范式
* 双引号中的字("word")代表着这些字符本身。在双引号外的字（有可能有下划线）代表着语法部分
* 主要规则如下:
    - < > : 内包含的为必选项。 
    - [  ] : 内包含的为可选项。 
    - { } : 内包含的为可重复0至无数次的项。 
    - |  : 表示在其左右两边任选一项，相当于"OR"的意思。 
    - ::= : 是“被定义为”的意思 
    - "..." : 术语符号 
    - [...] : 选项，最多出现一次 
    - {...} : 重复项，任意次数，包括 0 次 
    - (...) : 分组 
    - |   : 并列选项，只能选一个 
    - 斜体字: 参数，在其它地方有解释 
    
### Python主要表达式
- 获取对象属性：`attributeref ::=  primary "." identifier`
    - 如`boy.age`,`tower.height`
    - 如果对象类定义了\__getattr__(self,name)方法，未被定义的属性将使用它，如以下代码输出100：

    ```
    class sth():
        def __getattr__(self,name):
            return 100
    a=sth()
    a.age
    ```
- 获取子项目：`subscription ::=  primary "[" expression_list "]"`
    - 如`boy['age']`,`mylist[3]`
- 切片：`proper_slice ::=  [lower_bound] ":" [upper_bound] [ ":" [stride] ]`
    - 如`mylist[0:10:3]`,`mylist[0:]`,`mylist[:10:2]`,`mylist[::5]`,`mylist[-30::3]`
- 调用方法：`call::=  primary "(" [argument_list [","] | comprehension] ")"`
    - 如`car.run()`,`person.say('hello')`,`someone.hit(sth,3)`
    - 参数的顺序很重要，**加字典，*加枚举，如下几种语法都正确输出`1 2 3`：
    
    ```
    def p(a,b,c):
        print(a,b,c)
    p(a=1,c=3,b=2)
    p(**{'a':1,'c':3,'b':2})
    p(*{1,2,3})
    ```
