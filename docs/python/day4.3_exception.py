# -*- coding: utf-8 -*-
"""
Created on Thu Sep 20 17:35:46 2018

@author: KDK
"""

print('################### SYS 모듈 ###################')
import sys

# 인자 조사
print('arg count:',len(sys.argv))
for i,argv in enumerate(sys.argv):
    print(str(i)+":", argv)
# 예외 정보를 튜플로 반환 : (예외클래스, exmsg, traceback)
try:
    1/0
except:
    exclass,exmsg,traceback = sys.exc_info()
    print(exclass)
    print(exmsg)
    print(traceback)

# 최상위 오류
try :
    1/0
except Exception as e:
    print('error', e)
    raise
finally :
    print('exit')
    
# 예외 생성 
if name not in authorized:
    raise RuntimeError(f'{name} not authorized')

# with context 를 벗어나면 리소스가 해제된다 
with open(filename) as f:
    # 파일을 사용
    ...
# 파일을 닫음