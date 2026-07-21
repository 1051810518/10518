import streamlit as st
from openai import OpenAI

# 1. 세션 상태(Session State) 초기화 (새로고침 시 데이터 유지용)
if 'report_generated' not in st.session_state:
    st.session_state.report_generated = False
if 'report_content' not in st.session_state:
    st.session_state.report_content = ""

# 2. OpenAI 클라이언트 초기화
try:
    ai_client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except Exception as e:
    st.error("OpenAI API 키 설정(.streamlit/secrets.toml)을 확인해주세요.")
    st.stop()

# 앱 기본 설정
st.set_page_config(page_title="나의 진로 파인더", layout="centered")
st.title("🧩 나의 성향 맞춤형 진로 디자인")
st.caption("질문에 답하고 나에게 맞는 직업, 필요한 능력치, 실천 방법을 알아보세요!")
st.markdown("---")

# 3. 성향 파악을 위한 질문 섹션
st.header("📋 나의 성향 알아보기")

q1 = st.selectbox(
    "Q1. 평소에 문제를 해결할 때 나는 어떤 방식을 선호하나요?",
    ["데이터와 사실을 바탕으로 논리적으로 분석한다.", 
     "새로운 아이디어를 내고 창의적인 방법을 찾아낸다.", 
     "다른 사람들의 의견을 듣고 협력하여 조율한다."]
)

q2 = st.selectbox(
    "Q2. 어떤 환경에서 일할 때 가장 능률이 오를 것 같나요?",
    ["규칙과 체계가 잘 잡혀있는 안정적인 환경", 
     "매번 새로운 도전이 있고 자유로운 환경", 
     "사람들과 소통하고 도움을 줄 수 있는 따뜻한 환경"]
)

q3 = st.selectbox(
    "Q3. 나의 가장 큰 장점이나 성향은 무엇인가요?",
    ["한 가지에 깊게 몰입하고 집중하는 능력", 
     "트렌드를 빠르게 읽고 변화에 적응하는 능력", 
     "공감을 잘하고 주변 사람을 챙기는 능력"]
)

# 4. 관심사 추가 입력 (주관식)
st.markdown("---")
st.header("✍️ 나의 관심사 추가하기")
user_interest = st.text_input(
    "평소 관심 있는 분야(예: 컴퓨터, 미술, 과학, 스포츠 등)를 자유롭게 적어주세요.",
    placeholder="예: 과학 실험을 좋아해요 / 영상 편집에 관심이 많아요"
)

st.markdown("---")

# 5. 결과 분석 및 보고서 생성 버튼
if st.button("🚀 나의 맞춤형 진로 분석하기", type="primary"):
    # AI에게 전달할 유저 프로필 데이터 구성
    user_profile = f"""
    - 문제 해결 방식: {q1}
    - 선호하는 업무 환경: {q2}
    - 개인적인 장점: {q3}
    - 추가 관심사: {user_interest if user_interest else '없음'}
    """
    
    with st.spinner("당신의 답변을 분석하여 최적의 커리어를 디자인하고 있습니다...💭"):
        system_prompt = """
        너는 전문적인 진로 설계 및 커리어 컨설턴트야. 
        사용자가 답변한 성향 질문과 관심사를 바탕으로 맞춤형 진로 가이드를 작성해줘.
        출력은 반드시 마크다운(Markdown) 형식을 사용하고, 다음 4가지 내용을 명확하게 포함해야 해:
        
        1. 🔮 [성향 분석 결과]: 사용자가 어떤 성향의 사람인지 정의해주는 요약문.
        2. 🎯 [어울리는 추천 직업 Top 3]: 성향과 관심사에 가장 잘 어울리는 직업 3개를 추천하고 구체적인 이유 설명.
        3. ⚡ [필요한 능력치 설명]: 이 직업들을 갖기 위해 필요한 핵심 능력치 종류와 수준을 설명.
        4. 🏃‍♂️ [우리가 실천할 수 있는 것]: 이 진로를 준비하기 위해 일상이나 학교에서 지금 바로 실천할 수 있는 활동 제안.
        """
        
        try:
            response = ai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"이 유저의 성향 데이터야:\n{user_profile}"}
                ]
            )
            st.session_state.report_content = response.choices[0].message.content
            st.session_state.report_generated = True
            st.rerun()  # 화면 갱신
        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")

# 6. 결과 출력 섹션
if st.session_state.report_generated:
    st.success("🎉 진로 분석 결과가 완성되었습니다!")
    st.markdown(st.session_state.report_content)
    
    st.markdown("---")
    if st.button("🔄 다시 테스트하기"):
        st.session_state.report_generated = False
        st.session_state.report_content = ""
        st.rerun()
