import random
res=[112, 67, 69, 114, 66, 119, 44, 122, 63]
# for i in range(9):
#     res.append(random.randint(30,128))
# print(res)
check="curiosity"
key=[]

for i in range(len(res)):
    key.append(res[i]^ord(check[i]))

print("key:",key )
flag="Th&_Septem_pe<<atA_m0rt@|ia"
asm_flag=[]
intflag=[]
print(len(flag))
for i in range(len(flag)):
    intflag.append(ord(flag[i]))
    asm_flag.append(ord(flag[i])^key[i%9])

print(asm_flag)