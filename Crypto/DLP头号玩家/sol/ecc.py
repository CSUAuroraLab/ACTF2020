# -*- coding:utf-8 *- 
# author: DYBOY 
# reference codes: https://blog.dyboy.cn/websecurity/121.html 
# description: ECC椭圆曲线加密算法实现 
""" 
 考虑K=kG ，其中K、G为椭圆曲线Ep(a,b)上的点，n为G的阶（nG=O∞ ），k为小于n的整数。 
 则给定k和G，根据加法法则，计算K很容易但反过来，给定K和G，求k就非常困难。 
 因为实际使用中的ECC原则上把p取得相当大，n也相当大，要把n个解点逐一算出来列成上表是不可能的。 
 这就是椭圆曲线加密算法的数学依据 
 点G称为基点（base point） 
 k（k<n）为私有密钥（privte key） 
 K为公开密钥（public key) 
""" 
 
def get_inverse(mu, p): 
 """ 
 获取y的负元 
 """ 
 for i in range(1, p): 
  if (i*mu)%p == 1: 
   return i 
 return -1 
 
def get_gcd(zi, mu): 
 """ 
 获取最大公约数 
 """ 
 if mu: 
  return get_gcd(mu, zi%mu) 
 else: 
  return zi 
 
def get_np(x1, y1, x2, y2, a, p): 
 """ 
 获取n*p，每次+p，直到求解阶数np=-p 
 """ 
 flag = 1 # 定义符号位（+/-） 
 
 # 如果 p=q k=(3x2+a)/2y1mod p 
 if x1 == x2 and y1 == y2: 
  zi = 3 * (x1 ** 2) + a # 计算分子  【求导】 
  mu = 2 * y1 # 计算分母 
 
 # 若P≠Q，则k=(y2-y1)/(x2-x1) mod p 
 else: 
  zi = y2 - y1 
  mu = x2 - x1 
  if zi* mu < 0: 
   flag = 0  # 符号0为-（负数） 
   zi = abs(zi) 
   mu = abs(mu) 
 
 # 将分子和分母化为最简 
 gcd_value = get_gcd(zi, mu)  # 最大公約數 
 zi = zi // gcd_value   # 整除 
 mu = mu // gcd_value 
 # 求分母的逆元 逆元： ∀a ∈G ，ョb∈G 使得 ab = ba = e 
 # P(x,y)的负元是 (x,-y mod p)= (x,p-y) ，有P+(-P)= O∞ 
 inverse_value = get_inverse(mu, p) 
 k = (zi * inverse_value) 
 
 if flag == 0:     # 斜率负数 flag==0 
  k = -k 
 k = k % p 
 # 计算x3,y3 P+Q 
 """ 
  x3≡k2-x1-x2(mod p) 
  y3≡k(x1-x3)-y1(mod p) 
 """ 
 x3 = (k ** 2 - x1 - x2) % p 
 y3 = (k * (x1 - x3) - y1) % p 
 return x3,y3 
 
def get_rank(x0, y0, a, b, p): 
 """ 
 获取椭圆曲线的阶 
 """ 
 x1 = x0    #-p的x坐标 
 y1 = (-1*y0)%p  #-p的y坐标 
 tempX = x0 
 tempY = y0 
 n = 1 
 while True: 
  n += 1 
  # 求p+q的和，得到n*p，直到求出阶 
  p_x,p_y = get_np(tempX, tempY, x0, y0, a, p) 
  # 如果 == -p,那么阶数+1，返回 
  if p_x == x1 and p_y == y1: 
   return n+1 
  tempX = p_x 
  tempY = p_y 
 
def get_param(x0, a, b, p): 
 """ 
 计算p与-p 
 """ 
 y0 = -1 
 for i in range(p): 
  # 满足取模约束条件，椭圆曲线Ep(a,b)，p为质数，x,y∈[0,p-1] 
  if i**2%p == (x0**3 + a*x0 + b)%p: 
   y0 = i 
   break 
 
 # 如果y0没有，返回false 
 if y0 == -1: 
  return False 
 
 # 计算-y（负数取模） 
 x1 = x0 
 y1 = (-1*y0) % p 
 return x0,y0,x1,y1 
 
