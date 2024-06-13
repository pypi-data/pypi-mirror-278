#python tools
#BUAACrypto2024 is an easy crypto packet for some crypto algorithm
##installation

###put the whole packet in any of your document 
###run setup.py 
'''shell
python setup.py sdist
cd ./dist
pip install BUAACrypto2024-0.0.5.tar.gz
'''shell
##uninstall
'''shell
pip uninstall BUAACrypto2024
'''shell
###or just use:
'''shell
pip install BUAACrypto2024
pip uninstall BUAACrypto2024
'''shell


##table of contents

#cal:包含一些常见的数学、编码运算
  - fast_times(N,a,b)
    -快速模幂算法，返回a^b mod N
  - Era(a,b)
    -拓展欧氏算法，返回满足xa+yb=r=gcd(a,b)的x,y,r
  - get_number(w)
    -随机w比特大整数
  - Is_Prime(n)
    -素性检验
  - getPrime(w)
    -w比特大整数选取
  - bytes_to_int(n:bytes)
  -字节串转整数
  - int_to_bytes(n:int,len)
  -返回长度为len的字节串
  - Words_to_Int(s:str/file)
    -字符串/文件转int
  -n2s(n:int)
  -整数转字符串
  -s2n(s:str)
  -字符串转整数


#Basic_Code:包含基本的密码学算法
  - SM4Chipher
    -init(self,key)
      -输入密钥key(bytes)进行加密和解密操作，密钥需为字节串形式，可使用int_to_bytes()函数转换。
    -encrypt(plaintext:str/bytes/file,mode='ECB'/'CBC')
      -加密操作，plaintext可为字符串、字节串、文件，mode可从两种工作模式选取，若不输入，默认为ECB模式，自动进行填充。默认16进制输出
    -decrypt(chiphertext:str,mode='ECB'/'CBC')
      -解密操作，chiphertext为字符串，mode可从两种工作模式选取，若不输入，默认为ECB模式。默认16进制输出。
    -HexOut(self)
      -输出方式为16进制
  -BytesOut(self)
    -输出方式为字节串
  -StrOut(self)
    -输出字符
  
  - RSA
    -init(w:int,e_w)
      -输入比特w, 生成w比特的两素数pq, 进一步生成公私钥，e_w为公钥比特数，不输入默认为w/2 
    -encrypt(self,m)
      -RSA加密操作，m为整数
    -decrypt(self,chiper)
    -需要建立对象后使用，解密操作
    -Get_Public_Key(self)
      - 如果使用了__init__初始化，则输出生成的公钥
    -Get_Secret_Key(self)
      - 如果使用了__init__初始化，则输出生成的私钥
    -Import_Public_Key(self,e,N)
      -不使用__init__生成，输入选取的公钥
    -Import_Secret_Key(self,d)
      -不使用__init__生成，输入选取的私钥

  - SHA_1
    -init(self,m)
      -输入待加密信息m, 支持文件输入
    -HexOutput(self)
      -16进制输出
    -BytesOutput(self)
      -字节串输出

  - ELGammaMode
    -init(self,p,g,m)
      -输入素数p, 原根g,消息m初始化 
    -sign_started(self,x,k)
      -输入私钥x和随机数k
    -check_started(self,s1,s2,y)
      -输入签名s1, s2和公钥y
    -ELGamma(self,mode)
      -签名和验签操作, mode=('Sign', 'Very')，不输入默认为签名操作