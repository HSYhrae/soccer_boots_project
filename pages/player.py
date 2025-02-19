import streamlit as st
import pandas as pd
import requests
import os
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
from streamlit_modal import Modal

##############################
# 데이터 로딩 및 전처리 함수
##############################
@st.cache_data
def load_data():
    df = pd.read_csv("./data/player.csv")
    return df

def get_valid_image(url):
    """
    주어진 이미지 URL로 요청을 보내어 정상 응답이 오면 해당 URL을,
    그렇지 않으면 로컬 이미지(./image/man.png)를 반환합니다.
    """
    try:
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            return url
        else:
            return "./image/man.png"
    except Exception:
        return "./image/man.png"

def get_text_color_for_bg(bg_color: str) -> str:
    """
    #RRGGBB 형식의 배경색(bg_color)에 따라 글자색을 흰색(#FFFFFF) 또는 검은색(#000000)으로 결정.
    - 밝기(휘도, Luminance)가 0.5보다 작으면 흰색, 크면 검은색을 사용.
    - bg_color가 형식에 맞지 않으면 기본적으로 검은색(#000000) 사용.
    """
    # 유효성 검사
    if not (isinstance(bg_color, str) and bg_color.startswith('#') and len(bg_color) == 7):
        return "#000000"  # 기본 검정색
    
    # 배경색을 RGB 정수로 파싱
    try:
        r = int(bg_color[1:3], 16)
        g = int(bg_color[3:5], 16)
        b = int(bg_color[5:7], 16)
    except ValueError:
        return "#000000"
    
    # 가중치에 따른 휘도 계산 (sRGB -> Luminance 추정)
    # 간단히 0.299*r + 0.587*g + 0.114*b 사용
    luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255.0
    
    # 임계값(0.5) 기준으로 어두우면 흰색, 밝으면 검정색
    if luminance < 0.5:
        return "#FFFFFF"
    else:
        return "#000000"

###################
# 메인 실행 함수  #
###################
def main():
    st.title("KNN 유사 선수 추천 서비스")
    st.write("**포지션**과 **키(cm)**를 입력하면, 해당 특성과 유사한 선수 10명을 추천해드립니다.")

    # --- Session State 초기화 ---
    if "similar_players" not in st.session_state:
        st.session_state["similar_players"] = None  # KNN 결과
    if "modal_open" not in st.session_state:
        st.session_state["modal_open"] = False      # 모달 열림 상태
    if "selected_player" not in st.session_state:
        st.session_state["selected_player"] = None  # 선택된 선수 식별(이름 등)

    # --- Modal 객체 생성 ---
    modal = Modal(key="player_modal", title="축구선수 정보 보기")

    # --- 데이터 불러오기 ---
    df = load_data()

    # --- 사용자 입력 (포지션 & 키) ---
    positions = df['position'].dropna().unique().tolist()
    selected_position = st.selectbox("포지션을 선택하세요", positions)
    selected_height = st.number_input("키를 입력하세요 (cm)",
                                      min_value=140.0,
                                      max_value=220.0,
                                      value=180.0,
                                      step=0.5)

    # --- 유사 선수 찾기 버튼 ---
    if st.button("유사 선수 10명 찾기"):
        # (1) Feature Matrix 구성 (포지션: one-hot 인코딩 + height)
        features = pd.concat([
            pd.get_dummies(df['position'], prefix='pos'),
            df[['height']]
        ], axis=1)

        # (2) 스케일링
        scaler = StandardScaler()
        features_scaled = scaler.fit_transform(features)

        # (3) KNN 모델 학습 (10명 추천)
        knn = NearestNeighbors(n_neighbors=10)
        knn.fit(features_scaled)

        # (4) 사용자 입력 전처리
        query_df = pd.DataFrame({
            "position": [selected_position],
            "height": [selected_height]
        })
        query_features = pd.concat([
            pd.get_dummies(query_df['position'], prefix='pos'),
            query_df[['height']]
        ], axis=1)
        query_features = query_features.reindex(columns=features.columns, fill_value=0)
        query_scaled = scaler.transform(query_features)

        # (5) 유사 선수 10명 추천
        distances, indices = knn.kneighbors(query_scaled)
        similar_players = df.iloc[indices[0]].copy()
        similar_players["distance"] = distances[0]

        # --- 세션 스테이트에 결과 저장 ---
        st.session_state["similar_players"] = similar_players
        st.session_state["modal_open"] = False
        st.session_state["selected_player"] = None

    # --- 추천 결과 표시 ---
    similar_players = st.session_state["similar_players"]
    if similar_players is not None:
        st.subheader("유사한 선수 10명")

        # 5명씩 가로로 배치
        for i in range(0, len(similar_players), 5):
            cols = st.columns(5)
            for idx, col in enumerate(cols):
                row_idx = i + idx
                if row_idx < len(similar_players):
                    row = similar_players.iloc[row_idx]
                    with col:
                        # 이미지 표시
                        img = get_valid_image(row["image_url"])
                        st.image(img, width=100)
                        st.write(row["name_en"])
                        
                        # 선수 정보 보기 버튼
                        if st.button("선수 정보 보기", key=f"btn_{row['name_en']}_{row_idx}"):
                            # 클릭 시 모달 열기 상태와 선택된 선수 설정
                            st.session_state["modal_open"] = True
                            st.session_state["selected_player"] = row["name_en"]
                            modal.open()

    # --- 모달 표시 ---
    # session_state["modal_open"]가 True라면 모달을 열기
    if modal.is_open():
        with modal.container():
            selected_name = st.session_state["selected_player"]
            if selected_name:
                # 해당 선수 정보 추출
                player_info = df.loc[df["name_en"] == selected_name].iloc[0].to_dict()
                img = get_valid_image(player_info.get("image_url"))
                
                # color 컬럼이 있다면, 그 값으로 배경색 지정
                player_color = player_info.get("color", "#B53D3D")
                text_color = get_text_color_for_bg(player_color)  # 배경색에 맞춰 글씨색 결정

                # 모달 내부 HTML
                html_content = f"""
                <div style="background-color: {player_color}; color: {text_color};
                            padding: 20px; border-radius: 10px;">
                    <h3>선수 상세 정보</h3>
                    <img src="{img}" width="150">
                    <p><strong>이름:</strong> {player_info.get('name_en')}</p>
                    <p><strong>포지션:</strong> {player_info.get('position')}</p>
                    <p><strong>키:</strong> {player_info.get('height')} cm</p>
                </div>
                """
                st.markdown(html_content, unsafe_allow_html=True)
            else:
                st.write("선수를 찾을 수 없습니다.")

            # # 모달 닫기 버튼
            # if st.button("닫기", key="close_modal"):
            #     st.session_state["modal_open"] = False
            #     modal.close()

if __name__ == "__main__":
    main()



