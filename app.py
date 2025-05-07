
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load data
@st.cache_data
def load_data():
    url = 'https://raw.githubusercontent.com/MWisKid/DATA-315/refs/heads/main/updated_player_stats.csv'
    return pd.read_csv(url)

df = load_data()

# Streamlit Title
st.title("Basketball Player Performance Dashboard")

# Add explanatory text
st.markdown("""
### Overview of Player Performance
This dashboard allows you to explore the performance of basketball players over time. You can filter the data by season type (regular season or playoffs), player, and stat. Interactive features such as sliders and dropdowns allow you to customize your analysis.

Below, you will find various visualizations to compare and analyze different player stats.
""")

# Define player options globally
player_options = df['PLAYER'].unique()

# Tab navigation
tab = st.radio("Select a Tab", ["Overview", "Player Performance Over Time", "Individual Player Stats by Year", "Player Comparison", "Stat Distribution", "Player Stats Table"])

if tab == "Overview":
    st.markdown("""
    ### Introduction
    This dashboard provides insights into basketball player performances across different seasons. 
    - You can explore individual player performance over time.
    - Compare stats between players.
    - Analyze the distribution of stats.
    - View detailed stats for a specific year and season.
    """)

elif tab == "Player Performance Over Time":
    # Stat selection inside the tab
    selected_stat = st.selectbox("Select Stat", ['PTS', 'REB', 'AST', 'STL', 'BLK', 'FG_PCT', 'FG3_PCT'], key="stat_selectbox_performance")

    # Dropdown to select player
    selected_player = st.selectbox("Select Player", player_options, key="player_selectbox")

    # Filter data for selected player
    df_player = df[df['PLAYER'] == selected_player]

    # Dropdown for season type selection
    season_type = st.selectbox("Select Season Type", ['Both', 'Regular%20Season', 'Playoffs'], key="season_type_selectbox")

    # Filter data based on season type
    if season_type != 'Both':
        df_player = df_player[df_player['Season_type'] == season_type]

    # Line chart for player performance over time
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

elif tab == "Individual Player Stats by Year":
    # Dropdown to select player (this was missing in the previous version)
    selected_player = st.selectbox("Select Player", player_options, key="player_stats_year_selectbox")

    # Dropdown to select year and season type for detailed stats
    year_options = df['Year'].unique()
    selected_year = st.slider("Select Year", int(year_options.min()), int(year_options.max()), int(year_options.max()), key="year_slider")
    selected_season_type = st.selectbox("Select Season Type", ['Regular%20Season', 'Playoffs'], key="season_type_selectbox_2")

    # Filter data based on selected player, year, and season type
    df_selected = df[(df['PLAYER'] == selected_player) &
                     (df['Year'] == selected_year) &
                     (df['Season_type'] == selected_season_type)]

    # Display the stats for the selected player, year, and season type
    if not df_selected.empty:
        st.subheader(f"Stats for {selected_player} in {selected_year} ({selected_season_type})")
        st.write(df_selected[['PLAYER', 'Year', 'Season_type', 'FG_PCT', 'FG3_PCT', 'REB', 'AST', 'STL', 'BLK', 'PTS']])
    else:
        st.write("No data available for this selection.")

elif tab == "Player Comparison":
    # Stat selection inside the tab
    selected_stat = st.selectbox("Select Stat", ['PTS', 'REB', 'AST', 'STL', 'BLK', 'FG_PCT', 'FG3_PCT'], key="stat_selectbox_comparison")

    # Dropdown for selecting multiple players to compare
    selected_players = st.multiselect("Select Players to Compare", options=df['PLAYER'].unique(), default=df['PLAYER'].unique()[:2], key="players_comparison_multiselect")
    selected_season_type_comparison = st.selectbox("Select Season Type for Comparison", ['Regular%20Season', 'Playoffs'], key="season_type_comparison_selectbox")

    # Filter the data based on the selected players and season type
    df_comparison = df[df['PLAYER'].isin(selected_players) & (df['Season_type'] == selected_season_type_comparison)]

    # Line chart comparing stats for multiple players
    st.subheader(f"Comparison of {', '.join(selected_players)} Over Time ({selected_season_type_comparison})")
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

elif tab == "Stat Distribution":
    # Stat selection inside the tab
    selected_stat = st.selectbox("Select Stat", ['PTS', 'REB', 'AST', 'STL', 'BLK', 'FG_PCT', 'FG3_PCT'], key="stat_selectbox_histogram")

    # Dropdown for selecting the stat to visualize in histogram
    stat_histogram = selected_stat
    season_type_histogram = st.selectbox("Select Season Type for Histogram", ['Regular%20Season', 'Playoffs'], key="season_type_histogram_selectbox")

    # Filter data based on selected season type
    df_histogram = df[df['Season_type'] == season_type_histogram]

    # Ensure the selected stat is numeric and fill NaN with 0
    df_histogram[stat_histogram] = pd.to_numeric(df_histogram[stat_histogram], errors='coerce')
    df_histogram = df_histogram[df_histogram[stat_histogram] != 0]  # Exclude rows where stat is 0

    # Plot the histogram for the selected stat
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(df_histogram[stat_histogram], bins=20, color='skyblue', edgecolor='black')

    # Add labels and title
    ax.set_xlabel(stat_histogram)
    ax.set_ylabel('Frequency')
    ax.set_title(f'Distribution of {stat_histogram} in {season_type_histogram}')
    st.pyplot(fig)

elif tab == "Player Stats Table":
    # Dropdown to select player
    selected_player_table = st.selectbox("Select Player", player_options, key="player_table_selectbox")

    # Filter data for the selected player
    df_player_table = df[df['PLAYER'] == selected_player_table]

    # Show stats for the selected player over all years and both seasons
    st.write(f"**Stats for {selected_player_table} Over Time (Including Playoffs and Regular Season)**")
    st.write(df_player_table[['PLAYER', 'Year', 'Season_type', 'FG_PCT', 'FG3_PCT', 'REB', 'AST', 'STL', 'BLK', 'PTS']])
