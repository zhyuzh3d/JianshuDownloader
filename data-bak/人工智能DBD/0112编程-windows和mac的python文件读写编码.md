>[点击这里进入**人工智能嘚吧嘚**目录，观看全部文章](https://www.jianshu.com/p/ff37dbc75edb)
---
在python编程中，苹果macOS（linux、unix..)的系统默认文件数据读写编码是`utf-8`,而windows系统默认是`gbk`。所以很多在mac中正常运行的`with open...`却可能在mac下出错。

下面是mac和win的几个对比：

##读取所有文件列表
- ###macOS
```
import os
files=os.listdir('/Users/zhyuzh/Desktop/Jupyter/tutor/jobui/')
```
- ###windows
```
import os
files=os.listdir(r'C:\Users\zhyuzh\Desktop\Jupyter\tutor\jobui')
```
>mac的路径是正斜杠`/`,win的路径是反斜杠`\`,而字符串的反斜杠还有转义的功能，比如`\n`表示换行，所以必须开头加`r'...'`确保格式不变，另外也要注意win下面的文件夹路径不要以反斜杠结尾。

##读取文件数据
- macOS
```
with open('./jobui/12384.html','r') as f:
        html=f.read()
```
-windows
```
with open('./jobui/12384.html','rb') as f:
        html=f.read().decode('utf-8')
```
>在windows下以byte形式读取字节，`rb`，所以`f.read()`得到的是字节形式的字符串，等同于b开头的字节`bytestr=b'...'`，所以然后需要使用utf-8解码`.decode('utf-8')`。

##将数据写入文件
- ###macOS
```
with open('/jobui/12839.html', 'w') as f:
        f.write(res.text)
```
- ###windows
```
with open('/jobui/12839.html', 'w',encoding='utf-8') as f:
        f.write(res.text)
```
>macOS默认就是utf-8编码，而windows则需要显式的添加`encoding='utf-8'`参数。

最后，是json.dumps和json.loads两个方法似乎并不受到编码影响，待验证。

---
>[点击这里进入**人工智能DBD嘚吧嘚**目录，观看全部文章](https://www.jianshu.com/p/ff37dbc75edb)
---
###每个人的智能新时代
如果您发现文章错误，请不吝留言指正；
如果您觉得有用，请点喜欢；
如果您觉得很有用，欢迎转载~
---
END