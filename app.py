import sys
import streamlit as st
import pandas as pd
import plotly.express as px
st.set_page_config(page_title="SK Spotify Charts",layout="wide")
st.title(":headphones: South Korea Spotify Charts Dashboard")
st.write("### Comeback Momentum, Chart Re-Entry and Fandom Intensity Analysis")
df= pd.read_csv("Atlantic_South_Korea.csv")
df=df.drop_duplicates()
df['date']=pd.to_datetime(df['date'],format='%d-%m-%Y')
df['duration_min']=(df['duration_ms']/6000).round(2)
st.markdown("---")
st.write("### :bar_chart: Dataset Overview")
col1, col2, col3, col4 = st.columns(4)
col1.metric(":musical_note: Total Records", f"{len(df):,}")
col2.metric(":microphone: Unique Artists", df['artist'].nunique())
col3.metric(":headphones: Unique Songs", df['song'].nunique())
col4.metric(":calendar: Days of Data", df['date'].nunique())
st.markdown("---")

st.markdown("""
### :sparkles: About This Project
This dashboard analyzes **555 days** of South Korea's Spotify Top 50 chart data to uncover:

- :repeat: **Chart Re-Entry** — Which songs came back to charts after disappearing
- :fire: **Comeback Momentum** — How strong was the ranking jump after re-entry  
- :trophy: **Fandom Intensity** — Which artists have the most dedicated fandoms
- :headphones: **Content Analysis** — Singles vs Albums, Explicit vs Clean
""")

st.markdown("---")
st.info(":point_left: Use the sidebar to navigate between pages!")