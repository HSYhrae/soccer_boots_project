import streamlit as st
# from streamlit_option_menu import option_menu

# 🚀 여기서 가장 먼저 실행해야 함!
st.set_page_config(page_title="FindBoots", layout="wide")

# # 네비게이션 바 (상단)
# selected = option_menu(
#     menu_title=None,
#     options=["Home", "Find", "Player"],
#     icons=["house", "search", "person"],
#     default_index=0,
#     orientation="horizontal",
# )

import streamlit as st
from streamlit_navigation_bar import st_navbar

page = st_navbar(["Home", "Find", "player"])

# 각 페이지에 맞는 내용 표시
if page == "Home":
    st.title("🏠 Home 페이지")
    st.write("여기는 홈입니다.")

elif page == "Find":
    st.switch_page("pages/Find.py")

elif page == "player":
    st.switch_page("pages/player.py")

