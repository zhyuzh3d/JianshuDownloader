使用Mounty挂载移动硬盘后，新建文件夹失败，然后整个硬盘全部数据丢失，只剩下一个.Trashes...

解决方法：

把硬盘接到windows系统中，管理员运行cmd命令行程序，输入```chkdsk E:/f```然后等待完成，一切就回来了。这里的E盘是你的移动硬盘号。