import pandas as pd

def get_batsman_statistics(batsman, df, matches):
    if not batsman or df[df['batter'] == batsman].empty:
        return {}
    batsman_df = df[df['batter'] == batsman]
    total_runs = batsman_df['batsman_runs'].sum()
    total_balls = batsman_df[batsman_df['extras_type'].ne('wides')]['ball'].count()
    dismissals = batsman_df['is_wicket'].sum()
    innings = batsman_df['match_id'].nunique()
    fours = batsman_df[batsman_df['batsman_runs'] == 4]['ball'].count()
    sixes = batsman_df[batsman_df['batsman_runs'] == 6]['ball'].count()
    fifties = (batsman_df.groupby('match_id')['batsman_runs'].sum() >= 50).sum()
    centuries = (batsman_df.groupby('match_id')['batsman_runs'].sum() >= 100).sum()
    highest_score = batsman_df.groupby('match_id')['batsman_runs'].sum().max()
    not_outs = innings - dismissals
    mom = matches[(matches['player_of_match'] == batsman) & (matches['season'].isin(df['season']))].shape[0]
    return {
        'player_name': batsman,
        'total_innings': innings,
        'total_runs': int(total_runs),
        'total_fours': int(fours),
        'total_sixes': int(sixes),
        'batting_average': round(total_runs / dismissals, 2) if dismissals > 0 else 'N/A',
        'strike_rate': round((total_runs / total_balls) * 100, 2) if total_balls > 0 else 0,
        'total_fifties': int(fifties),
        'total_centuries': int(centuries),
        'highest_score': int(highest_score),
        'not_outs': int(not_outs),
        'player_of_the_match_awards': int(mom)
    }

def get_bowler_statistics(bowler, df, matches):
    if not bowler or df[df['bowler'] == bowler].empty:
        return {}
    bowler_df = df[df['bowler'] == bowler]
    wickets = bowler_df['isBowlerWicket'].sum()
    runs_given = bowler_df['bowler_run'].sum()
    balls = bowler_df['ball'].count()
    innings = bowler_df['match_id'].nunique()
    overs = balls / 6
    fours = bowler_df[bowler_df['batsman_runs'] == 4]['ball'].count()
    sixes = bowler_df[bowler_df['batsman_runs'] == 6]['ball'].count()
    match_wickets = bowler_df.groupby('match_id')['isBowlerWicket'].sum()
    best_wickets = match_wickets.max()
    best_match_ids = match_wickets[match_wickets == best_wickets].index
    best_runs = bowler_df[bowler_df['match_id'].isin(best_match_ids)]['bowler_run'].sum()
    three_w = (match_wickets >= 3).sum()
    four_w = (match_wickets >= 4).sum()
    five_w = (match_wickets >= 5).sum()
    mom = matches[(matches['player_of_match'] == bowler) & (matches['season'].isin(df['season']))].shape[0]
    return {
        'bowler': bowler,
        'innings': int(innings),
        'wickets': int(wickets),
        'economy': round(runs_given / overs, 2) if overs > 0 else 0,
        'average': round(runs_given / wickets, 2) if wickets > 0 else 'N/A',
        'strike_rate': round(balls / wickets, 2) if wickets > 0 else 'N/A',
        'fours': int(fours),
        'sixes': int(sixes),
        'best_figure': f"{int(best_wickets)}/{int(best_runs)}",
        '3w': int(three_w),
        '4w': int(four_w),
        '5w': int(five_w),
        'mom': int(mom)
    }