import streamlit as st
import os
from streamlit_navigation_bar import st_navbar
import pages as pg  

st.set_page_config(page_title="Soccerly", initial_sidebar_state='auto', layout="wide")

st.query_params["pages"] = "home"

# ✅ 스크롤 문제 해결 (iPhone Safari 대응)
st.markdown("""
<style>
/* ✅ 전체 화면 컨테이너 스크롤 허용 /
html, body, [data-testid="stAppViewContainer"], .st-emotion-cache-bm2z3a {
    min-height: 100vh !important;
    height: 100% !important;
    overflow: auto !important;
    -webkit-overflow-scrolling: touch !important;
    pointer-events: auto !important;
}

/ ✅ Streamlit 기본 레이아웃 조정 /
[data-testid="stMainBlockContainer"] {
    display: block !important;
    overflow: auto !important;
    height: auto !important;
    min-height: 100vh !important;
}

/ ✅ 사이드바 스크롤 활성화 /
[data-testid="stSidebarContent"] {
    height: auto !important;
    min-height: 100vh !important;
    overflow-y: auto !important;
}

/ ✅ iFrame(네비게이션 바) 스크롤 허용 /
iframe {
    min-height: auto !important;
    height: fit-content !important;
    overflow-y: auto !important;
    pointer-events: auto !important;
}

/ ✅ Streamlit 네비게이션 바 고정 및 스크롤 문제 해결 /
iframe[title="streamlit_navigation_bar.st_navbar"] {
    height: auto !important;
    position: fixed !important;
    z-index: 9999 !important;
    top: 0px !important;
    left: 0px !important;
    width: 100% !important;
}

/ ✅ Streamlit 기본 UI 요소 터치 가능하도록 수정 */
div[data-testid="stAppViewContainer"] {
    pointer-events: auto !important;
}
div[data-testid="stMainBlockContainer"] {
    pointer-events: auto !important;
}
section[data-testid="stSidebar"] {
    pointer-events: auto !important;
}
</style>
""", unsafe_allow_html=True)

# 
st.markdown("""
<style>
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
""", unsafe_allow_html=True)

# 웹페이지에 로고 삽입
st.logo('image/logo.png', size = 'Large', icon_image = 'image/logo.png')

# 네비게이션 바에 표시할 페이지 이름
pages = ["Home", "Boots", "Player","Matching"]


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
        "padding": "5px",
        "font-family": "auto",
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

# 네비게이션 바 옵션 설정 (메뉴와 사이드바를 활성화)
options = {
    "show_menu": False,
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
    "Home": pg.show_home,
    "Boots": pg.show_boots,
    "Player": pg.show_player,
    "Matching":pg.show_matching
}

# 페이지 하단 고정
st.markdown(
    """
    <style>
        .footer {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: rgba(248, 249, 250, 1); /* 기본 색 */
            text-align: center;
            padding: 10px;
            font-size: 14px;
            color: #333;
            border-top: 1px solid #ddd;
            transition: background-color 0.5s ease-in-out; /* 부드러운 전환 효과 */
        }
    </style>

    <script>
        window.addEventListener("scroll", function() {
            var footer = document.querySelector(".footer");
            if (window.scrollY > 50) {  // 스크롤 50px 이상 내려가면
                footer.style.backgroundColor = "rgba(248, 249, 250, 0)"; // 투명하게
            } else {
                footer.style.backgroundColor = "rgba(248, 249, 250, 1)"; // 원래 색상
            }
        });
    </script>

    <div class="footer">
        📩 문의: <a href="mailto:shinyeop1224@gmail.com">shinyeop1224@gmail.com</a><br>
        📋 피드백 제출: <a href="https://forms.gle/Chx2ECTp5F1qvQzS9" target="_blank">Google Forms 바로가기</a>
    </div>
    """,
    unsafe_allow_html=True
)

# 선택한 페이지의 함수를 호출하여 해당 페이지 내용 표시
go_to = functions.get(page)
if go_to:
    go_to()