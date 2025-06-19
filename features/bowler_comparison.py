import streamlit as st
import pandas as pd

def bowler_comparison(deliveries, matches, players):
    col1, col2 = st.columns(2)
    with col1:
        bowler1 = st.selectbox("Select Bowler 1", [""] + players, key="bowler1")
    with col2:
        bowler2 = st.selectbox("Select Bowler 2", [""] + players, key="bowler2")
    
    if st.button("Analyze", key="bowler_comparison"):
        if bowler1 == "" or bowler2 == "" or bowler1 == bowler2:
            st.error("Please select two different bowlers.")
        else:
            df_filtered = deliveries.merge(matches[['id', 'season']], left_on='match_id', right_on='id', how='left')
            df_filtered = df_filtered[df_filtered['inning'].isin([1, 2])]
            df_bowler1 = df_filtered[df_filtered['bowler'] == bowler1].groupby('season', as_index=False)['is_wicket'].sum()
            df_bowler2 = df_filtered[df_filtered['bowler'] == bowler2].groupby('season', as_index=False)['is_wicket'].sum()
            if df_bowler1.empty or df_bowler2.empty:
                st.error(f"Data not found for one or both bowlers: {bowler1}, {bowler2}")
            else:
                df_bowler1.rename(columns={'is_wicket': f'{bowler1}_wickets'}, inplace=True)
                df_bowler2.rename(columns={'is_wicket': f'{bowler2}_wickets'}, inplace=True)
                df_merged = pd.merge(df_bowler1, df_bowler2, on='season', how='outer').fillna(0)
                df_merged.set_index('season', inplace=True)

                st.subheader(f"{bowler1} Wickets")
                st.line_chart(df_merged[[f'{bowler1}_wickets']])

                st.subheader(f"{bowler2} Wickets")
                st.line_chart(df_merged[[f'{bowler2}_wickets']])

                st.subheader("Combined Data")
                st.dataframe(df_merged.style.set_properties(**{'text-align': 'center'}))