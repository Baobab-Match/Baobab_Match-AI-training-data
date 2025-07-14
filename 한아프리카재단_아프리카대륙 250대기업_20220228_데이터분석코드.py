import pandas as pd
import re

# 1. 텍스트 정제 함수
def clean_text(text):
    if pd.isna(text):
        return ""
    text = re.sub(r"[^a-zA-Z0-9가-힣\s]", " ", str(text))
    text = text.lower()
    text = re.sub(r"\s+", " ", text).strip()
    return text

# 2. 아프리카 국가명 → ISO 2자리코드 맵 (지역 기준 정렬)
africa_iso_map = {
    # 북아프리카
    "알제리": "DZ", "이집트": "EG", "리비아": "LY", "모로코": "MA", "수단": "SD", "튀니지": "TN",

    # 서아프리카
    "베냉": "BJ", "부르키나파소": "BF", "카보베르데": "CV", "코트디부아르": "CI", "감비아": "GM",
    "가나": "GH", "기니": "GN", "기니비사우": "GW", "라이베리아": "LR", "말리": "ML",
    "모리타니": "MR", "니제르": "NE", "나이지리아": "NG", "세네갈": "SN", "시에라리온": "SL", "토고": "TG",

    # 중앙아프리카
    "앙골라": "AO", "카메룬": "CM", "중앙아프리카공화국": "CF", "차드": "TD", "콩고": "CG",
    "콩고민주공화국": "CD", "적도기니": "GQ", "가봉": "GA", "상투메프린시페": "ST",

    # 동아프리카
    "부룬디": "BI", "코모로": "KM", "지부티": "DJ", "에리트레아": "ER", "에티오피아": "ET",
    "케냐": "KE", "마다가스카르": "MG", "말라위": "MW", "모리셔스": "MU", "르완다": "RW",
    "세이셸": "SC", "소말리아": "SO", "남수단": "SS", "탄자니아": "TZ", "우간다": "UG", "잠비아": "ZM", "짐바브웨": "ZW",

    # 남아프리카
    "보츠와나": "BW", "레소토": "LS", "나미비아": "NA", "남아프리카공화국": "ZA", "에스와티니": "SZ"
}

# 3. 카테고리별 키워드 정의
category_keywords = {
    "재생에너지 및 에너지전환": [
        "태양광", "풍력", "지열", "수력", "해상풍력", "수소", "신재생에너지",
        "에너지전환", "에너지자립", "탈탄소", "탄소중립",
        "renewable energy", "solar", "wind", "geothermal", "hydropower",
        "biomass energy", "hydrogen energy", "decarbonization", "carbon neutral", "energy transition"
    ],
    "물 부족 및 정수 기술": [
        "가뭄", "식수", "정수", "수질", "빗물", "관개", "지하수", "물관리",
        "drought", "drinking water", "water purification", "rainwater harvesting",
        "irrigation system", "groundwater", "water management", "filtration"
    ],
    "홍수 및 재해 대응 인프라": [
        "홍수", "폭풍", "열대폭풍", "배수시설", "침수", "재난", "복구", "경보 시스템", "토양 침식",
        "flood", "storm", "tropical cyclone", "drainage", "disaster recovery", "early warning", "erosion control"
    ],
    "농업 및 식량안보": [
        "식량안보", "흉작", "기근", "영양실조", "농업", "작물", "비료",
        "food security", "crop failure", "famine", "malnutrition", "agriculture", "fertilizer"
    ],
    "기후변화 대응 및 탄소감축": [
        "기후변화", "온실가스", "탄소배출", "감축", "배출권거래", "net zero",
        "climate change", "greenhouse gas", "carbon emission", "carbon reduction", "emissions trading", "carbon saving"
    ],
    "친환경 교통 및 인프라": [
        "전기차", "수소차", "친환경 교통", "지속가능 인프라", "그린빌딩",
        "electric vehicle", "hydrogen vehicle", "eco-friendly transport",
        "sustainable infrastructure", "green building"
    ],
    "자원순환 및 친환경 소재": [
        "폐기물 처리", "재활용", "생분해성", "바이오 플라스틱", "대체 소재",
        "waste management", "recycling", "biodegradable", "bioplastic", "alternative material"
    ],
    "교육 및 역량 강화": [
        "환경 교육", "디지털 학습", "모바일 학습", "교육 플랫폼", "역량 강화",
        "environmental education", "digital learning", "mobile learning",
        "learning platform", "capacity building"
    ],
    "사회적 갈등 및 강제이주": [
        "강제이주", "내전", "분쟁", "폭력", "난민", "이재민", "주거 불안정", "사회 갈등",
        "forced migration", "civil war", "conflict", "violence", "refugee", "displacement", "housing insecurity", "social conflict"
    ]
}

# 4. 카테고리 분류 함수
def assign_category(text):
    text = clean_text(text)
    matched = []
    for category, keywords in category_keywords.items():
        for kw in keywords:
            if kw in text:
                matched.append(category)
                break
    return matched if matched else []

# 5. 데이터 불러오기 및 전처리
df = pd.read_csv("한아프리카재단_아프리카대륙 250대기업_20220228.csv", encoding='utf-8-sig')
df = df[['iso 2자리코드', '기업명(국문)', '취급분야']].copy()
df['정제된취급분야'] = df['취급분야'].apply(clean_text)
df['카테고리리스트'] = df['정제된취급분야'].apply(assign_category)
df_exploded = df.explode('카테고리리스트')
df_exploded = df_exploded[df_exploded['카테고리리스트'] != ""]

# 6. 피벗 테이블 (국가별 카테고리별 기업 수)
df_pivot = pd.pivot_table(
    df_exploded,
    index='iso 2자리코드',
    columns='카테고리리스트',
    values='기업명(국문)',
    aggfunc='count',
    fill_value=0
).reset_index()

# 7. 아프리카 국가 전체 포함 후 결측 0 채우기
africa_iso_list = list(africa_iso_map.values())
df_all_iso = pd.DataFrame({'iso 2자리코드': africa_iso_list})
df_final = df_all_iso.merge(df_pivot, on='iso 2자리코드', how='left').fillna(0)

# 8. 모든 카테고리 값이 0인 행 제거
category_cols = [col for col in df_final.columns if col != 'iso 2자리코드']
df_final = df_final[df_final[category_cols].sum(axis=1) > 0]

# 9. 저장 및 출력
df_final.to_csv("AI학습용_아프리카진출기업_분류데이터.csv", index=False, encoding='utf-8-sig')
print(df_final.head())
