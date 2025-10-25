import streamlit as st
import openai
from transfermarkt_api import get_team_info, get_team_players, clean_team_profile
from prompt_builder import build_prompt
from utils import fetch_player_data, toggle_timer, get_elapsed_time, goal_scored, select_competition
from dotenv import load_dotenv
import os
st.set_page_config(
    page_title="Match Event Tracker",
    layout="wide",  # <- questo fa occupare tutta la larghezza
    initial_sidebar_state="auto"
)
# --- OpenAI Key ---
load_dotenv()  # carica le variabili dal .env

api_key = os.getenv("OPENAI_API_KEY")
col_left, col_right = st.columns([1, 1])

# -------------------------
# --- Inizializzazione stato sessione   ---
# -------------------------
if "team_players_home" not in st.session_state:
    st.session_state.team_players_home = []

if "team_players_away" not in st.session_state:
    st.session_state.team_players_away = []

if "competition_selected" not in st.session_state:
    st.session_state.competition_selected = False
if "home_team" not in st.session_state:
    st.session_state.home_team = None
if "away_team" not in st.session_state:
    st.session_state.away_team = None
if "running" not in st.session_state:
    st.session_state.running = False
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "elapsed" not in st.session_state:
    st.session_state.elapsed = 0
if "score" not in st.session_state:
    st.session_state.score = [0, 0]  # [home, away]
if "selected_event" not in st.session_state:
    st.session_state.selected_event = None
if "kwargs" not in st.session_state:
    st.session_state.kwargs = {}
if "comments" not in st.session_state:
    st.session_state.comments = []

