# -*- coding: utf-8 -*-
"""
Created on Thu Sep  6 10:24:32 2018

@author: KDK
"""

print('### 1. implement function ###')

def add(num1, num2):

    return num1 + num2
          
print('add(1,2)=',add(1,2))      

print('### 2.1. default arguments ###')
      
def add(num1, num2=1):
    return num1 + num2

print('add(num1)=', add(1))

print('### 2.2. keyword arguments ###')      

def add(num1, num2, num3):
    print('num1=',num1,'num2=',num2,'num3=',num3)
    return num1+num2+num3      

print('add(num3=3,num2=2,num1=1)=',add(num3=3,num2=2,num1=1))
# add(num3=2,1,3)  => 오류: 키워드 인수가 있으면 그 뒤는 모두 키워드 인수여야 한다

# **kwargs : 키워드 가변인자를 의미한다. builtin 함수 선언에 자주 보이는 이름.
def foo(x,**kwargs) :
    print(x, kwargs)            # x=1, kwargs = {'flag':True, 'mode':'fast'}
    print(kwargs.get('flag'))   # kwargs 는 dictionary
foo(1, flag=True, mode='fast')

dic = {'flag':True, 'mode':'fast'}
foo(1, **dic)   # dict 를 인자로 전달할 때 ** 사용 

print('### 2.3. variable arguments ###')

def add(num1, num2, *args):     # 가변 인수는 마지막에만 정의
    
    mysum = num1 + num2
    for i in args:
        mysum += i
    
    return mysum

print('add(1,2,3,4,5)=',add(1,2,3,4,5))

print('### 2.4. 키워드 인자를 dictionary 로 받음 ###' )

def add(**args):

    print('args["num1"]=', args["num1"])
    print('args["num2"]=', args["num2"])
    return args['num1']+args['num2']

print(add(num1=1, num2=2))      

# scope : 변수 검색 순서 (LGB규칙)
# 함수 내 : local scope
# 함수 밖 : global scope
# 파이썬이 정의한 것 : built-in scope

# 재귀 함수
# factorial
# Hanoi : 출력예) 1번 기둥의 1번 원반을 3번 기둥에 옮깁니다

# 함수 포인터와 유사 (패키지도 지정 가능)
import math
list1 = [abs, math]
print(list1[0](-1))
print(list1[1].sqrt(4))

'''
    Closure(클로저) : 함수 안에 내부함수를 정의하여 내부함수를 반환
    - 지연 평가 
    - callback
    - decorator --> AOP ? 함수 호출 전후에 별도의 로직을 넣을 수 있음...더 찾아봐야 함. 
'''
def summation(x, y) :
    # execute : closure
    def execute() :
        print("execute")
        return x+y
    
    return execute  # 함수명 반환 
    
doit = summation(1, 2)      # 아직 두 수를 저장만 하고 계산되지 않음. 실행 지연
doit()                      # 계산 실행

# callback 의 예제 코드 
def after(x, y, cbfunc) :
    print(x + y)
    cbfunc()
    
def callback() :
    print('성공입니다. 콜백 호출 수행')

after(1, 2, callback)    