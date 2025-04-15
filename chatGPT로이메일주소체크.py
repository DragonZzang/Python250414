import re

# 이메일 유효성 검사 함수
def is_valid_email(email):
    # 간단하고 일반적인 이메일 패턴
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


# 테스트용 이메일 주소 목록 (유효한 것과 유효하지 않은 것 섞여 있음)
email_samples = [
    "test@example.com",         # 유효
    "user.name@domain.co",      # 유효
    "user_name@domain.com",     # 유효
    "username123@sub.domain.net", # 유효
    "user-name@domain.org",     # 유효
    "invalid-email@",           # 무효
    "@no-local-part.com",       # 무효
    "no-at-symbol.com",         # 무효
    "user@.com",                # 무효
    "user@domain..com"          # 무효
]

# 검사 실행
print("=== 이메일 유효성 검사 ===")
for email in email_samples:
    result = is_valid_email(email)
    print(f"{email}: {'유효함 ✅' if result else '무효함 ❌'}")