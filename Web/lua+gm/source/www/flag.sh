echo $FLAG > /flag
echo "23333" > /tmp/testflag
export FLAG=not_flag
FLAG=not_flag
rm -f /flag.sh

