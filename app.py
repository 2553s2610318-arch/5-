import streamlit as st
from google import genai
from google.genai import types

# 페이지 설정
st.set_page_config(
    page_title="연애상담 챗봇",
    page_icon="💌",
)

st.title("💌 연애상담 챗봇")
st.caption("Gemini 2.5 Flash Lite 기반")

# API 키 불러오기
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    st.error("Secrets에 GEMINI_API_KEY를 설정해주세요.")
    st.stop()

# Gemini 클라이언트 생성
try:
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error(f"Gemini 클라이언트 생성 실패: {e}")
    st.stop()

# 채팅 기록 저장
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "안녕하세요 😊 연애 고민을 편하게 이야기해주세요!"
        }
    ]

# 이전 채팅 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력
prompt = st.chat_input("고민을 입력해주세요...")

if prompt:
    # 사용자 메시지 저장
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    # 사용자 메시지 출력
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI 응답 생성
    with st.chat_message("assistant"):
        message_placeholder = st.empty()

        try:
            # Gemini용 대화 변환
            history_text = ""

            for msg in st.session_state.messages:
                role = "사용자" if msg["role"] == "user" else "상담사"
                history_text += f"{role}: {msg['content']}\n"

            system_prompt = """
            너는 공감 능력이 뛰어난 연애상담 전문가야.
            사용자의 감정을 존중하고 따뜻하게 답변해.
            너무 단정적으로 판단하지 말고 현실적인 조언을 제공해.
            답변은 친근한 한국어로 작성해.
            """

            full_prompt = f"""
            시스템 지침:
            {system_prompt}

            대화 기록:
            {history_text}

            상담사:
            """

            response = client.models.generate_content(
                model="gemini-2.5-flash-lite",
                contents=full_prompt,
                config=types.GenerateContentConfig(
                    temperature=0.8,
                    max_output_tokens=500,
                )
            )

            ai_response = response.text

            message_placeholder.markdown(ai_response)

            # 응답 저장
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": ai_response
                }
            )

        except Exception as e:
            error_message = f"""
            ⚠️ 오류가 발생했습니다.

            오류 내용:
            {str(e)}
            """

            message_placeholder.error(error_message)
