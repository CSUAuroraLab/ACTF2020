#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from Cryptodome.Util.number import *
import random
from flag import FLAG
from hashlib import sha512
 
def pow_check():
    n=getRandomRange(0,0xfffff)
    s=sha512(long_to_bytes(n)).hexdigest()
    print("Enter number n so that sha512(long_to_bytes(n)).hexdigest()[:20]={}".format(s[:20]))
    m=input()
    if(int(m)!=n):
        exit(0)

def main():
    pow_check()
    p=getPrime(520)
    q=getPrime(500)
    if(p<q):
        tmp=p
        p=q
        q=tmp

    print("p%q={}".format(p%q))
    N=p*q
    print("N={}".format(N))
    e=65537
    flag=bytes_to_long(FLAG)
    enc = pow(flag,e,N)
    print ("enc={}".format(enc))

if __name__ == "__main__":
    try:
        main()
    except:
        print("The programme is exiting. If you are not WRONG, please contact admin.")




