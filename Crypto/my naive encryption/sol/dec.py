from Cryptodome.Util.number import *

def inv(u,v):
    u3,v3=u,v
    u1,v1=1,0
    while v3>0:
        q=u3//v3
        u1,v1=v1,u1-v1*q
        u3,v3=v3,u3-v3*q
    while u1<0:
        u1=u1+v
    return u1
    

k=[3,5,7,11,13,17,19,23,29,31,37,
    41,43,47,53,59,61,67,71,73,79,
    83,89,97,101,103,107,109,113,
    127,131,137,139,149,151,157,
    163,167,173,179,181,191,193,
    197,199,211,223,227,229,233,
    239,241,251]
n=1000
len_k=len(k)
cipher=[71, 37, 4, 242, 109, 227, 22, 207, 36, 5, 39, 87, 22, 155, 19, 5, 19, 36, 155, 36, 224, 2, 104, 155, 39, 2, 19, 241, 155, 70, 210, 241, 53, 5, 19, 39, 22, 70, 22, 210, 70, 75]

flag=0
len_cipher=len(cipher)
while(n>0):
    pointer=1001-n
    for i in range(len_cipher):
        #cipher[i]=(cipher[i]*k[((pointer+2)%len_k]+k[(pointer*7)%len_k])&0xff
        cipher[i]=((cipher[i]-k[(pointer*7)%len_k])*inv(k[(pointer+2)%len_k],0x100))&0xff
    n=n-1
for i in range(0,len_cipher):
    flag+=cipher[i]
    flag=flag<<8
flag=flag>>8
print(long_to_bytes(flag))
