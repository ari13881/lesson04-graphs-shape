import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="영화 데이터 그래프 도감 2 - 분포와 관계", layout="wide")
st.title("영화 데이터 그래프 도감 2 - 분포와 관계")

DATA_URL = "https://raw.githubusercontent.com/happykth/data/main/kobis_movies.csv"


@st.cache_data
def load_data():
    # 1년간 박스오피스 10위권에 든 영화 216편의 요약표를 불러옵니다
    df = pd.read_csv(DATA_URL)
    # 장르가 세로막대 기호(|)로 여러 개 적힌 영화는 첫 번째 장르만 씁니다
    df["장르"] = df["genre"].str.split("|").str[0]
    return df


df = load_data()

# ── 그래프 1. 장르별 영화 편수 도넛 ──
st.header("1. 장르별 영화 편수 (도넛)")
genre_count = df["장르"].value_counts().reset_index()
genre_count.columns = ["장르", "편수"]

fig = px.pie(
    genre_count,
    names="장르",
    values="편수",
    hole=0.45,  # 가운데 구멍을 뚫어 도넛 모양으로
)
# 조각에 마우스를 올리면 편수와 비율이 보이게 합니다
fig.update_traces(hovertemplate="%{label}<br>%{value}편 (%{percent})<extra></extra>")
st.plotly_chart(fig, width="stretch")

# '이 그래프로 알 수 있는 것' 한 문장을 적는 자리
st.text_input("이 그래프로 알 수 있는 것", key="note1")

st.divider()

# ── 그래프 2. 장르 안에 영화가 담긴 트리맵 ──
st.header("2. 장르별 영화 트리맵 (총 관객수 기준)")

fig_tree = px.treemap(
    df,
    path=["장르", "movieNm"],
    values="total_audi",
)
# 칸에 마우스를 올리면 영화명과 총 관객수가 보이게 합니다
fig_tree.update_traces(hovertemplate="%{label}<br>총 관객: %{value:,}명<extra></extra>")
st.plotly_chart(fig_tree, width="stretch")

# '이 그래프로 알 수 있는 것' 한 문장을 적는 자리
st.text_input("이 그래프로 알 수 있는 것", key="note2")

st.divider()

# ── 그래프 3. 총 관객수 히스토그램 ──
st.header("3. 총 관객수 분포 (히스토그램)")

fig_hist = px.histogram(
    df,
    x="total_audi",
    nbins=20,
    labels={"total_audi": "총 관객수"},
)
fig_hist.update_layout(yaxis_title="영화 편수")
st.plotly_chart(fig_hist, width="stretch")

# 어느 구간에 영화가 가장 많이 몰려 있는지 계산합니다
counts, bin_edges = np.histogram(df["total_audi"].dropna(), bins=20)
peak_idx = counts.argmax()
peak_low, peak_high = bin_edges[peak_idx], bin_edges[peak_idx + 1]

# 총 관객수가 가장 많은 영화를 찾습니다
top_movie = df.loc[df["total_audi"].idxmax()]

st.markdown(
    f"대부분의 영화는 총 관객 **{peak_low:,.0f}명 ~ {peak_high:,.0f}명** 구간에 몰려 있고, "
    f"가장 관객이 많은 영화는 **{top_movie['movieNm']}**"
    f"(총 {top_movie['total_audi']:,.0f}명)입니다."
)

# '이 그래프로 알 수 있는 것' 한 문장을 적는 자리
st.text_input("이 그래프로 알 수 있는 것", key="note3")

st.divider()
# 앞으로 그래프를 계속 추가할 구역
st.header("4. (다음 그래프를 여기에 추가)")
