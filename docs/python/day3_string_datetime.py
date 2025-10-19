# -*- coding: utf-8 -*-
"""
Created on Thu Sep  6 11:07:39 2018

@author: KDK
"""

print('############################### 문자열함수 ###############################')
      
# 기본 함수 
str1 = 'python programming'
print(str1+ 3) # TypeError: can only concatenate str (not "int") to str
print(str1 + str(3))     # + 연산
for i in range(0,10,1) : # * n 연산은 문자열을 n회 반복하여 생성한다 
  print('*'*(i+1))

print('len(str1)=',len(str1))               # 길이 
print('str1.find("o")=',str1.find('o'))     # 인덱스 
print('str1.rfind("o")=',str1.rfind('o'))   # 우측 인덱스
print('str1.count("o")=',str1.count('o'))   # 갯수 
print('a' in str1)                          # 포함 여부 
print('x' not in str1)
print(str1.startswith('p'))                 # 시작여부
print(str1.endswith('g'))                   # 종료여부 
print(str1.isdecimal())                     # 숫자형 문자인지 여부 
print('trim()->strip():',str1.strip())      # trim 
print('trim()->strip():',str1.rstrip())     # rtrim 
print(str1.split())                         # split
'http://m.naver.com'.partition("://")       # partition : 튜플로 반환 ('http','://','m.naver.com')
print(str1.replace('python','C++'))         # 치환 
str1 = 'hello world'                        # join : 리스트/튜플/문자열 사이에 특정문자열을 넣어서 하나의 문자열로 재구성 
print('|'.join(str1))
print('|'.join(['w','o','r','l','d']))
print('[','zxdefayc'.rjust(20,'p'),']',sep='')  # rjust(전체width,char) : padding 함수. 왼쪽에 'p'문자가 붙음
print('[','1234'.zfill(10),']',sep='')          # left zero padding.(rjust를 써도 동일)
'''
%s	문자열(String)
%c	문자 1개(character)
%d	정수(Integer) 
    데이터 : 123.45678901234
%f	부동소수점수 [-]m.dddddd        123.456789
%e  부동소수점수 [-]m.dddddde+-xx   1.234568e+02
%g  E 표기를 선택적으로 사용        123.457
%o	8진수
%x	16진수
%%	Literal % (문자 % 자체)
'''
print('나는 %s에서 태어나' % 'seoul')
print('나는 %d월 %d일 %s에서 태어나' % (12,14,'seoul')) # tuple 괄호 없으면 안됨. c 와 혼동.

# format 함수 (since 2.6)
string = '이름:{},나이:{},키:{}'
string2 = '이름:{name},나이:{age},키:{height}'
print(string.format('kdk',44,180.1))
print(string2.format(name='kdk',age=44,height=180.1))

# 인덱스 format {index:format}, thousands separator,percentage
var1 = "hello world"
print("{0:<30}".format(var1))   # 좌측 정렬 
print("{0:>30}".format(var1))
print("{0:^30}".format(var1))   # 가운데 정렬 
print("{0:=^30}".format(var1))  # ======hello world======= 타이틀 문자열로 이용
'{:#>+20}'.format(123)          # 출력:################+123 (`#`를 padding. +: 부호 항상 표시)
'금액표시=>{:-10,.3f}'.format(-123.4567)  # float. '-': 음수일때만 표시. ',': 정수부에 comma 삽입 
help('FORMATTING') 

dic = {'name':'홍길동', 'age':30}
print(f'나의 이름은 {dic["name"]}입니다. 나이는 {dic["age"]}입니다.')

# 일자 시각 
import time
# date Object
from datetime import date 
from datetime import time as dtm
# datetime Object
from datetime import datetime as dt

print(time.time())
print(date.today())
print(date.fromtimestamp(time.time()))
print(date.today().strftime('%y%m%d%H%M%S'))
print(time.strftime('%H%M%S'))

import datetime as dt
now = dt.datetime.now()
print(now)
결과: datetime.datetime(2022, 8, 23, 10, 19, 31, 756530)
print(now.second)
# 특정 시각 생성
cal=datetime.datetime(2018,4,1)
# 날짜 비교
print(now > cal)
결과: True
# 날짜 연산
now + dt.timedelta(days=30) # 오늘+30일 증가. hours, minutes, seconds. year와 month 는 없음
'''
timedelta에는 year와 month라는 매개변수가 없다. 
년과 월은 어떤 년도와 월인지에 따라서 각각 길이가 다르기 때문. 
년과 월을 계산하는 방법은 relativedelta 이용. dateutil 을 pip install 해야 한다.
'''
from dateutil.relativedelta import relativedelta
now-relativedelta(months=3)
# datetime <---> string 변환
now.strftime('%Y/%m/%d %H:%M:%S')
결과:'2022/08/23 10:20:59'
dt.datetime.strptime('20171011','%Y%m%d')   # string parse time
결과:datetime.datetime(2017, 10, 11, 0, 0)

# misc 
print(dir('__name__'))   # dir : 인자로 받은 객체의 속성을 리턴 
print(dir('__builtins__'))

help(print)
# python 의 root 객체인 object 에 __doc__ 이라는 속성에 설명을 기입하면 help 로 볼 수 있음
# """ 주석을 이용하면 자동으로 __doc__ 에 저장이 됩니다
def usedoc():
    print('doc 사용')
    
def usecomment():
    """ __doc__ 속성을 사용한 문서화 """

usedoc.__doc__ = 'doc 속성을 이용'    
help(usedoc)
help(usecomment)
