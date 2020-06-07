## ACTF2020密码学部分writeup

#### 入门题

##### Column Permutation Cipher：[题目目录](Column Permutation Cipher)

简单的矩阵换位密码，首先统计字段长度为625，由于题目中告诉我们是m*n举证换位，所以m,n的可能值是(5,125),(25,25),(125,5)，然后爆破即可，示例脚本: 

```python
#-*- coding=UTF-8 -*-
possiblelen=[5,25,125]
for k in possiblelen:
    plaintext=""
    line=625//k
    for i in range(k):
        for j in range(line):
            plaintext+=cipher[j*k+i]
    print(plaintext)
```

##### 我的密码本: [题目目录](我的密码本)

统计英文文本中每个字符的出现频率，并查找概率表进行对比。当然其中需要用到一些英文知识，一般这种题目语义都是连贯的，一定要注意最后解出来的明文语义上是否通顺。

![image-20200529003238548](images\image-20200529003238548.png)

如果你统计好词频并确定了明文-密文对以后，即可还原出原文。

```python
code_book="ㅡ贰ㅒㄱёㄴ伍ㅊあムг肆ンㅇэ叁йΣωθξ壹ㅣのл￥"
plaintext=""
for j in range(len(cipher)):
    flag=0
    for i in range(len(code_book)):
        if(cipher[j]==code_book[i]):
            plaintext+=str(chr(0x61+i))
            flag=1
    if(flag==0):
        plaintext+=cipher[j]
print(plaintext)

```

#### 简单题

##### bomb or boom：[题目目录](bomb or boom)

题目给出了5个压缩包文件和一个密码本，并告知我们5个压缩包只要破解4个就行。所以应该涉及到门限方案，这里虽然没有题目名，但是hint中给出来了，用的是bloom门限。这是一个（4,5）门限，消息被5个随机模数求模，得到a<sub>i</sub>和m<sub>i</sub>。并被封装在五个压缩包中。

