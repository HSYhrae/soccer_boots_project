import streamlit as st

st.set_page_config(page_title="Soccerly", initial_sidebar_state='auto', layout="wide")

st.markdown("""
<style>
.st-emotion-cache-bm2z3a {
    height: 100vh !important;               /* 전체 화면 높이를 할당 /
    overflow: auto !important;              / 콘텐츠가 넘칠 때 스크롤이 나타나도록 설정 /
    -webkit-overflow-scrolling: touch !important; / iOS 모멘텀 스크롤 활성화 /
    display: flex !important;               / flex 컨테이너로 설정하여 내부 요소 정렬 제어 /
    flex-direction: column !important;
    pointer-events: auto !important;        / 터치 이벤트가 정상적으로 전달되도록 설정 */
}
</style>
""", unsafe_allow_html=True)

import os
from streamlit_navigation_bar import st_navbar
import pages as pg  

# 네비게이션 바에 표시할 페이지 이름
pages = ["Home", "Boots", "Player","Dashboard"]
st.logo('image/logo.png', size = 'Large', icon_image = 'image/logo.png')

# 네비게이션 바 스타일 설정 (원하는 대로 수정 가능)
styles = {
    "nav": {
        "background-color": "transparent",
    },
    "div": {
        "max-width": "32rem",
    },
    "span": {
        "color": "white",
        "padding": "14px",
    },
    "active": {
        "background-color": "white",
        "color": "var(--text-color)",
        "font-weight": "normal",
        "padding": "14px",
    },
    "hover": {
        "background-color": "rgba(255, 255, 255, 0.35)",
    },
}

# 네비게이션 바 옵션 설정 (메뉴와 사이드바를 활성화)
options = {
    "show_menu": True,
    "show_sidebar": True,
    "use_padding": True,
}

st.markdown("""
    <style>
    ul[data-v-1d8bbd58] {
        display: flex;
        width: 100%;
        justify-content: center;
    }
    </style>
    """, unsafe_allow_html=True)


st.markdown("""
<style>
button[data-testid="stBaseButton-headerNoPadding"] {
    background-color: red !important;
}
</style>
""", unsafe_allow_html=True)

# 네비게이션 바 생성: 선택한 페이지 이름이 반환됩니다.
page = st_navbar(
    pages,
    styles=styles,
    options=options,
) # 선택한 페이지 이름을 출력 (디버깅 용도)

# 각 페이지에 해당하는 함수 매핑
functions = {
    "Home": pg.show_home,
    "Boots": pg.show_Find,
    "Player": pg.show_player,
    "Dashboard":pg.show_dashboard
}



# 선택한 페이지의 함수를 호출하여 해당 페이지 내용 표시
go_to = functions.get(page)
if go_to:
    go_to()


