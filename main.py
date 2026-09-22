import streamlit as st
import pandas as pd
import plotly.express as px

# ────────────────────────────────────────────────────────────
# 기본 설정
# ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    page_icon="🎬",
    layout="wide",
)

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"


@st.cache_data
def load_data(url: str) -> pd.DataFrame:
    df = pd.read_csv(url)

    # genre 열에 세로막대(|) 기호로 여러 장르가 적힌 경우 첫 번째 장르만 사용
    if "genre" in df.columns:
        df["genre"] = df["genre"].astype(str).str.split("|").str[0].str.strip()

    return df


df = load_data(DATA_URL)

# ────────────────────────────────────────────────────────────
# 제목 & 데이터 소개
# ────────────────────────────────────────────────────────────
st.title("🎬 영화 데이터 그래프 도감 2 - 분포와 관계")

st.markdown(
    """
이 앱은 **최근 1년간 박스오피스 10위권에 들었던 영화 216편**의 데이터를 바탕으로,
장르 · 국가 · 스크린수 · 관객수 등 다양한 지표의 **분포와 관계**를 그래프로 살펴봅니다.
"""
)

with st.expander("📄 원본 데이터 미리보기"):
    st.dataframe(df, use_container_width=True)

st.divider()

# ────────────────────────────────────────────────────────────
# 그래프 1. 장르별 영화 편수 (도넛 그래프)
# ────────────────────────────────────────────────────────────
st.header("1️⃣ 장르별 영화 편수")

genre_counts = (
    df["genre"]
    .value_counts()
    .reset_index()
)
genre_counts.columns = ["genre", "count"]

fig_donut = px.pie(
    genre_counts,
    names="genre",
    values="count",
    hole=0.5,
    title="장르별 영화 편수 분포",
)
fig_donut.update_traces(
    textinfo="label+percent",
    hovertemplate="%{label}<br>편수: %{value}편<br>비율: %{percent}<extra></extra>",
)
fig_donut.update_layout(
    legend_title_text="장르",
    margin=dict(t=60, b=20, l=20, r=20),
)

st.plotly_chart(fig_donut, use_container_width=True)

st.markdown("**🔎 이 그래프로 알 수 있는 것:** ")
# TODO: 위 문장 뒤에 그래프를 보고 파악한 내용을 한 문장으로 채워 넣으세요.

st.divider()

# ────────────────────────────────────────────────────────────
# (이후 그래프가 추가될 자리)
# 새 그래프를 추가할 때는 위와 같은 형식으로
#   st.header(...) → 그래프 → "이 그래프로 알 수 있는 것" → st.divider()
# 순서를 반복해 주세요.
# ────────────────────────────────────────────────────────────
