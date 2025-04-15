# demoFile.py

#유니코드로 쓰기(utf-8)
f = open("c:\\work\\test.txt", "wt", encoding="utf-8")
f.write("첫 번째 \n두 번째 \n세 번째 \n")
f.close()

#읽기
f = open(r"c:\work\test.txt", "rt", encoding="utf-8")
result = f.read()
print(result)
f.close()