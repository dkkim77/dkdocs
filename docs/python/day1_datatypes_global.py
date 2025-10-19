# -*- coding: utf-8 -*-
"""
Created on Fri Sep 21 16:02:41 2018

@author: KDK
"""

print('octal:0o10', 0o10)
print('hex:0x10',   0x10)
print('binary:0b10',0b10)

print('oct(8):' ,oct(8))
print('hex(16):',hex(16))
print('bin(2):' ,bin(2))

print(type(1))
print(type(3.14))
x = 3-4j       # j 를 써야함. i 쓰면 안됨
print(type(x)) 
print(x.imag)  
print(x.real)  
print(x.conjugate())    # 켤레복소수   

'''
bool 판단 기준

값          참/거짓
----------------------
"python"	참
""	        거짓
[1, 2, 3]	참
[]	        거짓
()	        거짓
{}	        거짓
1	        참
0	        거짓
None	    거짓
'''
# 응용 : queue 데이터를 처리할 동안 반복 
a = [1, 2, 3, 4]
while a:
     print(a.pop())

print('0:',bool(0))
print('-100:',bool(-100))
print('HaHa:',bool('HaHa'))
print('"":',bool(''))
print('None:',bool(None))

print('####################### Encoding #######################') 

import sys
print(sys.getdefaultencoding())

print(type('가'))                    # string
print(type('AB가나'.encode('utf-8')))    # 문자열을 --> bytes로 변환
print('AB가나'.encode('utf-8'))
print(b'AB\xea\xb0\x80\xeb\x82\x98'.decode('utf-8'))    # 접두어 b는 '...' 내용을 바이트 배열 리터럴로 취급하라는 의미
print(ord('가'))   # 문자     --> 유니코드
print(chr(44032))  # 유니코드 --> 문자

# raw 문자열 : 'r' 접두사를 붙임. escape 문자가 적용되지 않음 
print('\t\t\t탭\n개행')
print(r'\t\t\t탭\n개행')

# 전역변수의 사용
count = 0
def callee() :
  for i in range(0,5,1) :
    print('callee 호출')
    global count      # global 로 선언하여 사용해야 함. 안하면 UnboundLocalError: local variable 'count' referenced before assignment
    count = count + 1
    yield count
  
for i in callee() : 
  print('caller 에서 호출 :', i)