This project is a Streamlit-based dashboard that allows users to explore and analyze the performance of basketball players over time. 
The dashboard displays various player stats, including points, rebounds, assists, steals, blocks, and shooting percentages, for both the Regular Season and Playoffs. Various people, like analysts, common fans, and even players, might take an interest in this page because it shows them different statistics. 


The different features I have implemented are: 
- Player Performance Over Time (Visualize a player's performance in a specific stat (e.g., PTS, REB, AST, etc.) over multiple years). You can choose between Regular Season and Playoffs, or view both at once.
- Detailed Player Stats (View all stats for a selected player for a specific year and season type (e.g., Regular Season or Playoffs)). Here you use a slider to select the year and a dropdown to select the season type.
- Player Comparison (Compare performance of multiple players across years in a selected stat (e.g., PTS, REB)). Here, you choose multiple players to compare and view their performance over time.
- Stat Distribution Histogram (Display the distribution of a specific stat (e.g., points or rebounds) across all players for the selected season type). This allows you to choose a stat and the season type to see the distribution.
- Player Stats Table (View a table displaying all available stats (e.g., FG_PCT, REB, PTS, etc.) over multiple years for a specific player). In this one, you can switch between players and view their stats over the years, including both Regular Season and Playoffs.


The data used in this project contains player statistics for several years, including the Regular Season and Playoffs. The dataset includes the following columns:
- PLAYER: Name of the player
- Year: The year of the season
- Season_type: Type of season (Regular Season or Playoffs)
- FG_PCT: Field goal percentage
- FG3_PCT: Three-point field goal percentage
- REB: Rebounds
- AST: Assists
- STL: Steals
- BLK: Blocks
- PTS: Points scored

The dataset has been cleaned and processed to ensure data accuracy and consistency. In locations where all of the columns for statitics for a certain player are 0, the player either didn't meet the required amount of games to have stats counted or didn't play at all. 
