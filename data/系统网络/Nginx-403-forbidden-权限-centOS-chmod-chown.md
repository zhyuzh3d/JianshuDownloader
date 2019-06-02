Nginx的web文件服务，同样目录下，有的图片可以正常访问，有的403 Forbidden打不开。这是由于文件权限问题，nginx没有读取权限。
centOS下,先cd进入文件夹，然后批量修改文件夹和文件权限的命令：
```shell
find -type d|xargs chmod 755
find -type f|xargs chmod 644
```
---
####chmod命令
chmod（change mode）,改变文件夹、文件的权限。



命令格式：
```
[ugoa...][[+-=][rwxX]...][,...]，
```


####示例说明

* [ugoa...] u 表示该档案的拥有者，g 表示与该档案的拥有者属于同一个群体(group)者，o 表示其他以外的人，a 表示所有（包含上面三者）
* [+-=] + 表示增加权限，- 表示取消权限，= 表示唯一设定权限。
* [rwxX] r 表示可读取，w 表示可写入，x 表示可执行，X 表示只有当该档案是个子目录或者该档案已经被设定过为可执行。

设置所有用户可读a.conf
```
chmod a+r a.conf
```

设置只有作者可读写执行
```
chmod u+rwx c.conf 
```

设置文件 a.conf 与 b.xml 权限为拥有者与其所属同一个群组 可读写，其它组可读不可写
```
chmod a+r,ug+w,o-w a.conf b.xml
```
设置当前目录下的所有档案与子目录皆设为任何人可读写
```
  chmod -R a+rw *
```
>-R, --recursive 递归处理当前目录下所有的子目录和文件
-c --change  更改成功后显示报告
-f, --silent, --quiet 抑制报告信息，错误也不提示
-v, --verbose 显示非常详细的报告
--no-preserve-root 默认不特殊处理斜杠
--preserve-root 递归操作斜杆失败
--reference=RFILE 使用RFILE代替MODE模式
--help 显示此帮助信息
--version 显示版本信息

####8进制模式

```
chmod UGO file...
```
UGO是三个数字，分别表示User、Group、Others用户权限。

读r=4,写w=2,运行x=1
那么 
* 读写运行=rwx=7
* 读写=rw-=6
* 读运行=r-x=5

>r-- = 100
-w- = 010
--x = 001
--- = 000
所以二进制100是7，010是4，001是1，000是0

所有人所有权限就是 777,相当于chmod u=rwx,g=rwx,o=rwx file或chmod a=rwx file
```
chmod 777 file
```
设置作者读写，其他人完全没权限
```
chmod 600 file
```


---
####chown
chown（change owner）改变文件所有者。需要root权限。
```
chown [可选项] user[:group] file...
```
设置a.conf所有者归tom所有(tom属于users用户组)
```
chown tom:users file a.conf
```
当前目录下所有文件都归jam所有
```
chown -R Jam:users *
```

---
END




