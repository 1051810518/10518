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

# 2. 직업추천 페이지 (NEW)
def page_recommendation():
    st.header("🔍 2. 맞춤형 직업 추천받기")
    st.write("간단한 관심사나 좋아하는 과목, 성격 등을 입력하면 AI가 어울리는 직업을 추천해 드립니다.")
    
    interest_input = st.text_area(
        "나에 대해 알려주세요!", 
        placeholder="예: 저는 수학을 좋아하고 조용한 편이에요. 컴퓨터로 무언가 만드는 것에 관심이 많아요."
    )
    
    if st.button("어울리는 직업 추천받기", type="primary"):
        if not interest_input.strip():
            st.warning("내용을 입력한 후 버튼을 눌러주세요!")
        else:
            with st.spinner("AI가 회원님에게 딱 맞는 직업을 분석 중입니다... 🕵️‍♂️"):
                prompt = [
                    {"role": "system", "content": "너는 청소년 진로 상담 전문가야. 학생이 입력한 관심사, 성격, 좋아하는 과목을 바탕으로 흥미를 가질 만한 구체적인 직업 3가지를 추천하고, 추천 이유를 친절하게 설명해줘."},
                    {"role": "user", "content": interest_input}
                ]
                response = ai_client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=prompt
                )
                st.markdown("### 🌟 AI 추천 직업 결과")
                st.markdown(response.choices[0].message.content)

# 3. 직업과 할 일 페이지 (NEW)
def page_roadmap():
    st.header("📋 3. 희망 직업과 실천할 일")
    st.write("알아보고 싶거나 되고 싶은 직업을 입력하면, 준비하기 위해 무엇을 실천해야 하는지 단계별 로드맵을 제공합니다.")
    
    target_job = st.text_input("궁금한 희망 직업을 입력하세요", placeholder="예: 데이터 과학자, 웹툰 작가 등")
    
    if st.button("실천 로드맵 확인하기"):
        if not target_job.strip():
            st.warning("직업 이름을 입력해주세요!")
        else:
            with st.spinner(f"AI가 {target_job}이(가) 되기 위한 실천 과제를 뽑아내고 있습니다... 🚀"):
                prompt = [
                    {"role": "system", "content": "너는 청소년 커리어 코치야. 사용자가 입력한 직업이 되기 위해 중·고등학교 시절 및 일상에서 실천하면 좋은 구체적인 활동 목록(추천 도서, 공부해야 할 과목, 참여하면 좋은 동아리나 활동 등)을 단계별로 나누어 보기 쉽게 작성해줘."},
                    {"role": "user", "content": f"희망 직업: {target_job}"}
                ]
                response = ai_client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=prompt
                )
                st.markdown(f"### 🛠️ '{target_job}'이 되기 위한 실천 리스트")
                st.markdown(response.choices[0].message.content)

# 4. 진로 실천 활동 페이지 (기존 2페이지)
def page_activities():
    st.header("🏃‍♂️ 4. 꿈을 위한 실천 리스트")
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

# 5. 진로 준비도 페이지 (기존 3페이지)
def page_report():
    st.header("📊 5. 나의 진로 준비도")
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

# 6. AI 진로 상담소 페이지 (기존 4페이지)
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

# 네비게이션 설정 (신규 페이지 배치)
pg = st.navigation([
    st.Page(page_dream, title="1. 목표 진로 설정", icon="🎯"),
    st.Page(page_recommendation, title="2. 직업 추천", icon="🔍"),
    st.Page(page_roadmap, title="3. 직업과 할 일", icon="📋"),
    st.Page(page_activities, title="4. 진로 실천 리스트", icon="🏃‍♂️"),
    st.Page(page_report, title="5. 진로 준비도", icon="📊"),
    st.Page(page_career_coach, title="AI 진로 상담소", icon="🧠")
], position="top")

st.title("🌱 꿈찾기 진로 플래너")
pg.run()
