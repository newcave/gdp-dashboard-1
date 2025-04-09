import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# Set Streamlit page configuration
st.set_page_config(
    page_title='Water Quality Dashboard',
    page_icon='💧',
)

# -------------------------------------------------------------------
# Data loading utility
@st.cache_data
def load_data():
    BASE_DIR = Path(__file__).parent
    DATA_DIR = BASE_DIR / "data"

    file_paths = [
        DATA_DIR / "Johnstone_river_coquette_point_joined.csv",
        DATA_DIR / "Johnstone_river_innisfail_joined.csv",
        DATA_DIR / "Mulgrave_river_deeral_joined.csv",
        DATA_DIR / "Pioneer_Dumbleton_joined.csv",
        DATA_DIR / "Plane_ck_sucrogen_joined.csv",
        DATA_DIR / "Proserpine_river_glen_isla_joined.csv",
        DATA_DIR / "russell_river_east_russell_joined.csv",
        DATA_DIR / "sandy_ck_homebush_joined.csv",
        DATA_DIR / "sandy_ck_sorbellos_road_joined.csv",
        DATA_DIR / "Tully_river_euramo_joined.csv"
    ]
    
    dfs = []
    for path in file_paths:
        if path.exists():
            df = pd.read_csv(path, parse_dates=["Timestamp"])
            df["Site"] = path.stem.replace("_joined", "")
            dfs.append(df)
        else:
            st.warning(f"파일을 찾을 수 없습니다: {path}")
    return pd.concat(dfs, ignore_index=True)

# Load data
df = load_data()

# Filter to recent 1 month
df = df[df['Timestamp'] >= df['Timestamp'].max() - pd.Timedelta(days=30)]

# -------------------------------------------------------------------
# UI Header
'''
# 💧 Water Quality Dashboard

최근 1개월 동안의 다중 수질 측정 지점 데이터를 시각화합니다.
'''

# Parameter and Site selection
all_sites = sorted(df['Site'].unique())
selected_sites = st.multiselect("측정 지점 선택", all_sites, default=all_sites[:3])

parameters = ['Conductivity', 'NO3', 'Temp', 'Turbidity', 'Level']
selected_param = st.selectbox("수질 지표 선택", parameters)

# Filter data for selected sites
filtered_df = df[df['Site'].isin(selected_sites)]

# -------------------------------------------------------------------
# Chart
st.header(f"📈 {selected_param} 추이 (최근 1개월)", divider="gray")

fig = px.line(
    filtered_df,
    x="Timestamp",
    y=selected_param,
    color="Site",
    labels={"Timestamp": "시간", selected_param: selected_param}
)
st.plotly_chart(fig, use_container_width=True)

# -------------------------------------------------------------------
# Site average metrics
st.header(f"📊 지점별 평균 {selected_param}", divider="gray")

cols = st.columns(len(selected_sites))
for i, site in enumerate(selected_sites):
    site_data = filtered_df[filtered_df["Site"] == site]
    avg_value = site_data[selected_param].mean()
    with cols[i]:
        st.metric(label=site, value=f"{avg_value:.2f}")
