import streamlit as st
from transfermarkt_api import (
    get_team_info,
    get_team_players,   
    clean_team_profile
)

from prompt_builder import build_prompt 
from utils import fetch_player_data, toggle_timer, get_elapsed_time, goal_scored, select_competition


if "team_players_home" not in st.session_state:
    st.session_state.team_players_home = []

if "team_players_away" not in st.session_state:
    st.session_state.team_players_away = []
# --------------------------
# --- Stato della sessione ---
# --------------------------
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

# --------------------------

# --------------------------
# --- Selezione competizione ---
# --------------------------
if not st.session_state.get("competition_selected", False):
    st.title("Match Event Tracker")

    competitions = {
        "1": "Premier League",
        "2": "La Liga",
        "3": "Serie A",
        "4": "Bundesliga",
        "5": "Ligue 1",
    }

    st.selectbox(
        "",
        list(competitions.values()),
        key="competition_select",
        placeholder="Select Competition"
    )

    st.button("Select Competition", on_click=select_competition)

else:
    st.title(f"Match Event Tracker")
    clubs = st.session_state.clubs

    # --- Home Team Selection ---

    if not st.session_state.get("home_team"):
        home_team_name = st.selectbox(
            "Select Home Team",
            [c['name'] for c in clubs],
            key="home_select"
        )
        if st.button("Select Home Team", key="home_selected"):
            team = next((c for c in clubs if c['name'] == home_team_name), None)
            if team:
                st.session_state.home_team = team
                team_info = get_team_info(team['id'])
                st.session_state.team_profile_home = clean_team_profile(team_info)
                st.session_state.team_players_home = get_team_players(team['id'])
                st.rerun()

    else:
        st.success(f"✅ Home Team locked: {st.session_state.home_team.get('name', 'Unknown')}")

    # --- Away Team ---
    if st.session_state.get("home_team") and not st.session_state.get("away_team"):
        away_team_name = st.selectbox(
            "Select Away Team",
            [c['name'] for c in clubs if c['name'] != st.session_state.home_team.get('name')],
            key="away_select"
        )
        if st.button("Select Away Team", key="away_selected"):
            team = next((c for c in clubs if c['name'] == away_team_name), None)
            if team:
                st.session_state.away_team = team
                team_info = get_team_info(team['id'])
                st.session_state.team_profile_away = clean_team_profile(team_info)
                st.session_state.team_players_away = get_team_players(team['id'])
                st.rerun()
    elif st.session_state.get("away_team"):
        st.success(f"✅ Away Team locked: {st.session_state.away_team.get('name', 'Unknown')}")


    # --- Reset Option (optional) ---
    if "home_team" in st.session_state and "away_team" in st.session_state:
        if st.button("🔄 Reset Teams"):
            del st.session_state.home_team
            del st.session_state.away_team
            st.rerun()


if st.session_state.get("home_team") and st.session_state.get("away_team"):
    col1, col2, col3 = st.columns([2, 1, 2])  # colonne con proporzioni diverse
    with col1:
        st.subheader(st.session_state.home_team['name'])
        st.image(st.session_state.team_profile_home['image'], width=120)
    with col2:
        st.markdown(f"### {st.session_state.score[0]} - {st.session_state.score[1]}")
    with col3:
        st.subheader(st.session_state.away_team['name'])
        st.image(st.session_state.team_profile_away['image'], width=120)


