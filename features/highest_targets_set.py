import streamlit as st
import pandas as pd

def highest_targets_set(matches):
    if st.button("Show Top 10", key="highest_targets"):
        def toss_winner(row):
            if row['toss_winner'] == row['team1']:
                return row['team1'] if row['toss_decision'] == 'bat' else row['team2']
            else:
                return row['team2'] if row['toss_decision'] == 'bat' else row['team1']

        df_copy = matches.copy()
        df_copy['batting_team'] = df_copy[['toss_decision', 'toss_winner', 'team1', 'team2']].apply(toss_winner, axis=1)
        df_copy['team_against'] = df_copy.apply(lambda row: row['team2'] if row['batting_team'] == row['team1'] else row['team1'], axis=1)
        df_copy = df_copy.sort_values(by="target_runs", ascending=False).reset_index().drop_duplicates()
        df_copy['target_runs'] = df_copy['target_runs'] - 1
        top_10 = df_copy[['batting_team', 'team_against', 'target_runs', 'date', 'venue', 'city', 'winner', 'result_margin']].head(10)

        st.dataframe(top_10.style.set_properties(**{'text-align': 'center'}))