压缩包的密码被一些编码方式加密了，想了解这些编码方式请看[这里](https://www.cnblogs.com/mq0036/p/6544055.html)。

下面稍微解释一下这些有趣的编码，第一个是培根，第二个盲文，第三个用的是千千秀字的文本转音符（大可搜索一下，如何把文本加密为音符，仅此一家，ps.看着音符的样子难道不好看嘛），第四个是aaencode（学过web应该都知道的吧），第五个是brainfuck，参考一下资料即可。

然后用门限方案的脚本直接跑，就可以辽

```python
import math
from Cryptodome.Util.number import *
import gmpy2
def re(w1,m1):#乘法逆
	t1=w1
	t2=m1
	i=0
	s=[]
	while(t1):
		y=t2%t1
		s.append(int(t2//t1))
		t2=t1
		t1=y
	re1= 0
	re2= 1
	i=len(s)-2	
	while(i>=0):
		t=re2
		re2=re1*1-re2*s[i]
		re1=t
		i-=1
	return re2
def debloom(k):
    x=[]
    m=[]
    for i in range(0,k):
        print("inputs x"+str(i+1)+" and m"+str(i+1)+":")
        x.append(int(input()))
        m.append(int(input()))
    Mn=1
    for i in range(0,k):
        Mn=Mn*m[i]

    w=[]
    for i in range(0,k):
        w.append(int(Mn//m[i]))
    t=[]
    for i in range(0,k):
        t.append(re(w[i],m[i]))
    result=0#初始化
    for i in range(0,k):
        result+=(w[i]*t[i]*x[i])
    result=result%Mn
    print(long_to_bytes(result))

print("input bloom k:")
k=int(input())
debloom(k)

```

运行结果：

![解密图片](images\解密图片.png)

##### naive encryption: [题目链接](my naive encryption)

一道改装后的仿射密码题，只不过采用了不同的a,b进行了更多的轮加密，所以说这道题目更像是算法逆向。关键知识是乘法逆。解题脚本如下：

```python
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

```

##### naive rsa：[题目链接](naive rsa)

本来这道题目我已经出好推送想送分的，但不料推送还没轮到我，所以没发出来，希望大家多多支持“中南极光网安实验室”的公众号，支持痛并快乐着的作品。

回到题目，这是一道简单的coppersmith，主要问题出在getPrime函数和给出的p%q上。p是520位素数，q是500位素数，所以p//q就在2<sup>19</sup>到2<sup>21</sup>之间，我们假设p//q=k，p%q=a，那么p=kq+a，那么我们只需要在2<sup>19</sup>到2<sup>21</sup>之间爆破k即可，脚本如下：

```python
import gmpy2
from Cryptodome.Util.number import *
a=int(input())
N=int(input())
c=int(input())
e=65537
for k in range(2**19,2**21):
    #print(gmpy2.iroot(k*k+4*N, 2)[0])
    q = (-a + gmpy2.iroot(a*a+4*k*N, 2)[0])//(2*k)
    p = k*q+a
    #print(k)
    if(p*q==N):
        #print (k)
        phi = (p-1)*(q-1)
        d = gmpy2.invert(e,phi)
        m = pow(c,d,N)
        print (long_to_bytes(m))
        break

```

#### 中等题

##### Imitation game：[题目链接](Imitation game)

由于在密码学实验期间，我发现基本没有同学完成mtp的实验，所以在这里稍微加深了一下mtp以后形成了新的题目。这道题目和一般的mtp的区别就是，这里对密钥进行了类似于CBC的块加密，代码如下：

```python
def encrypt(iv,message):
    padding=[iv]   
    cipher=[message[0]^padding[0]]
    for i in range(1,len_flag):
        #print(cipher)
        padding.append(cipher[i-1]^padding[i-1])
        cipher.append(message[i]^padding[i])
    print("cipher={}".format(cipher))
```

但是由于初始iv范围很小，而且它嵌入到了密钥的每一个字节中，所以我们只需要爆破iv就可以得到明文。甚至我们可以知道密钥最后一位是"}"，直接与mtp后得到的密钥异或就知道iv值了。然后整个密钥每个字节异或iv就得到明文。

而对于mtp，题目中已经给出，密文都来自于书本原句，即可见字符，那么我们只需要通过限定课件字符的范围就可以排除很多无关答案。这里推荐python的mtp包，效果很棒，运行截图如下：

![样例-得到的key每一位异或0xab即可](images\样例-得到的key每一位异或0xab即可.png)

得到的key不是最后的key，但是0xd6^b'}'=0xab，所以对每一位异或0xab即可得到明文。

##### naive aes：[题目链接](naive aes)

又是一道算法逆向题。

from： [nactf——Super Duper AES](https://ctftime.org/task/9330 )

writeup: [detail link]( https://seymour.hackstreetboys.ph/chals/ctf/2019_NACTF/crypto/5_Super_Duper_AES.html )

all you need is to:

1.Reverse the **permute()** function.

2.Reverse the **substitute()** function.

3.Put everything together and run the script.

Isn't it easy?

##### tiny_PRNG0: [题目链接](tiny_PRNG0)

出题人：[DJ](csuwangj.github.io)

出题人只给了我脚本，不过mt19937最近的CTF题目很多，大家可以参考这个[博客](https://blog.wuhao13.xin/1245.html )。

基本思想：根据输出的随机数逆向extract_number对应的状态，实际上只需要前624个随机数恢复前624个state，就可以预测此后生成的随机数。 脚本：

1.mt19937.py

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def inv_right_shift(v, b, m):
    '
        >>> from cryptonita.attacks.prng import inv_right_shift
        >>> y, b, m = 524889969, 11, 0x010101
        >>> v = y ^ ((y >> b) & m)
        >>> inv_right_shift(v, b, m)
        524889969
        >>> y, b, m = 0xffffffff, 4, 0xffffffff
        >>> v = y ^ ((y >> b) & m)
        >>> inv_right_shift(v, b, m)
        4294967295
    '
    assert 0 < b < 32

    g = 0
    i = 0
    while i < 32:
        g = v ^ ((g >> b) & m)
        i += b

    return g

def inv_left_shift(v, b, m):
    '
        >>> from cryptonita.attacks.prng import inv_left_shift
        >>> y, b, m = 524889969, 3, 0x010101
        >>> v = y ^ ((y << b) & m)
        >>> inv_left_shift(v, b, m)
        524889969
        >>> y, b, m = 0xffffffff, 4, 0xffffffff
        >>> v = y ^ ((y << b) & m)
        >>> inv_left_shift(v, b, m)
        4294967295
    '
    assert 0 < b < 32

    g = 0
    i = 0
    while i < 32:
        g = v ^ ((g << b) & m)
        i += b

    return g

def clone_mt19937(out):
    '   Clone the internal state of a Mersenne Twister 19937 (MT19937)
        from its output <out>.
        For MT19937 we need 624 sequential bytes at minimum to clone
        the state.
            >>> from cryptonita.attacks.prng import clone_mt19937
            >>> clone_mt19937(B('abc'))           # byexample: +norm-ws
            Traceback <...>
            ValueError: You need at least 624 bytes to clone the MT19937 PRNG
                        but you have only 3.
        With 624+n, the first 624 are used to clone the
        MT19937's state and the next byte is used to validate.
        If the validation fails, "shift to the right one byte": the first
        byte is ignored, the next 624 bytes are used to re-clone the state
        and the next byte is used to validate the generator.
        The process continues until one validation success or until reach the
        end of the string.
        The last cloned MT19937 cannot be validated.
        Given 624 bytes only, no validation is performed; given 624*2 bytes,
        it is guaranteed that a valid clone can be found.
        '

    n = 624
    if len(out) < n:
        raise ValueError(("You need at least %i bytes to clone the MT19937 PRNG" +\
                          " but you have only %i.") % (n, len(out)))

    u, d = 11, 0xffffffff
    s, b = 7, 0x9d2c5680
    t, c = 15, 0xefc60000
    l = 18

    state = []
    for y in out:
        y = inv_right_shift(y, l, 0xffffffff)    # inv of y ^ ((y >> l) & 0)
        y = inv_left_shift(y, t, c)     # inv of y ^ ((y << t) & c)
        y = inv_left_shift(y, s, b)     # inv of y ^ ((y << s) & b)
        y = inv_right_shift(y, u, d)    # inv of y ^ ((y >> u) & d)

        state.append(y)

    found = False
    i = 0
    g = MT19937(0)
    g.reset_state(state[i:i+n], index=n)

    while i+n < len(out):
        v = g.extract_number()
        found = v == out[i+n]
        if found:
            g.reset_state(state[i:i+n], index=n)
            break

        i += 1
        g.reset_state(state[i:i+n], index=n)

    return g

# https://en.wikipedia.org/wiki/Mersenne_Twister
class MT19937:
    def __init__(self, seed):
        w, n, m, r = 32, 624, 397, 31
        a, f = 0x9908b0df, 1812433253
        W = 0xffffffff
        u, d = 11, 0xffffffff
        s, b = 7, 0x9d2c5680
        t, c = 15, 0xefc60000
        l = 18

        # Create a length n array to store the state of the generator
        self.MT = MT = [] # n size
        self.index = n+1
        lower_mask = (1 << r) - 1
        upper_mask = (~lower_mask) & W

        # Initialize the generator from a seed
        index = n
        MT.append(seed)
        for i in range(1, n):
            MT.append((f * (MT[i-1] ^ (MT[i-1] >> (w-2))) + i) & W)


        # Generate the next n values from the series x_i
        def twist():
            for i in range(n):
                 x = (MT[i] & upper_mask) \
                           + (MT[(i+1) % n] & lower_mask)

                 xA = x >> 1
                 if (x % 2) != 0:  # lowest bit of x is 1
                     xA = xA ^ a

                 MT[i] = MT[(i + m) % n] ^ xA

            self.index = 0

        # Extract a tempered value based on MT[index]
        # calling twist() every n numbers
        def extract_number():
            while 1:
                if self.index >= n:
                    twist()

                y = MT[self.index]
                y = y ^ ((y >> u) & d)
                y = y ^ ((y << s) & b)
                y = y ^ ((y << t) & c)
                y = y ^ (y >> l)

                self.index += 1
                yield y & W

        self.extract_number = extract_number

    def reset_state(self, MT, index=0):
        assert len(MT) == len(self.MT)

        self.index = index
        if not (0 <= self.index <= len(MT)):
            raise IndexError("Setting index=%i is out of range" \
                    % (self.index))

        self.MT[:] = MT

    def __iter__(self):
        return self.extract_number()
```

2.exp.py

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sys import argv
from typing import List
from tqdm import tqdm
from mt19937 import clone_mt19937
import re 
from pwn import (
    process,
    remote,
    log,
    # context
)
# context.log_level = "DEBUG"


def get_output(io, size):
    output = []
    with tqdm(total=size) as bar:
        while len(output) < size:
            io.sendlineafter("> ", "1")
            line = io.recvline().decode("utf-8")
            output += list(map(int, line.strip().split(" ")))
            bar.update(10)
    bar.close()
    return output

def main():
    if len(argv) == 1:
        io = process("./a.out")
    else:
        io = remote(argv[1], int(argv[2]))
    log.info("get output from mt19937")
    out = get_output(io, 640)
    log.info("clone mt19937 from output")
    new_iter = iter(clone_mt19937(out))
    io.sendline("2")
    log.info("send answer")
    io.sendline(str(next(new_iter)))
    s = str(io.recvuntil("4) "))
    s = str(io.recvuntil("4) "))
    log.success(re.search("ACTF{.*}", s).group(0))

if __name__ == "__main__":
    main()
```

#### 难题

##### DLP头号玩家：[题目链接](DLP头号玩家)

这道题主要是想考察离散对数问题，设计的考点有：如何计算离散对数，ElGamal算法，ecc算法。

level1:计算离散对数

采用大步小步法即可。

level2：ElGamal算法

首先，这里的密钥是两个字节的（见下面代码），可以直接考虑爆破：

```python
d=bytes_to_long(message[0:2])
```

然后根据密钥进行ElGamal算法解密即可。

level3：ECC算法

先回顾一下ECC算法

![1](images\1.png)

这里我在具体代码中做了一些手脚，令k=100,d=100，把100当成常量嵌入到了kG的运算中，所以其实解密的时候只需要代入d=100,k=100即可。

解题脚本示例如下(省略交互)：

```python
from math import ceil,sqrt
from Cryptodome.Util.number import *
from ecc import get_inverse,get_gcd,get_np,get_ng
def bsgs(g, y, p):
    res = []
    m = int(ceil(sqrt(p - 1)))
    S = {pow(g, j, p):j for j in range(m)}
    gs = pow(g, p - 1 - m, p)
    for i in range(m):
        if y in S:
            res.append(i * m + S[y])
        y = y * gs % p
    return res

def get_inverse(u,v):
    u3,v3=u,v
    u1,v1=1,0
    while v3>0:
        q=u3//v3
        u1,v1=v1,u1-v1*q
        u3,v3=v3,u3-v3*q
    while u1<0:
        u1=u1+v
    return u1

#level1
p=5391644857
g=2
c1=[4908063849,1283736637,4385640372,428852363]
for i in range(len(c1)):
    inp=c1[i]
    c=int(inp)
    res=bsgs(g,c,p)
    for i in res:
        print(long_to_bytes(i))

#level2
e,g,p=(2685568775701283525351462610033561666387306287538522499134808519515971408889570947875407095838440735098786110848850070468375238474921045086123009358906,
       2,
       3108147961599785276150798080269087679501293709501455568774725039866085754219397531303169017523045103124751042601841840328290404343235853405579539233773)
a,b=(1968486588460454870108621075441203470309302694739442500606039058477890260262954690597523764122825500774397066089804125306327432806567312924827814647950,
     1024812622664084668424411594448713407303536660751692688061972897584163822765150299422248209733371319297760175591974882337903320853550670045641950256872)
       
for i in range(2**16):
    if(pow(g,i,p)==e):
        print(long_to_bytes(i))
        d=i
inv=get_inverse(a,p)
m2=(b*pow(inv,d,p))%p
print(long_to_bytes(m2))

#level3
cipher=[[414,131,27744],
        [249,291,27612],
        [26,255,26656],
        [452,278,31968],
        [78,308,17034],
        [319,33,15400],
        [598,457,51200],
        [310,478,2695],
        [307,739,5500],
        [397,455,89500]
        ]
p=769
a=23
b=711

key=100
k=100
for ci in cipher:
    kG=[0,0]
    kG[0],kG[1]=get_ng(ci[0], ci[1] , k, a, p) 
    decrypto_text_x,decrypto_text_y = get_ng(kG[0], kG[1] , key, a, p)
    print(chr(ci[2]//decrypto_text_x),end="") 
```

##### tiny_PRNG1：[题目链接](tiny_PRNG1)

出题人：[DJ](csuwangj.github.io)

主要是对xoroshiro128plus随机数发生器，[参考资料](https://github.com/lemire/crackingxoroshiro128plus/blob/master/xoroshiftall.py )

直接放解题脚本：

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, z3
from sys import argv
from typing import List
from pwn import (
    process,
    remote,
    log,
    # context
)
from Crypto.Util.number import long_to_bytes
# context.log_level = "DEBUG"
bit64 = 0xffffffffffffffff

def LShL(x, n): return (x << n) & bit64

def xo128(x, y, LShR = lambda x,i: x>>i):
    y ^= x
    return y ^ LShL(y, 14) ^ (LShL(x,55)|LShR(x,9)), (LShL(y,36)|LShR(y,28))

def get_output(io, size):
    output = []
    with tqdm(total=size) as bar:
        while len(output) < size:
            io.sendlineafter("> ", "1")
            line = io.recvline().decode("utf-8")
            output += list(map(int, line.strip().split(" ")))
            bar.update(10)
    bar.close()
    return output

def main():
    if len(argv) == 1:
        io = process("./a.out")
    else:
        io = remote(argv[1], int(argv[2]))
    log.info("get output")
    out = get_output(io, 10)
    x0, y0 = z3.BitVecs('x0 y0', 64)
    x, y = x0, y0
    s = z3.SimpleSolver()
    
    for v in out:
        s.add((x + y) & bit64 == v)
        x, y = xo128(x, y, z3.LShR)
    
    ans = []

    for i in range(1, sys.maxsize):
        if s.check().r != 1: break  # quit if failed
        soln = s.model()
        x, y = (soln[i].as_long() for i in (x0,y0))
        ans += ["ACTF{" 
            + long_to_bytes(x).decode("utf-8")[::-1]
            + long_to_bytes(y).decode("utf-8")[::-1]
            + "}"]
        for j in range(10):
            x, y = xo128(x, y)
        s.add( z3.Or(x0 != soln[x0], y0 != soln[y0]) )
    
    for a in ans:
        log.info("possible flag: " + a)

if __name__ == "__main__":
    main()
```

