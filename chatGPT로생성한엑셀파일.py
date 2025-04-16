import random
from openpyxl import Workbook

# 엑셀 파일 생성
wb = Workbook()
ws = wb.active
ws.title = "제품리스트"

# 헤더 추가
ws.append(["제품ID", "제품명", "수량", "가격"])

# 샘플 데이터 생성
product_names = ["TV", "냉장고", "세탁기", "에어컨", "전자레인지", "청소기", "컴퓨터", "스피커", "모니터", "키보드"]

for i in range(1, 101):  # 100개의 데이터 생성
    product_id = f"P{i:03d}"  # 제품ID (P001, P002, ...)
    product_name = random.choice(product_names)  # 랜덤 제품명 선택
    quantity = random.randint(1, 50)  # 수량 (1~50 랜덤)
    price = random.randint(100, 10000)  # 가격 (10,000원 ~ 1,000,000원 랜덤)
    ws.append([product_id, product_name, quantity, price])

# 엑셀 파일 저장
file_path = "products.xlsx"
wb.save(file_path)
print(f"{file_path} 파일이 생성되었습니다.")