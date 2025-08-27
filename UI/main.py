# streamlit_recipe_app.py

import streamlit as st
from dotenv import load_dotenv

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 이미지 경로 설정
ASSETS_PATH = os.path.join(os.path.dirname(__file__), "assets", "images")
USER_AVATAR_PATH = os.path.join(ASSETS_PATH, "user_avatar.png")
ASSISTANT_AVATAR_PATH = os.path.join(ASSETS_PATH, "assistant_avatar.png")

from State import *
from Mcp_Tool import *
from Node import *
from Graph import *

# =============================
# 🌱 초기 설정
# =============================

# 환경 변수 로드 (OpenAI API 키 등)
load_dotenv()

# LangGraph 인스턴스 생성
graph_app = Project_Graph()

# 페이지 설정
st.set_page_config(page_title="식사비서 재규니", layout="wide", page_icon="🍽️")

# CSS 스타일 추가  
st.markdown("""
<style>
/* 전체 채팅 영역 스타일링 - 헤더 높이만큼 여백 추가 */
.main .block-container {
    padding-top: 6rem !important;
    padding-bottom: 5rem !important;
}

/* 헤더 고정 - 다크모드 대응 */
header[data-testid="stHeader"] {
    position: fixed !important;
    top: 0 !important;
    left: 0 !important;
    right: 0 !important;
    z-index: 999999 !important;
    background: var(--background-color) !important;
    border-bottom: 1px solid var(--secondary-background-color) !important;
}

/* 다크모드 감지 및 헤더 배경색 설정 */
@media (prefers-color-scheme: dark) {
    header[data-testid="stHeader"] {
        background: #0e1117 !important;
        border-bottom: 1px solid #262730 !important;
    }
}

/* Streamlit 다크모드 클래스가 있을 때 */
.dark header[data-testid="stHeader"],
[data-theme="dark"] header[data-testid="stHeader"] {
    background: #0e1117 !important;
    border-bottom: 1px solid #262730 !important;
}

/* 사용자 메시지만 오른쪽 정렬 - img alt="user avatar"로 구분 */
.stChatMessage:has(img[alt="user avatar"]) {
    display: flex !important;
    flex-direction: row-reverse !important;
    justify-content: flex-start !important;
    margin-bottom: 1.5rem !important;
    padding: 0 1rem !important;
}

/* 어시스턴트 메시지는 왼쪽 정렬 - img alt="assistant avatar"로 구분 */
.stChatMessage:has(img[alt="assistant avatar"]) {
    display: flex !important;
    flex-direction: row !important;
    justify-content: flex-start !important;
    margin-bottom: 1.5rem !important;
    padding: 0 1rem !important;
}

/* 사용자 메시지 내용 - 모던한 파란색 말풍선 */
.stChatMessage:has(img[alt="user avatar"]) [data-testid="stChatMessageContent"] {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    color: white !important;
    border-radius: 20px 20px 5px 20px !important;
    margin-left: auto !important;
    margin-right: 0.75rem !important;
    max-width: 75% !important;
    padding: 1rem 1.25rem !important;
    box-shadow: 0 2px 10px rgba(102, 126, 234, 0.3) !important;
    overflow: hidden !important;
    border: none !important;
}

/* 사용자 메시지 모든 emotion-cache 클래스 배경 제거 */
.stChatMessage:has(img[alt="user avatar"]) [class*="st-emotion-cache"] {
    background: transparent !important;
}

.stChatMessage:has(img[alt="user avatar"]) [data-testid="stChatMessageContent"] {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
}

/* 사용자 메시지의 기본 배경 제거 */
.stChatMessage:has(img[alt="user avatar"]) [data-testid="stChatMessageContent"]::before,
.stChatMessage:has(img[alt="user avatar"]) [data-testid="stChatMessageContent"]::after {
    display: none !important;
}

.stChatMessage:has(img[alt="user avatar"]) [data-testid="stChatMessageContent"] > div {
    background: transparent !important;
}

/* 사용자 메시지 내부 컨테이너들 스타일 재설정 */
.stChatMessage:has(img[alt="user avatar"]) [data-testid="stChatMessageContent"] .stVerticalBlock,
.stChatMessage:has(img[alt="user avatar"]) [data-testid="stChatMessageContent"] .stElementContainer,
.stChatMessage:has(img[alt="user avatar"]) [data-testid="stChatMessageContent"] .stMarkdown {
    background: transparent !important;
    padding: 0 !important;
    margin: 0 !important;
}

/* 어시스턴트 메시지 컨테이너 - 왼쪽 정렬 */
.stChatMessage:has([data-testid="stChatMessageAvatarAssistant"]) {
    display: flex !important;
    flex-direction: row !important;
    justify-content: flex-start !important;
    margin-bottom: 1.5rem !important;
    padding: 0 1rem !important;
}

/* 어시스턴트 메시지 내용 - 세련된 회색 말풍선 */
.stChatMessage:has(img[alt="assistant avatar"]) [data-testid="stChatMessageContent"] {
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%) !important;
    color: #2d3748 !important;
    border-radius: 20px 20px 20px 5px !important;
    margin-right: auto !important;
    margin-left: 0.75rem !important;
    max-width: 75% !important;
    padding: 1rem 1.25rem !important;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1) !important;
    border: 1px solid rgba(195, 207, 226, 0.5) !important;
    overflow: hidden !important;
}

/* 어시스턴트 메시지 내부 컨테이너들 스타일 재설정 */
.stChatMessage:has(img[alt="assistant avatar"]) [data-testid="stChatMessageContent"] .stVerticalBlock,
.stChatMessage:has(img[alt="assistant avatar"]) [data-testid="stChatMessageContent"] .stElementContainer,
.stChatMessage:has(img[alt="assistant avatar"]) [data-testid="stChatMessageContent"] .stMarkdown {
    background: transparent !important;
    padding: 0 !important;
    margin: 0 !important;
}

/* 메시지 내부 텍스트 스타일링 */
.stChatMessage [data-testid="stMarkdownContainer"] {
    padding: 0 !important;
    margin: 0 !important;
}

.stChatMessage [data-testid="stMarkdownContainer"] p {
    margin: 0 !important;
    line-height: 1.5 !important;
    font-size: 0.95rem !important;
}

/* 아바타 스타일링 - 크기 조정 */
.stChatMessage img,
[data-testid="stChatMessageAvatarUser"],
[data-testid="stChatMessageAvatarAssistant"] {
    min-width: 3.5rem !important;
    width: 3.5rem !important;
    height: 3.5rem !important;
    border-radius: 50% !important;
    background: white !important;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.15) !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    object-fit: cover !important;
    flex-shrink: 0 !important;
}

/* 사용자 아바타 색상 */
[data-testid="stChatMessageAvatarUser"] {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    color: white !important;
}

/* 어시스턴트 아바타 색상 */
[data-testid="stChatMessageAvatarAssistant"] {
    background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%) !important;
    color: white !important;
}

/* 호버 효과 */
.stChatMessage:has([data-testid="stChatMessageAvatarUser"]) [data-testid="stChatMessageContent"]:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4) !important;
    transition: all 0.2s ease !important;
}

.stChatMessage:has([data-testid="stChatMessageAvatarAssistant"]) [data-testid="stChatMessageContent"]:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15) !important;
    transition: all 0.2s ease !important;
}

/* 메시지 루트 자체의 배경 제거 (아이콘/말풍선은 건드리지 않음) */
.stChatMessage {
  background: transparent !important;
  box-shadow: none !important;
  border: none !important;
}

/* 콘텐츠 랩퍼 배경만 제거: 아바타/말풍선은 제외 */
.stChatMessage > div[class^="st-emotion-cache"]
  :not([data-testid^="stChatMessageAvatar"])
  :not([data-testid="stChatMessageContent"]) {
  background: transparent !important;
  box-shadow: none !important;
  border: none !important;
}

[data-testid="stChatMessageAvatarUser"] {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
  color: white !important;
}
[data-testid="stChatMessageAvatarAssistant"] {
  background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%) !important;
  color: white !important;
}

</style>
""", unsafe_allow_html=True)

