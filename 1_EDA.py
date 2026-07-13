import sys
import pandas as pd
import streamlit as st

st.set_page_config(page_title="EDA",layout="wide")
st.title(":chart_with_upwards_trend: Decoding K-Pop Chart Trends")
df = pd.read_csv("Atlantic_South_Korea.csv")
df = df.drop_duplicates()
df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y').dt.strftime('%Y-%m-%d')
df['duration_min'] = (df['duration_ms'] / 60000).round(2)

st.markdown("---")

st.write("### :mag: Dataset Preview")
st.dataframe(df.head(10))

st.markdown("---")

st.write("### :bar_chart: Quick Stats")
col1, col2, col3, col4 = st.columns(4)
col1.metric(" :1234: Total Rows", f"{len(df):,}")
col2.metric(" :card_index: Total Columns", len(df.columns))
col3.metric(" :microphone: Unique Artists", df['artist'].nunique())
col4.metric(" :headphones: Unique Songs", df['song'].nunique())

st.markdown("---")
st.write("### :mag: Missing Values Check")
missing = df.isnull().sum().reset_index()
missing.columns = ["Column", "Missing Values"]
st.dataframe(missing)

st.markdown("---")
st.write("### :trophy: Top 10 Artists")
top_artists = df['artist'].value_counts().head(10).reset_index()
top_artists.columns = ["Artist", "Chart Appearances"]
st.dataframe(top_artists)

st.markdown("---")
st.write("### :musical_note: Top 10 Songs")
top_songs = df['song'].value_counts().head(10).reset_index()
top_songs.columns = ["Song", "Chart Appearances"]
st.dataframe(top_songs)

st.markdown("---")
st.write("### :bar_chart: Basic Statistics")
st.dataframe(df.describe())

st.markdown("---")
st.write("### :mag: Missing Values Check")
missing = df.isnull().sum().reset_index()
missing.columns = ["Column", "Missing Values"]
st.dataframe(missing)

st.markdown("---")
st.write("### :trophy: Top 10 Artists")
top_artists = df['artist'].value_counts().head(10).reset_index()
top_artists.columns = ["Artist", "Chart Appearances"]
st.dataframe(top_artists)

st.markdown("---")
st.write("### :musical_note: Top 10 Songs")
top_songs = df['song'].value_counts().head(10).reset_index()
top_songs.columns = ["Song", "Chart Appearances"]
st.dataframe(top_songs)

st.markdown("---")
st.write("### :bar_chart: Basic Statistics")
st.dataframe(df.describe(include='number'))
import plotly.express as px

st.markdown("---")
st.write("### :bar_chart: Top 10 Artists — Chart Appearances")
top_artists_chart = df['artist'].value_counts().head(10).reset_index()
top_artists_chart.columns = ["Artist", "Appearances"]
fig1 = px.bar(top_artists_chart, x="Artist", y="Appearances", 
              color="Appearances", color_continuous_scale="reds",
              title="Top 10 Artists by Chart Appearances")
st.plotly_chart(fig1, use_container_width=True)

st.markdown("---")
st.write("### :cd: Album Type Distribution")
album_dist = df['album_type'].value_counts().reset_index()
album_dist.columns = ["Album Type", "Count"]
fig2 = px.pie(album_dist, names="Album Type", values="Count",
              title="Singles vs Albums vs Compilations",
              color_discrete_sequence=["#FF0050", "#1DB954", "#7B2FBE"])
st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")
st.write("### :underage: Explicit vs Non-Explicit Songs")
explicit_dist = df['is_explicit'].value_counts().reset_index()
explicit_dist.columns = ["Is Explicit", "Count"]
explicit_dist["Is Explicit"] = explicit_dist["Is Explicit"].map({True: "Explicit", False: "Clean"})
fig3 = px.pie(explicit_dist, names="Is Explicit", values="Count",
              title="Explicit vs Clean Content",
              color_discrete_sequence=["#FF0050", "#1A1A2E"])
st.plotly_chart(fig3, use_container_width=True)