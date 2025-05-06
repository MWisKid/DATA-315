
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the data (ensure the path is correct)
@st.cache_data
def load_data():
    return pd.read_csv('/content/updated_player_stats.csv')

df = load_data()

# Streamlit Title
st.title("Basketball Player Performance Dashboard")

# Add explanatory text
st.markdown("""
### Overview of Player Performance
This dashboard allows you to explore the performance of basketball players over time. You can filter the data by season type (regular season or playoffs), player, and stat. Interactive features such as sliders and dropdowns allow you to customize your analysis.

Below, you will find various visualizations to compare and analyze different player stats.
""")

# 1. Player Performance Over Time with Stat Selection
# Dropdown to select player
player_options = df['PLAYER'].unique()
selected_player = st.selectbox("Select Player", player_options, key="player_selectbox")

# Filter data for selected player
df_player = df[df['PLAYER'] == selected_player]

# Dropdown for season type selection (add unique key)
season_type = st.selectbox("Select Season Type", ['Both', 'Regular%20Season', 'Playoffs'], key="season_type_selectbox")

# Dropdown for stat selection (add unique key)
stat_options = ['PTS', 'REB', 'AST', 'STL', 'BLK', 'FG_PCT', 'FG3_PCT']
selected_stat = st.selectbox("Select Stat", stat_options, key="stat_selectbox")

# Filter data based on season type
if season_type != 'Both':
    df_player = df_player[df_player['Season_type'] == season_type]

# Line chart for player performance over time (selected stat)
st.subheader(f"{selected_player}'s {selected_stat} Over Time")
fig, ax = plt.subplots(figsize=(10, 6))
for season in df_player['Season_type'].unique():
    season_data = df_player[df_player['Season_type'] == season]
    ax.plot(season_data['Year'], season_data[selected_stat], marker='o', label=season)

ax.set_xlabel('Year')
ax.set_ylabel(selected_stat)
ax.set_title(f"{selected_player}'s {selected_stat} Over Time")
ax.legend(title='Season Type')
ax.grid(True)
st.pyplot(fig)

# 2. Player Stats for a Specific Year and Season Type (with year slider)
# Dropdown to select year and season type for detailed stats
year_options = df['Year'].unique()
selected_year = st.slider("Select Year", int(year_options.min()), int(year_options.max()), int(year_options.max()), key="year_slider")

# Dropdown for season type (add unique key)
selected_season_type = st.selectbox("Select Season Type", ['Regular%20Season', 'Playoffs'], key="season_type_selectbox_2")

# Filter data based on selected year and season type
df_selected = df[(df['PLAYER'] == selected_player) &
                 (df['Year'] == selected_year) &
                 (df['Season_type'] == selected_season_type)]

# Display the stats for the selected player, year, and season type
if not df_selected.empty:
    st.subheader(f"Stats for {selected_player} in {selected_year} ({selected_season_type})")
    st.write(df_selected[['PLAYER', 'Year', 'Season_type', 'FG_PCT', 'FG3_PCT', 'REB', 'AST', 'STL', 'BLK', 'PTS']])
else:
    st.write("No data available for this selection.")

# 4. Player Comparison (Compare multiple players)
# Dropdown for selecting multiple players to compare (add unique key)
selected_players = st.multiselect("Select Players to Compare", options=df['PLAYER'].unique(), default=df['PLAYER'].unique()[:2], key="players_comparison_multiselect")

# Filter the data based on the selected players
df_comparison = df[df['PLAYER'].isin(selected_players)]

# Line chart comparing stats for multiple players
st.subheader(f"Comparison of {', '.join(selected_players)} Over Time")
fig, ax = plt.subplots(figsize=(10, 6))
for player in selected_players:
    player_data = df_comparison[df_comparison['PLAYER'] == player]
    ax.plot(player_data['Year'], player_data[selected_stat], label=player)

ax.set_xlabel('Year')
ax.set_ylabel(selected_stat)
ax.set_title(f"Comparison of {selected_stat} Over Time")
ax.legend(title='Player')
ax.grid(True)
st.pyplot(fig)
