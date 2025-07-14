import pandas as pd

# CSV 파일 불러오기
df = pd.read_csv("CCKP(에티오피아).csv")

# 맨 앞 열에 'iso 2자리 코드' 열 추가하고 모든 행에 'ET' 입력
df.insert(0, 'iso 2자리 코드', 'ET')

# 결과 저장 (선택)
df.to_csv("CCKP(에티오피아)_ET_열 추가.csv", index=False)

# 확인
print(df.head())
