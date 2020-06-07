from secret import flag,d
from math import ceil
from Cryptodome.Util.number import *
from ecc import get_inverse,get_gcd,get_np,get_rank,get_param
from hashlib import sha512
 
def pow_check():
    n=getRandomRange(0,0xfffff)
    s=sha512(long_to_bytes(n)).hexdigest()
    print("Enter number n so that sha512(long_to_bytes(n)).hexdigest()[:20]={}".format(s[:20]))
    m=input()
    if(int(m)!=n):
        exit(0)
        

def get_ng(G_x, G_y, a, p): 
 temp_x = G_x 
 temp_y = G_y
 i=100
 while i != 1: 
  temp_x,temp_y = get_np(temp_x,temp_y, G_x, G_y, a, p) 
  i -= 1 
 return temp_x,temp_y 

def level1(message):
    p=getPrime(33)
    print("p={}".format(p))
    g=2
    for i in range(0,ceil(len(message)/4)):
        y=bytes_to_long(message[i*4:4+i*4])
        print("c={}".format(pow(g,y,p)))
    #print(str(message)[2:-1])
    i=input("please input the message:")
    if(str(message)[2:-1]!=i):
        print("Game Over!")
        exit(0)
    else:
        print("Pass!")

def level2(message):
    d=bytes_to_long(message[0:2])
    m=bytes_to_long(message[2:])
    g=2
    p=getPrime(500)
    e=pow(g,d,p)
    print("pubkey= ({},{},{})".format(e,g,p))
    k=getRandomRange(2,p-1)
    a=pow(g,k,p)
    b=(m*pow(e,k,p))%p
    print("cipher= ({},{})".format(a,b))
    #print(str(message)[2:-1])
    i=input("please input the message:")
    if(str(message)[2:-1]!=i):
        print("Game Over!")
        exit(0)
    else:
        print("Pass!")


def level3(message):
    p=getPrime(10)
    print("p={}".format(p))
    a=getRandomRange(1,p-1)
    b=getRandomRange(1,p-1)
    while (4*(a**3)+27*(b**2))%p == 0:
        a=getRandomRange(1,p-1)
        b=getRandomRange(1,p-1)
    print("a={}, b={}".format(a,b))
    leng=len(message)
    print("密文分别为：")
    k=0
    while(k<leng):
        while(True):
            i=getRandomRange(1,p-1)
            val =get_param(i, a, b, p) # 椭圆曲线上的点 
            if(val != False): 
               g1,g2,c,d = val
               if(k>leng/2):
                   g1=c
                   g2=d
               break
        n=get_rank(g1, g2, a, b, p)
        if(n>d):
            print("G=({},{})".format(g1,g2),end=",")
            KEY_x,kEY_y = get_ng(g1, g2, a, p) 
            k_G_x,k_G_y = get_ng(g1, g2, a, p)       # kG 
            k_Q_x,k_Q_y = get_ng(KEY_x, kEY_y, a, p) # kQ
            cipher_text = message[k]*k_Q_x 
            print("C={}".format(cipher_text)) 
            k+=1
        


    #print(str(message)[2:-1])
    i=input("please input the message:")
    if(str(message)[2:-1]!=i):
        print("Game Over!")
        exit(0)
    else:
        print("Pass!")

def main():
    pow_check()
    message1=flag[0:16]
    level1(message1)
    message2=flag[16:32]
    level2(message2)
    message3=flag[32:]
    level3(message3)
    print("Congratulation!")
if __name__ == "__main__":
    try:
        main()
    except:
        print("The programme is exiting. If you are not WRONG, please contact admin.")
