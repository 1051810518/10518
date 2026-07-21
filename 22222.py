import streamlit as st
from openai import OpenAI

# OpenAI 클라이언트 초기화
ai_client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# 세션 상태(Session State) 초기화
if 'todo_list' not in st.session_state:
    st.session_state.todo_list = []
if 'user_motto' not in st.session_state:
    st.session_state.user_motto = "오늘도 화이팅!"
if 'motto_updated' not in st.session_state:
    st.session_state.motto_updated = False
# 진로 상담용 MBTI 세션 상태 추가
if 'user_mbti' not in st.session_state:
    st.session_state.user_mbti = "선택 안 함"

# 할 일 추가 함수
def add_todo():
    task = st.session_state.todo_input.strip()
    if task:
        st.session_state.todo_list.append([task, False])
        st.toast("할 일이 추가되었습니다! 🎉")
        st.session_state.todo_input = ""
    else:
        st.toast("⚠️ 할 일을 먼저 입력해주세요!")

# 다짐 수정 다이얼로그
@st.dialog("오늘의 다짐 수정")
def edit_motto():
    motto = st.text_input("나의 한 줄 좌우명을 적어주세요.", value=st.session_state.user_motto)
    if st.button("다짐 저장"):
        if motto.strip():
            st.session_state.user_motto = motto
            st.session_state.motto_updated = True
            st.rerun()

# 1. 오늘의 다짐 페이지
def page_motto():
    st.header("📣 1. 오늘의 다짐")
    st.info(f"현재 다짐: **{st.session_state.user_motto}**")
    if st.button("다짐 수정하기"):
        edit_motto()
    
    if st.session_state.motto_updated:
        st.success("새로운 좌우명이 등록되었습니다!")
        st.session_state.motto_updated = False
    st.markdown("---")

# 2. 오늘의 할 일 페이지
def page_todo():
    st.header("✅ 2. 오늘의 할 일")
    st.write(f"현재 다짐: **{st.session_state.user_motto}**")
    st.text_input("추가할 할 일을 입력하세요", key="todo_input", on_change=add_todo)
    st.button("추가하기", on_click=add_todo)
    
    st.markdown("---")
    if not st.session_state.todo_list:
        st.info("아직 등록된 할 일이 없습니다.")
    else:
        for i in range(len(st.session_state.todo_list)):
            col_task, col_btn, col_status = st.columns([4, 1, 1])
            with col_task:
                st.write(f"{i+1}. {st.session_state.todo_list[i][0]}")
            with col_btn:
                is_done = st.session_state.todo_list[i][1]
                if st.button("완료", key=f"btn_{i}", disabled=is_done):
