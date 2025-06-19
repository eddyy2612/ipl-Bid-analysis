import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    matches = pd.read_csv('./data/matches.csv')
    deliveries = pd.read_csv('./data/deliveries.csv')
    # Merge datasets for season information
    merged_df = deliveries.merge(matches[['id', 'season', 'team1', 'team2', 'winner']], left_on='match_id', right_on='id', how='left')
    merged_df['batting_team'] = merged_df.apply(lambda x: x['team1'] if x['batting_team'] == x['team1'] else x['team2'], axis=1)
    merged_df['bowling_team'] = merged_df.apply(lambda x: x['team2'] if x['batting_team'] == x['team1'] else x['team1'], axis=1)
    # Bowler data
    bowler_data = deliveries.merge(matches[['id', 'season']], left_on='match_id', right_on='id', how='left')
    bowler_data['isBowlerWicket'] = bowler_data['is_wicket'].where(bowler_data['dismissal_kind'].isin(['caught', 'bowled', 'lbw', 'stumped', 'caught and bowled', 'hit wicket']), 0)
    # Calculate bowler runs (exclude legbyes from total_runs)
    bowler_data['bowler_run'] = bowler_data['total_runs'] - bowler_data['extra_runs'].where(bowler_data['extras_type'] == 'legbyes', 0)
    # Extract teams, players, seasons
    teams = sorted(matches['team1'].unique())
    players = sorted(deliveries['batter'].unique())  # Includes bowlers
    seasons = sorted(matches['season'].unique())
    return matches, deliveries, merged_df, bowler_data, teams, players, seasons