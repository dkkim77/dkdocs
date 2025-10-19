# -*- coding: utf-8 -*-
"""
Created on Thu Sep  6 17:21:26 2018

@author: KDK
"""
import os

# 사용자 home dir.
os.path.expanduser("~") 
os.getenv("USERPROFILE") # linux 에서는 "HOME" 이었다.

# file handling
f = open('c:/Users/KDK/Documents/pyworkspace/hello/live.txt', 'wt')
f.write("""테스트
잘될까요
readline()
개행문자테스트
""")
f.close()

f = None
try :
    f = open('c:\\Users\\KDK\\Documents\\pyworkspace\\hello\\live.txt', 'rt')
#    text = f.read()
    while True :
#        text = f.readline()  개행문자를 버리지 않고 text 에 저장된다.
#        if not text :      # 비문자열이면 break      
        text = f.read(10)   # 10 문자씩 읽는다 
        if len(text) == 0:
            break
        else:
            print(':',text,':',len(text),sep='')
        
except FileNotFoundError :
    print('파일이 없습니다')
#    raise FileNotFoundError
finally :
    print('호출돼?')
    f.close()

import sys

try :
    f = open('c:/Users/KDK/Documents/pyworkspace/hello/live.txt', 'rt')
    lines = f.readlines()
    
    for line in lines:
        print(line, end='')

except FileNotFoundError :
    print('file not found')
    exclass,exmsg,traceback = sys.exc_info()
    print(exclass)
    print(exmsg)
    print(traceback)    

finally:
    f.close()

# 파일에 객체 직렬화 pickle
f= open('colors', 'wb')
    
colors = ['red', 'green', 'black']    

import pickle
pickle.dump(colors, f)

f.close()

del colors

f=open('colors', 'rb')
colors = pickle.load(f)

f.close()
print(colors)

import os

os.listdir()                # 현재 디렉토리의 모든 디렉토리/파일명을 리스트로 반환 
os.remove('abc.txt')        # 파일이나 디렉토리 지우기 
os.mkdir('abc')             # 디렉토리 만들기 
os.makedirs('/tmp/foo')     # /tmp/include/gl/temp 처럼 긴 경로를 한번에 만들어 준다. 
os.path.abspath('abc.txt')  # 파일의 절대 경로 반환(파일명 포함) 
os.path.exists('abc.txt')   # 주어진 경로의 파일이 있는지 확인하는 함수 
os.curdir() # 현재 디렉토리 얻기 
os.pardir() # 부모 디렉토리 얻기 
os.sep()    # 디렉토리 분리 문자 얻기. windows는 \ linux는 / 를 반환한다.

os.path.basename(filename)  # 파일명만 추출 
os.path.dirname(filename)   # 디렉토리 경로 추출 
os.path.split(filename)     # 경로와 파일명을 분리 
os.path.splitext(filename)  # 확장자와 나머지 분리


firstdir = os.getcwd    # 작업디렉토리 관련
os.chdir('../')
# 입력받은 파일경로에 대해 해당 작업이 가능한지 bool 리턴
print(os.access('.', os.F_OK))  # 존재하는지
print(os.access('.', os.W_OK | os.X_OK | os.R_OK))  # 쓰기, 실행, 읽기 가능한지

print('파일정보:',os.stat('test.db'))  # 파일 정보 조회
# os.umask('411')#  umask 설정 변경 
# utime(path, times)
# 파일 엑세스 시간(last access time), 수정 시간(last modified time)을 수정
os.utime('test.db', None)   # None : 현재시각으로 변경 