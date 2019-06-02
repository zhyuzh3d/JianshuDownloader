安装windows的PC下移动硬盘经常使用NTFS(New Technology File System)，这个是微软专有的。NTFS格式的硬盘接到了苹果电脑下面就只能读不能写了(如下图，注意左下角铅笔图表被杠掉了，有些情况这个图标出现在左上角)。
![](imgs/4324074-5baa0495ab9258da.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

这个可能是由于微软没有把NTFS的写入操作授权给苹果吧，总之这是个恼火的问题，下面是解决方案：

---
####新硬盘
如果是新购买的硬盘，那么强烈建议您右键格式化，选择exFAT文件系统，不要选NTFS，更不要选FAT32（会导致大文件不能拷贝）。

exFAT是跨越windows和Mac的文件系统，以后自然就没有问题了。
>不支持windowsXP。mac OS需要10.6以上版本。

---
####无需工具
如果你的硬盘已经NTFS格式存储了很多文件，那么格式化就行不通了。
请从访达的菜单【前往-前往文件夹】/etc，然后下面找到fstab文件，把它拖拽到桌面上复制出来一个同名文件，右键【选择打开方式-其他】找到【文本编辑】，打开后在里面添加一行：
```
LABEL=HDName none ntfs rw,auto,nobrowse
```
这里的HDName改成你的硬盘的名称，可以有大小写，【但不能包含特殊字符不包含空格】，如果你的硬盘名称不符合要求，请到windows电脑里面右键修改一下再回来。
![就是这个图表的名称 zhyuzhHDD1T](imgs/4324074-372c06937f135f7f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


保存这个桌面上的fstab文件，然后把它拖回去/etc文件夹下，鉴定，替换文件，输入管理员密码。

>也可以直接使用命令```sudo vi /etc/fstab```打开直接编辑，然后粘贴```LABEL=HDName none ntfs rw,auto,nobrowse```,然后冒号wq保存退出```:wq```，不保存用```:q!```。

如果你已经把硬盘插上了，请把它推出，拔掉重新插上，这次在桌面或者访达里面都看不到你的硬盘了...

【程序-实用工具-磁盘工具】，在这里你应该可以看到移动硬盘，右键在访达中显示，这次应该看不到铅笔杠掉的图标了～你可以任意粘贴删除文件操作。

![磁盘工具](imgs/4324074-14068a5c4aa949d2.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

最后，弹出硬盘的操作也要在磁盘工具右键执行。
>注意！右键一定要卸载-推出后再拔出硬盘，否则可能导致非正常推出的错误，再次插入也不能写入了。遇到这种问题，可以再到windows上面正常弹出试试看，如果还不行那就在windows上面右键属性-工具-检查，检查修复一遍一般都能恢复正常。

这个方法虽然繁琐，但是当我们到其他人的mac上拷贝文件的时候，却是最实用的方法，——不需要在别人电脑上安装任何软件就能解决问题。

此方法只要改一次永久有效。——永久在桌面和访达不能直接看到；永久在磁盘工具打开后可以写入修改。

>另外也可以把LABEL=XXX换成UUID=YYYY，你可以在终端通过diskutil info /Volumes/DRIVENAME | grep UUID命令获取这个硬盘的UUID

---
####免费软件
如果你的朋友信任你，那么可以为他的mac安装Mounty软件。
[Mounty官方站点](http://enjoygineering.com/mounty/)
[百度网盘传送门](https://pan.baidu.com/s/14DaV9WTNTtVeI1HhFi2DBg) 密码:sofk
这个软件很简单好用，打开后会在顶部菜单栏右侧出现一个小山按钮，当NTFS硬盘插入的时候，它会弹出提示询问是否设置可以读写操作。

---
####收费软件(破解软件)
比较知名的比如Paragon NTFS，安装后会在【系统-偏好设置】里面出现新图标，点击进行设置。
以前用这个，印象就是破解版难找，新版本的破解版更难找，很烦人。
我现在用Mounty~
>用了一段时间发现Mounty问题也很多，经常不能写入。当然比Paragon偶尔会把全部文件搞丢要靠谱些。
---
>还有一个程序员可能喜欢的方法，就是手工安装第三方开源驱动NTFS 3G
[NTFS 3G Github传送门](https://github.com/osxfuse/osxfuse/wiki/NTFS-3G)

>修改fstab和Mounty的方法，最近都遇到一个问题，就是在windows下没有正常弹出硬盘，导致fstab和Mounty都无效。解决也容易，重新插入windows，正常弹出再回来就好了...

---
END






