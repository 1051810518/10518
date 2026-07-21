import streamlit as st
from openai import OpenAI

# 1. Streamlit 세션 상태(Session State) 완전 초기화 (최상단 배치)
if 'todo_list' not in st.session_state:
    st.session_state.todo_list = []
if 'user_motto' not in st.session_state:
    st.session_state.user_motto = "오늘도 화이팅!"
if 'motto_updated' not in st.session_state:
    st.session_state.motto_updated = False
if 'user_mbti' not in st.session_state:
    st.session_state.user_mbti = "선택 안 함"
if 'messages' not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": """
        너는 청소년과 대학생을 위한 따뜻하고 전문적인 AI 진로 설계 코치야. 
        사용자의 MBTI 성향, 오늘의 다짐, 그리고 평소 할 일 목록 데이터를 바탕으로 입체적인 진로 상담을 제공해야 해.
        사용자가 고민을 이야기하면 성향적 장점을 칭찬해주고, 추천 직업군이나 필요한 역량을 구체적으로 조언해줘.
        대화할 때는 항상 격려하는 긍정적인 말투를 유지해줘.
        """}
    ]

# 2. OpenAI 클라이언트 초기화 
# (비밀번호/키 에러 방지를 위해 try-except로 안전장치 추가)
try:
    ai_client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except Exception as e:
    st.error("OpenAI API 키 설정(.streamlit/secrets.toml)을 확인해주세요.")
    st.stop()

# 3. 기능 함수 정의
def add_todo():
    task = st.session_state.todo_input.strip()
    if task:
        st.session_state.todo_list.append([task, False])
        st.toast("할 일이 추가되었습니다! 🎉")
        st.session_state.todo_input = ""
    else:
        st.toast("⚠️ 할 일을 먼저 입력해주세요!")

@st.dialog("오늘의 다짐 수정")
def edit_motto():
    motto = st.text_input("나의 한 줄 좌우명을 적어주세요.", value=st.session_state.user_motto)
    if st.button("다짐 저장"):
        if motto.strip():
            st.session_state.user_motto = motto
            st.session_state.motto_updated = True
            st.rerun()

# 4. 각 페이지 정의
def page_motto():
    st.header("📣 1. 오늘의 다짐")
    st.info(f"현재 다짐: **{st.session_state.user_motto}**")
    if st.button("다짐 수정하기"):
        edit_motto()
    
    if st.session_state.motto_updated:
        st.success("새로운 좌우명이 등록되었습니다!")
        st.session_state.motto_updated = False
    st.markdown("---")

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
                    st.session_state.todo_list[i][1] = True
                    st.rerun()
            with col_status:
                if is_done:
                    st.write("✅ **달성!**")
                else:
                    st.write("⏳ 진행 중")
    st.markdown("---")

def page_report():
    st.header("📈 3. 나의 갓생 지수")
    if not st.session_state.todo_list:
        st.write("아직 등록된 할 일이 없습니다.")
    else:
        total = len(st.session_state.todo_list)
        count = sum(1 for item in st.session_state.todo_list if item[1])
        
        progress = (count / total) * 100
        st.metric("오늘의 달성률", f"{progress:.1f}%")
        st.progress(progress / 100)
        
        if progress == 100:
            st.balloons()
            st.success("모든 목표를 달성하셨습니다! 🏆")
        if st.button("기록 전체 초기화", type="primary"):
            st.session_state.todo_list = []
            st.rerun()

def page_ai_coach():
    st.header("🧐 AI 맞춤형 진로 상담소")
    st.write("나의 성향(MBTI)과 일상 활동을 바탕으로 AI 코치와 진로를 상담해보세요.")
    
    mbti_options = ["선택 안 함", "INFJ", "INFP", "INTJ", "INTP", "ISFJ", "ISFP", "ISTJ", "ISTP", 
                    "ENFJ", "ENFP", "ENTJ", "ENTP", "ESFJ", "ESFP", "ESTJ", "ESTP"]
    
    default_idx = mbti_options.index(st.session_state.user_mbti)
    selected_mbti = st.selectbox("🎯 나의 MBTI 성향을 선택해주세요:", mbti_options, index=default_idx)
    
    if selected_mbti != st.session_state.user_mbti:
        st.session_state.user_mbti = selected_mbti
        st.toast(f"성향이 {selected_mbti}(으)로 반영되었습니다!")
    
    st.markdown("---")
        
    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                
    question = st.chat_input("진로, 직업, 전공에 대해 궁금한 점을 질문해보세요!")
    if question:
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)
            
        with st.chat_message("assistant"):
            status_context = f"""
            [현재 사용자 프로필]
            - MBTI 성향: {st.session_state.user_mbti}
            - 목표 및 다짐: {st.session_state.user_motto}
            - 평소 행동/할 일 패턴: {st.session_state.todo_list}
            """
            prompt = st.session_state.messages + [{"role": "system", "content": status_context}]
            
            with st.spinner("AI 진로 코치가 답변을 구성하고 있습니다...💭"):
                response = ai_client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=prompt
                )
                ai_response = response.choices[0].message.content
                st.markdown(ai_response)
        st.session_state.messages.append({"role": "assistant", "content": ai_response})

# 5. 네비게이션 및 앱 실행
pg = st.navigation([
    st.Page(page_motto, title="오늘의 다짐", icon="📣"),
    st.Page(page_todo, title="오늘의 할 일", icon="✅"),
    st.Page(page_report, title="나의 갓생 지수", icon="📈"),
    st.Page(page_ai_coach, title="AI 진로 코칭", icon="🧐")
], position="top")

st.title("🌱 갓생 살기 & 꿈찾기 플래너")
pg.run()
