import streamlit as st
from openai import OpenAI

# OpenAI 클라이언트 초기화
ai_client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="MBTI 진로 매칭", layout="centered")

st.title("🧬 MBTI 기반 맞춤형 진로 파인더")
st.caption("간단한 성향 테스트를 통해 나에게 숨겨진 최고의 진로를 찾아보세요!")
st.markdown("---")

# 1. 성향 검사 섹션 (MBTI 핵심 축을 응용한 질문)
st.header("📋 1단계: 나의 성향 체크")
st.write("나와 더 가까운 행동 패턴을 선택해주세요.")

# 질문 1: 에너지 방향 (E vs I)
q1 = st.radio(
    "Q1. 주말이나 쉬는 시간에 나는 주로?",
    ["친구들을 만나거나 야외 활동을 하며 에너지를 얻는다. (외향형)", 
     "집에서 혼자 책을 보거나 게임, 휴식을 취하며 에너지를 얻는다. (내향형)"]
)

# 질문 2: 정보 수집 (S vs N)
q2 = st.radio(
    "Q2. 문제를 해결하거나 새로운 것을 배울 때 나는?",
    ["눈에 보이는 구체적인 사실과 과거의 경험, 데이터를 중시한다. (현실형)", 
     "아이디어나 미래의 가능성, 전체적인 흐름과 직관을 중시한다. (이상형)"]
)

# 질문 3: 판단과 결정 (T vs F)
q3 = st.radio(
    "Q3. 친구가 고민을 털어놓을 때 나는 보통 어떻게 반응할까?",
    ["상황을 객관적으로 분석하고 실질적인 해결책을 먼저 생각한다. (이성형)", 
     "친구의 감정에 깊이 공감해주고 위로의 말을 먼저 건넨다. (감정형)"]
)

# 질문 4: 생활 양식 (J vs P)
q4 = st.radio(
    "Q4. 여행을 가거나 프로젝트를 시작할 때 나의 방식은?",
    ["일정이나 계획을 미리 체계적으로 세워두어야 마음이 편하다. (계획형)", 
     "상황에 따라 유연하게 대처하며 즉흥적으로 즐기는 편이다. (자유형)"]
)

st.markdown("---")

# 2. 추가 주관식 의견 수집
st.header("✍️ 2단계: 나의 한 마디 추가하기")
extra_info = st.text_input(
    "관심 있는 분야나 꼭 피하고 싶은 환경(예: '오래 앉아있는 일은 싫어요')이 있다면 적어주세요.",
    placeholder="예: 과학 과목을 좋아해요 / 사람들을 많이 만나는 직업이 궁금해요"
)

st.markdown("---")

# 3. 결과 분석 및 매칭 버튼
if st.button("🚀 나의 진로 매칭 결과 보기", type="primary"):
    # 사용자의 선택 결과 요약 정보 생성
    user_profile = f"""
    - 에너지 방향: {q1}
    - 정보 수집 방식: {q2}
    - 판단 방식: {q3}
    - 생활 양식: {q4}
    - 추가 요구사항: {extra_info if extra_info else '없음'}
    """
    
    with st.spinner("성향 지도를 분석하여 찰떡 진로를 매칭하는 중..."):
        system_prompt = """
        너는 MBTI 및 성격 심리학에 기반한 진로 컨설턴트야.
        제공된 사용자의 4가지 성향 선택지와 추가 정보를 바탕으로, 이 사람에게 가장 잘 맞는 진로를 분석해줘.
        형식은 반드시 마크다운(Markdown)을 사용하여 아래 구조로 출력해줘:
        
        ### 🔮 나의 성향 요약
        (선택한 성향들을 한 줄로 정의해주는 재미있는 칭호나 키워드 예: '체계적인 전략가', '따뜻한 아이디어 뱅크')
        
        ### 🎯 추천 진로 및 직업분야 Top 3
        1. **직업명** - 이 직업이 성향과 잘 맞는 이유 설명
        2. **직업명** - 이 직업이 성향과 잘 맞는 이유 설명
        3. **직업명** - 이 직업이 성향과 잘 맞는 이유 설명
        
        ### 🛠️ 나를 위한 역량 업그레이드 팁
        (이 성향의 사람이 진로를 발전시키기 위해 보완하거나 키우면 좋은 습관이나 역량 제안)
        """
        
        response = ai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"이 유저의 성향 프로필이야:\n{user_profile}"}
            ]
        )
        
        # 결과를 화면에 멋지게 표시
        st.success("🎉 성향 분석이 완료되었습니다!")
        st.markdown(response.choices[0].message.content)
