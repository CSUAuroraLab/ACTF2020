from secret import flag
from Cryptodome.Util.number import *
from hashlib import sha512
 
def pow_check():
    n=getRandomRange(0,0xfffff)
    s=sha512(long_to_bytes(n)).hexdigest()
    print("Enter number n so that sha512(long_to_bytes(n)).hexdigest()[:20]={}".format(s[:20]))
    m=input()
    if(int(m)!=n):
        exit(0)

k=[3,5,7,11,13,17,19,23,29,31,37,
    41,43,47,53,59,61,67,71,73,79,
    83,89,97,101,103,107,109,113,
    127,131,137,139,149,151,157,
    163,167,173,179,181,191,193,
    197,199,211,223,227,229,233,
    239,241,251]
def main():
    pow_check()
    n=1000
    len_flag=len(flag)
    len_k=len(k)
    cipher=[]
    for i in range(len_flag):
        cipher.append(flag[i])
    while(n>0):
        for i in range(len_flag):
            cipher[i]=(cipher[i]*k[(n+2)%len_k]+k[(n*7)%len_k])&0xff
        n=n-1
    print("cipher={}".format(cipher))

if __name__ == "__main__":
    try:
        main()
    except:
        print("The programme is exiting. If you are not WRONG, please contact admin.")

        
        

    
