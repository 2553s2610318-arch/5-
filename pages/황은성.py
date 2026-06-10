import streamlit as st
import google.generativeai as genai

st.set_page_config(
    page_title="체육 종목 단점 보완 코치",
    page_icon="🏃",
    layout="centered"
)

st.title("🏃 체육 종목 단점 보완 코치")
st.write(
    "자신이 어려워하는 체육 종목과 부족한 부분을 입력하면 "
    "AI가 연습 방법과 마음가짐을 알려드립니다."
)

# API 설정
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except Exception:
    st.error("GEMINI_API_KEY가 설정되지 않았습니다.")
    st.stop()

# 종목 선택
sports = [
    "축구",
    "농구",
    "배구",
    "피구",
    "달리기",
    "줄넘기",
    "배드민턴",
    "탁구",
    "기타"
]

sport = st.selectbox(
    "체육 종목 선택",
    sports
)

if sport == "기타":
    sport = st.text_input("직접 종목 입력")

weakness = st.text_area(
    "부족한 부분 입력",
    placeholder="예) 공을 잘 못 찬다, 체력이 부족하다, 드리블이 어렵다"
)

if st.button("AI 코칭 받기"):

    if not sport:
        st.warning("종목을 입력해주세요.")
        st.stop()

    if not weakness.strip():
        st.warning("부족한 부분을 입력해주세요.")
        st.stop()

    prompt = f"""
당신은 학교 체육 코치입니다.

종목: {sport}
부족한 점: {weakness}

다음 형식으로 친절하게 작성하세요.

① 부족한 점 분석

② 연습 방법 5가지

③ 경기 중 주의사항

④ 자신감을 높이는 마음가짐

⑤ 1주일 훈련 계획

학생이 이해하기 쉽게 작성하세요.
"""

    try:
        model = genai.GenerativeModel(
            "gemini-2.5-flash-lite"
        )

        response = model.generate_content(prompt)

        st.success("분석 완료!")

        st.markdown("## 📋 AI 코칭 결과")
        st.write(response.text)

    except Exception as e:
        st.error("AI 응답 생성 중 오류가 발생했습니다.")
        st.error(str(e))

st.divider()

st.markdown(
    """
### 💡 활용 예시

- 종목: 축구
- 부족한 점: 슛 정확도가 낮음

- 종목: 농구
- 부족한 점: 드리블이 서툼

- 종목: 달리기
- 부족한 점: 체력이 약함
"""
)
