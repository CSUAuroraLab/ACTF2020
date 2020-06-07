from hashlib import sha512
from Cryptodome.Util.number import *
for i in range(0,0xfffff):
    n=long_to_bytes(i)
    if(sha512(n).hexdigest()[:20]=="ee1192a993eec0c12653"):#等号右边填上远程主机的输出
        print(i)
        break;
