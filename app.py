import streamlit as st
import random
import time

st.set_page_config(
    page_title="오늘의 AI 운세",
    page_icon="🔮",
    layout="centered"
)

st.title("🔮 오늘의 AI 운세")
st.write("이름을 입력하고 오늘의 운세를 확인하세요!")

name = st.text_input("이름 입력")

fortunes = [
    "오늘은 예상치 못한 행운이 찾아옵니다 🍀",
    "커피를 마시면 좋은 아이디어가 떠오릅니다 ☕",
    "누군가 당신에게 고마워할 일이 생깁니다 😊",
    "코딩 실력이 +1 상승합니다 💻",
    "오늘 밤 야식의 유혹을 조심하세요 🍗",
    "새로운 도전을 시작하기 좋은 날입니다 🚀",
    "버그 하나를 잡고 레벨업합니다 🐞",
    "뜻밖의 메시지를 받게 됩니다 📩"
]

scores = {
    "연애운 ❤️": random.randint(1, 100),
    "금전운 💰": random.randint(1, 100),
    "코딩운 👨‍💻": random.randint(1, 100),
    "건강운 🏃": random.randint(1, 100),
}

if st.button("운세 보기"):
    if name.strip() == "":
        st.warning("이름을 입력해주세요!")
    else:
        with st.spinner("AI가 운세를 분석 중입니다..."):
            time.sleep(2)

        st.success(f"{name}님의 오늘 운세!")

        st.subheader(random.choice(fortunes))

        st.write("---")

        for k, v in scores.items():
            st.write(f"### {k}")
            st.progress(v)
            st.write(f"{v}점")
