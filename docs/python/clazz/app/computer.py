class Computer:
    # 클래스 멤버 변수들 
    power = ''
    cpu = ''
    memory = 0
    hdd = 0
    # 첫번째 인수는 this 변수, 변수명이 self 가 아니라도 됨
    # 생성자를 통해서 멤버변수에 값설정하는 로직이 있어야 com.__dict__ 를 통해 인스턴스값들을 확인.
    # 멤버변수 선언시 값을 초기화해도 [변수 = 값] 대입이 발생하기 전에는 __dict__ 로 값이 안나옴 
    def __init__(self, power, cpu, memory, hdd):
        self.power = power  # self 를 통한 인스턴스 변수??
        self.cpu = cpu
        self.memory = memory
        self.hdd = hdd

    # 멤버 메소드 
    def turnon(self):
        print('booting...')
        self.power = True
        print('Welcome~ start your computer')

# machine = Computer(False, '1GHz', '4GB', '1TB')
machine = Computer()    
machine.turnon() # bound 메소드 호출(self 를 넘기지 않는 호출 방식)
