#!/bin/sh
echo 'ServerName localhost:80' >> /etc/apache2/apache2.conf
mkdir /etc/cron.daily
service apache2 start
useradd -m actf
echo actf:actf2020|chpasswd
echo '#!/bin/sh'>>/etc/cron.daily/backup
echo 'for i in $(ls /home); do cd /home/$i && /bin/tar -zcf /etc/backups/home-$i.tgz *; done'>>/etc/cron.daily/backup
chmod +x /etc/cron.daily/backup
echo '*/1 * * * * root /etc/cron.daily/backup'>>/etc/crontab
echo 'flag in /root/'>>/flag_here
echo 'actf:actf2020'>>/flag_here
echo $FLAG > /root/flag
echo "1234"

chmod 700 /root/flag

export FLAG=not_flag
FLAG=not_flag

rm -f /flag.sh

cron

while true;
do echo hello docker;
sleep 1;
done