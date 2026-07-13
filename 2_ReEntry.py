import sys
import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Re-Entry Analysis",layout="wide")
st.title(":repeat: Chart Re-Entry Analysis")
df=pd.read_csv("Atlantic_South_Korea.csv")
df=df.drop_duplicates()
df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y')
song_name = "Like Crazy"
song_df = df[df['song'] == song_name].sort_values('date')
st.sidebar.title(":control_knobs: Filters")

# Date range selector
min_date = df['date'].min()
max_date = df['date'].max()
date_range = st.sidebar.date_input("Select Date Range", value=(min_date, max_date), 
                                     min_value=min_date, max_value=max_date)

# Artist search
artist_search = st.sidebar.selectbox("Filter by Artist", ["All"] + sorted(df['artist'].unique().tolist()))

# Album type toggle
album_filter = st.sidebar.multiselect("Album Type", options=df['album_type'].unique().tolist(), 
                                        default=df['album_type'].unique().tolist())
# Apply filters to create a filtered dataframe
filtered_df = df.copy()

# Apply date range filter
if len(date_range) == 2:
    start_date, end_date = date_range
    filtered_df = filtered_df[(filtered_df['date'] >= pd.to_datetime(start_date)) & 
                                (filtered_df['date'] <= pd.to_datetime(end_date))]

# Apply artist filter
if artist_search != "All":
    filtered_df = filtered_df[filtered_df['artist'] == artist_search]

# Apply album type filter
filtered_df = filtered_df[filtered_df['album_type'].isin(album_filter)]

st.write(f"**Showing data for {len(filtered_df):,} records** (filtered from {len(df):,} total)")
st.write(f"### Demo Example: Tracking '{song_name}'")
st.dataframe(song_df[['date', 'position', 'artist']])
st.markdown("---")
st.write("### Detecting Gaps (Re-Entries)")

song_df = song_df.sort_values('date').reset_index(drop=True)
song_df['days_gap'] = song_df['date'].diff().dt.days

st.dataframe(song_df[['date', 'position', 'days_gap']])
st.markdown("---")
st.write("### Where Re-Entries Happened")

re_entries = song_df[song_df['days_gap'] > 1]
st.dataframe(re_entries[['date', 'position', 'days_gap']])

st.write(f"**Total re-entries for '{song_name}':** {len(re_entries)}")
st.markdown("---")
st.write("### :rocket: Now Let's Do This For ALL Songs")

df_sorted = df.sort_values(['song', 'date']).reset_index(drop=True)

df_sorted['days_gap'] = df_sorted.groupby('song')['date'].diff().dt.days

all_re_entries = df_sorted[df_sorted['days_gap'] > 1]

st.write(f"**Total re-entry events across all songs:** {len(all_re_entries)}")
st.dataframe(all_re_entries[['date', 'song', 'artist', 'position', 'days_gap']])

st.markdown("---")
st.write("### :trophy: KPI 1 — Re-Entry Frequency")

re_entry_freq = all_re_entries.groupby(['song', 'artist']).size().reset_index(name='re_entry_count')

re_entry_freq = re_entry_freq.sort_values('re_entry_count', ascending=False)

st.write("**:fire: Top 10 Songs with Most Re-Entries**")
st.dataframe(re_entry_freq.head(10))

st.markdown("---")

col1, col2 = st.columns(2)
col1.metric(":repeat: Total Unique Songs with Re-Entries", re_entry_freq.shape[0])
col2.metric(":crown: Highest Re-Entry Count", re_entry_freq['re_entry_count'].max())
st.markdown("---")
st.write("### :zap: KPI 2 — Momentum Spike Score")

df_sorted['position_before'] = df_sorted.groupby('song')['position'].shift(1)

all_re_entries = df_sorted[df_sorted['days_gap'] > 1].copy()
all_re_entries['momentum_spike'] = all_re_entries['position_before'] - all_re_entries['position']

st.write("**:dizzy: Biggest Comeback Jumps (Highest Momentum Spikes)**")
top_momentum = all_re_entries.sort_values('momentum_spike', ascending=False)
st.dataframe(top_momentum[['date', 'song', 'artist', 'position_before', 'position', 'momentum_spike']].head(10))

st.markdown("---")
st.write("### :calendar: KPI 3 — Post-Comeback Retention Days")
df_sorted['new_streak'] = (df_sorted['days_gap'] > 1) | (df_sorted['days_gap'].isna())
df_sorted['streak_id'] = df_sorted.groupby('song')['new_streak'].cumsum()

retention = df_sorted.groupby(['song', 'artist', 'streak_id']).size().reset_index(name='retention_days')
retention_after_reentry = retention[retention['streak_id'] > 1]

