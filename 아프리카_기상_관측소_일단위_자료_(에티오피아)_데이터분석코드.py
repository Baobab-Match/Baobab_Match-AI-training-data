import pandas as pd
import calendar

# ===== CSV 불러오기 및 전처리 =====
df = pd.read_csv("아프리카_기상_관측소_일단위_자료_(에티오피아).csv")

# 날짜 처리
df['OBSR_DE'] = pd.to_datetime(df['OBSR_DE'].astype(str), format="%Y%m%d", errors='coerce')
df = df[df['OBSR_DE'] >= '1995-01-01']

# 컬럼명 정리
df.rename(columns={
    'OBSR_SN': '관측소_일련번호',
    'OBSRVT_NO': '관측소_번호',
    'NATION_CD': '국가코드',
    'OBSR_DE': '날짜',
    'PRCPT_QY': '강수량_mm',
    'AVRG_TP': '평균기온_℉',
    'MXMM_TP': '최고기온_℉',
    'LWET_TP': '최저기온_℉',
    'DEW_POINT_TP': '이슬점_℉',
    'AVRG_WIND_VE': '평균풍속_m/s',
    'AVRG_SLVL_ARCSR_VAL': '해면기압_hPa'
}, inplace=True)

# 결측치 제거
df_clean = df.dropna(subset=[
    '강수량_mm', '평균기온_℉', '최고기온_℉', '최저기온_℉',
    '이슬점_℉', '평균풍속_m/s', '해면기압_hPa'
])

# 화씨 → 섭씨 변환 함수
def f_to_c(f):
    return (f - 32) * 5 / 9

# 변환 적용
df_clean['평균기온_℃'] = df_clean['평균기온_℉'].apply(f_to_c)
df_clean['최고기온_℃'] = df_clean['최고기온_℉'].apply(f_to_c)
df_clean['최저기온_℃'] = df_clean['최저기온_℉'].apply(f_to_c)
df_clean['이슬점_℃'] = df_clean['이슬점_℉'].apply(f_to_c)

# 월 및 월 이름 추가
df_clean['월'] = df_clean['날짜'].dt.month
df_clean['월_이름'] = df_clean['월'].astype(str) + "월"

# ===== 월별 요약 =====
monthly_summary = df_clean.groupby('월').agg({
    '강수량_mm': 'sum',
    '평균기온_℃': 'mean',
    '최고기온_℃': 'mean',
    '최저기온_℃': 'mean',
    '이슬점_℃': 'mean',
    '평균풍속_m/s': 'mean',
    '해면기압_hPa': 'mean'
}).reset_index()

# ===== 기술 라벨링 함수 =====
def label_technology(row):
    labels = []

    # 강수량 라벨
    if row['강수량_mm'] < 50:
        labels.append("가뭄 대응 기술")
    elif 50 <= row['강수량_mm'] < 300:
        labels.append("스마트 관개 기술")
    elif 300 <= row['강수량_mm'] < 800:
        labels.append("일반 강우 대비 기술")
    else:
        labels.append("홍수 대응·물 관리 기술")

    # 기온 라벨
    if row['평균기온_℃'] >= 30:
        labels.append("고온 대응 기술")
    elif row['평균기온_℃'] < 15:
        labels.append("저온 대응 기술")
    elif 15 <= row['평균기온_℃'] < 25:
        labels.append("적정 기온 유지 기술")

    # 풍속 라벨
    if row['평균풍속_m/s'] >= 6:
        labels.append("풍력 에너지 기술")
    elif row['평균풍속_m/s'] >= 3:
        labels.append("소형 풍력 가능 지역")

    return ", ".join(labels)

# 라벨 적용
monthly_summary['추천_기술_라벨'] = monthly_summary.apply(label_technology, axis=1)

# iso 2자리코드 추가
monthly_summary['iso 2자리코드'] = 'ET'

# 컬럼 순서 정리
cols_order = ['iso 2자리코드', '월', '강수량_mm', '평균기온_℃', '최고기온_℃', '최저기온_℃',
              '이슬점_℃', '평균풍속_m/s', '해면기압_hPa', '추천_기술_라벨']
monthly_summary = monthly_summary[cols_order]

# ===== 저장 및 출력 =====
monthly_summary.to_csv("AI학습용_에티오피아_월별기후요약_기술매칭.csv", index=False)

print("✅ 월별 요약 데이터 저장 완료!")
print(monthly_summary[['iso 2자리코드', '강수량_mm', '평균기온_℃', '평균풍속_m/s', '추천_기술_라벨']])