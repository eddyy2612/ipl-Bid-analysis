import streamlit as st
import pandas as pd

def overall_team_performance(matches, teams):
    if st.button("Show Performance", key="overall_team_performance"):
        team_stats = pd.DataFrame()
        for team in teams:
            matches_played = matches[(matches['team1'] == team) | (matches['team2'] == team)].shape[0]
            wins = matches[matches['winner'] == team].shape[0]
            losses = matches_played - wins - matches[(matches['result'] == 'tie') & ((matches['team1'] == team) | (matches['team2'] == team))].shape[0] - matches[(matches['winner'].isna()) & ((matches['team1'] == team) | (matches['team2'] == team))].shape[0]
            ties = matches[(matches['result'] == 'tie') & ((matches['team1'] == team) | (matches['team2'] == team))].shape[0]
            no_results = matches[(matches['winner'].isna()) & ((matches['team1'] == team) | (matches['team2'] == team))].shape[0]
            
            team_data = {
                'Team': team,
                'Matches Played': matches_played,
                'Wins': wins,
                'Losses': losses,
                'Ties': ties,
                'No Results': no_results,
                'Win Percentage': round((wins / matches_played * 100), 2) if matches_played > 0 else 0
            }
            team_stats = pd.concat([team_stats, pd.DataFrame([team_data])], ignore_index=True)
        
        team_stats.set_index('Team', inplace=True)
        st.subheader("Overall Team Performance Across All Seasons")
        st.dataframe(team_stats.style.set_properties(**{'text-align': 'center'}))