# =============================
# 💾 세션 상태 초기화
# =============================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "session_id" not in st.session_state:
    import uuid
    st.session_state.session_id = f"session_{uuid.uuid4().hex[:8]}"

# 챗봇 메시지 형식 출력
with st.chat_message("assistant", avatar=ASSISTANT_AVATAR_PATH if os.path.exists(ASSISTANT_AVATAR_PATH) else None):
    st.markdown("안녕하세요! 저는 당신의 **식사비서 재규니**입니다. 무엇을 도와드릴까요?")

# 사이드바
with st.sidebar:
    st.header("식사비서 재규니")
    
    if st.button("New Chat"):
        st.session_state.messages = []
        import uuid
        st.session_state.session_id = f"session_{uuid.uuid4().hex[:8]}"
        st.rerun()
    
    st.write(f"세션 ID: `{st.session_state.session_id}`")

# =============================
# ✨ 유틸 함수 정의
# =============================


# =============================
# 💬 기존 대화 출력
# =============================
for msg in st.session_state.messages:
    avatar_path = None
    if msg["role"] == "user" and os.path.exists(USER_AVATAR_PATH):
        avatar_path = USER_AVATAR_PATH
    elif msg["role"] == "assistant" and os.path.exists(ASSISTANT_AVATAR_PATH):
        avatar_path = ASSISTANT_AVATAR_PATH
    
    with st.chat_message(msg["role"], avatar=avatar_path):
        st.markdown(msg["content"])

