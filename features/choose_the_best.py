def choose_the_best(matches, deliveries, players, seasons):
    import streamlit as st
    
    # Define team name mappings
    team_mappings = {
        'Delhi Capitals': 'Delhi Capitals/Delhi Daredevils',
        'Delhi Daredevils': 'Delhi Capitals/Delhi Daredevils',
        'Royal Challengers Bangalore': 'Royal Challengers Bangalore/Bengaluru',
        'Royal Challengers Bengaluru': 'Royal Challengers Bangalore/Bengaluru',
        'Punjab Kings': 'Punjab Kings/Kings XI Punjab',
        'Kings XI Punjab': 'Punjab Kings/Kings XI Punjab',
        'Rising Pune Supergiant': 'Rising Pune Supergiant/Supergiants',
        'Rising Pune Supergiants': 'Rising Pune Supergiant/Supergiants'
    }
    
    # Apply team name mappings to deliveries
    deliveries_with_seasons = deliveries.copy()
    deliveries_with_seasons['batting_team'] = deliveries_with_seasons['batting_team'].replace(team_mappings)
    deliveries_with_seasons['bowling_team'] = deliveries_with_seasons['bowling_team'].replace(team_mappings)
    
    # Apply team name mappings to matches
    matches_with_seasons = matches.copy()
    matches_with_seasons['team1'] = matches_with_seasons['team1'].replace(team_mappings)
    matches_with_seasons['team2'] = matches_with_seasons['team2'].replace(team_mappings)
    matches_with_seasons['toss_winner'] = matches_with_seasons['toss_winner'].replace(team_mappings)
    matches_with_seasons['winner'] = matches_with_seasons['winner'].replace(team_mappings)
    
    # Merge deliveries with matches to get season information
    deliveries_with_seasons = deliveries_with_seasons.merge(matches_with_seasons[['id', 'season']], left_on='match_id', right_on='id', how='left')
    
    st.subheader("Choose the Best Batsman")
    
    # Select first batsman and up to 5 opponent bowlers
    batsman1 = st.selectbox("Select 1st Batsman", [""] + players, key="batsman1")
    bowler_options1 = st.multiselect("Select 5 Opponent Bowlers", players, max_selections=5, key="bowlers1")
    
    # Select second batsman and up to 5 opponent bowlers
    batsman2 = st.selectbox("Select 2nd Batsman", [""] + players, key="batsman2")
    bowler_options2 = st.multiselect("Select 5 Opponent Bowlers", players, max_selections=5, key="bowlers2")
    
    if st.button("Analyze", key="choose_best"):
        if not batsman1 or not batsman2 or (batsman1 == batsman2) or (not bowler_options1 and not bowler_options2):
            st.error("Please select two different batsmen and at least one bowler for each.")
        else:
            # Analysis for Batsman 1
            st.write("### Analysis for", batsman1)
            for bowler in bowler_options1:
                bowler_data = deliveries_with_seasons[
                    (deliveries_with_seasons['batter'] == batsman1) & 
                    (deliveries_with_seasons['bowler'] == bowler)
                ]
                if not bowler_data.empty:
                    st.write(f"#### Bowler: {bowler}")  # Display bowler name above table
                    season_stats = bowler_data.groupby('season').agg({
                        'batsman_runs': [  # Multi-aggregation for runs, sixes, and fours
                            ('total_runs', 'sum'),  # Total runs scored
                            ('sixes', lambda x: (x == 6).sum()),
                            ('fours', lambda x: (x == 4).sum())
                        ],
                        'is_wicket': lambda x: (x.notna() & (x != 0)).sum(),  # Times Dismissed
                        'batter': lambda x: (x == batsman1).sum()  # Balls Faced
                    }).reset_index()
                    # Flatten multi-level columns
                    season_stats.columns = [''.join(col).strip() if isinstance(col, tuple) else col for col in season_stats.columns]
                    # Rename columns
                    season_stats = season_stats.rename(columns={
                        'season': 'Season',
                        'batsman_runstotal_runs': 'Runs Scored',
                        'is_wickett': 'Times Dismissed',
                        'batter<lambda>': 'Balls Faced',
                        'batsman_runnssixes': 'Sixes Hit',
                        'batsman_runsfours': 'Fours Hit'
                    })
                    # Ensure all 6 columns exist
                    for col in ['Runs Scored', 'Times Dismissed', 'Balls Faced', 'Sixes Hit', 'Fours Hit']:
                        if col not in season_stats.columns:
                            season_stats[col] = 0
                    st.dataframe(season_stats.style.set_properties(**{
                        'text-align': 'center',
                        'border': '2px solid #444',
                        'background-color': '#2e2e2e',
                        'color': '#ffffff'
                    }).set_table_styles([
                        {'selector': 'th', 'props': [('background-color', '#333'), ('color', '#fff'), ('border', '2px solid #444')]},
                        {'selector': 'td:hover', 'props': [('background-color', '#555'), ('color', '#fff')]}
                    ]))
            
            # Analysis for Batsman 2
            st.write("### Analysis for", batsman2)
            for bowler in bowler_options2:
                bowler_data = deliveries_with_seasons[
                    (deliveries_with_seasons['batter'] == batsman2) & 
                    (deliveries_with_seasons['bowler'] == bowler)
                ]
                if not bowler_data.empty:
                    st.write(f"#### Bowler: {bowler}")  # Display bowler name above table
                    season_stats = bowler_data.groupby('season').agg({
                        'batsman_runs': [  # Multi-aggregation for runs, sixes, and fours
                            ('total_runs', 'sum'),  # Total runs scored
                            ('sixes', lambda x: (x == 6).sum()),
                            ('fours', lambda x: (x == 4).sum())
                        ],
                        'is_wicket': lambda x: (x.notna() & (x != 0)).sum(),  # Times Dismissed
                        'batter': lambda x: (x == batsman2).sum()  # Balls Faced
                    }).reset_index()
                    # Flatten multi-level columns
                    season_stats.columns = [''.join(col).strip() if isinstance(col, tuple) else col for col in season_stats.columns]
                    # Rename columns
                    season_stats = season_stats.rename(columns={
                        'season': 'Season',
                        'batsman_runstotal_runs': 'Runs Scored',
                        'is_wickett': 'Times Dismissed',
                        'batter<lambda>': 'Balls Faced',
                        'batsman_runnssixes': 'Sixes Hit',
                        'batsman_runsfours': 'Fours Hit'
                    })
                    # Ensure all 6 columns exist
                    for col in ['Runs Scored', 'Times Dismissed', 'Balls Faced', 'Sixes Hit', 'Fours Hit']:
                        if col not in season_stats.columns:
                            season_stats[col] = 0
                    st.dataframe(season_stats.style.set_properties(**{
                        'text-align': 'center',
                        'border': '2px solid #444',
                        'background-color': '#2e2e2e',
                        'color': '#ffffff'
                    }).set_table_styles([
                        {'selector': 'th', 'props': [('background-color', '#333'), ('color', '#fff'), ('border', '2px solid #444')]},
                        {'selector': 'td:hover', 'props': [('background-color', '#555'), ('color', '#fff')]}
                    ]))
            
            # Prediction Logic
            def calculate_performance_score(batsman_data, bowler_options):
                if batsman_data.empty:
                    return 0  # Return 0 if no data to avoid IndexError
                total_runs = batsman_data['batsman_runs'].sum()
                total_dismissals = batsman_data['is_wicket'].sum() if 'is_wicket' in batsman_data else 0  # Fallback
                total_sixes = (batsman_data['batsman_runs'] == 6).sum()
                total_fours = (batsman_data['batsman_runs'] == 4).sum()
                balls_faced = (batsman_data['batter'] == batsman_data['batter'].iloc[0]).sum()
                if balls_faced > 0:
                    strike_rate = (total_runs / balls_faced) * 100
                else:
                    strike_rate = 0
                return (total_runs * 1.5 + strike_rate + total_sixes * 10 + total_fours * 5) / (total_dismissals + 1)

            # Calculate scores for both batsmen
            batsman1_data = deliveries_with_seasons[
                (deliveries_with_seasons['batter'] == batsman1) & 
                (deliveries_with_seasons['bowler'].isin(bowler_options1))
            ]
            batsman2_data = deliveries_with_seasons[
                (deliveries_with_seasons['batter'] == batsman2) & 
                (deliveries_with_seasons['bowler'].isin(bowler_options2))
            ]
            
            score1 = calculate_performance_score(batsman1_data, bowler_options1)
            score2 = calculate_performance_score(batsman2_data, bowler_options2)
            
            st.write("### Prediction")
            if batsman1_data.empty or batsman2_data.empty:
                st.info("Cannot do analysis as player might not have faced a particular bowler.")
            elif score1 > score2:
                st.success(f"{batsman1} is better to pick for the team against the selected bowlers with a performance score of {score1:.2f} vs {batsman2}'s {score2:.2f}.")
            elif score2 > score1:
                st.success(f"{batsman2} is better to pick for the team against the selected bowlers with a performance score of {score2:.2f} vs {batsman1}'s {score1:.2f}.")
            elif score1 == score2:
                st.info(f"Both {batsman1} and {batsman2} have similar performance scores ({score1:.2f}), making them equally viable choices.")