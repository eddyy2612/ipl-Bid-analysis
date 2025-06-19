import streamlit as st
import pandas as pd
import numpy as np

def team_vs_team_growth(matches, teams, deliveries, seasons):
    col1, col2, col3 = st.columns(3)
    with col1:
        team1 = st.selectbox("Select Team 1", [""] + teams, key="team1")
    with col2:
        team2 = st.selectbox("Select Team 2", [""] + teams, key="team2")
    with col3:
        season = st.selectbox("Select Season (Optional)", ["All"] + [str(s) for s in seasons], key="season")

    if st.button("Analyze", key="team_vs_team"):
        if team1 == "" or team2 == "" or team1 == team2:
            st.error("Please select two different teams.")
        else:
            # Filter matches involving both teams
            df_filtered = matches[(matches['team1'].isin([team1, team2])) & (matches['team2'].isin([team1, team2]))]

            if season != "All":
                # Filter for the selected season
                df_filtered = df_filtered[df_filtered['season'].astype(str) == season]
                if df_filtered.empty:
                    st.error(f"No matches found between {team1} and {team2} in season {season}.")
                    return

                # Season-specific match summary
                st.subheader(f"Match Summary: {team1} vs {team2} in Season {season}")
                total_matches = df_filtered.shape[0]
                team1_wins = df_filtered[df_filtered['winner'] == team1].shape[0]
                team2_wins = df_filtered[df_filtered['winner'] == team2].shape[0]
                ties = df_filtered[df_filtered['result'] == 'tie'].shape[0]
                no_results = df_filtered[df_filtered['winner'].isna()].shape[0]

                summary_data = {
                    'Metric': ['Total Matches', f'{team1} Wins', f'{team2} Wins', 'Ties', 'No Results'],
                    'Value': [total_matches, team1_wins, team2_wins, ties, no_results]
                }
                summary_df = pd.DataFrame(summary_data).set_index('Metric')
                st.dataframe(summary_df.style.set_properties(**{'text-align': 'center'}))

                # Scorecards for each match in the season
                st.subheader(f"Match Scorecards: {team1} vs {team2} in Season {season}")
                for idx, match in df_filtered.iterrows():
                    match_id = match['id']
                    match_date = match['date']
                    venue = match['venue']
                    winner = match['winner'] if pd.notna(match['winner']) else "No Result"
                    result_margin = match['result_margin'] if pd.notna(match['result_margin']) else "-"
                    result = match['result'] if pd.notna(match['result']) else "No Result"

                    st.write(f"**Match ID: {match_id} | Date: {match_date} | Venue: {venue}**")
                    st.write(f"Result: {winner} won by {result_margin} {result}" if winner != "No Result" else "Result: No Result")

                    # Get deliveries for this match
                    match_deliveries = deliveries[deliveries['match_id'] == match_id]

                    # Process innings (assuming 1st and 2nd innings)
                    for inning in [1, 2]:
                        inning_data = match_deliveries[match_deliveries['inning'] == inning]
                        if inning_data.empty:
                            st.write(f"Innings {inning}: No data available")
                            continue

                        batting_team = inning_data['batting_team'].iloc[0]
                        total_runs = inning_data['total_runs'].sum()
                        wickets = inning_data['is_wicket'].sum()
                        balls = inning_data[inning_data['extras_type'].ne('wides')]['ball'].count()
                        overs = balls // 6 + (balls % 6) / 10

                        # Batsmen performance
                        batsmen_stats = inning_data.groupby('batter').agg(
                            runs=('batsman_runs', 'sum'),
                            balls=('ball', lambda x: inning_data.loc[x.index, 'extras_type'].ne('wides').sum())
                        ).reset_index()
                        batsmen_stats['strike_rate'] = (batsmen_stats['runs'] / batsmen_stats['balls'] * 100).round(2).replace([np.inf, -np.inf], 0)

                        # Bowlers performance
                        bowlers_stats = inning_data.groupby('bowler').agg(
                            runs_conceded=('total_runs', 'sum'),
                            wickets=('is_wicket', 'sum'),
                            balls=('ball', lambda x: inning_data.loc[x.index, 'extras_type'].ne('wides').sum())
                        ).reset_index()
                        bowlers_stats['overs'] = (bowlers_stats['balls'] // 6 + (bowlers_stats['balls'] % 6) / 10).round(2)
                        bowlers_stats['economy'] = (bowlers_stats['runs_conceded'] / (bowlers_stats['balls'] / 6)).round(2).replace([np.inf, -np.inf], 0)

                        st.write(f"**Innings {inning}: {batting_team} - {int(total_runs)}/{int(wickets)} ({overs:.1f} overs)**")
                        st.write("Batting Scorecard")
                        st.dataframe(batsmen_stats.style.set_properties(**{'text-align': 'center'}))
                        st.write("Bowling Scorecard")
                        st.dataframe(bowlers_stats.style.set_properties(**{'text-align': 'center'}))

            else:
                # Original behavior: Show wins across all seasons
                df_team1 = df_filtered[df_filtered['winner'] == team1].groupby('season', as_index=False).size()
                df_team2 = df_filtered[df_filtered['winner'] == team2].groupby('season', as_index=False).size()
                df_team1.rename(columns={'size': f'{team1}_wins'}, inplace=True)
                df_team2.rename(columns={'size': f'{team2}_wins'}, inplace=True)
                df_merged = pd.merge(df_team1, df_team2, on='season', how='outer').fillna(0)
                df_merged.set_index('season', inplace=True)

                st.subheader(f"{team1} Wins")
                st.line_chart(df_merged[[f'{team1}_wins']])

                st.subheader(f"{team2} Wins")
                st.line_chart(df_merged[[f'{team2}_wins']])

                st.subheader("Combined Data")
                st.dataframe(df_merged.style.set_properties(**{'text-align': 'center'}))