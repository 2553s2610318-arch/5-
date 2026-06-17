import streamlit as st

# =========================
# 기본 설정
# =========================
st.set_page_config(page_title="체육 약점 보완 트레이너", page_icon="🏃")

st.title("🏃 체육 약점 보완 트레이너")
st.write("자신이 부족한 체육 종목을 입력하면 맞춤 연습 방법과 마음가짐을 알려드립니다.")

# =========================
# 입력 UI
# =========================
sport = st.text_input("운동 종목을 입력하세요 (예: 축구, 농구, 달리기, 배드민턴 등)")
weakness = st.text_area("현재 부족한 점을 적어주세요 (예: 체력이 부족하다, 드리블이 약하다)")
level = st.selectbox("현재 실력 수준", ["초급", "중급", "고급"])

# =========================
# 기본 추천 로직
# =========================
def generate_plan(sport, weakness, level):
    plan = f"""
### 🧠 분석 결과
- 종목: {sport}
- 수준: {level}
- 주요 약점: {weakness}

---

### 🏋️ 맞춤 연습 방법

1. 기본기 반복 훈련 (매일 20~30분)
   - 정확한 동작을 느리게 반복하기
   - 거울 또는 영상 촬영 활용

2. 약점 집중 훈련
   - 약한 부분만 따로 분리해서 연습
   - 예: 체력 부족 → 인터벌 달리기
   - 예: 드리블 약함 → 콘 드리블 훈련

3. 실전 적용 훈련
   - 실제 경기 상황을 가정해서 연습
   - 친구 또는 혼자 시뮬레이션

---

### 📅 추천 루틴 (주간)

- 월/수/금: 기본기 + 약점 훈련
- 화/목: 체력 및 보조 운동
- 토: 실전 경기 연습
- 일: 휴식 + 스트레칭

---

### 🧘 마음가짐 (중요)

- 실력 향상은 “반복”에서 나온다
- 하루 1%씩만 성장해도 충분하다
- 실패는 연습 과정의 일부이다
- 비교하지 말고 “어제의 나”와 비교하라
"""
    return plan


# =========================
# Gemini AI (선택 기능)
# =========================
def gemini_feedback(sport, weakness, level):
    try:
        import google.generativeai as genai

        api_key = st.secrets.get("GEMINI_API_KEY", None)
        if not api_key:
            return None

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.5-flash-lite")

        prompt = f"""
너는 체육 코치이다.
종목: {sport}
수준: {level}
약점: {weakness}

다음 3가지를 한국어로 알려줘:
1. 핵심 문제 분석
2. 개선 훈련 방법
3. 멘탈 조언
"""

        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        return None


# =========================
# 실행 버튼
# =========================
if st.button("훈련 계획 생성하기"):
    if not sport or not weakness:
        st.warning("종목과 부족한 점을 모두 입력해주세요.")
    else:
        st.subheader("📌 기본 맞춤 훈련 계획")
        st.markdown(generate_plan(sport, weakness, level))

        st.subheader("🧠 AI 추가 코칭 (선택)")

        ai_result = gemini_feedback(sport, weakness, level)

        if ai_result:
            st.success(ai_result)
        else:
            st.info("AI 기능은 설정되지 않았거나 오류가 발생하여 기본 코칭만 제공합니다.")
