import computer as c

class Laptop(c.Computer):
    
    innerbattery = 500
    '''
    생성자
    def __init__(self, battery):
        super.__init__('1GHz','3','2','1')
        self.inner_battery = '5000mA'     
    소멸자: 레퍼런스 카운터가 0 일때 호출
    def __del___(self):
        print('deleted')
    '''
    def transportable(self):
        power = False

# machine = Computer(False, '1GHz', '4GB', '1TB')
machine = c.Computer()        
machine2 = c.Computer()

# 변수에 접근할 때 찾는 순서 
#인스턴스 객체 영역 --> 클래스 객체 영역 --> 전역 영역

# 런타임시 멤버 추가
c.Computer.video = 'VGA'
print('인스턴스1 신규멤버:', machine.video)
print('인스턴스2 신규멤버:', machine2.video)
# 클래스가 아닌 인스턴스에만 추가할 때
machine2.odd = 'LG'
print('인스턴스2 신규멤버:', machine2.odd)

# 리플렉션
machine.__class__.video = 'XGA' # __class__ 속성을 이용하면 모든 인스턴스들이 바뀜
print(machine.video)
print(machine2.video)

# isinstance(인스턴스, 클래스) since 2.2
print(isinstance(machine, c.Computer)) 

'''
레퍼런스 카운터 테스트
machine_copy = machine  --> counter : 2
del machine             --> counter : 1
del machine_copy        --> counter : 0
'''

# 정적메소드, 클래스메소드 등록
# staticmethod(...), classmethod(...)
