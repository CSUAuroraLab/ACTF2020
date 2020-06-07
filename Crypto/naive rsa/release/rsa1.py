#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from Cryptodome.Util.number import *
import random
from flag import FLAG


p=getPrime(516)
q=getPrime(508)
if(p<q):
    tmp=p
    p=q;
    q=tmp

print(p%q)
N=p*q
print(N)
e=65537
enc = pow(FLAG,e,N)
print (enc)



