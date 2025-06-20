import streamlit as st
from data_loader import load_data
from features.team_vs_team_growth import team_vs_team_growth
from features.bowler_comparison import bowler_comparison
from features.season_stats import season_stats
from features.winning_probability import winning_probability
from features.top_batsmen_strike_rate import top_batsmen_strike_rate
from features.highest_targets_set import highest_targets_set
from features.player_vs_team_stats import player_vs_team_stats
from features.overall_team_performance import overall_team_performance
from features.live_match_prediction import live_match_prediction
from features.batsman_vs_bowler_stats import batsman_vs_bowler_stats
from features.choose_the_best import choose_the_best

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "home"

# Set page config with custom styling
st.set_page_config(
    page_title="IPL Analysis Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed",
    page_icon=":cricket_bat_and_ball:"
)

# Custom CSS to center title, enhance home page, and style buttons
st.markdown(
    """
    <style>
    .main {
        background-color: #1a1a1a;
        color: #ffffff;
        font-family: 'Arial', sans-serif;
    }
    .hero {
        padding: 50px 0;
        text-align: center;
    }
    .hero h1 {
        font-size: 3em;
        margin: 0;
        text-align: center;
        color: #ffffff;
    }
    .hero p {
        font-size: 1.2em;
        margin: 10px 0;
        animation: fadeIn 2s infinite alternate;
    }
    @keyframes fadeIn {
        from { opacity: 0.5; }
        to { opacity: 1; }
    }
    .animated-text {
        background: linear-gradient(to right, #d33682, #ffffff);
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
        animation: gradientShift 3s ease infinite;
    }
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .stButton>button {
        background-color: #d33682; /* Pink for all other buttons */
        color: white;
        border: none;
        border-radius: 20px;
        padding: 10px 30px;
        font-size: 1.1em;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #ff8c00; /* Orange hover for all other buttons */
        transform: scale(1.1);
    }
    .choose-the-best-button>button {
        background-color: #ff0000; /* Red for Choose the Best */
        color: white;
        border: none;
        border-radius: 20px;
        padding: 10px 30px;
        font-size: 1.1em;
        transition: all 0.3s;
    }
    .choose-the-best-button>button:hover {
        background-color: #cc0000; /* Darker red hover for Choose the Best */
        transform: scale(1.1);
    }
    .feature-card {
        background-color: #2a2a2a;
        padding: 20px;
        border-radius: 10px;
        margin: 10px;
        text-align: center;
        transition: transform 0.3s;
    }
    .feature-card:hover {
        transform: scale(1.05);
        background-color: #333;
    }
    .footer {
        text-align: center;
        padding: 10px;
        background-color: #1a1a1a;
        color: #bbb;
        position: fixed;
        bottom: 0;
        width: 100%;
    }
    .go-home-button {
        position: absolute;
        top: 10px;
        right: 10px;
        background-color: #ff0000;
    }
    .go-home-button>button:hover {
        background-color: #cc0000;
        transform: scale(1.1);
    }
    .go-back-button {
        position: absolute;
        top: 10px;
        left: 10px;
        background-color: #d33682;
    }
    .go-back-button>button:hover {
        background-color: #ff8c00;
        transform: scale(1.1);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Home page
if st.session_state.page == "home":
    st.markdown('<div class="hero">', unsafe_allow_html=True)
    st.title(":blue[Welcome to IPL Analysis] :sunglasses:")
    st.markdown(
        """
        <p class="animated-text"; style="font-weight: bold; font-size: 35px;">Betting made Easy ! </p>
        <p></p>
        <p style="text-align: left; font-weight: bold; font-size: 20px; font-style: italic; color: LightSalmon ;">
    Immerse yourself in the exhilarating realm of the Indian Premier League with our state-of-the-art analytical platform. Unlock real-time match forecasts, dynamic player comparisons, and comprehensive team insights through a visually captivating, interactive interface. Tailored for passionate cricket enthusiasts and data aficionados, this tool elevates your experience—ignite your journey into the game!
</p>
        """,
        unsafe_allow_html=True
    )
    st.image("./data/cricket.jpg.webp", use_container_width=True)
    if st.button("Enter Dashboard"):
        st.session_state.page = "dashboard"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# Load data
matches, deliveries, merged_df, bowler_data, teams, players, seasons = load_data()
venues = sorted(matches['venue'].dropna().unique())

# Dashboard page
if st.session_state.page == "dashboard":
    st.markdown('<div style="text-align: center; margin-bottom: 20px;">', unsafe_allow_html=True)
    st.title("IPL Analysis Features")
    st.markdown('</div>', unsafe_allow_html=True)

    # Go to Home Page button at top right
    st.markdown('<div class="go-home-button">', unsafe_allow_html=True)
    if st.button("Go to Home Page", key="home_button"):
        st.session_state.page = "home"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # Feature selection
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Team vs Team Growth"):
            st.session_state.page = "team_vs_team_growth"
            st.rerun()
    with col2:
        if st.button("Bowler Comparison"):
            st.session_state.page = "bowler_comparison"
            st.rerun()
    with col3:
        if st.button("Season Stats"):
            st.session_state.page = "season_stats"
            st.rerun()

    col4, col5, col6 = st.columns(3)
    with col4:
        if st.button("Winning Probability"):
            st.session_state.page = "winning_probability"
            st.rerun()
    with col5:
        if st.button("Top Batsmen Strike Rate"):
            st.session_state.page = "top_batsmen_strike_rate"
            st.rerun()
    with col6:
        if st.button("Highest Targets Set"):
            st.session_state.page = "highest_targets_set"
            st.rerun()

    col7, col8, col9 = st.columns(3)
    with col7:
        if st.button("Player vs Team Stats"):
            st.session_state.page = "player_vs_team_stats"
            st.rerun()
    with col8:
        if st.button("Overall Team Performance"):
            st.session_state.page = "overall_team_performance"
            st.rerun()
    with col9:
        if st.button("Live Match Prediction"):
            st.session_state.page = "live_match_prediction"
            st.rerun()

    col10, col11, col12 = st.columns(3)
    with col10:
        if st.button("Batsman vs Bowler Stats"):
            st.session_state.page = "batsman_vs_bowler_stats"
            st.rerun()
    with col11:
        if st.button("Choose the Best", key="choose_the_best_button"):
            st.session_state.page = "choose_the_best"
            st.rerun()

# Feature pages
if st.session_state.page in ["team_vs_team_growth", "bowler_comparison", "season_stats", "winning_probability",
                            "top_batsmen_strike_rate", "highest_targets_set", "player_vs_team_stats",
                            "overall_team_performance", "live_match_prediction", "batsman_vs_bowler_stats",
                            "choose_the_best"]:
    st.markdown('<div style="margin-top: 20px;">', unsafe_allow_html=True)
    st.subheader(st.session_state.page.replace("_", " ").title())
    
    # Go Back button at top left
    st.markdown('<div class="go-back-button">', unsafe_allow_html=True)
    if st.button("Go Back", key="go_back"):
        st.session_state.page = "dashboard"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # Render the selected feature
    if st.session_state.page == "team_vs_team_growth":
        team_vs_team_growth(matches, teams, deliveries, seasons)
    elif st.session_state.page == "bowler_comparison":
        bowler_comparison(deliveries, matches, players)
    elif st.session_state.page == "season_stats":
        season_stats(merged_df, bowler_data, matches, teams, players, seasons)
    elif st.session_state.page == "winning_probability":
        winning_probability(matches, teams)
    elif st.session_state.page == "top_batsmen_strike_rate":
        top_batsmen_strike_rate(deliveries)
    elif st.session_state.page == "highest_targets_set":
        highest_targets_set(matches)
    elif st.session_state.page == "player_vs_team_stats":
        player_vs_team_stats(merged_df, bowler_data, players, teams)
    elif st.session_state.page == "overall_team_performance":
        overall_team_performance(matches, teams)
    elif st.session_state.page == "live_match_prediction":
        live_match_prediction(matches, deliveries, teams, venues)
    elif st.session_state.page == "batsman_vs_bowler_stats":
        batsman_vs_bowler_stats(matches, deliveries, players, teams, venues, seasons)
    elif st.session_state.page == "choose_the_best":
        choose_the_best(matches, deliveries, players, seasons)
    
    st.markdown('</div>', unsafe_allow_html=True)

    # Footer
    st.markdown('<div class="footer">About IPL Analysis | © 2025</div>', unsafe_allow_html=True)