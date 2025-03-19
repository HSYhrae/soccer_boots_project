import streamlit as st
import pandas as pd
import os

# 검색 기록 파일 경로
SEARCH_COUNT_FILE = "./data/search_counts.csv"

def main():
    # 데이터 로드 함수
    @st.cache_data
    def load_data():
        df = pd.read_csv("./data/player.csv")  # 선수 데이터 불러오기
        selected_columns = {
            "name_ko": "이름",
            "country_ko": "국가",
            "position_ko": "포지션",
            "team_name": "팀",
            "age": "나이",
            "height": "키",
            "img": "이미지",
            "img_src": "배경 이미지",
            "boots_ko": "축구화",
            "boots_img": "축구화 이미지"
        }
        df = df[list(selected_columns.keys())]  # 필요한 컬럼 선택
        df = df.rename(columns=selected_columns)  # 컬럼명 변경
        return df

    # 검색 기록을 불러오는 함수
    def load_search_counts():
        if not os.path.exists(SEARCH_COUNT_FILE):
            return pd.DataFrame(columns=["이름", "검색 횟수"])
        return pd.read_csv(SEARCH_COUNT_FILE)

    # 검색 횟수 업데이트 함수
    def update_search_count(player_name):
        search_df = load_search_counts()
        
        if player_name in search_df["이름"].values:
            search_df.loc[search_df["이름"] == player_name, "검색 횟수"] += 1
        else:
            search_df = pd.concat([search_df, pd.DataFrame({"이름": [player_name], "검색 횟수": [1]})], ignore_index=True)
        
        search_df.to_csv(SEARCH_COUNT_FILE, index=False)

    # 유효한 이미지 URL 가져오기
    def get_valid_image(url):
        if pd.isna(url) or url == "":
            return "https://via.placeholder.com/150"
        return url

    # Streamlit UI
    st.title("선수 목록")
    st.write("👈 사이드바에서 선수를 검색하여 상세 목록을 확인하세요!")

    # 데이터 로드
    df = load_data()

    # 사이드바에서 선수 이름 선택
    selected_name = st.sidebar.selectbox("선수 이름을 선택하세요", [""] + df["이름"].unique().tolist())

    # 검색 버튼 추가
    search_button = st.sidebar.button("검색하기")

    # 선수 정보 표시
    if not search_button:
        df_display = df.drop(columns=["이미지", "배경 이미지", "축구화 이미지"])
        st.dataframe(df_display)
    elif selected_name:
        # 검색 횟수 업데이트
        update_search_count(selected_name)

        player_info = df.loc[df["이름"] == selected_name].iloc[0].to_dict()
        img_1 = get_valid_image(player_info.get("배경 이미지"))
        img_2 = get_valid_image(player_info.get("이미지"))
        boots_img = get_valid_image(player_info.get("축구화 이미지"))

        # HTML로 선수 정보 표시
        html_content = f"""
        <div style="padding: 20px; border-radius: 10px; text-align: center;">
            <div style="position: relative; width: 200px; height: 200px; margin: auto;">
                <img src="{img_1}" style="width: 120%; opacity: 0.5; border-radius: 10px;">
                <img src="{img_2}" style="position: absolute; top: 75px; left: 50px; width: 60%;">
            </div>
            <div>
                <img src="{boots_img}" style="width: 200px; margin-top: 10px;">
            </div>
            <p><strong>이름:</strong> {player_info.get('이름')}</p>
            <p><strong>포지션:</strong> {player_info.get('포지션')}</p>
            <p><strong>축구화:</strong> {player_info.get('축구화')}</p>
            <p><strong>팀:</strong> {player_info.get('팀')}</p>
            <p><strong>국가:</strong> {player_info.get('국가')}</p>
            <p><strong>나이:</strong> {player_info.get('나이')}</p>
            <p><strong>키:</strong> {player_info.get('키')} cm</p>
        </div>
        """
        st.markdown(html_content, unsafe_allow_html=True)

    # 🔥 **실시간 검색 순위 (검색량 숨김)**
    st.sidebar.subheader("🔥 실시간 검색 순위")
    search_df = load_search_counts()

    if not search_df.empty:
        search_df = search_df.sort_values(by="검색 횟수", ascending=False).head(10)
        st.sidebar.write("\n".join(f"⭐ {name}" for name in search_df["이름"]))
    else:
        st.sidebar.write("아직 검색된 선수가 없습니다.")

def show_player():
    st.query_params["pages"] = "player"
    main()