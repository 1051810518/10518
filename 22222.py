# 2. 진로 실천 활동 페이지
def page_activities():
    st.header("🏃‍♂️ 2. 꿈을 위한 실천 리스트")
    st.subheader(f"✨ 목표: {st.session_state.user_dream}")
    
    # 중복 입력을 막기 위해 on_change는 제거하고, 
    # 엔터를 누르거나 버튼을 누르는 두 경우 모두 on_click 하나로 처리되도록 input 컴포넌트를 구성합니다.
    st.text_input("진로와 관련된 활동(책 읽기, 코딩 연습, 글쓰기 등)을 입력하세요", key="activity_input")
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
