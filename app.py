import streamlit as st

st.set_page_config(page_title="Soccerly", initial_sidebar_state='auto', layout="wide")

st.query_params["pages"] = "홈"

# 폰트 적용 (네비게이션 바 제외)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css?family=Poor+Story:400');

/* 모든 요소에 Poor Story 폰트 적용 (네비게이션 바 제외) */
body, .stButton button, .stTextInput input, .stSelectbox, .stMultiselect,
h1, h2, h3, h4, h5, h6, p, div:not([data-v-96be9aef]), span:not([data-v-96be9aef]), 
li:not([data-v-96be9aef]), a:not([data-v-96be9aef]) {
    font-family: 'Poor Story', cursive !important;
}

/* Streamlit 특정 클래스에 폰트 적용 */
.st-emotion-cache-bm2z3a {
    min-height: 100vh !important;
    overflow: auto !important;
    -webkit-overflow-scrolling: touch !important;
    display: flex !important;
    flex-direction: column !important;
    pointer-events: auto !important;
    font-family: 'Poor Story', cursive !important;
}

/* 이미지 컨테이너 스타일 추가 */
[data-testid="stImageContainer"] {
    display: flex !important;
    justify-content: center !important;
}

/* 전체 화면 프레임 스타일 */
[data-testid="stFullScreenFrame"] {
    display: flex !important;
    justify-content: center !important;
    width: 100% !important;
}

/* 버튼 스타일 */
button[data-testid="stBaseButton-headerNoPadding"] {
    background-color: #d3d3d3 !important;
    font-family: 'Poor Story', cursive !important;
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
        "background-color": "#d3d3d3",
    },
    "div": {
        "max-width": "20rem",
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
    "show_menu": False,
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