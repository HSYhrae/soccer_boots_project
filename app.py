import streamlit as st
import os
from streamlit_navigation_bar import st_navbar
import pages as pg  

st.set_page_config(page_title="Soccerly", initial_sidebar_state='auto', layout="wide")

# ✅ 스크롤 문제 해결 (iPhone Safari 대응)
st.markdown("""
    <style>
    html, body, [data-testid="stAppViewContainer"], .st-emotion-cache-bm2z3a {
        min-height: 100vh !important; /* 전체 화면 채우기 */
        height: 100% !important;
        overflow: auto !important;
        -webkit-overflow-scrolling: touch !important; /* iPhone 스크롤 부드럽게 */
    }

    [data-testid="stSidebarContent"] {
        overflow-y: auto !important;
        height: 100% !important;
    }
    </style>
""", unsafe_allow_html=True)

# 웹페이지에 로고 삽입
st.logo('image/logo.png', size='Large', icon_image='image/logo.png')

# 네비게이션 바에 표시할 페이지 이름
pages = ["Home", "Boots", "Player", "Dashboard"]

# 네비게이션 바 스타일 설정 (모바일 환경 고려)
styles = {
    "nav": {
        "background-color": "#d3d3d3",
    },
    "div": {
        "max-width": "unset",  # 모바일에서 제한 해제
        "width": "100%",  # 전체 너비 사용
    },
    "span": {
        "color": "white",
        "padding": "5px",
        "font-family": "Poor Story",
    },
    "active": {
        "background-color": "white",
        "color": "var(--text-color)",
        "font-weight": "bold",
        "padding": "14px",
    },
    "hover": {
        "background-color": "rgba(255, 255, 255, 0.35)",
    },
}

# 네비게이션 바 옵션 설정 (메뉴와 사이드바 활성화)
options = {
    "show_menu": False,
    "show_sidebar": True,
    "use_padding": True,
}

# 네비게이션 바 생성
page = st_navbar(pages, styles=styles, options=options)

# 각 페이지에 해당하는 함수 매핑
functions = {
    "Home": pg.show_home,
    "Boots": pg.show_Find,
    "Player": pg.show_player,
    "Dashboard": pg.show_dashboard
}

# 선택한 페이지의 함수를 호출하여 해당 페이지 내용 표시
go_to = functions.get(page)
if go_to:
    go_to()
