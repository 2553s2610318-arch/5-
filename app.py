import streamlit as st
import random

st.set_page_config(
    page_title="순서 정하기 앱",
    page_icon="🎲",
    layout="centered"
)

st.title("🎲 순서 정하기 앱")
st.caption("발표, 게임, 면접, 당번 등의 순서를 랜덤으로 정하고 진행 상황을 관리합니다.")

# 세션 상태 초기화
if "order" not in st.session_state:
    st.session_state.order = []

if "current_index" not in st.session_state:
    st.session_state.current_index = -1

if "generated" not in st.session_state:
    st.session_state.generated = False


def reset_all():
    st.session_state.order = []
    st.session_state.current_index = -1
    st.session_state.generated = False


st.subheader("참가자 입력")

participants_text = st.text_area(
    "이름을 한 줄에 한 명씩 입력하세요",
    height=200,
    placeholder="""홍길동
김철수
이영희
박민수"""
)

col1, col2 = st.columns(2)

with col1:
    generate_btn = st.button("🎲 순서 생성", use_container_width=True)

with col2:
    reset_btn = st.button("🔄 초기화", use_container_width=True)

if reset_btn:
    reset_all()
    st.rerun()

if generate_btn:
    participants = [
        name.strip()
        for name in participants_text.split("\n")
        if name.strip()
    ]

    if len(participants) == 0:
        st.error("참가자를 1명 이상 입력해주세요.")
    else:
        random.shuffle(participants)

        st.session_state.order = participants
        st.session_state.current_index = -1
        st.session_state.generated = True

if st.session_state.generated:

    st.divider()

    st.subheader("📋 생성된 순서")

    for idx, person in enumerate(st.session_state.order, start=1):
        st.write(f"{idx}. {person}")

    st.divider()

    total = len(st.session_state.order)
    completed = max(0, st.session_state.current_index + 1)
    remaining = total - completed

    col1, col2, col3 = st.columns(3)

    col1.metric("전체 인원", total)
    col2.metric("완료", completed)
    col3.metric("남은 인원", remaining)

    st.subheader("▶ 진행 관리")

    if st.session_state.current_index == -1:
        st.info("아직 시작되지 않았습니다.")

    elif st.session_state.current_index < total:
        current_person = st.session_state.order[
            st.session_state.current_index
        ]

        st.success(
            f"현재 순서: {current_person}"
        )

    if st.session_state.current_index >= total:
        st.balloons()
        st.success("모든 순서가 완료되었습니다!")

    next_btn = st.button(
        "다음 순서",
        use_container_width=True
    )

    if next_btn:
        if st.session_state.current_index < total:
            st.session_state.current_index += 1
            st.rerun()

    st.divider()

    st.subheader("✅ 완료된 사람")

    completed_people = st.session_state.order[
        :max(0, st.session_state.current_index + 1)
    ]

    if completed_people:
        for person in completed_people:
            st.write(f"✔ {person}")
    else:
        st.write("아직 없음")

    st.subheader("⏳ 남은 사람")

    remaining_people = st.session_state.order[
        max(0, st.session_state.current_index + 1):
    ]

    if remaining_people:
        for person in remaining_people:
            st.write(f"• {person}")
    else:
        st.write("없음")
