import streamlit as st
from openai import OpenAI

# 1. 세션 상태(Session State) 초기화
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
st.set_page_config(page_title="커리어 나침반", layout="centered")
st.title("🧩 나의 성향 맞춤형 진로 디자인")
st.caption("간단한 성향 질문에 답하고, 나에게 맞는 직업과 필요한 능력치를 알아보세요!")
st.markdown("---")

# 3. 성향 파악을 위한 4가지 질문 (객관식)
st.header("📋 1단계: 나의 성향 알아보기")

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

# 4. 주관식 추가 답변 (정밀한 추천을 위함)
st.markdown("---")
st.header("✍️ 2단계: 관심사 추가하기")
user_interest = st.text_input(
    "평소 관심 있는 분야(예: 컴퓨터, 미술, 과학, 스포츠 등)나 하고 싶은 이야기를 자유롭게 적어주세요.",
    placeholder="예: 게임 개발에 관심이 있어요 / 요리하는 것을 좋아해요"
)

st.markdown("---")

# 5. 결과 분석 및 보고서 생성
if st.button("🚀 나의 맞춤형 진로 분석하기", type="primary"):
    # AI에게 보낼 유저 데이터 정리
    user_profile = f"""
    - 문제 해결 방식: {q1}
    - 선호하는 업무 환경: {q2}
    - 개인적인 장점: {q3}
    - 추가 관심사: {user_interest if user_interest else '없음'}
    """
    
    with st.spinner("당신의 성향을 분석하여 최적의 커리어를 디자인하고 있습니다...💭"):
        system_prompt = """
        너는 전문적인 진로 설계 및 커리어 컨설턴트야. 
        사용자가 답변한 성향 질문과 관심사를 바탕으로 맞춤형 진로 가이드를 작성해줘.
        출력은 반드시 마크다운(Markdown) 형식을 사용하고, 다음 4가지 내용을 명확하게 포함해야 해:
        
        1. 🔮 [성향 분석 결과]: 사용자가 어떤 성향의 사람인지 재미있고 긍정적인 타이틀과 함께 요약해줘.
        2. 🎯 [추천 직업 Top 3]: 성향에 가장 잘 어울리는 직업 3개를 추천하고, 왜 어울리는지 이유를 설명해줘.
        3. ⚡ [필요한 핵심 능력치]: 이 직업들을 갖기 위해 특별히 키워야 하는 핵심 능력(예: 논리적 사고력 80%, 소통 능력 90% 등)을 설명해줘.
        4. 🏃‍♂️ [지금 실천할 수 있는 것]: 이 진로를 준비하기 위해 일상이나 학교에서 지금 바로 실천할 수 있는 구체적인 활동(독서, 동아리, 습관 등)을 제안해줘.
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
        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")

# 6. 결과 출력 섹션
if st.session_state.report_generated:
    st.success("🎉 진로 분석 보고서가 완성되었습니다!")
    st.markdown(st.session_state.report_content)
    
    st.markdown("---")
    if st.button("🔄 다시 테스트하기"):
        st.session_state.report_generated = False
        st.session_state.report_content = ""
        st.rerun()
