import streamlit as st
import pandas as pd
import numpy as np

def live_match_prediction(matches, deliveries, teams, cities):
    # Helper function to create a mapping for categorical encoding
    def create_mapping(values):
        unique_values = sorted(list(set(values)))
        return {val: idx for idx, val in enumerate(unique_values)}

    # Helper function to calculate player form
    def calculate_player_form(team, deliveries, matches, n_matches=5):
        team_matches = matches[(matches['team1'] == team) | (matches['team2'] == team)].sort_values(by='date', ascending=False).head(n_matches)
        match_ids = team_matches['id'].values
        team_deliveries = deliveries[deliveries['match_id'].isin(match_ids)]

        # Batting form: Top 5 run-scorers
        batting_stats = team_deliveries[team_deliveries['batting_team'] == team].groupby('batter').agg(
            runs=('batsman_runs', 'sum'),
            balls=('ball', lambda x: team_deliveries.loc[x.index, 'extras_type'].ne('wides').sum())
        ).reset_index()
        batting_stats['strike_rate'] = (batting_stats['runs'] / batting_stats['balls'] * 100).replace([np.inf, -np.inf], 0)
        top_batsmen = batting_stats.sort_values(by='runs', ascending=False).head(5)
        avg_batting_form = top_batsmen['strike_rate'].mean() if not top_batsmen.empty else 0

        # Bowling form: Top 5 wicket-takers
        bowling_stats = team_deliveries[team_deliveries['bowling_team'] == team].groupby('bowler').agg(
            wickets=('is_wicket', 'sum'),
            runs_conceded=('total_runs', 'sum'),
            balls=('ball', 'count')
        ).reset_index()
        bowling_stats['economy'] = (bowling_stats['runs_conceded'] / (bowling_stats['balls'] / 6)).replace([np.inf, -np.inf], 0)
        top_bowlers = bowling_stats.sort_values(by='wickets', ascending=False).head(5)
        avg_bowling_form = top_bowlers['wickets'].sum() / n_matches if not top_bowlers.empty else 0

        return avg_batting_form, avg_bowling_form, top_batsmen, top_bowlers

    # Helper function to calculate recent team performance
    def calculate_team_form(team, matches, n_matches=5):
        team_matches = matches[(matches['team1'] == team) | (matches['team2'] == team)].sort_values(by='date', ascending=False).head(n_matches)
        wins = team_matches[team_matches['winner'] == team].shape[0]
        total_runs = team_matches.apply(
            lambda row: deliveries[(deliveries['match_id'] == row['id']) & (deliveries['batting_team'] == team)]['total_runs'].sum(), axis=1
        ).sum()
        total_wickets = team_matches.apply(
            lambda row: deliveries[(deliveries['match_id'] == row['id']) & (deliveries['bowling_team'] == team)]['is_wicket'].sum(), axis=1
        ).sum()
        win_rate = wins / n_matches if n_matches > 0 else 0
        avg_runs = total_runs / n_matches if n_matches > 0 else 0
        avg_wickets = total_wickets / n_matches if n_matches > 0 else 0
        return win_rate, avg_runs, avg_wickets

    # Prepare historical data for prediction
    @st.cache_data
    def prepare_training_data():
        match_data = matches.copy()
        match_data['team1'] = match_data['team1'].str.strip()
        match_data['team2'] = match_data['team2'].str.strip()
        match_data['winner'] = match_data['winner'].str.strip()
        match_data['city'] = match_data['city'].str.strip()

        # Create mappings for teams, cities, and weather
        all_teams = pd.concat([match_data['team1'], match_data['team2']]).unique()
        team_mapping = create_mapping(all_teams)
        city_mapping = create_mapping(match_data['city'].fillna('Unknown'))
        weather_conditions = ['Clear', 'Rainy', 'Humid']
        weather_mapping = create_mapping(weather_conditions)

        match_data['team1_encoded'] = match_data['team1'].map(team_mapping)
        match_data['team2_encoded'] = match_data['team2'].map(team_mapping)
        match_data['city_encoded'] = match_data['city'].fillna('Unknown').map(city_mapping)

        # Historical win rates and team form
        team_wins = {}
        team_forms = {}
        for team in all_teams:
            wins = match_data[match_data['winner'] == team].shape[0]
            total = match_data[(match_data['team1'] == team) | (match_data['team2'] == team)].shape[0]
            team_wins[team] = wins / total if total > 0 else 0.5  # Default to 0.5 if no matches
            win_rate, avg_runs, avg_wickets = calculate_team_form(team, match_data)
            team_forms[team] = (win_rate, avg_runs, avg_wickets)

        # Player form for each team
        player_forms = {}
        for team in all_teams:
            batting_form, bowling_form, _, _ = calculate_player_form(team, deliveries, match_data)
            player_forms[team] = (batting_form, bowling_form)

        # Simulate weather impact
        match_data['weather'] = np.random.choice(weather_conditions, size=len(match_data))
        match_data['weather_encoded'] = match_data['weather'].map(weather_mapping)

        return match_data, team_mapping, city_mapping, weather_mapping, team_wins, team_forms, player_forms

    # Custom probabilistic model
    def predict_probability(features, team_wins, team_forms, player_forms):
        team1, team2, city, run_rate, required_run_rate, wickets_remaining, weather = features
        team1_win_rate, team1_avg_runs, team1_avg_wickets = team_forms[team1]
        team2_win_rate, team2_avg_runs, team2_avg_wickets = team_forms[team2]
        team1_batting_form, team1_bowling_form = player_forms[team1]
        team2_batting_form, team2_bowling_form = player_forms[team2]

        # Normalize features to [0, 1] range
        def normalize(value, min_val, max_val):
            if max_val == min_val:
                return 0.5
            return (value - min_val) / (max_val - min_val)

        # Historical win rate contribution (weight: 0.3)
        hist_prob_team1 = team_wins.get(team1, 0.5)
        hist_prob_team2 = team_wins.get(team2, 0.5)
        hist_factor = hist_prob_team1 / (hist_prob_team1 + hist_prob_team2) if hist_prob_team1 + hist_prob_team2 > 0 else 0.5
        hist_contrib = hist_factor * 0.3

        # Recent team form contribution (weight: 0.2)
        form_factor = team1_win_rate / (team1_win_rate + team2_win_rate) if team1_win_rate + team2_win_rate > 0 else 0.5
        form_contrib = form_factor * 0.2

        # Player form contribution (weight: 0.2)
        batting_form_factor = normalize(team1_batting_form, min(team1_batting_form, team2_batting_form), max(team1_batting_form, team2_batting_form))
        bowling_form_factor = normalize(team1_bowling_form, min(team1_bowling_form, team2_bowling_form), max(team1_bowling_form, team2_bowling_form))
        player_form_contrib = (batting_form_factor * 0.5 + bowling_form_factor * 0.5) * 0.2

        # Match situation contribution (weight: 0.2)
        run_rate_factor = normalize(run_rate, 0, 10)  # Assuming max run rate ~10
        req_run_rate_factor = 1 - normalize(required_run_rate, 0, 15)  # Lower required run rate is better
        wickets_factor = normalize(wickets_remaining, 0, 10)
        match_situation_contrib = (run_rate_factor * 0.4 + req_run_rate_factor * 0.4 + wickets_factor * 0.2) * 0.2

        # Weather and home advantage contribution (weight: 0.1)
        home_advantage = 0.55 if city in matches[matches['team1'] == team1]['city'].values else 0.45
        weather_factor = 0.55 if weather == 'Rainy' else 0.5  # Rain favors batting team
        external_contrib = (home_advantage * 0.5 + weather_factor * 0.5) * 0.1

        # Combine contributions
        team1_prob = hist_contrib + form_contrib + player_form_contrib + match_situation_contrib + external_contrib
        team1_prob = max(0.0, min(1.0, team1_prob))  # Clamp to [0, 1]
        team2_prob = 1.0 - team1_prob

        return team1_prob, team2_prob

    # Load historical data
    match_data, team_mapping, city_mapping, weather_mapping, team_wins, team_forms, player_forms = prepare_training_data()
    if match_data.empty:
        st.error("No valid data available for prediction.")
        return

    # UI for match prediction
    st.subheader("Live Match Prediction")
    col1, col2 = st.columns(2)
    with col1:
        batting_team = st.selectbox("Select the batting team", [""] + teams, key="batting_team")
    with col2:
        bowling_team = st.selectbox("Select the bowling team", [""] + teams, key="bowling_team")

    col3, col4 = st.columns(2)
    with col3:
        host_city = st.selectbox("Select Host City", [""] + cities, key="host_city")
    with col4:
        weather = st.selectbox("Select Weather Condition", ["Clear", "Rainy", "Humid"], key="weather")

    col5, col6, col7 = st.columns(3)
    with col5:
        target = st.number_input("Target", min_value=0.0, value=151.0, step=1.0)
    with col6:
        score = st.number_input("Score", min_value=0.0, value=125.0, step=1.0)
    with col7:
        overs_completed = st.number_input("Overs Completed", min_value=0.0, max_value=20.0, value=16.0, step=0.1)

    wickets_out = st.number_input("Wickets Out", min_value=0, max_value=10, value=2, step=1)

    if st.button("Predict Probability", key="predict"):
        if batting_team == "" or bowling_team == "" or host_city == "":
            st.error("Please select batting team, bowling team, and host city.")
        elif batting_team == bowling_team:
            st.error("Batting and bowling teams must be different.")
        else:
            # Display player form and team form
            st.subheader("Team and Player Form")
            team1, team2 = batting_team, bowling_team
            team1_batting_form, team1_bowling_form, team1_top_batsmen, team1_top_bowlers = calculate_player_form(team1, deliveries, matches)
            team2_batting_form, team2_bowling_form, team2_top_batsmen, team2_top_bowlers = calculate_player_form(team2, deliveries, matches)
            team1_win_rate, team1_avg_runs, team1_avg_wickets = calculate_team_form(team1, matches)
            team2_win_rate, team2_avg_runs, team2_avg_wickets = calculate_team_form(team2, matches)

            st.write(f"**{team1} Recent Form**")
            st.write(f"Win Rate: {team1_win_rate:.2f}, Avg Runs: {team1_avg_runs:.0f}, Avg Wickets: {team1_avg_wickets:.1f}")
            st.write("Top Batsmen (Strike Rate):")
            st.dataframe(team1_top_batsmen.style.set_properties(**{'text-align': 'center'}))
            st.write("Top Bowlers (Wickets per Match):")
            st.dataframe(team1_top_bowlers.style.set_properties(**{'text-align': 'center'}))

            st.write(f"**{team2} Recent Form**")
            st.write(f"Win Rate: {team2_win_rate:.2f}, Avg Runs: {team2_avg_runs:.0f}, Avg Wickets: {team2_avg_wickets:.1f}")
            st.write("Top Batsmen (Strike Rate):")
            st.dataframe(team2_top_batsmen.style.set_properties(**{'text-align': 'center'}))
            st.write("Top Bowlers (Wickets per Match):")
            st.dataframe(team2_top_bowlers.style.set_properties(**{'text-align': 'center'}))

            # Prepare features for prediction
            run_rate = score / overs_completed if overs_completed > 0 else 0
            required_run_rate = (target - score) / (20 - overs_completed) if overs_completed < 20 else 0
            wickets_remaining = 10 - wickets_out
            weather_encoded = weather_mapping[weather]

            features = (
                team1,
                team2,
                host_city,
                run_rate,
                required_run_rate,
                wickets_remaining,
                weather
            )

            # Predict probability
            team1_prob, team2_prob = predict_probability(features, team_wins, team_forms, player_forms)

            # Adjust probabilities based on match situation
            if overs_completed >= 20 or wickets_out >= 10:
                if score >= target:
                    team1_prob, team2_prob = 1.0, 0.0
                else:
                    team1_prob, team2_prob = 0.0, 1.0
            # Adjust for weather
            if weather == "Rainy":
                team1_prob = min(1.0, team1_prob * 1.1)  # Slight boost to batting team
                team2_prob = max(0.0, 1.0 - team1_prob)

            st.subheader("Winning Probability")
            st.write(f"**{team1}**: {team1_prob * 100:.0f}%")
            st.write(f"**{team2}**: {team2_prob * 100:.0f}%")