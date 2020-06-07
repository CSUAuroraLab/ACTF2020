from Cryptodome.Util.number import *
from secret import flag,book
from Cryptodome.Util.strxor import strxor
from hashlib import sha512
 
def pow_check():
    n=getRandomRange(0,0xfffff)
    s=sha512(long_to_bytes(n)).hexdigest()
    print("Enter number n so that sha512(long_to_bytes(n)).hexdigest()[:20]={}".format(s[:20]))
    m=input()
    if(int(m)!=n):
        exit(0)

len_flag=len(flag)

def encrypt(iv,message):
    padding=[iv]   
    cipher=[message[0]^padding[0]]
    for i in range(1,len_flag):
        #print(cipher)
        padding.append(cipher[i-1]^padding[i-1])
        cipher.append(message[i]^padding[i])
    print("cipher={}".format(cipher))
    
def main():
    pow_check()
    iv=getRandomRange(1,0xff)
    Book_size=60000
    plaintext = []

    start_index=getRandomRange(0,Book_size-len_flag)
    textall = book[start_index:]
    for i in range(10):
        plaintext.append(textall[start_index: start_index+len_flag])
        start_index += len_flag
    for i in range(10):
        message=strxor(flag,plaintext[i])
        encrypt(iv,message)

if __name__ == "__main__":
    try:
        main()
    except:
        print("The programme is exiting. If you are not WRONG, please contact admin.")

