import streamlit as st

st.set_page_config(page_title="Soccerly", initial_sidebar_state='auto', layout="wide")

import os
from streamlit_navigation_bar import st_navbar
import pages as pg  

st.markdown(
    """
    <style>
        body {
            overflow: auto !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# 네비게이션 바에 표시할 페이지 이름
pages = ["홈", "축구화", "축구선수","대시보드"]
# st.logo('image/logo.png', size = 'Large', link = 'http://54.79.9.198:8501/',icon_image = 'image/logo.png')
st.markdown(
    """
    <style>
        .logo-container {
            display: flex;
            justify-content: center;
            margin-bottom: 20px;
        }
    </style>
    <div class="logo-container">
        <a href="/" onclick="window.location.href='/'">
            <img src="image/logo.png" width="120">
        </a>
    </div>
    """,
    unsafe_allow_html=True
)

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

# 네비게이션 바 생성: 선택한 페이지 이름이 반환됩니다.
page = st_navbar(
    pages,
    styles=styles,
    options=options,
) # 선택한 페이지 이름을 출력 (디버깅 용도)

# 각 페이지에 해당하는 함수 매핑
functions = {
    "홈": pg.show_home,
    "축구화": pg.show_Find,
    "축구선수": pg.show_player,
    "대시보드":pg.show_dashboard
}

# 선택한 페이지의 함수를 호출하여 해당 페이지 내용 표시
go_to = functions.get(page)
if go_to:
    go_to()


