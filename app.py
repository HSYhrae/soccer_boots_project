import streamlit as st
import os
from streamlit_navigation_bar import st_navbar
import pages as pg  

st.set_page_config(page_title="Soccerly", initial_sidebar_state='auto', layout="wide")

st.query_params["pages"] = "홈"

# ✅ 스크롤 문제 해결 (iPhone Safari 대응)
st.markdown("""
    <style>
    html, body, [data-testid="stAppViewContainer"], .st-emotion-cache-bm2z3a {
        height: 100% !important;
        overflow: auto !important;
        -webkit-overflow-scrolling: touch !important;
    }
    
    [data-testid="stSidebar"] {
        overflow: auto !important;
        height: 100% !important;
    }
    </style>
""", unsafe_allow_html=True)

# ✅ 폰트 적용 (Safari 호환성을 위해 `@import` 대신 `<link>` 방식)
st.markdown("""
    <link href="https://fonts.googleapis.com/css?family=Nanum+Gothic+Coding:400" rel="stylesheet">
    <style>
        body, .stButton button, .stTextInput input, .stSelectbox, .stMultiselect, h1, h2, h3, h4, h5, h6, p, div, span, li, a {
            font-family: 'Nanum Gothic Coding', monospace !important;
        }
    </style>
""", unsafe_allow_html=True)

# ✅ 로고 표시 (`st.logo()` → `st.sidebar.image()`로 변경)
st.sidebar.image("image/logo.png", use_column_width=True)

# ✅ 네비게이션 바 설정
pages = ["Home", "Boots", "Player","Dashboard"]

styles = {
    "nav": {
        "background-color": "#d3d3d3",
    },
    "div": {
        "max-width": "20rem",
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

options = {
    "show_menu": False,
    "show_sidebar": True,
    "use_padding": True,
}

page = st_navbar(pages, styles=styles, options=options)

# ✅ 페이지 라우팅 (매핑 오류 수정)
functions = {
    "Home": pg.show_home,
    "Boots": pg.show_Find,
    "Player": pg.show_player,
    "Dashboard": pg.show_dashboard
}

if page in functions:
    functions[page]()
