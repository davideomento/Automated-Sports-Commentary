from transfermarkt_api import (
    search_player_by_name,
    get_player_info,
    get_player_stats, 
    get_player_achievements,
    get_competition_clubs,  
    search_competition_by_name,
    clean_player_profile,
    clean_player_stats_achievements
)
import time
import streamlit as st


def fetch_player_data(name):
    """Search player and fetch info, stats, achievements."""
    player_id = search_player_by_name(name)
    if not player_id:
        return None, None, None
    info = get_player_info(player_id)
    info = clean_player_profile(info)
    stats = get_player_stats(player_id)
    stats = clean_player_stats_achievements(stats)
    achievements = get_player_achievements(player_id)
    achievements = clean_player_stats_achievements(achievements)
    return info, stats, achievements




def toggle_timer():
    if st.session_state.running:
        st.session_state.running = False
        st.session_state.elapsed = time.time() - st.session_state.start_time
    else:
        st.session_state.running = True
        st.session_state.start_time = time.time() - st.session_state.elapsed

def get_elapsed_time():
    elapsed = st.session_state.elapsed
    if st.session_state.running:
        elapsed = time.time() - st.session_state.start_time
    minutes = int(elapsed // 60)
    seconds = int(elapsed % 60)
    return minutes, seconds

def goal_scored(team_name):
    if team_name == st.session_state.home_team['name']:
        st.session_state.score[0] += 1
    else:
        st.session_state.score[1] += 1


def select_competition():
    comp_choice = st.session_state.competition_select
    comp_id = search_competition_by_name(comp_choice)
    clubs_info = get_competition_clubs(comp_id)
    st.session_state.competition = comp_choice
    st.session_state.clubs = clubs_info["clubs"]
    st.session_state.competition_selected = True