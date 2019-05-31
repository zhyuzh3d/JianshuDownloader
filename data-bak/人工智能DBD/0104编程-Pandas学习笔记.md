>[点击这里进入**人工智能嘚吧嘚**目录，观看全部文章](https://www.jianshu.com/p/ff37dbc75edb)
---

###生成DataFrame
直接使用pd.DataFrame(list)方法生成,这里的columns可以省略，默认[0,1,2...]
![](imgs/4324074-cb06c2b30ae9b1b9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

如果columns和列表不匹配就会自动填充Nan，如果列表数据超出columns长度就会出错。
![](imgs/4324074-2cd7f92bf3e81c23.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

###将Nan补零
df的第一个方括号是列，第二个是行，fillna补零针对列补。
![](imgs/4324074-c3b27fe3da2f60c1.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

###获取行
使用loc[n]获取第n行，然后使用loc[n]['colname']获取cell
![](imgs/4324074-1401af59e8be3d2a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


###设置索引
设置索引set_index之后，索引会降低一行出现
![](imgs/4324074-f265c6fe635cba2f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

###插入和删除行
df.insert(pos,col_name,value_arr)插入行.
df.drop(row_n_or_col_name,axis=0)中axis默认为0，可以删除行，axis=1删除列
![image.png](imgs/4324074-6914315c25fef37c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

默认drop并不破坏原df。
pop(col_name)获得列。

![](imgs/4324074-643f95462f868cb3.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

###排序
sort_value(by=col_name , ascending=True)
![](imgs/4324074-1fb3095f3b08072b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

###使用索引
loc[index_name]根据index提取行，iloc(row_n)根据顺序提取行

![](imgs/4324074-3dd67cc47288304e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

###生成矩阵
df的每个cell也可以是list、dict等。
![](imgs/4324074-6864d7f159c6472a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

###序列和面板
df的一列就是一个series；多个df组成列表就是面板panel(已弃用)。
![](imgs/4324074-561d31f7b052a72b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)





---
>[点击这里进入**人工智能DBD嘚吧嘚**目录，观看全部文章](https://www.jianshu.com/p/ff37dbc75edb)
---
###每个人的智能新时代
如果您发现文章错误，请不吝留言指正；
如果您觉得有用，请点喜欢；
如果您觉得很有用，欢迎转载~
---
END