# -*- coding:utf-8 *- 
 
def get_inverse(mu, p): 
 for i in range(1, p): 
  if (i*mu)%p == 1: 
   return i 
 return -1 
 
def get_gcd(zi, mu): 
 if mu: 
  return get_gcd(mu, zi%mu) 
 else: 
  return zi 
 
def get_np(x1, y1, x2, y2, a, p): 
 flag = 1  
 
 if x1 == x2 and y1 == y2: 
  zi = 3 * (x1 ** 2) + a  
  mu = 2 * y1 
 else: 
  zi = y2 - y1 
  mu = x2 - x1 
  if zi* mu < 0: 
   flag = 0   
   zi = abs(zi) 
   mu = abs(mu) 
 
 gcd_value = get_gcd(zi, mu)  
 zi = zi // gcd_value    
 mu = mu // gcd_value 
 inverse_value = get_inverse(mu, p) 
 k = (zi * inverse_value) 
 
 if flag == 0:     
  k = -k 
 k = k % p 
 x3 = (k ** 2 - x1 - x2) % p 
 y3 = (k * (x1 - x3) - y1) % p 
 return x3,y3 
 
def get_rank(x0, y0, a, b, p): 
 x1 = x0    
 y1 = (-1*y0)%p  
 tempX = x0 
 tempY = y0 
 n = 1 
 while True: 
  n += 1 
  p_x,p_y = get_np(tempX, tempY, x0, y0, a, p) 
  if p_x == x1 and p_y == y1: 
   return n+1 
  tempX = p_x 
  tempY = p_y 
 
def get_param(x0, a, b, p): 
 y0 = -1 
 for i in range(p): 
  if i**2%p == (x0**3 + a*x0 + b)%p: 
   y0 = i 
   break 
 
 if y0 == -1: 
  return False 
  
 x1 = x0 
 y1 = (-1*y0) % p 
 return x0,y0,x1,y1 
