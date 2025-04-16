import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook

# 검색어와 URL
query = "반도체"
url = f"https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query={query}"

# User-Agent 헤더 설정
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

try:
    # 요청 및 파싱
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # HTTP 요청 에러 확인
    soup = BeautifulSoup(response.text, "html.parser")

    # 뉴스 제목 링크 추출
    titles = soup.select("a.news_tit")

    if not titles:
        print("뉴스 제목을 찾을 수 없습니다. CSS 선택자를 확인하세요.")
    else:
        # 엑셀 파일 생성
        wb = Workbook()
        ws = wb.active
        ws.title = "News Results"

        # 헤더 추가
        ws.append(["번호", "제목", "링크"])

        # 데이터 추가
        for idx, title in enumerate(titles, 1):
            ws.append([idx, title['title'], title['href']])

        # 엑셀 저장
        file_path = "results.xlsx"
        wb.save(file_path)
        print(f"{file_path} 파일이 저장되었습니다. 총 {len(titles)}개의 뉴스가 저장되었습니다.")

except requests.exceptions.RequestException as e:
    print(f"HTTP 요청 중 오류가 발생했습니다: {e}")
except Exception as e:
    print(f"오류가 발생했습니다: {e}")
