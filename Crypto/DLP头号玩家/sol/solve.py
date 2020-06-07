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
#ACTF{2fc487b4-c1
#a5-423c-83a7-0d8
