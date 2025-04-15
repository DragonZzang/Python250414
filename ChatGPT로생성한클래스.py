# 클래스 정의
class Person:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def printInfo(self):
        #f-string 문법으로 변수명 바로 넘김
        print(f"[Person] ID: {self.id}, Name: {self.name}")


class Manager(Person):
    def __init__(self, id, name, title):
        super().__init__(id, name)
        self.title = title

    def printInfo(self):
        print(f"[Manager] ID: {self.id}, Name: {self.name}, Title: {self.title}")


class Employee(Person):
    def __init__(self, id, name, skill):
        super().__init__(id, name)
        self.skill = skill

    def printInfo(self):
        print(f"[Employee] ID: {self.id}, Name: {self.name}, Skill: {self.skill}")


# 테스트 코드
def run_tests():
    print("=== 테스트 시작 ===")
    
    # 테스트 1: 기본 Person 객체 생성 및 출력
    p1 = Person(1, "Alice")
    p1.printInfo()

    # 테스트 2: Manager 객체 생성 및 출력
    m1 = Manager(2, "Bob", "Project Manager")
    m1.printInfo()

    # 테스트 3: Employee 객체 생성 및 출력
    e1 = Employee(3, "Charlie", "Python")
    e1.printInfo()

    # 테스트 4: ID가 0인 Person
    p2 = Person(0, "Zero")
    p2.printInfo()

    # 테스트 5: 빈 이름을 가진 Manager
    m2 = Manager(4, "", "Team Lead")
    m2.printInfo()

    # 테스트 6: 특수문자 포함 이름 Employee
    e2 = Employee(5, "J@ne D0e", "Java")
    e2.printInfo()

    # 테스트 7: Manager 객체의 title 변경 확인
    m1.title = "Senior Manager"
    m1.printInfo()

    # 테스트 8: Employee 객체의 skill 변경 확인
    e1.skill = "JavaScript"
    e1.printInfo()

    # 테스트 9: 여러 Manager 인스턴스 테스트
    for i in range(6, 9):
        m = Manager(i, f"Manager{i}", f"Title{i}")
        m.printInfo()

    # 테스트 10: Employee 인스턴스 리스트에서 정보 출력
    employees = [
        Employee(9, "Dave", "C++"),
        Employee(10, "Eve", "SQL"),
    ]
    for emp in employees:
        emp.printInfo()

    print("=== 테스트 완료 ===")

# 테스트 실행
run_tests()
