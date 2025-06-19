import streamlit as st
import pandas as pd

def batsman_vs_bowler_stats(matches, deliveries, players, teams, venues, seasons):
    st.subheader("Batsman vs Bowler Stats")
    col1, col2, col3 = st.columns(3)
    with col1:
        batsman = st.selectbox("Select Batsman", [""] + players, key="batsman")
    with col2:
        bowler = st.selectbox("Select Bowler", [""] + players, key="bowler")
    with col3:
        season = st.selectbox("Select Season", ["All"] + [str(s) for s in seasons], key="season")

    if st.button("Analyze", key="batsman_bowler"):
        if not batsman or not bowler or (batsman == bowler):
            st.error("Please select different batsman and bowler.")
        else:
            # Merge deliveries with matches to get season and venue information
            deliveries_with_details = deliveries.merge(matches[['id', 'season', 'venue']], 
                                                    left_on='match_id', 
                                                    right_on='id', 
                                                    how='left')
            # Filter deliveries where batsman faced bowler
            relevant_deliveries = deliveries_with_details[
                (deliveries_with_details['batter'] == batsman) & 
                (deliveries_with_details['bowler'] == bowler)
            ]
            if relevant_deliveries.empty:
                st.error(f"No data available for {batsman} vs {bowler}.")
                return

            # Filter by season if selected
            if season != "All":
                relevant_deliveries = relevant_deliveries[relevant_deliveries['season'].astype(str) == season]

            # Aggregate stats by season
            season_stats = relevant_deliveries.groupby('season').agg({
                'batsman_runs': 'sum',
                'is_wicket': 'sum'
            }).reset_index()
            season_stats.columns = ['Season', 'Runs Scored', 'Times Dismissed']

            # Aggregate stats by venue for the selected/filtered season
            venue_stats = relevant_deliveries.groupby('venue').agg({
                'batsman_runs': 'sum',
                'is_wicket': 'sum'
            }).reset_index()
            venue_stats.columns = ['Venue', 'Runs Scored', 'Times Dismissed']

            # Overall summary across all seasons
            all_seasons_stats = deliveries_with_details[
                (deliveries_with_details['batter'] == batsman) & 
                (deliveries_with_details['bowler'] == bowler)
            ].agg({
                'batsman_runs': 'sum',
                'is_wicket': 'sum'
            }).to_frame().T
            all_seasons_stats.columns = ['Total Runs Scored', 'Total Times Dismissed']
            all_seasons_venues = deliveries_with_details[
                (deliveries_with_details['batter'] == batsman) & 
                (deliveries_with_details['bowler'] == bowler)
            ].groupby('venue').agg({
                'batsman_runs': 'sum',
                'is_wicket': 'sum'
            }).reset_index()
            all_seasons_venues.columns = ['Venue', 'Total Runs Scored', 'Total Times Dismissed']

            # Display results with custom styling
            if season != "All":
                st.write(f"### Stats for Season {season}")
                st.dataframe(season_stats[season_stats['Season'].astype(str) == season].style.set_properties(**{
                    'text-align': 'center',
                    'border': '2px solid #444',
                    'background-color': '#2e2e2e',
                    'color': '#ffffff'
                }).set_table_styles([
                    {'selector': 'th', 'props': [('background-color', '#333'), ('color', '#fff'), ('border', '2px solid #444')]},
                    {'selector': 'td:hover', 'props': [('background-color', '#555'), ('color', '#fff')]}
                ]))
            else:
                st.write("### Season-wise Stats")
                st.dataframe(season_stats.style.set_properties(**{
                    'text-align': 'center',
                    'border': '2px solid #444',
                    'background-color': '#2e2e2e',
                    'color': '#ffffff'
                }).set_table_styles([
                    {'selector': 'th', 'props': [('background-color', '#333'), ('color', '#fff'), ('border', '2px solid #444')]},
                    {'selector': 'td:hover', 'props': [('background-color', '#555'), ('color', '#fff')]}
                ]))

            if not venue_stats.empty:
                st.write("### Venue-wise Stats for Selected Season")
                st.dataframe(venue_stats.style.set_properties(**{
                    'text-align': 'center',
                    'border': '2px solid #444',
                    'background-color': '#2e2e2e',
                    'color': '#ffffff'
                }).set_table_styles([
                    {'selector': 'th', 'props': [('background-color', '#333'), ('color', '#fff'), ('border', '2px solid #444')]},
                    {'selector': 'td:hover', 'props': [('background-color', '#555'), ('color', '#fff')]}
                ]))

            st.write("### Overall Summary Across All Seasons")
            st.dataframe(all_seasons_stats.style.set_properties(**{
                'text-align': 'center',
                'border': '2px solid #444',
                'background-color': '#2e2e2e',
                'color': '#ffffff'
            }).set_table_styles([
                {'selector': 'th', 'props': [('background-color', '#333'), ('color', '#fff'), ('border', '2px solid #444')]},
                {'selector': 'td:hover', 'props': [('background-color', '#555'), ('color', '#fff')]}
            ]))
            st.write("### Venue-wise Summary Across All Seasons")
            st.dataframe(all_seasons_venues.style.set_properties(**{
                'text-align': 'center',
                'border': '2px solid #444',
                'background-color': '#2e2e2e',
                'color': '#ffffff'
            }).set_table_styles([
                {'selector': 'th', 'props': [('background-color', '#333'), ('color', '#fff'), ('border', '2px solid #444')]},
                {'selector': 'td:hover', 'props': [('background-color', '#555'), ('color', '#fff')]}
            ]))