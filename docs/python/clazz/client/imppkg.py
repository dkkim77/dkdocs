import app.computer as c

machine = c.Computer(False, '1GHz', '4GB', '1TB')
machine.turnon()

print('### import ###')
import math
print('PI:',math.pi)    # math. 를 써야한다.

# 많이 사용하는 것들을 동시에 import
import os, sys, io, time

# 모듈의 특정 속성/메소드만 사용하려면
from math import floor, sqrt    # 모듈이름없이 함수 이름만 사용 
print(floor(3.2))
print(sqrt(4))

from math import *
print('no module name:',pi)

# main 함수가 필수가 아닌 파이썬에서 전형적인 프로그램 구조.
def main(argv) :
    print('__name__:',__name__)
    print('argv:', argv)
    if (len(argv) == 0) :
      print("Usage : python3 myprog arg1 ...")
      sys.exit(-1)  # 예외로 처리 =>  raise SystemExit(-1) 와 동일 
# __name__ 변수: 모듈이 단독으로 실행될 경우 __main__ 이다.
# 다른 모듈에서 import 하여 사용할 때는 모듈 자신의 이름.. 여기서는 imppkg    
import sys
if __name__ == "__main__":
    main(sys.argv)

# import 할 모듈을 찾는 순서: 현재 경로, 파이썬 설치 경로인 PYTHONPATH 환경변수, 다음은 sys.path
import sys
print('sys.path:',sys.path)
sys.path.append("c:\\KDK")
print('sys.path:',sys.path)
'''
1. 모듈 검색 경로
  1) CWD 를 먼저 검색
  2) PYTHONPATH 환경 변수에 설정
  3) 표준 라이브러리 디렉토리 : sys.path 하면 나오는 위치들
    -> 소스상에서 등록 시: sys.path.append('C://mypythonLib')
    -> 소스상에서 삭제 시: sys.path.remove('C://mypythonLib')
    
2. 모듈 별칭 사용: import 모듈 as 별칭
3. from <모듈> import * : 밑줄(__) 로 시작하는 개체들은 import 하지 않음 
- from math import cos, sin => 여전히 math 모듈 전체를 적재. 모듈에 있는 cos와 sin이 로컬 스페이스에 복사될 뿐

4. 모듈 임포트의 내부 동작 
  1) import 를 만나면 sys.path 에서 검색
  2) 모듈의 바이트코드가 있으면 바로 임포트. 없으면 바이트코드 생성(.pyc)

5. 모듈을 한번 로드한 후 재로드하려면 reload 사용 
  import testmodule
  import imp
  imp.reload(testmodule)

6. 모듈 로딩 테스트(call by referece)
  testmodule.py
  --------------------
  print('hello world')
  -----------------------
  >>import testmodule as t1
  hello world
  >> import testmodule as t2
  아무것도 출력되지 않음
  ==> 이유는 module 은 메모리에 한 번, 하나만 로딩된다는 원칙때문에.
'''
# 배포
# 1. setup.py 를 최상위에 생성
# setup.py
import setuptools

setuptools.setup(
    name="porty",
    version="0.0.1",
    author="Your Name",
    author_email="you@example.com",
    description="Practical Python Code",
    packages=setuptools.find_packages(),
)
# 2. setup 실행
# > python setup.py sdist[enter]   => dist 디렉토리에 tar 를 생성

