
这篇文章记录的是在苹果笔记本上利用虚拟机VMware安装windows10操作系统的步骤。此方法仅把windows作为临时辅助系统使用。

--
####准备工作
首先确保您的macOS硬盘可用空间不少于60G。

从网络上搜索下载虚拟机软件VMware Fusion破解版。
也可以[点击这里](https://pan.baidu.com/s/1oyYp9YPMNeYUHgtOP3CKFg)从百度网盘下载（470M，提取密码: 3u5i）。

安装需要windows 10的正版序列号。如果没有的话，可以从淘宝上花十几块买到，购买时候请注意版本名称。

有的淘宝买家会提供相应的下载地址，如果没提供的话你可以直接从微软官方或者[https://msdn.itellyou.cn/](https://msdn.itellyou.cn/)下载希望安装的windows版本ios镜像文件。
>左侧：操作系统-windows 10，version...（留意后面的年份日期），
右侧：勾选中文简体中文版Windows 10 (multi-edition), Version xxxx (Updated xxxx) (x64) - DVD (Chinese-Simplified)，复制下面【已勾选】里面的地址，使用迅雷下载，大小约4G多，需要一段时间下载完。



--
####安装VMwareFusion
运行下载文件夹中的keygen，弹出窗口中找到一串XXXXX-XXXXX-XXXXX-XXXXX-XXXXX格式的文字，拷贝它。
双击下载到的VMware-Fusion....dmg文件，双击图标启动安装，输入管理员密码，如果提示开发者身份问题请在【系统偏好设置-安全与隐私】中允许它。
点击同意继续安装，粘贴刚才复制的密钥。
安装完成后自动启动进入下面界面：
![](imgs/4324074-41f9ec8cf07791eb.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

将下载的windows10的ios文件直接拖拽到这个界面上，自动进入【创建虚拟机】窗口，列表中选择刚才拖进来的文件，点继续。
![](imgs/4324074-3d01fbfa4df9d40e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

然后进入【快捷安装界面】，任意账户名，任意的密码，输入你的windows 10序列号，选windows 10 pro，然后继续进入【集成】窗口，根据需要选择【更加无缝（推荐）】或【更加独立】，完成配置，点击完成，确认开始安装。
>如果出错【找不到可以连接的有效对等进程】，这是由于没有允许开发者的原因，要在【系统偏好设置 - 安全性与隐私 - 通用 】 找到vm点击允许

![](imgs/4324074-d03824af981dd58c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

和PC安装windows一样，整个安装过程需要半小时到1个小时，系统安装完成后会自动在windows内安装VMware tools。

>提示，安装完成后可用全屏使用，通过ctrl+左右箭头或触摸板三指左右滑动快速在macOS和windows之间切换，按F3返回窗口模式。
>如果选择【更加无缝】那么两个操作系统桌面的文件夹都是公用，来回交换文件也很简单。


--
END