def get_graph(a, b, p): 
 """ 
 输出椭圆曲线散点图 
 """ 
 x_y = [] 
 # 初始化二维数组 
 for i in range(p): 
  x_y.append(['-' for i in range(p)]) 
 
 for i in range(p): 
  val =get_param(i, a, b, p) # 椭圆曲线上的点 
  if(val != False): 
   x0,y0,x1,y1 = val 
   x_y[x0][y0] = 1 
   x_y[x1][y1] = 1 
 
 print("椭圆曲线的散列图为：") 
 for i in range(p):    # i= 0-> p-1 
  temp = p-1-i  # 倒序 
 
  # 格式化输出1/2位数，y坐标轴 
  if temp >= 10: 
   print(temp, end=" ") 
  else: 
   print(temp, end=" ") 
 
  # 输出具体坐标的值，一行 
  for j in range(p): 
   print(x_y[j][temp], end=" ") 
  print("") #换行 
 
 # 输出 x 坐标轴 
 print(" ", end="") 
 for i in range(p): 
  if i >=10: 
   print(i, end=" ") 
  else: 
   print(i, end=" ") 
 print('\n') 
 
def get_ng(G_x, G_y, key, a, p): 
 """ 
 计算nG 
 """ 
 temp_x = G_x 
 temp_y = G_y 
 while key != 1: 
  temp_x,temp_y = get_np(temp_x,temp_y, G_x, G_y, a, p) 
  key -= 1 
 return temp_x,temp_y 
 
def ecc_main(): 
 while True: 
  a = int(input("请输入椭圆曲线参数a(a>0)的值：")) 
  b = int(input("请输入椭圆曲线参数b(b>0)的值：")) 
  p = int(input("请输入椭圆曲线参数p(p为素数)的值：")) #用作模运算 
 
  # 条件满足判断 
  if (4*(a**3)+27*(b**2))%p == 0: 
   print("您输入的参数有误，请重新输入！！！\n") 
  else: 
   break 
 
 # 输出椭圆曲线散点图 
 get_graph(a, b, p) 
 
 # 选点作为G点 
 print("user1：在如上坐标系中选一个值为G的坐标") 
 G_x = int(input("user1：请输入选取的x坐标值：")) 
 G_y = int(input("user1：请输入选取的y坐标值：")) 
 
 # 获取椭圆曲线的阶 
 n = get_rank(G_x, G_y, a, b, p) 
 
 # user1生成私钥，小key 
 key = int(input("user1：请输入私钥小key（<{}）：".format(n))) 
 
 # user1生成公钥，大KEY 
 KEY_x,kEY_y = get_ng(G_x, G_y, key, a, p) 
 
 # user2阶段 
 # user2拿到user1的公钥KEY，Ep(a,b)阶n，加密需要加密的明文数据 
 # 加密准备 
 k = int(input("user2：请输入一个整数k（<{}）用于求kG和kQ：".format(n))) 
 k_G_x,k_G_y = get_ng(G_x, G_y, k, a, p)       # kG 
 k_Q_x,k_Q_y = get_ng(KEY_x, kEY_y, k, a, p)      # kQ 
 
 # 加密 
 plain_text = input("user2：请输入需要加密的字符串:") 
 plain_text = plain_text.strip() 
 #plain_text = int(input("user1：请输入需要加密的密文：")) 
 c = [] 
 print("密文为：",end="") 
 for char in plain_text: 
  intchar = ord(char) 
  cipher_text = intchar*k_Q_x 
  c.append([k_G_x, k_G_y, cipher_text]) 
  print("({},{}),{}".format(k_G_x, k_G_y, cipher_text),end="-") 
 
 
 # user1阶段 
 # 拿到user2加密的数据进行解密 
 # 知道 k_G_x,k_G_y，key情况下，求解k_Q_x,k_Q_y是容易的，然后plain_text = cipher_text/k_Q_x 
 print("\nuser1解密得到明文：",end="") 
 for charArr in c: 
  decrypto_text_x,decrypto_text_y = get_ng(charArr[0], charArr[1], key, a, p) 
  print(chr(charArr[2]//decrypto_text_x),end="") 
 
if __name__ == "__main__": 
 print("*************ECC椭圆曲线加密*************") 
 ecc_main() 
