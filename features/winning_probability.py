import streamlit as st
import pandas as pd
import numpy as np

def winning_probability(matches, teams):
    col1, col2 = st.columns(2)
    with col1:
        team1 = st.selectbox("Select Team 1", [""] + teams, key="team1_win")
    with col2:
        team2 = st.selectbox("Select Team 2", [""] + teams, key="team2_win")
    
    if st.button("Analyze", key="winning_probability"):
        if team1 == "" or team2 == "" or team1 == team2:
            st.error("Please select two different teams.")
        else:
            head_to_head_matches = matches[((matches['team1'] == team1) & (matches['team2'] == team2)) | ((matches['team1'] == team2) & (matches['team2'] == team1))]
            total_matches = head_to_head_matches.shape[0]

            if total_matches == 0:
                st.error("No head-to-head matches found between the selected teams.")
            else:
                team1_wins = head_to_head_matches[head_to_head_matches['winner'] == team1].shape[0]
                team2_wins = head_to_head_matches[head_to_head_matches['winner'] == team2].shape[0]
                no_results = head_to_head_matches[head_to_head_matches['winner'].isna()].shape[0]
                tied_matches = head_to_head_matches[head_to_head_matches['result'] == 'tie'].shape[0]

                team1_win_pct = (team1_wins / total_matches) * 100 if total_matches > 0 else 0
                team2_win_pct = (team2_wins / total_matches) * 100 if total_matches > 0 else 0
                tied_pct = (tied_matches / total_matches) * 100 if total_matches > 0 else 0
                no_result_pct = (no_results / total_matches) * 100 if total_matches > 0 else 0

                team1_scores = []
                team2_scores = []
                for _, match in head_to_head_matches.iterrows():
                    if match['team1'] == team1:
                        if pd.notna(match['target_runs']):
                            team1_scores.append(match['target_runs'] - 1)
                    else:
                        if pd.notna(match['target_runs']):
                            team2_scores.append(match['target_runs'] - 1)
                    if match['team2'] == team1:
                        if pd.notna(match['result_margin']) and match['result'] == 'runs':
                            team1_scores.append(match['result_margin'])
                    else:
                        if pd.notna(match['result_margin']) and match['result'] == 'runs':
                            team2_scores.append(match['result_margin'])

                team1_highest_score = max(team1_scores) if team1_scores else 0
                team2_highest_score = max(team2_scores) if team2_scores else 0

                head_to_head_data = {
                    '': ['Matches Played', f'{team1} Result on', f'{team2} Result on', 'Tied', 'No Result', 'Highest Score'],
                    team1: [
                        total_matches,
                        f'{team1_win_pct:.0f}% Won',
                        f'{team2_win_pct:.0f}% Lost',
                        f'{tied_pct:.0f}%',
                        f'{no_result_pct:.0f}%',
                        team1_highest_score
                    ],
                    team2: [
                        total_matches,
                        f'{team2_win_pct:.0f}% Won',
                        f'{team1_win_pct:.0f}% Lost',
                        f'{tied_pct:.0f}%',
                        f'{no_result_pct:.0f}%',
                        team2_highest_score
                    ]
                }
                head_to_head_df = pd.DataFrame(head_to_head_data)
                head_to_head_df.set_index('', inplace=True)

                st.subheader("Head-to-Head Analysis")
                st.dataframe(head_to_head_df.style.set_properties(**{'text-align': 'center'}))

                recent_matches_team1 = matches[(matches['team1'] == team1) | (matches['team2'] == team1)].tail(5)
                recent_wins_team1 = recent_matches_team1[recent_matches_team1['winner'] == team1].shape[0]
                recent_form_win_rate_team1 = (recent_wins_team1 / 5) * 100 if not recent_matches_team1.empty else 50
                
                head_to_head_win_rate = (team1_wins / total_matches) * 100 if total_matches > 0 else 50
                final_win_probability = (0.7 * head_to_head_win_rate) + (0.3 * recent_form_win_rate_team1)

                result = pd.DataFrame([{team1: round(final_win_probability, 2), team2: round(100 - final_win_probability, 2)}])
                st.subheader("Winning Probability (On Team 1 HomeGround)")
                st.dataframe(result.style.set_properties(**{'text-align': 'center'}))