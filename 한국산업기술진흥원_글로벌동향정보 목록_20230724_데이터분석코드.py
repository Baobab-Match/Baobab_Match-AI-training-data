import pandas as pd
import re

# 1. 텍스트 정제 함수 (특수문자 제거, 소문자 변환, 공백 정리)
def clean_text(text):
    if pd.isna(text):
        return ""
    text = re.sub(r"[^a-zA-Z0-9가-힣\s]", " ", str(text))
    text = text.lower()
    text = re.sub(r"\s+", " ", text).strip()
    return text


# 2. CSV 파일 불러오기
file_path = "한국산업기술진흥원_글로벌동향정보 목록_20230724.csv"
df = pd.read_csv(file_path, encoding='cp949')

# 3. 필요한 열만 추출
df_clean = df[['기관기업고유번호', '기술명칭']].copy()

# 4. 정제된기술명 열 추가
df_clean['정제된기술명'] = df_clean['기술명칭'].apply(clean_text)

# 5. 카테고리별 키워드 정의
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

# 6. 카테고리 분류 함수
def assign_category(text):
    matched = []
    for category, keywords in category_keywords.items():
        for kw in keywords:
            if kw.lower() in text.lower():
                matched.append(category)
                break
    return ", ".join(matched) if matched else "분류없음"

# 7. 카테고리 열 추가
df_clean['카테고리'] = df_clean['정제된기술명'].apply(assign_category)

# 8. 분류된 데이터만 필터링
df_classified = df_clean[df_clean['카테고리'] != "분류없음"].copy()

# 9. 결과 확인
print(f"총 데이터 개수: {len(df_clean)}")
print(f"분류된 데이터 개수: {len(df_classified)}")
print("\n=== 분류된 샘플 ===")
print(df_classified.head(10))

# 10. CSV로 저장
df_classified.to_csv("AI학습용_해외진출기업_분류데이터.csv", index=False, encoding='utf-8-sig')

