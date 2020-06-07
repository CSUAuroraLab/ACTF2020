#!/bin/bash
echo "loading flag"
cp /web1/flag.txt /root/flag
chmod 400 /root/flag
rm /web1/flag.txt
echo "loading complete"
service ssh restart
tail -f /dev/null