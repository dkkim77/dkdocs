# -*- coding: utf-8 -*-
"""
Created on Thu Sep  6 11:20:20 2018

@author: KDK
"""

print('####################### List #######################')

numlist = [0,1,2,3,4,5,6,7,8,9]
numlist[1:1] = [10,20,30]   # [insert] index 1 의 자리에 삽입
numlist[1:4] = []           # [delete] index 1~3 을 삭제 [0, 4, 5, 6, 7, 8, 9]
del numlist[1]              # [delete] 키워드 사용 
numlist[1] = [10,20,30]     # [replace] index 1 의 replace
numlist.insert(2,15)        # [insert] 리턴 void. numlist 자체를 변경
numlist.append(11)          # [append] 리턴 void. numlist 자체를 변경
numlist.remove(11)          # [remove]
nums3 = numlist.sort()      # [sort]
nums3 = numlist.reverse()   # [reverse]
sorted(numlist)             # [sort]
reversed(numlist)           # [reverse]
item = numlist.pop(3)       # [pop]   index 3 의 값을 반환 후 리스트에서 삭제 
# 리스트 연산 +, *
nums1 = [1,3,5,7,9]
nums2 = [0,2,4,6,8]
print('append list(nums1+nums2):',nums1+nums2)  # [+연산]
print('리스트반복(nums2*2):',nums2 * 2)         # [*연산] => [0,2,4,6,8,0,2,4,6,8] 가 신규 생성 
nums1.extend(nums2)                             # '+'연산자와 다르다. nums1 자체가 확장된다. +연산은 제3의 리스트가 리턴 

print('index:',nums1.index(5))                  # [index] 리스트 내용이 5 인 요소의 index 리턴
print('count:',nums1.count(2))                  # [count] '2' 가 몇개 있는지 리턴 
print('리스트max값:',max(nums1), '리스트min값:',min(nums1)) # [max/min]


# 리스트의 참조
list1 = [1,2,3]
list2 = list1    # list2 는 참조
list1[1] = 100
print(list2)

list3 = list1.copy() # shallow copy
list3[1] = 2
print('list1',list1) 
print('list3',list3)

list3 = list1[:]    # copy 와 동일한 효과 

list4 = [['a','b','c'], 2, 3]
import copy
list3 = copy.deepcopy(list4)    # deep copy
# is : 동일한 객체를 가리키는지 조사
print(list2 is list1)
print(list3 is list1)

# any : 리스트에 참인 요소가 하나라도 있으면 참. 
# all : 리스트에 모든 요소가 참이면 참 리턴.
tof  = [True, False]
print(any(tof))
print(all(tof))    
# List Comprehesion (리스트 이해?..reading comprehesion...)
# [수식 for 변수 in 리스트 if 조건] ==> 조건이 있는 리스트를 생성할 때 좋을 듯.
nums1 = [ n * 2 for n in range(0,11)]
print(nums1)    
nums1 = [ n * 2 for n in range(0,11) if n % 10 == 0]  # for 적용 후 if 적용. 그 후 수식 적용
print(nums1)    

# 이중 리스트
dim2D = [
            [80,90,92],
            [70,85,80],
            [60,75,73]
        ]

sum = 0
avg = 0
acumAvg = 0
totAvg = 0

for student in dim2D:
    
    for subj in student:        
        sum += subj
        
    avg = sum / len(student)
    print('%d번째학생 평균: %5.2f' % (dim2D.index(student)+1,avg))
    acumAvg += avg
    sum = 0

totAvg = acumAvg / len(dim2D)
print('총 평균:%5.2f' % totAvg)

print('####################### Tuple #######################')
tu = '이순신', '김유신', '강감찬'  # 괄호 생략 가능
lee, kim, kang = tu               
print(lee, kim, kang)
# swap 도 편리
a,b = 1,2
a,b = b,a

import time
def getTime() :
    now = time.localtime()            # class time.struct_time 리턴 
    return now.tm_hour, now.tm_min    # tuple로 리턴 

# 튜플의 접근은 리스트처럼 배열 첨자로 접근 가능 
now = getTime()
print("%d 시" % now[0] )
print("%d 시" % now[1] )
print('it\'s %d:%d' % getTime())

print((1,2,3)+(4,5))        # [+연산] => (1,2,3,4,5) 가 신규 생성
print((1,2,3)*2)            # [*연산] => (1,2,3,1,2,3) 가 신규 생성 
# 변경/삭제 불가
# 슬라이스, 열갯수
import time
now = time.localtime()
print(now)
print(now[3:])          # [첨자접근] 일부만 추출
print(len(now))         # [len] 튜플의 열 갯수 
print(now.index(1))     # [index]
print(now.count(2021))  # [count] 특정 값을 세기 

# tuple 은 immutable. 가볍고 빠름. 변경이 필요할 시 list 로 변환
timeElements = list(getTime())
timeElements[0] = 23
print(timeElements)
 
print('####################### Dictionary #######################') 

dic = { 'boy':'소년', 'school':'학교', 'book':'책' }
print(dic['boy'])                           # [첨자접근]    해당 key 가 없을경우 KeyError 발생 
print(dic.get('student', '찾을 수 없음'))   # [get]         KeyError 를 피하기위해 get 사용. return 'None'
dic['boy'] = '남자애'                       # [put] 과 같음 (put 메소드는 없음) 
del dic['boy']                              # [remove]
dic2 = {'student':'학생', 'teacher':'선생님'}
dic.update(dic2)                            # [update] 두 사전을 병합한다
dic.clear()                                 # [clear]  key/value 모두 삭제 
print('boy' in dic)                         # [in]     key 가 존재하는지 여부. contains.

print(dic.keys())       # 리스트 타입이 아닌 편집 불가한 리스트(dict_*)를 리턴 =>  append,insert,pop,remove,sort 수행 불가
print(dic.values())     # 편집을 위해서 list() 를 사용 
print(dic.items())

print('####################### Set #######################') 

s1 = set([1,2,3])   # 집항 생성
s2 = set("Hello")   # 집합 생성(문자열을 이용)
s1.add(4)           # [add]     원소 추가
s1.remove(2)        # [remove]  원소 제거
s1.update([4,5])    # [update]  원소 여러 개 추가 

s1 = set([1, 2, 3, 4, 5, 6])
s2 = set([4, 5, 6, 7, 8, 9])
s3 = s1 & s2        # 교집합
s3 = s1 | s2        # 합집합
s3 = s1 - s2        # 차집합


print('####################### Conversion #######################') 

# dict() : 2차원 리스트를 사전으로 변환 

race = ['zerg', 'terran', 'protoss']
raceList = list(enumerate(race))    # enumerate 는 요소의 index 와 값을 tuple 로 리턴 
print(raceList)

for num, name in enumerate(race):    
    print(num,'번째',name)

day = ['월','화','수', '목','금']
food = ['갈비탕','순대국','고기']
menu = zip(day, food)   # zip 은 두 리스트를 1:1 대응시켜 하나의 튜플 컬렉션 생성 
for d, f in menu:       # 짧은 리스트를 기준으로 size 가 결정. 수요일까지 생성 
    print(d+'요일엔 ',f)
    
# dict(zip(day, food)) 사전으로 변환 

'''
builtin object : list, tuple, dict
변환 함수 정리

            items():튜플리스트로                     
            dict_items([('school', '학교'), ('book', '책')])
            list() : ['school', '학교'] 
            enumerate : 리스트의 인덱스, 값을 튜플로 변환
            
            items()              list()
Dictionary ------------> Tuple ---------> List
           <------------       <---------
            dict()               zip()
                               <---------
                                enumerate()
'''    