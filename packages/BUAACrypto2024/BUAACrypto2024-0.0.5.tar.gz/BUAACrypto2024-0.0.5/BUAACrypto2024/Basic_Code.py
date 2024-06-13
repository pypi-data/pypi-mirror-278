from .cal import *
import hashlib
import random
import os
from math import ceil

class SM4Cipher:
    def __init__(self, key: bytes):
        if not len(key) == 16:
            raise ValueError("SM4 key must be length of 16. ")
        self._key_r = self._generate_key(key)
        self.block_size = 16
    '''填充后输出字节分组'''
    @staticmethod
    def padding(text):
        mes=[]
        x=16-(len(text)//2)%16
        for i in range(0,x):
            text+="{:0>2}".format(hex(x)[2:])
        #print(text)
        for i in range(0,len(text)//32):
            mes.append(bytes.fromhex(text[i*32:i*32+32]))
        return mes
    '''解密不填充'''
    @staticmethod
    def padding2(text):
        mes=[]
        if len(text)%32!=0:
            raise ValueError("the length of chiphertext is invalid")
        for i in range(0,len(text)//32):
            mes.append(bytes.fromhex(text[i*32:i*32+32]))
        return mes
    '''去填充'''
    @staticmethod
    def unpad(s):
        '''change to 17'''
        for i in range(1,17):
            flag=1
            x="{:0>2}".format(hex(i)[2:])
            for j in range(16-i,16):
                if s[j*2:j*2+2]!=x:
                    flag=0
                    break
            if flag==1:
                return s[:(16-i)*2]
        return s
    '''异或运算'''
    @staticmethod
    def add(a,b):
        return (bytes_to_int(a)^bytes_to_int(b)).to_bytes(16,byteorder='big')
    '''CBC IV'''
    def CBC_Import(self,IV:bytes):
        self.IV=IV
    
    def text_get(self,text,mode):
        if os.path.isfile(text)==True:
            s=''
            with open(text,'r',encoding='utf-8') as file:
                s+=file.read()
            if mode==1:
                mes=self.padding(hex(s2n(s))[2:])
            else:
                mes=self.padding2(hex(s2n(s))[2:]) 
        elif type(text)==bytes:
            n=int.from_bytes(text,byteorder='big')
            if mode==1:
                mes=self.padding(hex(n)[2:])
            else:
                mes=self.padding2(hex(n)[2:])
        elif type(text)==str:
            if mode==1:
                mes=self.padding(hex(s2n(text.encode('utf-8')))[2:])
            else:
                mes=self.padding2(text)
        else:
            raise ValueError("the input type of the text is not str,bytes,and file! ")
        return mes
    
    def encrypt(self, plaintext,mode='ECB'):
        mes=self.text_get(plaintext,1)
        #print(mes)
        chipher=''
        if mode=='ECB':
            for i in range(0,len(mes)):
                chipher+=self._do(mes[i],self._key_r).hex()
            return chipher
        elif mode=='CBC':
            for i in range(0,len(mes)):
                x=self.add(mes[i],self.IV)
                w=self._do(x,self._key_r).hex()
            #print(w)
                self.IV=bytes.fromhex(w)
                chipher+=w
            return chipher            
        else:
            raise ValueError("Wrong Encode Mode!")
    
    def decrypt(self, ciphertext,mode='ECB'):
        mes=self.text_get(ciphertext,0)
        chipher=''
        if mode=='ECB':
            for i in range(0,len(mes)):
                if i==len(mes)-1:
                    chipher+=self.unpad(self._do(mes[i],self._key_r[::-1]).hex())
                else:
                    chipher+=self._do(mes[i],self._key_r[::-1]).hex()
                
                #chipher+=self._do(mes[i],self._key_r[::-1]).hex()
            self.res=chipher
            return chipher
        elif mode=='CBC':
            for i in range(0,len(mes)):
                
                w=self._do(mes[i],self._key_r[::-1])
            #print(w)
                x=self.add(w,self.IV).hex()
                self.IV=mes[i]
                chipher+=x
            self.res=chipher
            return chipher
        else:
            raise ValueError("Wrong Decode Mode!")        
    
    def HexOut(self):
        return self.res
    def BytesOut(self):
        return bytes.fromhex(self.res)
    def StrOut(self):
        return bytes.fromhex(self.res).decode('utf-8')
    def _do(self, text: bytes, key_r: list):
        text_ = [0 for _ in range(4)]
        # 将 128bit 转化成 4x32bit
        for i in range(4):
            text_[i] = int.from_bytes(text[4 * i:4 * i + 4], 'big')
        for i in range(32):
            box_in = text_[1] ^ text_[2] ^ text_[3] ^ key_r[i]
            box_out = self._s_box(box_in)
            temp = text_[0] ^ box_out ^ self._rot_left(box_out, 2) ^ self._rot_left(box_out, 10)
            temp = temp ^ self._rot_left(box_out, 18) ^ self._rot_left(box_out, 24)
            text_ = text_[1:] + [temp]
        text_ = text_[::-1]  # 结果逆序
        # 将 4x32bit 合并成 128bit
        result = bytearray()
        for i in range(4):
            result.extend(text_[i].to_bytes(4, 'big'))
        return bytes(result)

    def _generate_key(self, key: bytes):
        """密钥生成"""
        key_r, key_temp = [0 for _ in range(32)], [0 for _ in range(4)]
        FK = [0xa3b1bac6, 0x56aa3350, 0x677d9197, 0xb27022dc]
        CK = [0x00070e15, 0x1c232a31, 0x383f464d, 0x545b6269, 0x70777e85, 0x8c939aa1, 0xa8afb6bd, 0xc4cbd2d9,
              0xe0e7eef5, 0xfc030a11, 0x181f262d, 0x343b4249, 0x50575e65, 0x6c737a81, 0x888f969d, 0xa4abb2b9,
              0xc0c7ced5, 0xdce3eaf1, 0xf8ff060d, 0x141b2229, 0x30373e45, 0x4c535a61, 0x686f767d, 0x848b9299,
              0xa0a7aeb5, 0xbcc3cad1, 0xd8dfe6ed, 0xf4fb0209, 0x10171e25, 0x2c333a41, 0x484f565d, 0x646b7279]
        # 将 128bit 拆分成 4x32bit
        for i in range(4):
            temp = int.from_bytes(key[4 * i:4 * i + 4], 'big')
            key_temp[i] = temp ^ FK[i]
        # 循环生成轮密钥
        for i in range(32):
            box_in = key_temp[1] ^ key_temp[2] ^ key_temp[3] ^ CK[i]
            box_out = self._s_box(box_in)
            key_r[i] = key_temp[0] ^ box_out ^ self._rot_left(box_out, 13) ^ self._rot_left(box_out, 23)
            key_temp = key_temp[1:] + [key_r[i]]
        return key_r

    @staticmethod
    def _s_box(n: int):
        BOX = [0xD6, 0x90, 0xE9, 0xFE, 0xCC, 0xE1, 0x3D, 0xB7, 0x16, 0xB6, 0x14, 0xC2, 0x28, 0xFB, 0x2C, 0x05, 0x2B,
               0x67, 0x9A, 0x76, 0x2A, 0xBE, 0x04, 0xC3, 0xAA, 0x44, 0x13, 0x26, 0x49, 0x86, 0x06, 0x99, 0x9C, 0x42,
               0x50, 0xF4, 0x91, 0xEF, 0x98, 0x7A, 0x33, 0x54, 0x0B, 0x43, 0xED, 0xCF, 0xAC, 0x62, 0xE4, 0xB3, 0x1C,
               0xA9, 0xC9, 0x08, 0xE8, 0x95, 0x80, 0xDF, 0x94, 0xFA, 0x75, 0x8F, 0x3F, 0xA6, 0x47, 0x07, 0xA7, 0xFC,
               0xF3, 0x73, 0x17, 0xBA, 0x83, 0x59, 0x3C, 0x19, 0xE6, 0x85, 0x4F, 0xA8, 0x68, 0x6B, 0x81, 0xB2, 0x71,
               0x64, 0xDA, 0x8B, 0xF8, 0xEB, 0x0F, 0x4B, 0x70, 0x56, 0x9D, 0x35, 0x1E, 0x24, 0x0E, 0x5E, 0x63, 0x58,
               0xD1, 0xA2, 0x25, 0x22, 0x7C, 0x3B, 0x01, 0x21, 0x78, 0x87, 0xD4, 0x00, 0x46, 0x57, 0x9F, 0xD3, 0x27,
               0x52, 0x4C, 0x36, 0x02, 0xE7, 0xA0, 0xC4, 0xC8, 0x9E, 0xEA, 0xBF, 0x8A, 0xD2, 0x40, 0xC7, 0x38, 0xB5,
               0xA3, 0xF7, 0xF2, 0xCE, 0xF9, 0x61, 0x15, 0xA1, 0xE0, 0xAE, 0x5D, 0xA4, 0x9B, 0x34, 0x1A, 0x55, 0xAD,
               0x93, 0x32, 0x30, 0xF5, 0x8C, 0xB1, 0xE3, 0x1D, 0xF6, 0xE2, 0x2E, 0x82, 0x66, 0xCA, 0x60, 0xC0, 0x29,
               0x23, 0xAB, 0x0D, 0x53, 0x4E, 0x6F, 0xD5, 0xDB, 0x37, 0x45, 0xDE, 0xFD, 0x8E, 0x2F, 0x03, 0xFF, 0x6A,
               0x72, 0x6D, 0x6C, 0x5B, 0x51, 0x8D, 0x1B, 0xAF, 0x92, 0xBB, 0xDD, 0xBC, 0x7F, 0x11, 0xD9, 0x5C, 0x41,
               0x1F, 0x10, 0x5A, 0xD8, 0x0A, 0xC1, 0x31, 0x88, 0xA5, 0xCD, 0x7B, 0xBD, 0x2D, 0x74, 0xD0, 0x12, 0xB8,
               0xE5, 0xB4, 0xB0, 0x89, 0x69, 0x97, 0x4A, 0x0C, 0x96, 0x77, 0x7E, 0x65, 0xB9, 0xF1, 0x09, 0xC5, 0x6E,
               0xC6, 0x84, 0x18, 0xF0, 0x7D, 0xEC, 0x3A, 0xDC, 0x4D, 0x20, 0x79, 0xEE, 0x5F, 0x3E, 0xD7, 0xCB, 0x39,
               0x48]
        result = bytearray()
        # 将 32bit 拆分成 4x8bit，依次进行S盒变换
        for item in list(n.to_bytes(4, 'big')):
            result.append(BOX[item])
        return int.from_bytes(result, 'big')

    @staticmethod
    def _rot_left(n, m):
        """循环左移"""
        return ((n << m) | (n >> (32 - m))) & 0xFFFFFFFF
'''公钥加密RSA'''

class RSA:
    #def Generate_RSA(self,w:int):
    def __init__(self,w:int,e_w=0):
        self.prime=self.get_pq(w)
        self.phi=(self.prime[0]-1)*(self.prime[1]-1)
        self.N=(self.prime[0])*(self.prime[1])
        if e_w==0:
            self.e=self.get_e(self.phi,w/2)
        elif e_w<0:
            raise ValueError("invalid e_w")
        else:
            self.e=self.get_e(self.phi,e_w)
        self.d=Era(self.e,self.N)
    def Import_Public_Key(self,e,N):
        self.e=e
        self.N=N
    def Import_Secret_Key(self,d):
        self.d=d
    def Get_Public_Key(self):
        return self.N,self.e
    def Get_Secret_Key(self):
        return self.prime,self.d
    def encrypt(self,m:int):
        return fast_times(self.N,m,self.e)
    def decrypt(self,C:int):
        return fast_times(self.N,C,self.d)
    def get_pq(self,w:int):
        num=[]
        k=0
        while k<2:
            res=get_number(w//2)
            if(Is_Prime(res)==True):
                if(k==0):
                    num.append(res)
                    k+=1
                else:
                    if(res!=num[0]):
                        num.append(res)
                        k+=1
        return num[0],num[1]
    def get_e(self,phi,w:int):
        while True:
            e=random.randint(3,2**(w//2)-1)
            if gcd(e,phi)==1:
                break
        return e
'''杂凑函数'''

class SHA_1:
    def __init__(self,m=''):
        '''input check'''
        if os.path.isfile(m)==True:
            text=''
            with open(m,'r',encoding='utf-8') as file:
                text+=file.read()
            print(text)
            self.mes=text.encode('utf-8')
            self.hash=self.sha1()
        elif type(m)==str:
            self.mes=m.encode('utf-8')
            self.hash=self.sha1()
        else:
            raise ValueError("Unsupported Input Type!")
    def sha1(self):
        message=self.patch(self.get_message(self.mes))
        L=len(message)//512
        h1='67452301'
        h2='efcdab89'
        h3='98badcfe'
        h4='10325476'
        h5='c3d2e1f0'
        for j in range(0,L):
            Y=message[j*512:(j+1)*512]
            r=self.make_group(Y)
            A1=h1
            B1=h2
            C1=h3
            D1=h4
            E1=h5
            for i in range(0,80):
                temp=self.f(A1,B1,C1,D1,E1,i,r)
                E1=D1
                D1=C1
                C1="{:0>8}".format(hex(self.rotate(self.h2i(B1),30))[2:])
                B1=A1
                A1=temp
            h1="{:0>8}".format(hex((self.h2i(h1)+self.h2i(A1))%(2**32))[2:])
            h2="{:0>8}".format(hex((self.h2i(h2)+self.h2i(B1))%(2**32))[2:])
            h3="{:0>8}".format(hex((self.h2i(h3)+self.h2i(C1))%(2**32))[2:])
            h4="{:0>8}".format(hex((self.h2i(h4)+self.h2i(D1))%(2**32))[2:])
            h5="{:0>8}".format(hex((self.h2i(h5)+self.h2i(E1))%(2**32))[2:])
        return h1+h2+h3+h4+h5
    @staticmethod
    def rotate(x,n):
        s="{:0>32}".format(bin(x)[2:])
        #print(s)
        w=s[n:len(s)]+s[0:n]
    # print(w)
        k=1
        sum=0
        for i in range(0,len(s)):
            sum+=k*int(w[len(s)-1-i])
            k*=2
        return sum
    @staticmethod
    def b2i(x):
        return int(x,2)
    @staticmethod
    def h2i(x):
        
        return int(x,16)
    @staticmethod
    def patch(m):
        message=m
        message+='1'
        while len(message)%512!=448:
            message+='0'
        m1="{:0>64}".format(bin(len(m))[2:])
        return message+m1

    def make_group(self,m):
        r=[]
        for i in range(0,16):
            r.append(m[i*32:(i+1)*32])
        for i in range(16,80):
            r.append("{:0>32}".format(bin(self.rotate(self.b2i(r[i-3])^self.b2i(r[i-8])^self.b2i(r[i-14])^self.b2i(r[i-16]),1))[2:]))
        return r

    def f(self,A,B,C,D,E,i,r):
        if 0<=i<20:
            k='5a827999'
            s1=(self.h2i(B)&self.h2i(C))|(~self.h2i(B)&self.h2i(D))
            return "{:0>8}".format(hex((self.rotate(self.h2i(A),5)+(s1)+self.h2i(E)+self.b2i(r[i])+self.h2i(k))%(2**32))[2:])
        if 20<=i<40:
            k='6ed9eba1'
            s1=(self.h2i(B)^self.h2i(C)^self.h2i(D))
            return "{:0>8}".format(hex((self.rotate(self.h2i(A),5)+(s1)+self.h2i(E)+self.b2i(r[i])+self.h2i(k))%(2**32))[2:])
        if 40<=i<60:
            k='8f1bbcdc'
            s1=(self.h2i(B)&self.h2i(C))|(self.h2i(B)&self.h2i(D))|(self.h2i(C)&self.h2i(D))
            return "{:0>8}".format(hex((self.rotate(self.h2i(A),5)+(s1)+self.h2i(E)+self.b2i(r[i])+self.h2i(k))%(2**32))[2:])
        if 60<=i<80:
            k='ca62c1d6'
            s1=(self.h2i(B)^self.h2i(C)^self.h2i(D))
            return "{:0>8}".format(hex((self.rotate(self.h2i(A),5)+(s1)+self.h2i(E)+self.b2i(r[i])+self.h2i(k))%(2**32))[2:])
    @staticmethod
    def get_message(s):
        m=''
        for i in range(0,len(s)):
            m+="{:0>8}".format(bin(int(s[i]))[2:])
        return m
    def HexOutput(self):
        return self.hash
    def BytesOutput(self):
        return bytes.fromhex(self.hash)    
'''数字签名'''
'''缺少差错检测'''


class ELGammaMode:
    '''产生n bit的大素数,并找到原根'''
    def __init__(self,p,g,m):
        self.p=p
        self.g=g
        self.m=m
    def sign_started(self,x,k):
        self.x=x
        self.k=k
    def check_started(self,s1,s2,y):
        self.s1=s1
        self.s2=s2
        self.y=y
    def  ElGamma(self,mode='Sign'):
        if mode=='Sign':
            self.sig=self.sign
            return self.sig
        elif mode=='Very':
            return self.check()
        else:
            raise ValueError("invalid mode!")
    @staticmethod    
    def Hash(s):
        # 创建 SHA-1 哈希对象
        sha256 = hashlib.sha256()
        # 使用 UTF-8 编码将密码更新到 SHA-1 哈希对象中
        sha256.update(s.encode('utf-8'))
        #sha1.update(s)
        # 获取加密后的密码，以十六进制表示
        encrypted_password = sha256.hexdigest()
        # 返回加密后的密码
        return encrypted_password
    @staticmethod
    def h2i(x):        
        return int(x,16)
    def sign(self):
        m=self.Hash(self.m)
        m_int=self.h2i(m)
        s1=pow(self.g,self.k,self.p)
        s2=Era(self.k,self.p-1)[0]*(m_int-self.x*s1)%(self.p-1)
        return s1,s2
    def check(self):
        m=self.Hash(self.m)
        m_int=self.h2i(m)
        v1=pow(self.g,m_int,self.p)
        v2=(pow(self.y,self.s1,self.p)*pow(self.s1,self.s2,self.p))%self.p
        if v1==v2:
            return True
        else:
            return False    

