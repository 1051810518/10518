import streamlit as st
from openai import OpenAI

# OpenAI 클라이언트 초기화
ai_client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# 세션 상태(Session State) 초기화
if 'activity_list' not in st.session_state:
    st.session_state.activity_list = []
if 'user_dream' not in st.session_state:
    st.session_state.user_dream = "아직 탐색 중인 미래의 전문가"
if 'dream_updated' not in st.session_state:
    st.session_state.dream_updated = False

# 진로 실천 활동 추가 함수
def add_activity():
    activity = st.session_state.activity_input.strip()
    if activity:
        st.session_state.activity_list.append([activity, False])
        st.toast("진로 활동이 등록되었습니다! 📝")
        st.session_state.activity_input = ""
    else:
        st.toast("⚠️ 활동 내용을 먼저 입력해주세요!")

# 진로 수정 다이얼로그
@st.dialog("나의 목표 진로 설정/수정")
def edit_dream():
    dream = st.text_input("관심 있는 직업이나 학과, 혹은 꿈을 적어주세요.", value=st.session_state.user_dream)
    if st.button("꿈 저장하기"):
        if dream.strip():
            st.session_state.user_dream = dream
            st.session_state.dream_updated = True
            st.rerun()

# 1. 나의 꿈 정의 페이지
def page_dream():
    st.header("🎯 1. 나의 목표 진로")
    st.info(f"현재 관심 진로: **{st.session_state.user_dream}**")
    if st.button("진로 설정/변경하기"):
        edit_dream()
    
    if st.session_state.dream_updated:
        st.success("목표 진로가 업데이트되었습니다! 꿈을 향해 한 걸음 더 나아가봐요!")
        st.session_state.dream_updated = False
    st.markdown("---")
    st.write("""
    **💡 진로 탐색 팁:**
    아직 확실한 직업이 없어도 괜찮아요! '사람들을 돕는 일', '컴퓨터 프로그래밍', '예술 분야' 처럼 넓은 관심사로 시작해보세요.
    """)

# 2. 진로 실천 활동 페이지
def page_activities():
    st.header("🏃‍♂️ 2. 꿈을 위한 실천 리스트")
    st.subheader(f"✨ 목표: {st.session_state.user_dream}")
    
    st.text_input("진로와 관련된 활동(책 읽기, 코딩 연습, 글쓰기 등)을 입력하세요", 
                  key="activity_input", on_change=add_activity)
    st.button("활동 추가하기", on_click=add_activity)
    
    st.markdown("---")
    
    if not st.session_state.activity_list:
        st.info("아직 등록된 진로 활동이 없습니다. 작은 실천부터 추가해보세요!")
    else:
        for i in range(len(st.session_state.activity_list)):
            col_task, col_btn, col_status = st.columns([4, 1, 1])
            with col_task:
                st.write(f"{i+1}. {st.session_state.activity_list[i][0]}")
            with col_btn:
                is_done = st.session_state.activity_list[i][1]
                if st.button("완료", key=f"btn_{i}", disabled=is_done):
                    st.session_state.activity_list[i][1] = True
                    st.rerun()
            with col_status:
                if is_done:
                    st.write("✅ **완료!**")
                else:
                    st.write("⏳ 노력 중")
    st.markdown("---")

# 3. 진로 준비도 페이지
def page_report():
    st.header("📊 3. 나의 진로 준비도")
    if not st.session_state.activity_list:
        st.write("아직 등록된 진로 활동이 없습니다.")
    else:
        total = len(st.session_state.activity_list)
        count = sum(1 for item in st.session_state.activity_list if item[1])
        
        progress = (count / total) * 100
        st.metric("진로 활동 실천율", f"{progress:.1f}%", delta=f"{count}/{total} 개 완료")
        st.progress(progress / 100)
        
        if progress == 100:
            st.balloons()
            st.success("계획한 모든 진로 활동을 달성했습니다! 대단해요! 🏆")
            
        st.markdown("---")
        if st.button("리스트 전체 초기화", type="primary"):
            st.session_state.activity_list = []
            st.rerun()

# 4. AI 진로 상담소 페이지
def page_career_coach():
    st.header("🧠 AI 진로 상담소")
    st.write("관심 있는 분야에 대해 무엇이든 물어보세요. 직업 전망, 필요한 역량, 관련 학과 등을 알려드립니다!")
    
    if "career_messages" not in st.session_state:
        st.session_state.career_messages = [
            {"role": "system", "content": """
            너는 청소년들을 위한 따뜻하고 전문적인 AI 진로 상담 선생님이야. 
            사용자가 입력한 '관심 진로'와 '실천 활동 목록'을 바탕으로 학생의 흥미와 성실성을 분석해줘.
            진로에 대해 고민할 때 구체적인 직업 탐색 방법, 추천 도서, 관련 학과, 미래 전망 등을 친절하고 이해하기 쉽게 설명해주고, 
            도전하는 학생을 격려하고 응원하는 긍정적인 톤을 유지해줘.
            """}
        ]
        
    for message in st.session_state.career_messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                
    question = st.chat_input("예: 개발자가 되려면 고등학교 때 어떤 공부를 해야 하나요?")
    if question:
        st.session_state.career_messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)
            
        with st.chat_message("assistant"):
            # 현재 진로 상태와 활동 목록을 AI에게 컨텍스트로 전달
            status_context = f"학생의 관심 진로: {st.session_state.user_dream} / 현재까지의 진로 실천 활동: {st.session_state.activity_list}"
            prompt = st.session_state.career_messages + [{"role": "system", "content": status_context}]
            
            with st.spinner("진로 선생님이 답변을 생각하고 계십니다...💬"):
                response = ai_client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=prompt
                )
                ai_response = response.choices[0].message.content
                st.markdown(ai_response)
        st.session_state.career_messages.append({"role": "assistant", "content": ai_response})

# 네비게이션 설정
pg = st.navigation([
    st.Page(page_dream, title="목표 진로 설정", icon="🎯"),
    st.Page(page_activities, title="진로 실천 리스트", icon="🏃‍♂️"),
    st.Page(page_report, title="진로 준비도", icon="📊"),
    st.Page(page_career_coach, title="AI 진로 상담소", icon="🧠")
], position="top")

st.title("🌱 꿈찾기 진로 플래너")
pg.run()
