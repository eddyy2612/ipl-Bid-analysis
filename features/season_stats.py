import streamlit as st
import pandas as pd
from utils import get_batsman_statistics, get_bowler_statistics

def season_stats(merged_df, bowler_data, matches, teams, players, seasons):
    col1, col2, col3 = st.columns(3)
    with col1:
        year = st.selectbox("Select Season", [""] + [str(s) for s in seasons], key="season")
    with col2:
        team_name = st.selectbox("Select Team (Optional)", ["None"] + teams, key="team_name")
    with col3:
        player_name = st.selectbox("Select Player (Optional)", ["None"] + players, key="player_name")
    
    if st.button("Analyze", key="season_stats"):
        if year == "":
            st.error("Please select a season.")
        else:
            season_year = year
            season_df = merged_df[merged_df['season'].astype(str) == season_year]
            season_bowling_df = bowler_data[bowler_data['season'].astype(str) == season_year]

            if team_name != "None":
                season_df = season_df[(season_df['batting_team'] == team_name) | (season_df['bowling_team'] == team_name)]
                season_bowling_df = season_bowling_df[season_bowling_df['bowling_team'] == team_name]
            if player_name != "None":
                season_df = season_df[season_df['batter'] == player_name]
                season_bowling_df = season_bowling_df[season_bowling_df['bowler'] == player_name]

            if season_df.empty and season_bowling_df.empty:
                st.error("No data available for the given filters.")
            else:
                team_performance = pd.DataFrame()
                if player_name == "None":
                    team_performance = season_df.groupby('batting_team').agg(
                        matches=('match_id', 'nunique'),
                        total_runs=('total_runs', 'sum'),
                        total_wickets=('is_wicket', 'sum')
                    ).reset_index()

                top_batsmen = season_df.groupby('batter').agg(runs=('batsman_runs', 'sum')).reset_index()
                top_batsman_name = top_batsmen.sort_values(by='runs', ascending=False).iloc[0]['batter'] if not top_batsmen.empty else None
                top_bowlers = season_bowling_df.groupby('bowler').agg(wickets=('isBowlerWicket', 'sum')).reset_index()
                top_bowler_name = top_bowlers.sort_values(by='wickets', ascending=False).iloc[0]['bowler'] if not top_bowlers.empty else None

                top_batsman_stats = get_batsman_statistics(top_batsman_name, season_df, matches) if top_batsman_name else {}
                top_bowler_stats = get_bowler_statistics(top_bowler_name, season_bowling_df, matches) if top_bowler_name else {}

                st.subheader("Team Performance")
                if not team_performance.empty:
                    st.dataframe(team_performance.style.set_properties(**{'text-align': 'center'}))
                else:
                    st.write("No team performance data (player-specific filter applied or no data available).")

                st.subheader("Top Batsman")
                if top_batsman_stats:
                    st.dataframe(pd.DataFrame([top_batsman_stats]).style.set_properties(**{'text-align': 'center'}))
                else:
                    st.write("No batsman data available.")

                st.subheader("Top Bowler")
                if top_bowler_stats:
                    st.dataframe(pd.DataFrame([top_bowler_stats]).style.set_properties(**{'text-align': 'center'}))
                else:
                    st.write("No bowler data available.")