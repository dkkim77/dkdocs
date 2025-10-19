# -*- coding: utf-8 -*-
"""
Created on Thu Sep 20 17:35:46 2018

@author: KDK

print('################### OS 모듈 ###################')
'''
print(os.name)
print(os.environ)
    
for i in os.environ:
    print(i+":", os.getenv(i))
'''
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

# 파이썬 설치경로, 실행 파일
print(sys.prefix)    
print(sys.executable)

# 모듈을 찾는 경로
print(sys.path)

# 표준입출력
sys.stdin.read()
sys.stdout.write('hi\n')
sys.stderr.write('hi..errr\n')

print('################### Process 관련 ###################')
# os.system('notepad')    
# os.system('calc')  
# system() 과 차이점은 비동기라는 것 
os.startfile('notepad')    
os.startfile('calc')  
''' 
os.execl : fork 로 차일드 프로세스를 만든 후 그 프로세스를 독립적인 프로세스로 만들어 줌
호출하는 프로세스를 새로운 프로세스로 변경시키는데 사용
성공적으로 끝나면 제어가 복귀되지 않음. 실패일 경우만 -1 반환 
'''
print('################### Threading 모듈 ###################')
import threading
import time

count = 10                      # 전체 버그 수 
lock = threading.Lock()

class Developer(threading.Thread):
    
    def __init__(self, name):
        threading.Thread.__init__(self)    # 반드시 Thread 생성자를 호출
        self.name = name
        self.fixed = 0          # 수리한 갯수
        
    def run(self):
                
        global count
        
        while True:
           
           lock.acquire()   # LOck 획득
           
           if count > 0:
               count -= 1       # 전체 버그 수 
               lock.release()   # Lock 해제
               self.fixed += 1  # 해결한 수 증가 
               time.sleep(0.1)  # second
           else:
               lock.release()
               break

dev_room = []           
for name in ['Kim', 'Lee', 'Choi']:
    
    dev = Developer(name)           
    dev_room.append(dev)
    
    dev.start()
    
for dev in dev_room:
    
    dev.join()  # 스레드가 종료되기를 기다립니다 
    print(dev.name, dev.fixed)    
    