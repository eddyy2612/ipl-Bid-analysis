import streamlit as st
import pandas as pd

def top_batsmen_strike_rate(deliveries):
    min_balls = st.number_input("Minimum Balls Faced", min_value=1, value=100, step=10)
    
    if st.button("Analyze", key="top_batsmen"):
        batsman_stats_df = deliveries.groupby('batter').agg(
            total_runs=('batsman_runs', 'sum'),
            balls_faced=('batsman_runs', lambda x: deliveries.loc[x.index, 'extras_type'].ne('wides').sum())
        )
        batsman_stats_df['strike_rate'] = (batsman_stats_df['total_runs'] / batsman_stats_df['balls_faced']) * 100
        batsman_stats_df = batsman_stats_df[batsman_stats_df['balls_faced'] >= min_balls]
        top_10 = batsman_stats_df.sort_values(by='strike_rate', ascending=False).head(10).reset_index()
        top_10.set_index('batter', inplace=True)

        st.subheader("Top 10 Batsmen Strike Rate")
        st.bar_chart(top_10[['strike_rate']])

        st.subheader("Top 10 Batsmen Data")
        st.dataframe(top_10.style.set_properties(**{'text-align': 'center'}))