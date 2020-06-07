#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random
from secret import flag
from Cryptodome.Util.number import *
import gmpy2

def main():
    message = bytes_to_long(flag)
    length=len(flag)*8
    n=5
    k=4
    l=n-k+2
    m=[1,1,1,1,1]
    m[0]=getPrime(length//k+1)
    m[1]=getPrime(length//k+2)
    m[2]=getPrime(length//k+3)
    m[3]=getPrime(length//k+4)
    m[4]=getPrime(length//k+5)
   
    assert(message<m[0]*m[1]*m[2]*m[3])
    assert(message>m[2]*m[3]*m[4])
			
    for i in range(0,5):
    	print("a"+str(i+1)+"="+str(message%m[i])+"\n")
    	print("m"+str(i+1)+"="+str(m[i])+"\n")

if __name__ == "__main__":
    main()

