import streamlit as st
import pandas as pd
import numpy as np

def player_vs_team_stats(merged_df, bowler_data, players, teams):
    col1, col2, col3 = st.columns(3)
    with col1:
        player1 = st.selectbox("Select Player 1", [""] + players, key="player1_vs_team")
    with col2:
        opponent_team = st.selectbox("Select Opponent Team", [""] + teams, key="opponent_team")
    with col3:
        player2 = st.selectbox("Select Player 2 (Optional)", ["None"] + players, key="player2_vs_team")
    
    if st.button("Analyze", key="player_vs_team"):
        if player1 == "" or opponent_team == "":
            st.error("Please select a player and an opponent team.")
        elif player1 == player2 and player2 != "None":
            st.error("Please select different players for comparison.")
        else:
            # Filter data for Player 1
            batting_df1 = merged_df[(merged_df['batter'] == player1) & (merged_df['bowling_team'] == opponent_team)]
            bowling_df1 = bowler_data[(bowler_data['bowler'] == player1) & (bowler_data['batting_team'] == opponent_team)]
            
            # Batting stats for Player 1
            batting_stats1 = batting_df1.groupby('season').agg(
                matches=('match_id', 'nunique'),
                runs=('batsman_runs', 'sum'),
                balls=('ball', lambda x: batting_df1.loc[x.index, 'extras_type'].ne('wides').sum()),
                dismissals=('is_wicket', 'sum'),
                fifties=('batsman_runs', lambda x: (batting_df1.loc[x.index].groupby('match_id')['batsman_runs'].sum() >= 50).sum()),
                centuries=('batsman_runs', lambda x: (batting_df1.loc[x.index].groupby('match_id')['batsman_runs'].sum() >= 100).sum()),
                highest_score=('batsman_runs', lambda x: batting_df1.loc[x.index].groupby('match_id')['batsman_runs'].sum().max())
            ).reset_index()
            batting_stats1['strike_rate'] = (batting_stats1['runs'] / batting_stats1['balls'] * 100).round(2)
            batting_stats1['average'] = (batting_stats1['runs'] / batting_stats1['dismissals']).round(2).replace([np.inf, -np.inf], 'N/A')
            
            # Bowling stats for Player 1
            bowling_stats1 = bowling_df1.groupby('season').agg(
                matches=('match_id', 'nunique'),
                wickets=('isBowlerWicket', 'sum'),
                runs_conceded=('bowler_run', 'sum'),
                balls=('ball', 'count'),
                three_wickets=('isBowlerWicket', lambda x: (bowling_df1.loc[x.index].groupby('match_id')['isBowlerWicket'].sum() >= 3).sum()),
                four_wickets=('isBowlerWicket', lambda x: (bowling_df1.loc[x.index].groupby('match_id')['isBowlerWicket'].sum() >= 4).sum()),
                five_wickets=('isBowlerWicket', lambda x: (bowling_df1.loc[x.index].groupby('match_id')['isBowlerWicket'].sum() >= 5).sum())
            ).reset_index()
            bowling_stats1['overs'] = (bowling_stats1['balls'] / 6).round(2)
            bowling_stats1['economy'] = (bowling_stats1['runs_conceded'] / bowling_stats1['overs']).round(2).replace([np.inf, -np.inf], 'N/A')
            bowling_stats1['bowling_average'] = (bowling_stats1['runs_conceded'] / bowling_stats1['wickets']).round(2).replace([np.inf, -np.inf], 'N/A')

            st.subheader(f"{player1} vs {opponent_team}")
            st.write("Batting Statistics")
            st.dataframe(batting_stats1.style.set_properties(**{'text-align': 'center'}))
            st.write("Bowling Statistics")
            st.dataframe(bowling_stats1.style.set_properties(**{'text-align': 'center'}))

            if player2 != "None":
                # Filter data for Player 2
                batting_df2 = merged_df[(merged_df['batter'] == player2) & (merged_df['bowling_team'] == opponent_team)]
                bowling_df2 = bowler_data[(bowler_data['bowler'] == player2) & (bowler_data['batting_team'] == opponent_team)]
                
                # Batting stats for Player 2
                batting_stats2 = batting_df2.groupby('season').agg(
                    matches=('match_id', 'nunique'),
                    runs=('batsman_runs', 'sum'),
                    balls=('ball', lambda x: batting_df2.loc[x.index, 'extras_type'].ne('wides').sum()),
                    dismissals=('is_wicket', 'sum'),
                    fifties=('batsman_runs', lambda x: (batting_df2.loc[x.index].groupby('match_id')['batsman_runs'].sum() >= 50).sum()),
                    centuries=('batsman_runs', lambda x: (batting_df2.loc[x.index].groupby('match_id')['batsman_runs'].sum() >= 100).sum()),
                    highest_score=('batsman_runs', lambda x: batting_df2.loc[x.index].groupby('match_id')['batsman_runs'].sum().max())
                ).reset_index()
                batting_stats2['strike_rate'] = (batting_stats2['runs'] / batting_stats2['balls'] * 100).round(2)
                batting_stats2['average'] = (batting_stats2['runs'] / batting_stats2['dismissals']).round(2).replace([np.inf, -np.inf], 'N/A')
                
                # Bowling stats for Player 2
                bowling_stats2 = bowling_df2.groupby('season').agg(
                    matches=('match_id', 'nunique'),
                    wickets=('isBowlerWicket', 'sum'),
                    runs_conceded=('bowler_run', 'sum'),
                    balls=('ball', 'count'),
                    three_wickets=('isBowlerWicket', lambda x: (bowling_df2.loc[x.index].groupby('match_id')['isBowlerWicket'].sum() >= 3).sum()),
                    four_wickets=('isBowlerWicket', lambda x: (bowling_df2.loc[x.index].groupby('match_id')['isBowlerWicket'].sum() >= 4).sum()),
                    five_wickets=('isBowlerWicket', lambda x: (bowling_df2.loc[x.index].groupby('match_id')['isBowlerWicket'].sum() >= 5).sum())
                ).reset_index()
                bowling_stats2['overs'] = (bowling_stats2['balls'] / 6).round(2)
                bowling_stats2['economy'] = (bowling_stats2['runs_conceded'] / bowling_stats2['overs']).round(2).replace([np.inf, -np.inf], 'N/A')
                bowling_stats2['bowling_average'] = (bowling_stats2['runs_conceded'] / bowling_stats2['wickets']).round(2).replace([np.inf, -np.inf], 'N/A')

                st.subheader(f"{player2} vs {opponent_team}")
                st.write("Batting Statistics")
                st.dataframe(batting_stats2.style.set_properties(**{'text-align': 'center'}))
                st.write("Bowling Statistics")
                st.dataframe(bowling_stats2.style.set_properties(**{'text-align': 'center'}))

                # Comparison
                st.subheader("Comparison")
                batting_avg1 = pd.to_numeric(batting_stats1['average'], errors='coerce')
                batting_avg2 = pd.to_numeric(batting_stats2['average'], errors='coerce')
                bowling_avg1 = pd.to_numeric(bowling_stats1['bowling_average'], errors='coerce')
                bowling_avg2 = pd.to_numeric(bowling_stats2['bowling_average'], errors='coerce')
                economy1 = pd.to_numeric(bowling_stats1['economy'], errors='coerce')
                economy2 = pd.to_numeric(bowling_stats2['economy'], errors='coerce')

                comparison_data = {
                    'Metric': ['Total Runs', 'Batting Average', 'Strike Rate', 'Total Wickets', 'Bowling Average', 'Economy'],
                    player1: [
                        batting_stats1['runs'].sum(),
                        round(batting_avg1.mean(), 2) if not batting_avg1.isna().all() else 'N/A',
                        round(batting_stats1['strike_rate'].mean(), 2) if not batting_stats1['strike_rate'].isna().all() else 'N/A',
                        bowling_stats1['wickets'].sum(),
                        round(bowling_avg1.mean(), 2) if not bowling_avg1.isna().all() else 'N/A',
                        round(economy1.mean(), 2) if not economy1.isna().all() else 'N/A'
                    ],
                    player2: [
                        batting_stats2['runs'].sum(),
                        round(batting_avg2.mean(), 2) if not batting_avg2.isna().all() else 'N/A',
                        round(batting_stats2['strike_rate'].mean(), 2) if not batting_stats2['strike_rate'].isna().all() else 'N/A',
                        bowling_stats2['wickets'].sum(),
                        round(bowling_avg2.mean(), 2) if not bowling_avg2.isna().all() else 'N/A',
                        round(economy2.mean(), 2) if not economy2.isna().all() else 'N/A'
                    ]
                }
                comparison_df = pd.DataFrame(comparison_data)
                comparison_df.set_index('Metric', inplace=True)
                st.dataframe(comparison_df.style.set_properties(**{'text-align': 'center'}))