import streamlit as st
import pages as pg


def show_home():
    # 로고 이미지를 HTML/CSS로 중앙에 배치
    st.markdown("""
        <div style='display: flex; justify-content: center; align-items: center; margin: 20px 0;'>
            <img src='data:image/png;base64,{}' width='200'>
        </div>
    """.format(get_base64_encoded_image("image/logo.png")), unsafe_allow_html=True)

    # 설명 텍스트
    st.markdown("""
        <div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px; text-align: center; margin: 20px 0;'>
            <h2 style='color: #262730; margin: 0; font-size: 24px;'>💡Soccerly란?</h2>
            <p style='margin: 10px 0 0 0; font-size: 18px; font-weight: bold;'>인터넷에서 축구화를 주문하는 것을 어려워하는 당신!</p>
            <p style='margin: 10px 0 0 0; font-size: 16px;'>Soccerly는 발 길이와 발볼 너비등을 선택하여 최적의 축구화를 추천해 줍니다.</p>
            <p style='margin: 10px 0 0 0; font-size: 16px;'>키와 포지션을 입력하면, 나와 비슷한 플레이 스타일의 실제 선수도 찾아볼 수 있습니다.</p>
            <p style='margin: 15px 0 0 0; font-size: 18px; font-weight: bold;'>⚽ 나에게 딱 맞는 축구화를 쉽게 선택하고, 나와 비슷한 선수를 확인해 보세요!</p>
        </div>
    """, unsafe_allow_html=True)

    # 상태 초기화
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
            st.session_state.show_text1 = not st.session_state.show_text1
        if st.session_state.show_text1:
            st.write("발볼과 길이 등 원하는 조건을 선택하여 상품 후보를 확인할 수 있습니다")
            st.write("상단 탭에서 축구화를 눌러주세요")

    # 두 번째 컬럼에 선수 추천 버튼
    with col2:
        if st.button("👤 선수 찾기", use_container_width=True):
            st.session_state.show_text2 = not st.session_state.show_text2
        if st.session_state.show_text2:
            st.write("자신의 키와 포지션을 선택하여 유사한 선수를 확인할 수 있습니다")
            st.write("상단 탭에서 축구선수를 눌러주세요")

    # 세 번째 컬럼에 대시보드 버튼
    with col3:
        if st.button("🏆 대시보드", use_container_width=True):
            st.session_state.show_text3 = not st.session_state.show_text3
        if st.session_state.show_text3:
            st.write("각 나라의 브랜드 선호도와 시리즈별 선호도를 확인할 수 있습니다")
            st.write("상단 탭에서 대시보드를 눌러주세요")

# 이미지를 Base64로 인코딩하는 함수
def get_base64_encoded_image(image_path):
    import base64
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')