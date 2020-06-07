#!/bin/bash 
echo "nameserver 8.8.8.8" >> /etc/resolv.conf
echo "loading flag"
sed -i "s/flag{string}/$FLAG/g" /tmp/pastebin.sql
echo "loading complete"
sqlite3 /tmp/pastebin.db < /tmp/pastebin.sql
pip install flask
python app.py
/usr/bin/tail -f /dev/null