# -*- coding: utf-8 -*-
"""
Created on Thu Sep  6 10:23:44 2018

@author: KDK
"""

# call by reference
list1 = [1,2,3]
list2 = list1
print(id(list1))    # [id]  객체 주소 조회
print(id(list2))

list3 = [1,2,3]
print(list1 is list3)   # False : is 연산자는 객체의 주소를 비교
print(list1 == list3)   # True  : == 연산자는 리스트,튜플,맵의 값을 비교 
print(id(list1), id(list3))

print('################### 연산 ################### ')
print(7/4)  # 1.75
print(7//4) # 1 (몫)
print(2**4)

# 삼항연산자
result = '진실' if 1+1==2 and 2-1==1 else '거짓'

if conn is not None:  # null value 