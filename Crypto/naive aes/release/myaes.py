import sys
from Cryptodome.Util.number import *
from binascii import hexlify
from secret import flag
from hashlib import sha512
 
def pow_check():
    n=getRandomRange(0,0xfffff)
    s=sha512(long_to_bytes(n)).hexdigest()
    print("Enter number n so that sha512(long_to_bytes(n)).hexdigest()[:20]={}".format(s[:20]))
    m=input()
    if(int(m)!=n):
        exit(0)

def substitute(hexBlock):
    substitutedHexBlock = ""
    substitution =  [8, 4, 15, 9, 3, 14, 6, 2, 
                    13, 1, 7, 5, 12, 10, 11, 0]
    for hexDigit in hexBlock:
        newDigit = substitution[int(hexDigit, 16)]
        substitutedHexBlock += hex(newDigit)[2:]
    return substitutedHexBlock

def pad(message):
    numBytes = 4-(len(message)%4)
    return message + numBytes * chr(numBytes)

def hexpad(hexBlock):
    numZeros = 8 - len(hexBlock)
    return numZeros*"0" + hexBlock

def permute(hexBlock):
    permutation =   [6, 22, 30, 18, 29, 4, 23, 19, 
                    15, 1, 31, 11, 28, 14, 25, 2, 
                    27, 12, 21, 26, 10, 16, 0, 24,
                     7, 5, 3, 20, 13, 9, 17, 8]
    block = int(hexBlock, 16)
    permutedBlock = 0
    for i in range(32):
        bit = (block & (1 << i)) >> i
        permutedBlock |= bit << permutation[i]
    return hexpad(hex(permutedBlock)[2:])

def round(hexMessage):
    numBlocks = len(hexMessage)//8
    substitutedHexMessage = ""
    for i in range(numBlocks):
        substitutedHexMessage += substitute(hexMessage[8*i:8*i+8])
    permutedHexMessage = ""
    for i in range(numBlocks):
        permutedHexMessage += permute(substitutedHexMessage[8*i:8*i+8])
    return permutedHexMessage



def main():
    pow_check()
    hexMessage = str(hexlify(str.encode(pad(str(flag)))), "ascii")
    
    for i in range(10000):
        hexMessage = round(hexMessage)
    print (hexMessage)
    
if __name__ == "__main__":
    try:
        main()
    except:
        throw
        print("The programme is exiting. If you are not WRONG, please contact admin.")
        
