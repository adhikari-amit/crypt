from random import randint
import math

def generate_prime():
    x = randint(2, 50)
    while True:
        if is_prime(x):
            break
        else:
            x += 1
    return x

def is_prime(x):
    i = 2
    root = math.ceil(math.sqrt(x))
    while i <= root:
        if x % i == 0:
            return False
        i += 1
    return True

def gcd(a, b):
    while b:
        a, b = b, a%b
    return a

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a,m):
    g,x,y = egcd(a,m)
    if g != 1:
        return None
    else:
        return x%m

p = generate_prime()
while True:
    q = generate_prime()
    if q != p:
        break
   
while True:
    r = generate_prime()
    if r != p and r!=q:
        break
while True:
    s = generate_prime()
    if s != p and s!=q and s!=r:
        break

n = p * q * s *r
n1 = (p - 1) * (q - 1) *(s-1) *(r-1)

r6=int(math.log(n))
r2 = randint(r6,n1)
while True:
    if gcd(r2, n1) == 1:
        break
    else:
        r2 += 1
e = r2
d = modinv(e, n1)
#print("p=",p)
#print("q=",q)
#print("n=",n)
#print("e=",e)
#print("d=",d)
n=583
e=457
d=33
'''
print("p=",p)
print("q=",q)
print("n=",n)
print("e=",e)
print("d=",d)
'''
