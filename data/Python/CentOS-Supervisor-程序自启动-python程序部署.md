### CentOS下python程序的持续运行
* 使用ssh登录centOS云服务器，`python app.py`运行的程序在ssh登录退出后会自动结束
* 使用`nohup python app.py`运行的程序在ssh退出后仍能继续
* 使用ctrl+z把当前程序推到后台运行，使用`fg`命令可以切回前台，ctrl+c将终止当前程序
* 使用`nohup python app.py &`这个&符号将在ctrl+c后继续运行

### Supervisor的安装
* supervisor可以在centoOS下自动运行、重启指定程序，并进行有效管理
* supervisor目前只有python2.x版本
* 使用`virtualenv -p /usr/bin/python venv2x`创建一个python2.x的运行环境
* 然后`source venv2x/bin/activate`激活
* 然后`pip install supervisor`进行安装

### Supervisor的设置
* 创建配置文件，`echo_supervisord_conf > /etc/supervisord.conf`
* supervisord.conf包含了unix_http_server、supervisord、supervisorctl、include等几部分，分号开头表示注释内容
* 启动服务。`supervisord -c /etc/supervisord.conf`将启动服务
* 自动配置文件夹。在supervisor.conf中启用[include]，`file=/etc/supervisord.d/*.conf`,这将使supervisor自动加载此文件夹下的所有.conf文件
* 创建配置文件夹。`mkdir /etc/supervisord.d/`
* 增加一个配置文件。在supervisor.d文件夹中添加app.conf文件，内容包含以下内容:
```
[program:app]
command=python3 /tmp/app.py
```
* 然后重新启动服务。`supervisord -c /etc/supervisord.conf`。如遇到问题，可以`ps -A|grep supervisor`找到上一个程序的pid，然后`kill -9 xxx`结束上一个程序进程。

### Supervisor的进程管理
* 查看所有进程,`supervisorctl status all`
* 停止或重启全部进程,`supervisorctl stop all`,`supervisorctl start all`
* 为app.conf添加更多参数`autorestart=true`退出后自动重启，`startretries=3`自动重启最多3次，`startsecs=5`启动5秒后没退出视为启动成功

### 将Supervisor设置为随系统启动
* centOS自动启动/etc/rc.local中设置的命令
* `echo "/usr/bin/supervisord -c /etc/supervisord.conf" >> /etc/rc.local`将Supervisor命令加入命令列表