# =============================
# 🤖 챗봇 처리
# =============================

user_input = st.chat_input("오늘 뭐 먹을까?")

if user_input:
    # 유저 메시지 출력 및 저장
    with st.chat_message("user", avatar=USER_AVATAR_PATH if os.path.exists(USER_AVATAR_PATH) else None):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("assistant", avatar=ASSISTANT_AVATAR_PATH if os.path.exists(ASSISTANT_AVATAR_PATH) else None):
        with st.spinner("채팅작성중.."):
            try:
                # LangGraph에서 세션별 대화 기록 관리를 위한 config 설정
                config = {"configurable": {"thread_id": st.session_state.session_id}}
                
                # UI 세션 메시지를 LangGraph 형식으로 변환
                langgraph_messages = []
                for msg in st.session_state.messages:
                    if msg["role"] == "user":
                        langgraph_messages.append(("user", msg["content"]))
                    elif msg["role"] == "assistant":
                        langgraph_messages.append(("assistant", msg["content"]))
                
                result = graph_app.invoke({
                    "user_input": user_input,
                    "messages": langgraph_messages,
                    "session_id": st.session_state.session_id
                }, config=config)

                if isinstance(result, dict):
                    # 응답 메시지 추출
                    if "final_recommendations" in result:
                        response = result["final_recommendations"]
                    elif "exit_message" in result:
                        response = result["exit_message"]
                    else:
                        response = "❌ 추천 결과를 불러오는 데 실패했습니다."

                    # 응답 출력 및 저장
                    if isinstance(response, str):
                        st.markdown(response.replace("\n", "  \n"))
                        st.session_state.messages.append({"role": "assistant", "content": response})
                    else:
                        st.write(response)
                        st.session_state.messages.append({"role": "assistant", "content": str(response)})

                else:
                    st.error("❌ 시스템 오류: 올바른 결과를 반환하지 못했습니다.")

            except Exception as e:
                st.error("❌ LangGraph 실행 중 오류가 발생했습니다.")
                st.exception(e)