# --------------------------
# --- Timer e Eventi ---
# --------------------------
if st.session_state.home_team and st.session_state.away_team:
    if not st.session_state.selected_event:
        st.info("⚽ Select an event to generate the commentary prompt. ⚽")
    col1, col2 = st.columns([1,3])
    with col1:
        if st.button("Start/Stop Timer", key="timer"):
            toggle_timer()
    with col2:
        minutes, seconds = get_elapsed_time()
        st.metric("Match Time", f"{minutes:02d}:{seconds:02d}")

    # --- Eventi ---
    event_types = {
        "goal": "Goal",
        "foul": "Foul",
        "attempted_shot": "Attempted Shot",
        "dribbling": "Dribbling",
        "tackle": "Tackle",
        "pass": "Pass",
        "var_call": "VAR Call",
        "offside": "Offside",
        "start_half_end_game": "Start/Half/End Game",
        "substitution": "Substitution"
    }

    cols_per_row = 5
    event_list = list(event_types.keys())
    for i in range(0, len(event_list), cols_per_row):
        cols = st.columns(cols_per_row)
        for j, event in enumerate(event_list[i:i+cols_per_row]):
            if cols[j].button(event_types[event], key=f"event_{event}"):
                st.session_state.selected_event = event

    if st.session_state.selected_event:
        st.subheader(f"Attributes for {event_types[st.session_state.selected_event]}")
        kwargs = {
            "minute": minutes,
            "second": seconds,
            "current_score": f"{st.session_state.score[0]}-{st.session_state.score[1]}",
            "competition": st.session_state.competition,
            "home_team": st.session_state.home_team['name'],
            "away_team": st.session_state.away_team['name'],
        }

        # --- Goal Event ---
        if st.session_state.selected_event == "goal":
            # Scegli la squadra dal nome reale
            team_name = st.selectbox(
                "Team Scored",
                [st.session_state.home_team['name'], st.session_state.away_team['name']]
            )

            # Seleziona giocatori dalla squadra scelta
            if team_name == st.session_state.home_team['name']:
                players = st.session_state.team_players_home
            else:
                players = st.session_state.team_players_away
            
            scorer = st.selectbox("Scorer", [p['name'] for p in players])  
            assist_options = [p['name'] for p in players]
            assist_options.insert(0, "None")
            assist = st.selectbox("Assist (optional)", assist_options)
            if assist == "None":
                assist = None

            goal_type = st.selectbox("Goal Type", ["Right foot", "Left foot", "Header", "Other"])
            shot_position = st.selectbox("Shot Position", ["Inside box", "Outside box", "Penalty spot", "Free kick"])
            scorer_info, scorer_stats, scorer_achievements = fetch_player_data(scorer)

            if st.button("Confirm Goal", key="confirm_goal"):
                # Aggiorna il punteggio
                goal_scored(team_name)
                st.session_state.kwargs = {
                    "minute": minutes,
                    "second": seconds,
                    "competition": st.session_state.competition,
                    "home_team": st.session_state.home_team['name'],
                    "away_team": st.session_state.away_team['name'],
                    "team_profile_home": st.session_state.team_profile_home,
                    "team_profile_away": st.session_state.team_profile_away,
                    "team_players_home": st.session_state.team_players_home,
                    "team_players_away": st.session_state.team_players_away,
                    "current_score": f"{st.session_state.score[0]}-{st.session_state.score[1]}",
                    "team_involved": team_name,
                    "scorer": scorer,
                    "scorer_info": scorer_info,
                    "scorer_stats": scorer_stats,
                    "scorer_achievements": scorer_achievements,
                    "assist": assist,
                    "goal_type": goal_type,
                    "shot_position": shot_position
                }
                st.rerun()


        elif st.session_state.selected_event == "pass":
            # Scegli la squadra dal nome reale
            team_name = st.selectbox(
                "Team Pass",
                [st.session_state.home_team['name'], st.session_state.away_team['name']]
            )


            if team_name == st.session_state.home_team['name']:
                players = st.session_state.team_players_home
            else:
                players = st.session_state.team_players_away


            passer = st.selectbox("Passer", [p['name'] for p in players])
            receiver = st.selectbox("Receiver", [p['name'] for p in players])
            


            pass_type = st.selectbox("Pass Type", ["Short pass", "Long pass", "Through ball", "Cross"])
            success = st.selectbox("Successful/Unsuccessful", ["Successful", "Unsuccessful"])

                
            # Costruisci kwargs DOPO aver aggiornato lo score
            st.session_state.kwargs = {
                "minute": minutes,
                "second": seconds,
                "competition": st.session_state.competition,
                "home_team": st.session_state.home_team['name'],
                "away_team": st.session_state.away_team['name'],
                "team_profile_home": st.session_state.team_profile_home,
                "team_profile_away": st.session_state.team_profile_away,
                "team_players_home": st.session_state.team_players_home,
                "team_players_away": st.session_state.team_players_away,
                "current_score": f"{st.session_state.score[0]}-{st.session_state.score[1]}",
                "team_involved": team_name,
                "passer": passer,
                "receiver": receiver,
                "pass_type": pass_type,
                "success": success
            }
        elif st.session_state.selected_event == "offside":
            # Scegli la squadra dal nome reale
            team_name = st.selectbox(
                "Team Offside",
                [st.session_state.home_team['name'], st.session_state.away_team['name']]
            )

            # Seleziona giocatori dalla squadra scelta
            if team_name == st.session_state.home_team['name']:
                players = st.session_state.team_players_home
            else:
                players = st.session_state.team_players_away         

            passer = st.selectbox("Passer", [p['name'] for p in players])
            receiver = st.selectbox("Receiver", [p['name'] for p in players])
            


            # Costruisci kwargs DOPO aver aggiornato lo score
            st.session_state.kwargs = {
                "minute": minutes,
                "second": seconds,
                "competition": st.session_state.competition,
                "home_team": st.session_state.home_team['name'],
                "away_team": st.session_state.away_team['name'],
                "team_profile_home": st.session_state.team_profile_home,
                "team_profile_away": st.session_state.team_profile_away,
                "team_players_home": st.session_state.team_players_home,
                "team_players_away": st.session_state.team_players_away,
                "current_score": f"{st.session_state.score[0]}-{st.session_state.score[1]}",
                "team_involved": team_name,
                "passer": passer,
                "receiver": receiver,
            }
        elif st.session_state.selected_event == "dribbling":
            # Scegli la squadra dal nome reale
            team_name = st.selectbox(
                "Team Dribbling",
                [st.session_state.home_team['name'], st.session_state.away_team['name']]
            )

            # Seleziona giocatori dalla squadra scelta
            if team_name == st.session_state.home_team['name']:
                players = st.session_state.team_players_home
                opponents = st.session_state.team_players_away
            else:
                players = st.session_state.team_players_away         
                opponents = st.session_state.team_players_home

            dribbler = st.selectbox("Dribbler", [p['name'] for p in players])
            opponent = st.selectbox("Opponent", [p['name'] for p in opponents])
            

            success = st.selectbox("Successful/Unsuccessful", ["Successful", "Unsuccessful"])
            # Fetch dati del giocatore
            dribbler_info, dribbler_stats, _ = fetch_player_data(dribbler)
                
            # Costruisci kwargs DOPO aver aggiornato lo score
            st.session_state.kwargs = {
                "minute": minutes,
                "second": seconds,
                "competition": st.session_state.competition,
                "home_team": st.session_state.home_team['name'],
                "away_team": st.session_state.away_team['name'],
                "team_profile_home": st.session_state.team_profile_home,
                "team_profile_away": st.session_state.team_profile_away,
                "team_players_home": st.session_state.team_players_home,
                "team_players_away": st.session_state.team_players_away,
                "current_score": f"{st.session_state.score[0]}-{st.session_state.score[1]}",
                "team_involved": team_name,
                "dribbler": dribbler,
                "dribbler_info": dribbler_info,
                "dribbler_stats": dribbler_stats,                
                "opponent": opponent,
                "success": success
            }
        elif st.session_state.selected_event == "tackle":
            # Scegli la squadra dal nome reale
            team_name = st.selectbox(
                "Team Tackling",
                [st.session_state.home_team['name'], st.session_state.away_team['name']]
            )

            # Seleziona giocatori dalla squadra scelta
            if team_name == st.session_state.home_team['name']:
                players = st.session_state.team_players_home
                opponents = st.session_state.team_players_away
            else:
                players = st.session_state.team_players_away         
                opponents = st.session_state.team_players_home            
            tackler = st.selectbox("Tackler", [p['name'] for p in players])
            opponent = st.selectbox("Opponent", [p['name'] for p in opponents])
            

            success = st.selectbox("Successful/Unsuccessful", ["Successful", "Unsuccessful"])
                
            tackler_info, tackler_stats, _ = fetch_player_data(tackler)
            # Costruisci kwargs DOPO aver aggiornato lo score
            st.session_state.kwargs = {
                "minute": minutes,
                "second": seconds,
                "competition": st.session_state.competition,
                "home_team": st.session_state.home_team['name'],
                "away_team": st.session_state.away_team['name'],
                "team_profile_home": st.session_state.team_profile_home,
                "team_profile_away": st.session_state.team_profile_away,
                "team_players_home": st.session_state.team_players_home,
                "team_players_away": st.session_state.team_players_away,
                "current_score": f"{st.session_state.score[0]}-{st.session_state.score[1]}",
                "team_involved": team_name,
                "tackler": tackler,
                "tackler_info": tackler_info,
                "tackler_stats": tackler_stats,
                "opponent": opponent,
                "success": success
            }

        elif st.session_state.selected_event == "foul":
            # Scegli la squadra dal nome reale
            team_name = st.selectbox(
                "Team Fouling",
                [st.session_state.home_team['name'], st.session_state.away_team['name']]
            )

            if team_name == st.session_state.home_team['name']:
                players = st.session_state.team_players_home
            else:
                players = st.session_state.team_players_away
            player = st.selectbox("Fouling Player", [p['name'] for p in players])
            

            reason = st.selectbox("Foul Reason", ["Handball", "Tripping", "Pushing", "Other"])
            card = st.selectbox("Card Type", ["Yellow", "Red", "None"])
                
            player_info, player_stats, _ = fetch_player_data(player)
            # Costruisci kwargs DOPO aver aggiornato lo score
            st.session_state.kwargs = {
                "minute": minutes,
                "second": seconds,
                "competition": st.session_state.competition,
                "home_team": st.session_state.home_team['name'],
                "away_team": st.session_state.away_team['name'],
                "team_profile_home": st.session_state.team_profile_home,
                "team_profile_away": st.session_state.team_profile_away,
                "team_players_home": st.session_state.team_players_home,
                "team_players_away": st.session_state.team_players_away,
                "current_score": f"{st.session_state.score[0]}-{st.session_state.score[1]}",
                "team_involved": team_name,
                "player": player,
                "player_info": player_info,
                "player_stats": player_stats,
                "reason": reason,
                "card": card
            }

        elif st.session_state.selected_event == "attempted_shot":
            # Scegli la squadra dal nome reale
            team_name = st.selectbox(
                "Team Shooting",
                [st.session_state.home_team['name'], st.session_state.away_team['name']]
            )

            # Seleziona giocatori dalla squadra scelta
            if team_name == st.session_state.home_team['name']:
                players = st.session_state.team_players_home
            else:
                players = st.session_state.team_players_away            
            shooter = st.selectbox("Shooting Player", [p['name'] for p in players])
            shot_outcomes = st.selectbox("Outcome", ["Saved", "Missed", "Blocked"])
            

            shot_position = st.selectbox("Shot Position", ["Inside box", "Outside box", "Penalty", "Free kick"])
                
            shooter_info, shooter_stats, shooter_achievements = fetch_player_data(shooter)
            # Costruisci kwargs DOPO aver aggiornato lo score
            st.session_state.kwargs = {
                "minute": minutes,
                "second": seconds,
                "competition": st.session_state.competition,
                "home_team": st.session_state.home_team['name'],
                "away_team": st.session_state.away_team['name'],
                "team_profile_home": st.session_state.team_profile_home,
                "team_profile_away": st.session_state.team_profile_away,
                "team_players_home": st.session_state.team_players_home,
                "team_players_away": st.session_state.team_players_away,
                "current_score": f"{st.session_state.score[0]}-{st.session_state.score[1]}",
                "team_involved": team_name,
                "shooter": shooter,
                "shooter_info": shooter_info,
                "shooter_stats": shooter_stats,
                "shooter_achievements": shooter_achievements,
                "outcome": shot_outcomes,
                "shot_position": shot_position
            }

        elif st.session_state.selected_event == "var_call":
            # Scegli la squadra dal nome reale
            team_name = st.selectbox(
                "Team",
                [st.session_state.home_team['name'], st.session_state.away_team['name']]
            )

            var_reason = st.selectbox("VAR call reason", ["Potential penalty", "Offside", "Handball", "Foul", "Goal review", "Mistaken identity", "Other"])
                            
            # Costruisci kwargs DOPO aver aggiornato lo score
            st.session_state.kwargs = {
                "minute": minutes,
                "second": seconds,
                "competition": st.session_state.competition,
                "home_team": st.session_state.home_team['name'],
                "away_team": st.session_state.away_team['name'],
                "team_profile_home": st.session_state.team_profile_home,
                "team_profile_away": st.session_state.team_profile_away,
                "team_players_home": st.session_state.team_players_home,
                "team_players_away": st.session_state.team_players_away,
                "current_score": f"{st.session_state.score[0]}-{st.session_state.score[1]}",
                "team_involved": team_name,
                "reason": var_reason
            }

        elif st.session_state.selected_event == "start_half_end_game":
            # Scegli la squadra dal nome reale


            game_status = st.selectbox("Game status", ["Start First Half", "End First Half", "Start Second Half", "End Second Half"])
                            
            # Costruisci kwargs DOPO aver aggiornato lo score
            st.session_state.kwargs = {
                "minute": minutes,
                "second": seconds,
                "competition": st.session_state.competition,
                "home_team": st.session_state.home_team['name'],
                "away_team": st.session_state.away_team['name'],
                "team_profile_home": st.session_state.team_profile_home,
                "team_profile_away": st.session_state.team_profile_away,
                "team_players_home": st.session_state.team_players_home,
                "team_players_away": st.session_state.team_players_away,
                "current_score": f"{st.session_state.score[0]}-{st.session_state.score[1]}",
                "game_status": game_status
            }

        elif st.session_state.selected_event == "substitution":
            # Scegli la squadra dal nome reale
            team_name = st.selectbox(
                "Team Substituting",
                [st.session_state.home_team['name'], st.session_state.away_team['name']]
            )

            # Seleziona giocatori dalla squadra scelta
            if team_name == st.session_state.home_team['name']:
                players = st.session_state.team_players_home
            else:
                players = st.session_state.team_players_away         

            player_in = st.selectbox("Player in", [p['name'] for p in players])
            player_out = st.selectbox("Player out", [p['name'] for p in players])
            in_info, in_stats, in_achievements = fetch_player_data(player_in)
            out_info, out_stats, out_achievements = fetch_player_data(player_out)
                        
            # Costruisci kwargs DOPO aver aggiornato lo score
            st.session_state.kwargs = {
                "minute": minutes,
                "second": seconds,
                "competition": st.session_state.competition,
                "home_team": st.session_state.home_team['name'],
                "away_team": st.session_state.away_team['name'],
                "team_profile_home": st.session_state.team_profile_home,
                "team_profile_away": st.session_state.team_profile_away,
                "team_players_home": st.session_state.team_players_home,
                "team_players_away": st.session_state.team_players_away,
                "current_score": f"{st.session_state.score[0]}-{st.session_state.score[1]}",
                "team_involved": team_name,
                "player_in": player_in,
                "player_in_info": in_info,
                "player_in_stats": in_stats,
                "player_in_achievements": in_achievements,
                "player_out": player_out,
                "player_out_info": out_info,
                "player_out_stats": out_stats,
                "player_out_achievements": out_achievements
            }

if st.session_state.selected_event and st.session_state.kwargs:
    prompt = build_prompt(
        st.session_state.selected_event,
        **st.session_state.kwargs
    )

    st.subheader("=== Generated Prompt ===")
    st.text(prompt)

