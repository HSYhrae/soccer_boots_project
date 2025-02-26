import streamlit as st
import pages as pg

def show_home():
    st.query_params["pages"] = "홈"
# 제목 중앙 정렬
    st.markdown("<h1 style='text-align: center; font-size: 50px;'>Soccerly-축구하게?</h1>", unsafe_allow_html=True)
    st.image("image/soccer_image.jpg", width=300)
    # 사용설명버튼 스타일 개선
    st.markdown("""
        <div style='background-color: #f0f2f6; padding: 10px; border-radius: 5px; text-align: center; margin: 10px 0;'>
            <h3 style='color: #262730; margin: 0;'>📋 사용 설명</h3>
            <p style='margin: 5px 0 0 0;'>아래 버튼을 클릭하여 사용설명을 읽어보세요 (상단 탭 클릭 시 페이지 이동)</p>
        </div>
    """, unsafe_allow_html=True)
    # 상태 초기화
    # 목적 버튼 누르고 끄기
    if 'show_text1' not in st.session_state:
        st.session_state.show_text1 = False
    if 'show_text2' not in st.session_state:
        st.session_state.show_text2 = False
    if 'show_text3' not in st.session_state:
        st.session_state.show_text3 = False

    col1, col2, col3 = st.columns(3)

    # 첫 번째 컬럼에 축구화 추천 버튼
    with col1:
        if st.button("⚽ 축구화 추천 ", use_container_width=True):
            #st.query_params["pages"] = "축구화"
            st.session_state.show_text1 = not st.session_state.show_text1
        if st.session_state.show_text1:
            st.write("발볼과 길이 등 원하는 조건을 선택하여 상품 후보를 확인할 수 있습니다")

    # 두 번째 컬럼에 선수 추천 버튼
    with col2:
        if st.button("👤 선수 찾기", use_container_width=True):
            #st.query_params["pages"] = "축구선수"
            st.session_state.show_text2 = not st.session_state.show_text2
        if st.session_state.show_text2:
            st.write("자신의 키와 포지션을 선택하여 유사한 선수를 확인할 수 있습니다")

    with col3:
        if st.button("🏆 대시보드", use_container_width=True):
            #st.query_params["pages"] = "대시보드"
            st.session_state.show_text3 = not st.session_state.show_text3
        if st.session_state.show_text3:
            st.write("각 나라의 브랜드 선호도와 시리즈별 선호도를 확인할 수 있습니다")
