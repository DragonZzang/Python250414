#전역변수
strName = "Not Class Member"

class DemoString:
    def __init__(self):
        #인스턴스 멤버 변수
        self.strName = "" 
    def set(self, msg):
        self.strName = msg
    def print(self):
        #버그 발생!
        print(strName)
        print(self.strName)

d = DemoString()
d.set("First Message")
d.print()
