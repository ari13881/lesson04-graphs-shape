import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="영화 데이터 그래프 도감 2 - 분포와 관계", layout="wide")
st.title("영화 데이터 그래프 도감 2 - 분포와 관계")

DATA_URL = "https://raw.githubusercontent.com/happykth/data/main/kobis_movies.csv"


@st.cache_data
def load_data():
    # 1년간 박스오피스 10위권에 든 영화 216편의 요약표를 불러옵니다
    df = pd.read_csv(DATA_URL)
    # 장르가 세로막대 기호(|)로 여러 개 적힌 영화는 첫 번째 장르만 씁니다
    df["장르"] = df["genre"].str.split("|").str[0]
    # openDt(여덟 자리 숫자, 예: 20250101)에서 계절을 뽑아냅니다
    open_month = pd.to_datetime(df["openDt"].astype(str), format="%Y%m%d").dt.month

    def month_to_season(month):
        if month in (3, 4, 5):
            return "봄"
        if month in (6, 7, 8):
            return "여름"
        if month in (9, 10, 11):
            return "가을"
        return "겨울"

    df["계절"] = open_month.apply(month_to_season)
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

# ── 그래프 4. 개봉일 스크린수 vs 총 관객수 산점도 ──
st.header("4. 개봉일 스크린수와 총 관객수의 관계 (산점도)")

fig_scatter = px.scatter(
    df,
    x="first_scrn",
    y="total_audi",
    color="장르",
    hover_name="movieNm",  # 점에 마우스를 올리면 영화명이 보이게 합니다
    labels={"first_scrn": "개봉일 스크린수", "total_audi": "총 관객수"},
)
st.plotly_chart(fig_scatter, width="stretch")

# '이 그래프로 알 수 있는 것' 한 문장을 적는 자리
st.text_input("이 그래프로 알 수 있는 것", key="note4")

st.divider()

# ── 그래프 5. 장르별 총 관객수 상자 그림 (영화 10편 이상 장르만) ──
st.header("5. 장르별 총 관객수 분포 (상자 그림)")

genre_movie_counts = df["장르"].value_counts()
valid_genres = genre_movie_counts[genre_movie_counts >= 10].index
df_box = df[df["장르"].isin(valid_genres)]

fig_box = px.box(
    df_box,
    x="장르",
    y="total_audi",
    hover_name="movieNm",  # 상자 밖으로 튀는 점에 마우스를 올리면 영화명이 보이게 합니다
    points="outliers",
    labels={"total_audi": "총 관객수"},
)
st.plotly_chart(fig_box, width="stretch")

# '이 그래프로 알 수 있는 것' 한 문장을 적는 자리
st.text_input("이 그래프로 알 수 있는 것", key="note5")

st.divider()

# ── 그래프 6. 개봉일 스크린수 vs 총 관객수 버블 그래프 (점 크기 = 첫 주 관객) ──
st.header("6. 개봉일 스크린수와 총 관객수의 관계 (버블 그래프)")

fig_bubble = px.scatter(
    df,
    x="first_scrn",
    y="total_audi",
    size="first_week_audi",
    color="장르",
    hover_name="movieNm",  # 점에 마우스를 올리면 영화명이 보이게 합니다
    labels={
        "first_scrn": "개봉일 스크린수",
        "total_audi": "총 관객수",
        "first_week_audi": "첫 주 관객수",
    },
)
st.plotly_chart(fig_bubble, width="stretch")

# '이 그래프로 알 수 있는 것' 한 문장을 적는 자리
st.text_input("이 그래프로 알 수 있는 것", key="note6")

st.divider()

# ── 그래프 7. 제작 국가 → 장르 선버스트 (칸 크기 = 영화 편수) ──
st.header("7. 제작 국가별 장르 구성 (선버스트)")

fig_sunburst = px.sunburst(
    df,
    path=["nation", "장르"],  # 칸 크기는 지정하지 않으면 영화 편수(행 개수)로 계산됩니다
)
fig_sunburst.update_traces(hovertemplate="%{label}<br>편수: %{value}편<extra></extra>")
st.plotly_chart(fig_sunburst, width="stretch")

# '이 그래프로 알 수 있는 것' 한 문장을 적는 자리
st.text_input("이 그래프로 알 수 있는 것", key="note7")

st.divider()

# ── 그래프 8. 계절 → 장르 선버스트 (안쪽 원: 계절, 바깥 원: 장르) ──
st.header("8. 개봉일의 계절에 따른 영화 장르는 주로 어떠한가")

season_order = ["봄", "여름", "가을", "겨울"]

# 계절 x 장르로 묶어서 편수와 해당 영화명 목록을 만듭니다
grouped = (
    df.groupby(["계절", "장르"])["movieNm"]
    .apply(list)
    .reset_index()
)
grouped["편수"] = grouped["movieNm"].apply(len)
grouped["영화_목록"] = grouped["movieNm"].apply(lambda lst: ", ".join(lst))

ids, labels, parents, values, hover_text = [], [], [], [], []

# 안쪽 원: 계절
for season in season_order:
    season_rows = grouped[grouped["계절"] == season]
    if season_rows.empty:
        continue
    ids.append(season)
    labels.append(season)
    parents.append("")
    values.append(season_rows["편수"].sum())
    hover_text.append(f"{season}: 총 {season_rows['편수'].sum()}편")

# 바깥 원: 장르 (점에 마우스를 올리면 그 안에 든 영화명이 보이게 합니다)
for _, row in grouped.iterrows():
    ids.append(f"{row['계절']}-{row['장르']}")
    labels.append(row["장르"])
    parents.append(row["계절"])
    values.append(row["편수"])
    hover_text.append(row["영화_목록"])

fig_sunburst2 = go.Figure(
    go.Sunburst(
        ids=ids,
        labels=labels,
        parents=parents,
        values=values,
        customdata=hover_text,
        branchvalues="total",
        hovertemplate="%{label}<br>%{customdata}<extra></extra>",
    )
)
st.plotly_chart(fig_sunburst2, width="stretch")

# '이 그래프로 알 수 있는 것' 한 문장을 적는 자리
st.text_input("이 그래프로 알 수 있는 것", key="note8")

st.divider()
# 앞으로 그래프를 계속 추가할 구역
st.header("9. (다음 그래프를 여기에 추가)")
