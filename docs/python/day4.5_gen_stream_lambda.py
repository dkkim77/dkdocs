# -*- coding: utf-8 -*-
"""
Created on Thu Sep  6 11:07:39 2018

@author: KDK
"""

# 이터레이터 : 리스트,튜플,사전,문자열, 파일들은 이터레이터라는 객체를 포함
for e in [1,2,3]:
    print('리스트:',e)
for e in (1,2,3):
    print('튜플:',e)
for e in 'python':
    print('문자열:',e)
for e in {'one':'1', 'two':2}:
    print('사전:',e)
for line in open("test.txt"):
    print('파일라인:',line)    

# 이터레이터 내부동작 원리
string = 'python'
it = iter(string)    
while True:
    try:
        print(next(it)) # 또는 이터레이터의 next 메소드로 동일 효과 it.__next()__
    except StopIteration:
        exit(0)

# 제너레이터 : 이터레이터를 생성해주는 함수.
# 함수 안에서 yield를 사용하면 함수는 제너레이터가 되며 yield에는 값(변수)을 지정
# yield : 로직 실행을 잠시 멈추고 제어를 호출자로 넘김. return 은 함수가 끝나지만 yield 는 제어가 다시 돌아온다.    
def number_generator():
    yield 0
    yield 1
    yield 2
# number_genenrator 는 숫자를 3개 발생시킨다.   
# generator 사용예1.
for i in number_generator():  # number_generator() 는 generator 가 리턴되고 for in 에서 next(gen) 가 호출됨.
    print(i)
# generator 사용예2. 내부의 iterator를 사용
gen = number_generator()
a = next(gen)
b = next(gen)
c = next(gen)

def reverse(data):
    size = len(data)
    for index in range(size-1,-1,-1): # 0 까지 감소시키면서 반복 
        yield data[index]

for char in reverse('python'):
    print(char)
    
# filter(함수명, 이터레이션 가능 자료형) : 이터레이터를 리턴 
# 함수명이 None 이면 필터링하지 않음    
def flunk(s):
    return s < 60

score = [45, 89, 72]
for s in filter(flunk, score):
    print('filter:', s)
# map : 변환 함수를 적용하여 요소를 구성 
def half(s):
    return s / 2

for s in map(half, score):
    print('map:', s)
# 두 개 이상의 리스트를 인자로 할 때
def total(first, second):
    return first + second

first = [22, 34, 46]
second = [1, 2, 3]
for s in map(total, first, second):
    print('두개 이상 map:', s)

# 람다 함수
# lambda arg:statement ==> filter,map 둘다 미리 함수를 정의하는 것이 불편. lambda 가 보완
# lambda 는 이름이 없고 입력과 출력만으로 함수를 정의    
score = [45, 89, 72]
for s in filter(lambda s:s<60, score):
    print('filter lambda:', s)

# lambda 예)
testLamb = lambda x, y : x*y
print(testLamb(2, 3))

print((lambda x: x*x)(3))    