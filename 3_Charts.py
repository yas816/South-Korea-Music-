import sys
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Charts", layout="wide")
st.title(":chart_with_upwards_trend: K-Pop Chart Visualizations")

df = pd.read_csv("Atlantic_South_Korea.csv")
df = df.drop_duplicates()
df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y')
df['duration_min'] = (df['duration_ms'] / 60000).round(2)

st.markdown("---")

# Chart 1 - Top 10 Artists
st.write("### :microphone: Top 10 Artists by Chart Appearances")
top_artists = df['artist'].value_counts().head(10).reset_index()
top_artists.columns = ["Artist", "Appearances"]
fig1 = px.bar(top_artists, x="Artist", y="Appearances",
              color="Appearances", color_continuous_scale="reds",
              title="Top 10 Artists")
st.plotly_chart(fig1, use_container_width=True)

st.markdown("---")

# Chart 2 - Popularity trend over time
st.write("### :chart_with_upwards_trend: Average Popularity Over Time")
popularity_trend = df.groupby('date')['popularity'].mean().reset_index()
fig2 = px.line(popularity_trend, x="date", y="popularity",
               title="Average Song Popularity Over Time",
               color_discrete_sequence=["#FF0050"])
st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# Chart 3 - Top 10 Songs
st.write("### :musical_note: Top 10 Songs by Chart Appearances")
top_songs = df['song'].value_counts().head(10).reset_index()
top_songs.columns = ["Song", "Appearances"]
fig3 = px.bar(top_songs, x="Appearances", y="Song", orientation='h',
              color="Appearances", color_continuous_scale="purples",
              title="Top 10 Songs")
fig3.update_layout(yaxis={'categoryorder': 'total ascending'})
st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")

# Chart 4 - Popularity distribution
st.write("### :star: Popularity Score Distribution")
fig4 = px.histogram(df, x="popularity", nbins=20,
                    title="Distribution of Popularity Scores",
                    color_discrete_sequence=["#FF0050"])
st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")

# Chart 5 - Song duration distribution
st.write("### :stopwatch: Song Duration Distribution")
fig5 = px.histogram(df, x="duration_min", nbins=30,
                    title="Distribution of Song Durations (minutes)",
                    color_discrete_sequence=["#7B2FBE"])
st.plotly_chart(fig5, use_container_width=True)