with col_left:

    # -------------------------
    # --- Selezione competizione ---
    # -------------------------
    if not st.session_state.competition_selected:
        st.title("Match Event Tracker")
        competitions = {
            "1": "Premier League",
            "2": "La Liga",
            "3": "Serie A",
            "4": "Bundesliga",
            "5": "Ligue 1",
        }
        st.selectbox("", list(competitions.values()), key="competition_select", placeholder="Select Competition")
        st.button("Select Competition", on_click=select_competition)

    else:
        st.title("Match Event Tracker")
        clubs = st.session_state.clubs

        # --- Home Team ---
        if not st.session_state.home_team:
            home_team_name = st.selectbox("Select Home Team", [c['name'] for c in clubs], key="home_select")
            if st.button("Select Home Team", key="home_selected"):
                team = next(c for c in clubs if c['name'] == home_team_name)
                st.session_state.home_team = team
                st.session_state.team_profile_home = clean_team_profile(get_team_info(team['id']))
                st.session_state.team_players_home = get_team_players(team['id'])
                st.rerun()
        else:
            st.success(f"✅ Home Team locked: {st.session_state.home_team['name']}")

        # --- Away Team ---
        if st.session_state.home_team and not st.session_state.away_team:
            away_team_name = st.selectbox(
                "Select Away Team",
                [c['name'] for c in clubs if c['name'] != st.session_state.home_team['name']],
                key="away_select"
            )
            if st.button("Select Away Team", key="away_selected"):
                team = next(c for c in clubs if c['name'] == away_team_name)
                st.session_state.away_team = team
                st.session_state.team_profile_away = clean_team_profile(get_team_info(team['id']))
                st.session_state.team_players_away = get_team_players(team['id'])
                st.rerun()
        elif st.session_state.away_team:
            st.success(f"✅ Away Team locked: {st.session_state.away_team['name']}")

        # --- Reset Option (optional) ---
        if "home_team" in st.session_state and "away_team" in st.session_state:
            if st.button("🔄 Reset Teams"):
                del st.session_state.home_team
                del st.session_state.away_team
                st.rerun()
    # -------------------------
    # --- Timer ---
    # -------------------------
    if st.session_state.home_team and st.session_state.away_team:
        col_1, col_2 = st.columns([1, 2])
        with col_1:
            if st.button("Start/Stop Timer", key="timer"):
                toggle_timer()
        with col_2:
            minutes, seconds = get_elapsed_time()
            st.metric("Match Time", f"{minutes:02d}:{seconds:02d}")

        event_types = {
            "goal": "Goal", "foul": "Foul", "attempted_shot": "Attempted Shot", "dribbling": "Dribbling",
            "tackle": "Tackle", "pass": "Pass", "var_call": "VAR Call", "offside": "Offside",
            "start_half_end_game": "Start/Half/End Game", "substitution": "Substitution"
        }

        cols_per_row = 5
        event_list = list(event_types.keys())
        for i in range(0, len(event_list), cols_per_row):
            cols = st.columns(cols_per_row)
            for j, event in enumerate(event_list[i:i+cols_per_row]):
                if cols[j].button(event_types[event], key=f"event_{event}"):
                    st.session_state.selected_event = event

    # -------------------------
    # --- Event Handling & Confirmation ---
    # -------------------------
    if st.session_state.selected_event:
        minutes, seconds = get_elapsed_time()
        st.subheader(f"Attributes for {event_types[st.session_state.selected_event]}")

        event = st.session_state.selected_event


        def generate_comment(event_type, kwargs):
            prompt = build_prompt(event_type, **kwargs)

            response = openai.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a football commentator."},
                    {"role": "user", "content": prompt}
                ]
            )

            comment_text = response.choices[0].message.content
            return f"Minute: {kwargs['minute']+1} - {comment_text}"


        def confirm_event(kwargs):
            """Conferma evento, genera commento e aggiunge al log"""
            comment_text = generate_comment(event, kwargs)
            st.session_state.comments.append(f"{comment_text}")
            st.session_state.kwargs = kwargs
            st.rerun()

        # --- EVENT: GOAL ---
        if event == "goal":
            team_name = st.selectbox("Team Scored", [st.session_state.home_team['name'], st.session_state.away_team['name']])
            players = st.session_state.team_players_home if team_name == st.session_state.home_team['name'] else st.session_state.team_players_away
            scorer = st.selectbox("Scorer", [p['name'] for p in players])
            assist_options = ["None"] + [p['name'] for p in players]
            assist = st.selectbox("Assist (optional)", assist_options)
            if assist == "None":
                assist = None
            goal_type = st.selectbox("Goal Type", ["Right foot","Left foot","Header","Other"])
            shot_position = st.selectbox("Shot Position", ["Inside box","Outside box","Penalty spot","Free kick"])
            scorer_info, scorer_stats, scorer_achievements = fetch_player_data(scorer)
            if st.button("Confirm Goal"):
                goal_scored(team_name)
                confirm_event({
                    "minute": minutes, "second": seconds,
                    "competition": st.session_state.competition,
                    "home_team": st.session_state.home_team['name'], "away_team": st.session_state.away_team['name'],
                    "team_profile_home": st.session_state.team_profile_home,
                    "team_profile_away": st.session_state.team_profile_away,
                    "team_players_home": st.session_state.team_players_home,
                    "team_players_away": st.session_state.team_players_away,
                    "current_score": f"{st.session_state.score[0]}-{st.session_state.score[1]}",
                    "team_involved": team_name, "scorer": scorer, "scorer_info": scorer_info,
                    "scorer_stats": scorer_stats, "scorer_achievements": scorer_achievements,
                    "assist": assist, "goal_type": goal_type, "shot_position": shot_position
                })

        # --- EVENT: PASS ---
        elif event == "pass":
            team_name = st.selectbox("Team Pass", [st.session_state.home_team['name'], st.session_state.away_team['name']])
            players = st.session_state.team_players_home if team_name == st.session_state.home_team['name'] else st.session_state.team_players_away
            passer = st.selectbox("Passer", [p['name'] for p in players])
            receiver = st.selectbox("Receiver", [p['name'] for p in players])
            pass_type = st.selectbox("Pass Type", ["Short pass", "Long pass", "Through ball", "Cross"])
            success = st.selectbox("Successful/Unsuccessful", ["Successful", "Unsuccessful"])
            if st.button("Confirm Pass"):
                confirm_event({
                    "minute": minutes, "second": seconds,
                    "competition": st.session_state.competition,
                    "home_team": st.session_state.home_team['name'], "away_team": st.session_state.away_team['name'],
                    "team_profile_home": st.session_state.team_profile_home,
                    "team_profile_away": st.session_state.team_profile_away,
                    "team_players_home": st.session_state.team_players_home,
                    "team_players_away": st.session_state.team_players_away,
                    "current_score": f"{st.session_state.score[0]}-{st.session_state.score[1]}",
                    "team_involved": team_name, "passer": passer, "receiver": receiver,
                    "pass_type": pass_type, "success": success
                })

        # --- EVENT: OFFSIDE ---
        elif event == "offside":
            team_name = st.selectbox("Team Offside", [st.session_state.home_team['name'], st.session_state.away_team['name']])
            players = st.session_state.team_players_home if team_name == st.session_state.home_team['name'] else st.session_state.team_players_away
            passer = st.selectbox("Passer", [p['name'] for p in players])
            receiver = st.selectbox("Receiver", [p['name'] for p in players])
            if st.button("Confirm Offside"):
                confirm_event({
                    "minute": minutes, "second": seconds,
                    "competition": st.session_state.competition,
                    "home_team": st.session_state.home_team['name'], "away_team": st.session_state.away_team['name'],
                    "team_profile_home": st.session_state.team_profile_home,
                    "team_profile_away": st.session_state.team_profile_away,
                    "team_players_home": st.session_state.team_players_home,
                    "team_players_away": st.session_state.team_players_away,
                    "current_score": f"{st.session_state.score[0]}-{st.session_state.score[1]}",
                    "team_involved": team_name, "passer": passer, "receiver": receiver
                })

        # --- EVENT: DRIBBLING ---
        elif event == "dribbling":
            team_name = st.selectbox("Team Dribbling", [st.session_state.home_team['name'], st.session_state.away_team['name']])
            players = st.session_state.team_players_home if team_name == st.session_state.home_team['name'] else st.session_state.team_players_away
            opponents = st.session_state.team_players_away if team_name == st.session_state.home_team['name'] else st.session_state.team_players_home
            dribbler = st.selectbox("Dribbler", [p['name'] for p in players])
            opponent = st.selectbox("Opponent", [p['name'] for p in opponents])
            success = st.selectbox("Successful/Unsuccessful", ["Successful", "Unsuccessful"])
            dribbler_info, dribbler_stats, _ = fetch_player_data(dribbler)
            if st.button("Confirm Dribbling"):
                confirm_event({
                    "minute": minutes, "second": seconds,
                    "competition": st.session_state.competition,
                    "home_team": st.session_state.home_team['name'], "away_team": st.session_state.away_team['name'],
                    "team_profile_home": st.session_state.team_profile_home,
                    "team_profile_away": st.session_state.team_profile_away,
                    "team_players_home": st.session_state.team_players_home,
                    "team_players_away": st.session_state.team_players_away,
                    "current_score": f"{st.session_state.score[0]}-{st.session_state.score[1]}",
                    "team_involved": team_name, "dribbler": dribbler, "dribbler_info": dribbler_info,
                    "dribbler_stats": dribbler_stats, "opponent": opponent, "success": success
                })

        # --- EVENT: TACKLE ---
        elif event == "tackle":
            team_name = st.selectbox("Team Tackling", [st.session_state.home_team['name'], st.session_state.away_team['name']])
            players = st.session_state.team_players_home if team_name == st.session_state.home_team['name'] else st.session_state.team_players_away
            opponents = st.session_state.team_players_away if team_name == st.session_state.home_team['name'] else st.session_state.team_players_home
            tackler = st.selectbox("Tackler", [p['name'] for p in players])
            opponent = st.selectbox("Opponent", [p['name'] for p in opponents])
            success = st.selectbox("Successful/Unsuccessful", ["Successful", "Unsuccessful"])
            tackler_info, tackler_stats, _ = fetch_player_data(tackler)
            if st.button("Confirm Tackle"):
                confirm_event({
                    "minute": minutes, "second": seconds,
                    "competition": st.session_state.competition,
                    "home_team": st.session_state.home_team['name'], "away_team": st.session_state.away_team['name'],
                    "team_profile_home": st.session_state.team_profile_home,
                    "team_profile_away": st.session_state.team_profile_away,
                    "team_players_home": st.session_state.team_players_home,
                    "team_players_away": st.session_state.team_players_away,
                    "current_score": f"{st.session_state.score[0]}-{st.session_state.score[1]}",
                    "team_involved": team_name, "tackler": tackler, "tackler_info": tackler_info,
                    "tackler_stats": tackler_stats, "opponent": opponent, "success": success
                })

        # --- EVENT: FOUL ---
        elif event == "foul":
            team_name = st.selectbox("Team Fouling", [st.session_state.home_team['name'], st.session_state.away_team['name']])
            players = st.session_state.team_players_home if team_name == st.session_state.home_team['name'] else st.session_state.team_players_away
            player = st.selectbox("Fouling Player", [p['name'] for p in players])
            reason = st.selectbox("Foul Reason", ["Handball", "Tripping", "Pushing", "Other"])
            card = st.selectbox("Card Type", ["Yellow", "Red", "None"])
            player_info, player_stats, _ = fetch_player_data(player)
            if st.button("Confirm Foul"):
                confirm_event({
                    "minute": minutes, "second": seconds,
                    "competition": st.session_state.competition,
                    "home_team": st.session_state.home_team['name'], "away_team": st.session_state.away_team['name'],
                    "team_profile_home": st.session_state.team_profile_home,
                    "team_profile_away": st.session_state.team_profile_away,
                    "team_players_home": st.session_state.team_players_home,
                    "team_players_away": st.session_state.team_players_away,
                    "current_score": f"{st.session_state.score[0]}-{st.session_state.score[1]}",
                    "team_involved": team_name, "player": player, "player_info": player_info,
                    "player_stats": player_stats, "reason": reason, "card": card
                })
        # --- EVENT: ATTEMPTED SHOT ---
        elif event == "attempted_shot":
            team_name = st.selectbox("Team Shooting", [st.session_state.home_team['name'], st.session_state.away_team['name']])
            players = st.session_state.team_players_home if team_name == st.session_state.home_team['name'] else st.session_state.team_players_away
            shooter = st.selectbox("Shooting Player", [p['name'] for p in players])
            outcome = st.selectbox("Outcome", ["Saved", "Missed", "Blocked"])
            shot_position = st.selectbox("Shot Position", ["Inside box", "Outside box", "Penalty", "Free kick"])
            shooter_info, shooter_stats, shooter_achievements = fetch_player_data(shooter)
            if st.button("Confirm Attempted Shot"):
                confirm_event({
                    "minute": minutes, "second": seconds,
                    "competition": st.session_state.competition,
                    "home_team": st.session_state.home_team['name'], "away_team": st.session_state.away_team['name'],
                    "team_profile_home": st.session_state.team_profile_home,
                    "team_profile_away": st.session_state.team_profile_away,
                    "team_players_home": st.session_state.team_players_home,
                    "team_players_away": st.session_state.team_players_away,
                    "current_score": f"{st.session_state.score[0]}-{st.session_state.score[1]}",
                    "team_involved": team_name, "shooter": shooter, "shooter_info": shooter_info,
                    "shooter_stats": shooter_stats, "shooter_achievements": shooter_achievements,
                    "outcome": outcome, "shot_position": shot_position
                })

        # --- EVENT: VAR CALL ---
        elif event == "var_call":
            team_name = st.selectbox("Team", [st.session_state.home_team['name'], st.session_state.away_team['name']])
            var_reason = st.selectbox("VAR Call Reason", ["Potential penalty", "Offside", "Handball", "Foul", "Goal review", "Mistaken identity", "Other"])
            if st.button("Confirm VAR Call"):
                confirm_event({
                    "minute": minutes, "second": seconds,
                    "competition": st.session_state.competition,
                    "home_team": st.session_state.home_team['name'], "away_team": st.session_state.away_team['name'],
                    "team_profile_home": st.session_state.team_profile_home,
                    "team_profile_away": st.session_state.team_profile_away,
                    "team_players_home": st.session_state.team_players_home,
                    "team_players_away": st.session_state.team_players_away,
                    "current_score": f"{st.session_state.score[0]}-{st.session_state.score[1]}",
                    "team_involved": team_name, "reason": var_reason
                })

        # --- EVENT: START/HALF/END GAME ---
        elif event == "start_half_end_game":
            game_status = st.selectbox("Game Status", ["Start First Half", "End First Half", "Start Second Half", "End Second Half"])
            if st.button("Confirm Game Status"):
                confirm_event({
                    "minute": minutes, "second": seconds,
                    "competition": st.session_state.competition,
                    "home_team": st.session_state.home_team['name'], "away_team": st.session_state.away_team['name'],
                    "team_profile_home": st.session_state.team_profile_home,
                    "team_profile_away": st.session_state.team_profile_away,
                    "team_players_home": st.session_state.team_players_home,
                    "team_players_away": st.session_state.team_players_away,
                    "current_score": f"{st.session_state.score[0]}-{st.session_state.score[1]}",
                    "game_status": game_status
                })

        # --- EVENT: SUBSTITUTION ---
        elif event == "substitution":
            team_name = st.selectbox("Team Substituting", [st.session_state.home_team['name'], st.session_state.away_team['name']])
            players = st.session_state.team_players_home if team_name == st.session_state.home_team['name'] else st.session_state.team_players_away
            player_in = st.selectbox("Player In", [p['name'] for p in players])
            player_out = st.selectbox("Player Out", [p['name'] for p in players])
            in_info, in_stats, in_achievements = fetch_player_data(player_in)
            out_info, out_stats, out_achievements = fetch_player_data(player_out)
            if st.button("Confirm Substitution"):
                confirm_event({
                    "minute": minutes, "second": seconds,
                    "competition": st.session_state.competition,
                    "home_team": st.session_state.home_team['name'], "away_team": st.session_state.away_team['name'],
                    "team_profile_home": st.session_state.team_profile_home,
                    "team_profile_away": st.session_state.team_profile_away,
                    "team_players_home": st.session_state.team_players_home,
                    "team_players_away": st.session_state.team_players_away,
                    "current_score": f"{st.session_state.score[0]}-{st.session_state.score[1]}",
                    "team_involved": team_name,
                    "player_in": player_in, "player_in_info": in_info, "player_in_stats": in_stats, "player_in_achievements": in_achievements,
                    "player_out": player_out, "player_out_info": out_info, "player_out_stats": out_stats, "player_out_achievements": out_achievements
                })

with col_right:
    # -------------------------
    # --- Visualizzazione squadre e punteggio ---
    # -------------------------
    if st.session_state.home_team and st.session_state.away_team:
        col1, col2, col3 = st.columns([2,1,2])
        with col1:
            st.subheader(st.session_state.home_team['name'])
            st.image(st.session_state.team_profile_home['image'], width=120)
        with col2:
            st.markdown(f"### {st.session_state.score[0]} - {st.session_state.score[1]}")
        with col3:
            st.subheader(st.session_state.away_team['name'])
            st.image(st.session_state.team_profile_away['image'], width=120)



    # --- Display all comments ---
    if "comments" not in st.session_state:
        st.session_state.comments = []

    if st.session_state.comments:
        st.subheader("Match Commentary")
        for c in st.session_state.comments:
            st.write(c)
