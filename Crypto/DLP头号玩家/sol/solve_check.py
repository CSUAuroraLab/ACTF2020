from hashlib import sha512
from Cryptodome.Util.number import *
for i in range(0,0xfffff):
    n=long_to_bytes(i)
    if(sha512(n).hexdigest()[:20]=="bf35aeb65acaf4a4d403"):
        print(i)
        break;
