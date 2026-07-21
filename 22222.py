import streamlit as st
from openai import OpenAI

# OpenAI 클라이언트 초기화
ai_client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# 1. 세션 상태(Session State) 초기화 (원본 코드의 변수 구조 활용)
if 'todo_list' not in st.session_state:
    st.session_state.todo_list = []  # 여기서는 사용자의 진로 관심사 키워드 목록으로 활용합니다.
if 'user_motto' not in st.session_state:
    st.session_state.user_motto = "아직 탐색 중인 미래의 전문가"  # '현재 다짐' 대신 '현재 목표 진로'로 활용
if 'motto_updated' not in st.session_state:
    st.session_state.motto_updated = False

# 관심 진로 키워드 추가 함수 (원본 add_todo 함수 틀 유지)
def add_todo():
    task = st.session_state.todo_input.strip()
    if task:
        st.session_state.todo_list.append([task, False])
        st.toast("진로 관심 키워드가 추가되었습니다! 🎯")
        st.session_state.todo_input = ""

# 목표 진로 설정 다이얼로그 (원본 edit_motto 다이얼로그 틀 유지)
@st.dialog("목표 진로 설정/수정")
def edit_motto():
    motto = st.text_input("관심 있는 직업이나 학과, 꿈을 적어주세요.")
    if st.button("진로 저장"):
        if motto.strip():
            st.session_state.user_motto = motto
            st.session_state.motto_updated = True
            st.rerun()

# 1. 오늘의 다짐 탭 -> [나의 목표 진로] 페이지로 변경
def page_motto():
    st.header("📣 1. 나의 목표 진로")
    st.info(f"현재 관심 진로: **{st.session_state.user_motto}**")
    if st.button("목표 진로 설정하기"):
        edit_motto()
    if st.session_state.motto_updated:
        st.success("새로운 목표 진로가 등록되었습니다! 꿈을 향해 나아가봐요!")
        st.session_state.motto_updated = False
    st.markdown("---")

# 2. 오늘의 할 일 탭 -> [진로 관심 키워드] 페이지로 변경
def page_todo():
    st.header("✅ 2. 나의 관심 분야 & 키워드")
    st.write(f"현재 목표: **{st.session_state.user
