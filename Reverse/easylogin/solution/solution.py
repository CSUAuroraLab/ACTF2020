import random
param=[]
for i in range(10):
    param.append(str(i))

for i in range(26):
    param.append(chr(ord('a')+i))
    param.append(chr(ord('A')+i))

print(param)
usr="Hades"
encode1=[]
mark=0
for i in usr:
    encode1.append((ord(i)+1)^mark)
    mark=ord(i)

print(encode1)
passwd="Y0U_<a^_Alw@ys_7ru&t_BruTe_Force"
rand=[26, 15, 31, 80, 81, 24, 39, 56, 37, 31, 112, 124, 64, 27, 31, 106, 39, 121]
enc2=[]
mark=0
for k in passwd:
    tmp=ord(k)
    enc2.append(~(tmp&rand[mark])&(tmp|rand[mark]))
    mark=(mark+1)%18
print("enc2:",enc2)
enc3=[]
for i in range(18):
    enc3.append(rand[i]^ord(usr[i%5]))
print("enc3:",enc3)
for i in range(32):
    for j in range(1,128):
        if enc2[i]==(~(j&rand[i%18])&(j|rand[i%18])):
            print(i,j)