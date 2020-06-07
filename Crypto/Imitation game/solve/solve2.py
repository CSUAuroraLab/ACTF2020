from Crypto.Util.number import *
import os
ciphers=[[235, 27, 85, 73, 54, 39, 66, 73, 23, 59, 56, 10, 21, 0, 58, 37, 66, 90, 16],
[235, 79, 82, 28, 52, 54, 24, 45, 53, 63, 111, 69, 13, 72, 111, 52, 13, 13, 13],
[234, 64, 15, 110, 23, 121, 78, 48, 51, 123, 104, 27, 9, 24, 46, 117, 67, 10, 25],
[237, 0, 26, 1, 32, 32, 73, 123, 33, 63, 33, 26, 94, 83, 55, 52, 1, 67, 86],
[247, 6, 6, 13, 45, 114, 83, 43, 124, 50, 106, 30, 28, 67, 106, 53, 8, 12, 15],
[235, 27, 85, 77, 51, 55, 16, 39, 118, 109, 48, 28, 83, 79, 34, 60, 78, 89, 26],
[253, 89, 81, 6, 37, 50, 8, 42, 57, 41, 110, 94, 31, 65, 111, 52, 16, 10, 27],
[246, 21, 19, 6, 54, 45, 27, 43, 55, 121, 127, 13, 27, 66, 102, 33, 28, 6, 78],
[235, 26, 4, 15, 59, 45, 28, 49, 108, 109, 55, 18, 19, 13, 33, 36, 11, 28, 7],
[184, 83, 8, 92, 65, 9, 70, 34, 92, 21, 44, 24, 29, 14, 55, 103, 94, 82, 10]]
getiv=108
def decrypt(iv,cipher):
    padding=[iv]
    len_flag=len(ciphers[0])
    message=[cipher[0]^padding[0]]
    for i in range(1,len_flag):
        padding.append(cipher[i-1]^padding[i-1])
        message.append(cipher[i]^padding[i])
    mess=message[0]
    for i in range(1,len_flag):
        mess=mess<<8
        mess+=message[i]
    return mess

v=[(getiv+1),(getiv+1)|0x80]
for i in range(0,2):
    iv=v[i]
    f=open('cipher.txt','w')
    for cipher in ciphers:
        message=decrypt(iv,cipher)
        f.writelines(hex(message)[2:]+'\n')
    os.system('mtp cipher.txt')
    f.close
