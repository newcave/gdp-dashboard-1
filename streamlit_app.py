import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# 페이지 설정
st.set_page_config(
    page_title='Water Quality Dashboard',
    page_icon='💧',
)

# 데이터 불러오기
@st.cache_data
def load_data():
    file_paths = [
        "data/Johnstone_river_coquette_point_joined.csv",
        "data/Johnstone_river_innisfail_joined.csv",
        "data/Mulgrave_river_deeral_joined.csv",
        "data/Pioneer_Dumbleton_joined.csv",
        "data/Plane_ck_sucrogen_joined.csv",
        "data/Proserpine_river_glen_isla_joined.csv",
        "data/russell_river_east_russell_joined.csv",
        "data/sandy_ck_homebush_joined.csv",
        "data/sandy_ck_sorbellos_road_joined.csv",
        "data/Tully_river_euramo_joined.csv"
    ]
    
    dfs = []
    for path in file_paths:
        df = pd.read_csv(path, parse_dates=["Timestamp"])
        df["Site"] = Path(path).stem.replace("_joined", "")
        dfs.append(df)
        
    all_data = pd.concat(dfs, ignore_index=True)
    return all_data

df = load_data()

# 최근 30일 데이터만 필터링
df = df[df['Timestamp'] >= df['Timestamp'].max() - pd.Timedelta(days=30)]

# 지점 선택
sites = df['Site'].unique()
selected_sites = st.multiselect('측정 지점 선택', sites, default=sites[:3])

# 수질 파라미터 선택
parameters = ['Conductivity', 'NO3', 'Temp', 'Turbidity', 'Level']
selected_param = st.selectbox('수질 지표 선택', parameters)

# 필터링된 데이터
df_filtered = df[df['Site'].isin(selected_sites)]

# 시각화
st.header(f"{selected_param} 추이 (최근 1개월)")
fig = px.line(df_filtered, x="Timestamp", y=selected_param, color="Site")
st.plotly_chart(fig, use_container_width=True)

# 지점별 평균값
st.header(f"지점별 평균 {selected_param}")
cols = st.columns(len(selected_sites))
for i, site in enumerate(selected_sites):
    avg_value = df_filtered[df_filtered["Site"] == site][selected_param].mean()
    with cols[i]:
        st.metric(label=site, value=f"{avg_value:.2f}")
