import random
from math import gcd
import os
'''快速模幂'''
def fast_times(N,a,b):
    A=1
    x=a
    if b<0:
        b=-b
        x=Era(a,N)[0]
    while b>0:
        if b%2==1:
            A=(A*x)%N
        b=b//2
        x=(x*x)%N
    return A
'''拓展欧氏算法'''       
def Era(a,b):
    if(a<0):
        a1=-a
        flag1=-1
    else:
        a1=a
        flag1=1;
    if(b<0):
        b1=-b
    else:
        b1=b
    r1=a1
    r2=b1
    s1=1
    s2=0
    t1=0
    t2=1
    while (r2!=0):
        q=r1//r2
        temp1=r1-q*r2
        temp2=s1-q*s2
        temp3=t1-q*t2
        r1=r2
        s1=s2
        t1=t2
        r2=temp1
        s2=temp2
        t2=temp3
    s1=s1*flag1
    while(s1<=0):
        s1+=b1//r1
    t1=((r1-s1*a)//b)
    return s1,t1,r1
'''大整数选取'''
def get_number(w):
    return random.randrange(2**(w-1),2**w)
'''素性检验'''
def Is_Prime(n):
    k=0
    temp=n-1
    while temp%2==0:
        temp//=2
        k+=1
    #print(temp,k)
    flag=0 #证据数量
    count=0
    if n<10:
        if n==2 or n==3 or n==5 or n==7 :
            #print("YES")
            return True
        else:
            #print("NO")
            return False
    while count<10:
        a=random.randint(2,n-1)
        #print(a)
        if n%2==0 or 1<gcd(a,n)<n:
            #print("NO")
            return False
        else:
            count+=1
            b=pow(a,temp,n)
            if(b!=1):
                s=1
                for i in range(0,k):
                    x=2**i
                    if pow(a,x*temp,n)==n-1:
                        s=0
                        break
                if(s==1):
                    flag+=1
    if(flag==10):
        #print("NO")
        return False
    else:
        #print("YES")
        return True
'''大素数选取'''
def getPrime(w):
    while True:
        res=get_number(w)
        if(Is_Prime(res)==True):
            return res
'''字节转整数'''
def bytes_to_int(n:bytes):
    return int.from_bytes(n,byteorder='big')
def int_to_bytes(n:int,n_len):
    return n.to_bytes(n_len, byteorder='big')
'''字符串/文件->int'''
def Words_to_Int(s):
    '''input check'''
    if os.path.isfile(s)==True:
        text=''
        with open(s,'r') as file:
            text+=file.read()
        return s2n(text)
    elif type(s)==str:
        return s2n(s)
    else:
        raise ValueError("the input is neither a file or a string!")


def s2n(s):
    r"""
    String to number (big endian).

    >>> s2n("BA")  # 0x4241
    16961
    >>> s2n(b'\x01\x00')
    256
    """
    if isinstance(s, str):
        s = s.encode("utf-8")
    return int.from_bytes(s, "big")


def n2s(n):
    r"""
    Number to string (big endian).

    >>> n2s(0x4241)
    b'BA'
    >>> n2s(0x100)
    b'\x01\x00'
    """
    nbits = len_in_bits(n)
    nbytes = (nbits + 7) >> 3
    return n.to_bytes(nbytes, "big")

def len_in_bits(n):
    """
    Return number of bits in binary representation of @n.
    Probably deprecated by .bit_length().
    """
    if not isinstance(n, int):
        raise TypeError("len_in_bits defined only for ints")
    return n.bit_length()
