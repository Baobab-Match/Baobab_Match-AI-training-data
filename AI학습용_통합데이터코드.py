import pandas as pd

# 1. 데이터 불러오기
df_company = pd.read_csv("AI학습용_아프리카진출기업_분류데이터.csv")
df_cooperation = pd.read_csv("AI학습용_아프리카과거기후협력_분류데이터.csv")

# 2. 열 이름 정리: 공백, 슬래시 등 제거
clean_columns = lambda cols: cols.str.strip().str.replace("/", "", regex=False).str.replace("  ", " ")

df_company.columns = clean_columns(df_company.columns)
df_cooperation.columns = clean_columns(df_cooperation.columns)

# 3. ISO 코드 열 이름 통일
df_company.rename(columns={"iso 2자리코드": "ISO"}, inplace=True)
df_cooperation.rename(columns={"iso 2자리코드": "ISO"}, inplace=True)

# 4. 접미어 추가: 열 이름에 '기업 수', '협력 이력 수'
df_company = df_company.set_index("ISO")
df_cooperation = df_cooperation.set_index("ISO")

df_company.columns = [f"{col.strip()}_기업 수" for col in df_company.columns]
df_cooperation.columns = [f"{col.strip()}_협력 이력 수" for col in df_cooperation.columns]

# 5. ISO 기준 병합
df_merged = pd.merge(df_company, df_cooperation, left_index=True, right_index=True, how="outer")

# 6. NaN → 0, 정수형 변환
df_merged = df_merged.fillna(0).astype(int)

# 7. 인덱스 초기화 (ISO를 열로 이동)
df_merged = df_merged.reset_index()

# 8. CSV 저장
df_merged.to_csv("AI학습용_통합데이터.csv", encoding='utf-8-sig', index=False)