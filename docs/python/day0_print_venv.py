# -*- coding: utf-8 -*-
"""
Created on Thu Sep  6 10:23:44 2018

@author: KDK
"""

print('문자열은 4가지 생성방식:홑따옴표,홑따옴표3쌍,쌍따옴표,쌍따옴표3쌍')
print('이스케이프문자가 필요"없네???')
print("이스케이프문자가 필요'없네???")
print(""" 멀티라인을
출력하려하는데
잘되겠지?""" )
str1 = 'str1' 'str2' 'str3'
str2 = 'str1'+'str2'+'str3'
str3 = 'str1' * 3       # 문자열 반복
print('str1',':',str1)
print('str2',':',str2)
print('str3',':', str3)

print('### access string ###')
string = 'python'
print(string[3])
print(string[0:2])
print(string[3:])
print(string[-2:])
print(string[0::2]) # 마지막 첨자는 step. default=1
print(string[::-2])

''' index 그림
 -------------------------------------
 | p | y | t | h | o | n |
 -------------------------------------
 0   1   2   3   4   5   6
-6  -5  -4  -3  -2  -1
'''
print('### type casting func ###')
print('str(2)+"str1"',':', str(2)+'str1')
print('int("43")',':',int('43'))
print('float("4.3")',':',float(4.3))

print('### operator ###')
print('5/3=',5/3)    # 소수점 : 소수 16자리까지 표현
print('5//3=',5//3)  # 정수의 몫
print('5%3=',5%3)

print('### input func ###')
# age = int(input('how old are you?'))
age = 20
print('you are ',age,'years old')


print('### if statement ###')
if 0 < age < 20:
    print("teenager")
elif 20 <= age < 30:
    print('good')
else:
    print('adult')

print('### INDENT ###')
a = 1      
if a == 1: print('한줄 코딩')
if a == 1: print('한줄 코딩'); print('세미콜론 가능')
print('다음줄로 계속 표시'); a = 1 + (2 + 3) \
                                + 4 + 5; print(a)
                                
print('################### if [var] in clause ################### ')
# answer = input('continue[y/n]')
answer = 'y'
if answer in ['y','Y','yes','Yes']:  # IN 비교가 가능 
    print('you said "Yes"')
else:
    print('you mean "no"')

print('### not array. List! Tuple and Dictionary ###')
strlist  = ['str1', 'str2', 'str3']
strtuple = ('str1', 'str2', 'str3')
dic      = {'str1':'문자열1', 'str2':'문자열', 'str3':'문자열3'}

print('strlist',':',strlist)
print('strtuple',':',strtuple)
print('dic',':',dic)

print('################### 환경변수 ###################')

print(os.name)
print(os.environ)
    
for i in os.environ:
    print(i+":", os.getenv(i))


# 파이썬 설치경로, 실행 파일
print(sys.prefix)    
print(sys.executable)

# 모듈을 찾는 경로
print(sys.path)

# 표준입출력
sys.stdin.read()
sys.stdout.write('hi\n')
sys.stderr.write('hi..errr\n')

print('################### for statement ###################')
# 1. range(start,stop, step): stop-> exclusive. 이터레이터를 반환
# 감소 예: range(9, -1, -1)  => 9 ~ 0    
for i in range(10):   
    print('*' * i)
# continue, break 사용 가능 
# pass : 빈 줄과 같음 ==> if (a < 0) {;}    
# exit(0)

# 2. for ~ else 문 
for i in [1,2,3]:
    if i % 2 == 0 :
        continue
else:
    print("break 가 실행되지 않음")    
print('for 다음 문장')

# 3. for tuple in 문
records = [(1,2), (3,4), (5,6)]
for (first, last) in records:
    print(first + last)

# 4. List Comprehension
# List 데이터 가공
list1 = [1,2,3]

print('################### 환경 ################### ')
'''
$ python3 --version                 --> python3 설치 확인
$ sudo apt-get install python3      --> Ubuntu와 같은 Debian 계열
$ sudo yum install python3          --> Red Hat 및 계열
'''
print('################### 모듈 검색 #################### ')
1번째 : sys.moudules     - 이미 import된 모듈과 패키지들을 저장
2번째 : built-in modules - 파이썬 공식 라이브러리
3번째 : sys.path

interpreter 가 패키지로 인식하기 위해서 모든 디렉토리에 __init__.py 가 있어야 한다.
>>> import sys
>>> sys.path
>>> sys.path.append("/")

sys.path is initialized from these locations:
-The directory containing the input script (or the current directory when no file is specified).
-PYTHONPATH (a list of directory names, with the same syntax as the shell variable PATH).
-The installation-dependent default.
실행예)
$ export PYTHONPATH=/home/ec2-user/apps/python/pyunchart
$ /home/ec2-user/apps/python/pyunchart]$ python3 cctrade/client/pricedata.py

print('################## 명령행 전달인자 처리 #################### ')
$ python test.py /home/limsee/test.json
# 코드 예 
import sys
file_path = sys.argv[1]
if len(sys.argv) != 2:
    print("Insufficient arguments")
    sys.exit()
print("File path : " + file_path)

print('################### 가상 환경 ################### ')
#  
'''
$ python -m venv test_venv                  --> test_venv 디렉토리를 만들고 가상환경 box 로 지정 
$ test_venv/Scripts> activate.bat[enter]    --> test_venv 가상환경으로 입장
(test_venv) >>> deactivate                  --> 가상환경 빠져나오기
(test_venv) >>> python hello.py             --> 파이썬 프로그램 실행
(test_venv) >>> python hello.py KMK         --> 실행시 매개변수 전달(sys.argv[1] 로 접근)

'''