st.write("**:hourglass: Longest Retention After Comeback**")
top_retention = retention_after_reentry.sort_values('retention_days', ascending=False)
st.dataframe(top_retention[['song', 'artist', 'retention_days']].head(10))

st.markdown("---")
st.write("### :rocket: KPI 4 — Rank Recovery Speed")

# For each comeback streak, find first position, best position, and days taken to reach best
streak_groups = df_sorted[df_sorted['streak_id'] > 1].groupby(['song', 'artist', 'streak_id'])

recovery_data = []
for (song, artist, streak_id), group in streak_groups:
    group = group.sort_values('date').reset_index(drop=True)
    first_position = group.loc[0, 'position']
    best_position = group['position'].min()
    days_to_best = group['position'].idxmin()    
    
    if days_to_best > 0:  
        recovery_speed = (first_position - best_position) / days_to_best
        recovery_data.append({
            'song': song,
            'artist': artist,
            'first_position': first_position,
            'best_position': best_position,
            'days_to_best': days_to_best,
            'recovery_speed': round(recovery_speed, 2)
        })

recovery_df = pd.DataFrame(recovery_data)

st.write("**:dash: Fastest Rank Recovery After Comeback**")
top_recovery = recovery_df.sort_values('recovery_speed', ascending=False)
st.dataframe(top_recovery.head(10))
st.markdown("---")
st.write("### :cd: KPI 5 — Album Comeback Advantage Index")

album_advantage = all_re_entries.groupby('album_type')['momentum_spike'].agg(['mean', 'median', 'count']).reset_index()
album_advantage.columns = ['album_type', 'avg_momentum_spike', 'median_momentum_spike', 'total_re_entries']
album_advantage[['avg_momentum_spike', 'median_momentum_spike']] = album_advantage[['avg_momentum_spike', 'median_momentum_spike']].round(2)
album_advantage = album_advantage.sort_values('avg_momentum_spike', ascending=False)

st.write("**:bar_chart: Comeback Strength by Release Type**")
st.dataframe(album_advantage)

st.info("Note: Most re-entries are small chart fluctuations (±1-2 positions). Average spike values near 0 reflect this — the big comebacks (20+) are rare standout events, not the norm.")

fig = px.bar(album_advantage, x='album_type', y='avg_momentum_spike', 
             color='album_type', title="Average Momentum Spike by Album Type")
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.write("### :crown: KPI 6 — Fandom Intensity Proxy Score")

# Step 1: Re-entry frequency per artist
freq_by_artist = all_re_entries.groupby('artist').size().reset_index(name='total_re_entries')

# Step 2: Average momentum spike per artist
spike_by_artist = all_re_entries.groupby('artist')['momentum_spike'].mean().reset_index(name='avg_momentum_spike')

# Step 3: Average retention days per artist (using our earlier retention_after_reentry table)
retention_by_artist = retention_after_reentry.groupby('artist')['retention_days'].mean().reset_index(name='avg_retention_days')

# Step 4: Merge all three into one table
fandom_score = freq_by_artist.merge(spike_by_artist, on='artist').merge(retention_by_artist, on='artist')

# Step 5: Normalize each metric to a 0-100 scale so they're comparable
for col in ['total_re_entries', 'avg_momentum_spike', 'avg_retention_days']:
    min_val = fandom_score[col].min()
    max_val = fandom_score[col].max()
    fandom_score[col + '_norm'] = ((fandom_score[col] - min_val) / (max_val - min_val)) * 100

# Step 6: Combine normalized scores into one Fandom Intensity Score (simple average)
fandom_score['fandom_intensity_score'] = (
    fandom_score['total_re_entries_norm'] + 
    fandom_score['avg_momentum_spike_norm'] + 
    fandom_score['avg_retention_days_norm']
) / 3
fandom_score['fandom_intensity_score'] = fandom_score['fandom_intensity_score'].round(1)

# Step 7: Show final leaderboard
fandom_leaderboard = fandom_score.sort_values('fandom_intensity_score', ascending=False)

st.write("**:trophy: Fandom Intensity Leaderboard (Top 10 Artists)**")
st.dataframe(fandom_leaderboard[['artist', 'total_re_entries', 'avg_momentum_spike', 
                                    'avg_retention_days', 'fandom_intensity_score']].head(10))

fig = px.bar(fandom_leaderboard.head(10), x='artist', y='fandom_intensity_score',
             color='fandom_intensity_score', title="Top 10 Fandom Intensity Leaderboard")
st.plotly_chart(fig, use_container_width=True)