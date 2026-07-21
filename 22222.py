
import streamlit as st
from openai import OpenAI
import json

# OpenAI 클라이언트 초기화
ai_client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# 앱 스타일 지정
st.set_page_config(page_title="AI 진로 내비게이터", layout="centered")

# 세션 상태 초기화
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {
            "role": "assistant", 
            "content": "안녕하세요! 당신의 꿈을 함께 찾아갈 AI 진로 상담사입니다. 🎯\n먼저 당신에 대해 알고 싶어요. 요즘 가장 흥미를 느끼는 분야나 과목, 혹은 평소에 시간 가는 줄 모르고 하는 일이 무엇인가요?"
        }
    ]
if "interview_count" not in st.session_state:
    st.session_state.interview_count = 0
if "report_data" not in st.session_state:
    st.session_state.report_data = None

st.title("🧩 AI 1:1 심층 진로 상담소")
st.caption("AI와 편하게 대화하며 나에게 딱 맞는 미래의 직업과 로드맵을 찾아보세요.")
st.markdown("---")

# 좌측 사이드바: 진행 상황 표시
with st.sidebar:
    st.header("📋 상담 진행도")
    progress_percentage = min(st.session_state.interview_count / 4, 1.0)
    st.progress(progress_percentage)
    
    if st.session_state.interview_count < 4:
        st.write(f"💬 답변 단계: {st.session_state.interview_count} / 4")
        st.info("AI의 질문에 4번 이상 답변하면 맞춤형 진로 분석 보고서가 생성됩니다!")
    else:
        st.success("🎉 진로 분석 준비 완료!")
        if st.button("📊 맞춤형 진로 보고서 생성하기", type="primary"):
            with st.spinner("AI가 당신의 답변을 바탕으로 진로를 분석 중입니다..."):
                # 대화 기록 요약 및 보고서 요청
                conversation = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.chat_history])
                
                system_prompt = """
                너는 전문적인 진로 진단 상담사야. 제공된 대화 기록을 분석해서 학생을 위한 '진로 분석 보고서'를 한국어로 작성해줘.
                형식은 명확하게 마크다운(Markdown)을 사용하여 아래 항목을 반드시 포함해줘:
                1. 🎉 추천 직업 Top 3 (각 직업별 선정 이유 포함)
                2. 📚 추천 전공 학과 및 고등학교 때 하면 좋은 활동/도서
                3. 🚀 미래 커리어 로드맵 (단기/장기 계획)
                4. 💌 따뜻한 응원의 메시지
                """
                
                response = ai_client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"이 대화를 분석해줘:\n{conversation}"}
                    ]
                )
                st.session_state.report_data = response.choices[0].message.content
