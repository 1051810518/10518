import streamlit as st

st.title("카운터 앱")
if 'count' not in st.session_state:
    st.session_state.count = 0
if st.button("증가"):
    st.session_state.count += 1
st.markdown(f"## 현재 숫자: `{st.session_state.count}`")
def reset_all():
    st.session_state.user_name = ""
    st.session_state.weather = "맑음"
    st.session_state.top_type = "후드티"
    st.session_state.top_color = "밝음"
    st.session_state.bottom_type = "청바지"
    st.session_state.bottom_color = "슬림"
    st.session_state.shoes = "스니커즈"
    st.session_state.acc = []

st.button("전체 초기화", on_click=reset_all)
