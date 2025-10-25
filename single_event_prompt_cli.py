from transfermarkt_api import (
    search_player_by_name,
    get_player_info,
    get_player_stats, 
    get_player_achievements,
    get_competition_clubs,
    get_team_info,
    get_team_players,   
    search_competition_by_name
)
from prompt_builder import build_prompt 


def fetch_player_data(name):
    """Search player and fetch info, stats, achievements."""
    player_id = search_player_by_name(name)
    if not player_id:
        return None, None, None
    info = get_player_info(player_id)
    stats = get_player_stats(player_id)
    achievements = get_player_achievements(player_id)
    return info, stats, achievements


def select_team_and_players(home_team, home_stats, away_team, away_stats):
    """Utility to choose a team and return its players."""
    print("\nSelect the team involved:")
    print(f"1. {home_team['name']}")
    print(f"2. {away_team['name']}")
    team_choice = input("Enter team number: ").strip()
    if team_choice == "1":
        return home_team['name'], home_stats, away_stats
    elif team_choice == "2":
        return away_team['name'], away_stats, home_stats
    else:
        print("❌ Invalid team choice.")
        return None, None, None


def main():
    print("=== Football Event Prompt Builder ===")
    
    competitions = {
        "1": "Premier League",
        "2": "La Liga",
        "3": "Serie A",
        "4": "Bundesliga",
        "5": "Ligue 1",
    }

    # Select competition
    print("\nSelect Competition:")
    for num, name in competitions.items():
        print(f"{num}. {name}")
    
    competition_choice = input("Enter choice number: ").strip()
    competition_name = competitions.get(competition_choice)
    if not competition_name:
        print("❌ Invalid competition choice.")
        return

    competition_id = search_competition_by_name(competition_name)
    if not competition_id:
        print(f"❌ Could not find ID for {competition_name}.")
        return

    comp_info = get_competition_clubs(competition_id)
    if not comp_info or "clubs" not in comp_info:
        print(f"❌ No clubs found for {competition_name}.")
        return

    clubs = comp_info["clubs"]

    # Display clubs
    print(f"\nSelect Home and Away Teams for {competition_name}:")
    for idx, club in enumerate(clubs, 1):
        print(f"{idx}. {club['name']}")

    try:
        home_idx = int(input("Select Home Team number: ").strip())
        away_idx = int(input("Select Away Team number: ").strip())
        home_team = clubs[home_idx - 1]
        away_team = clubs[away_idx - 1]
    except (ValueError, IndexError):
        print("❌ Invalid team selection.")
        return


    team_profile_home = get_team_info(home_team['id'])
    team_players_home = get_team_players(home_team['id'])
    team_profile_away = get_team_info(away_team['id'])
    team_players_away = get_team_players(away_team['id'])

    event_types = {
        "1": "goal",
        "2": "foul",
        "3": "attempted_shot",
        "4": "dribbling",
        "5": "tackle",
        "6": "pass",
        "7": "var_call",
        "8": "offside",
        "9": "start_half_end_game",
        "10": "substitution"
        # add additional time
        # add penalty, freekick, throw-in, corner, penalty 
        # injury
    }

    print("\nSelect Event Type:")
    for num, name in event_types.items():
        print(f"{num}. {name.capitalize()}")
    
    choice = input("Enter choice number: ").strip()
    event_type = event_types.get(choice)
    if not event_type:
        print("❌ Invalid choice.")
        return

    minute = input("Enter event minute: ").strip()
    current_score = input("Enter current score (e.g., 1-0): ").strip()

    kwargs = {
        "minute": minute,
        "competition": competition_name,
        "home_team": home_team['name'],
        "away_team": away_team['name'],
        "team_profile_home": team_profile_home,
        "team_profile_away": team_profile_away,
        "team_players_home": team_players_home,
        "team_players_away": team_players_away,
        "current_score": current_score
    }

    # ==== EVENT-SPECIFIC PLAYER SELECTION ====
    if event_type == "goal":
        selected_team_name, selected_team_players, _ = select_team_and_players(home_team, team_players_home, away_team, team_players_away)
        if not selected_team_name:
            return

        print(f"\nSelect scorer from {selected_team_name}:")
        for idx, player in enumerate(selected_team_players, 1):
            print(f"{idx}. {player['name']}")
        scorer_idx = int(input("Enter scorer number: ").strip()) - 1
        scorer_name = selected_team_players[scorer_idx]['name']
        scorer_info, scorer_stats, scorer_achievements = fetch_player_data(scorer_name)

        goal_types = {"1": "Right foot", "2": "Left foot", "3": "Header", "4": "Other"}
        shot_positions = {"1": "Inside box", "2": "Outside box", "3": "Penalty spot", "4": "Free kick"}
        print("\nGoal type options:")
        for k, v in goal_types.items(): print(f"{k}. {v}")
        goal_type = goal_types.get(input("Select goal type: "), "Unknown")

        print("\nShot position options:")
        for k, v in shot_positions.items(): print(f"{k}. {v}")
        shot_position = shot_positions.get(input("Select shot position: "), "Unknown")

        print(f"\nSelect the player who made the assist from {selected_team_name}:")
        print("0. None")  # Opzione per nessun assist
        for idx, player in enumerate(selected_team_players, 1):
            print(f"{idx}. {player['name']}")

        assist_input = input("Enter assist player number (or 0 for None): ").strip()

        if assist_input == "0" or assist_input.lower() == "none":
            assist_name = None
        else:
            assist_idx = int(assist_input) - 1
            assist_name = selected_team_players[assist_idx]['name']

        kwargs.update({
            "team_involved": selected_team_name,
            "scorer": scorer_name,
            "scorer_info": scorer_info,
            "scorer_stats": scorer_stats,
            "scorer_achievements": scorer_achievements,
            "assist": assist_name,
            "goal_type": goal_type,
            "shot_position": shot_position
        })

    elif event_type == "pass":
        selected_team_name, selected_team_players, _ = select_team_and_players(
            home_team, team_players_home, away_team, team_players_away
        )
        if not selected_team_name:
            return

        # Passer
        print("\nSelect passer from this team:")
        for idx, player in enumerate(selected_team_players, 1):
            print(f"{idx}. {player['name']}")
        passer_idx = int(input("Enter passer number: ").strip()) - 1
        passer_name = selected_team_players[passer_idx]['name']

        # Receiver
        print("\nSelect receiver from same team:")
        for idx, player in enumerate(selected_team_players, 1):
            print(f"{idx}. {player['name']}")
        receiver_idx = int(input("Enter receiver number: ").strip()) - 1
        receiver_name = selected_team_players[receiver_idx]['name']

        # Pass type (numeric)
        pass_types = {
            "1": "Short pass",
            "2": "Long pass",
            "3": "Through ball",
            "4": "Cross"
        }
        print("\nPass type options:")
        for k, v in pass_types.items():
            print(f"{k} = {v}")
        pass_type_choice = input("Select pass type number (1-4): ").strip()
        pass_type = pass_types.get(pass_type_choice, "Unknown")

        # Pass success (0 = success, 1 = fail)
        success_choice = input("Was the pass successful? (1 = Yes, 0 = No): ").strip()
        success = "successful" if success_choice == "1" else "unsuccessful"

        kwargs.update({
            "team_involved": selected_team_name,
            "passer": passer_name,
            "receiver": receiver_name,
            "pass_type": pass_type,
            "success": success
        })

    elif event_type == "offside":
        selected_team_name, selected_team_players, _ = select_team_and_players(
            home_team, team_players_home, away_team, team_players_away
        )
        if not selected_team_name:
            return

        # Passer
        print("\nSelect passer from this team:")
        for idx, player in enumerate(selected_team_players, 1):
            print(f"{idx}. {player['name']}")
        passer_idx = int(input("Enter passer number: ").strip()) - 1
        passer_name = selected_team_players[passer_idx]['name']

        # Receiver
        print("\nSelect receiver from same team:")
        for idx, player in enumerate(selected_team_players, 1):
            print(f"{idx}. {player['name']}")
        receiver_idx = int(input("Enter receiver number: ").strip()) - 1
        receiver_name = selected_team_players[receiver_idx]['name']

        kwargs.update({
            "team_involved": selected_team_name,
            "passer": passer_name,
            "receiver": receiver_name
        })

    # Dribbling event
    elif event_type == "dribbling":
        selected_team_name, selected_team_players, opposing_team_players = select_team_and_players(
            home_team, team_players_home, away_team, team_players_away
        )
        if not selected_team_name:
            return

        print("\nSelect dribbler:")
        for idx, player in enumerate(selected_team_players, 1):
            print(f"{idx}. {player['name']}")
        dribbler_idx = int(input("Enter dribbler number: ").strip()) - 1
        dribbler_name = selected_team_players[dribbler_idx]['name']
        dribbler_info, dribbler_stats, dribbler_achievements = fetch_player_data(dribbler_name)

        print("\nSelect opponent:")
        for idx, player in enumerate(opposing_team_players, 1):
            print(f"{idx}. {player['name']}")
        opponent_idx = int(input("Enter opponent number: ").strip()) - 1
        opponent_name = opposing_team_players[opponent_idx]['name']

        success_choice = input("Was the dribble successful? (1 = Yes, 0 = No): ").strip()
        success = "successful" if success_choice == "1" else "unsuccessful"

        kwargs.update({
            "team_involved": selected_team_name,
            "dribbler": dribbler_name,
            "dribbler_info": dribbler_info,
            "dribbler_stats": dribbler_stats,
            "opponent": opponent_name,
            "success": success
        })

    # Tackle event
    elif event_type == "tackle":
        selected_team_name, selected_team_players, opposing_team_players = select_team_and_players(
            home_team, team_players_home, away_team, team_players_away
        )
        if not selected_team_name:
            return

        print("\nSelect tackler:")
        for idx, player in enumerate(selected_team_players, 1):
            print(f"{idx}. {player['name']}")
        tackler_idx = int(input("Enter tackler number: ").strip()) - 1
        tackler_name = selected_team_players[tackler_idx]['name']
        tackler_info, tackler_stats, tackler_achievements = fetch_player_data(tackler_name)

        print("\nSelect opponent:")
        for idx, player in enumerate(opposing_team_players, 1):
            print(f"{idx}. {player['name']}")
        opponent_idx = int(input("Enter opponent number: ").strip()) - 1
        opponent_name = opposing_team_players[opponent_idx]['name']

        success_choice = input("Was the tackle successful? (1 = Yes, 0 = No): ").strip()
        success = "successful" if success_choice == "1" else "unsuccessful"

        kwargs.update({
            "team_involved": selected_team_name,
            "tackler": tackler_name,
            "tackler_info": tackler_info,
            "tackler_stats": tackler_stats,
            "opponent": opponent_name,
            "success": success
        })


    elif event_type == "foul":
        selected_team_name, selected_team_players, _ = select_team_and_players(home_team, team_players_home, away_team, team_players_away)
        if not selected_team_name:
            return

        print("\nSelect player committing the foul:")
        for idx, player in enumerate(selected_team_players, 1):
            print(f"{idx}. {player['name']}")
        player_idx = int(input("Enter player number: ").strip()) - 1
        player_name = selected_team_players[player_idx]['name']
        player_info, player_stats, player_achievements = fetch_player_data(player_name)

        foul_reasons = {"1": "Handball", "2": "Tripping", "3": "Pushing", "4": "Other"}
        card_types = {"1": "Yellow", "2": "Red", "3": "None"}
        print("\nFoul reason options:")
        for k, v in foul_reasons.items(): print(f"{k}. {v}")
        reason = foul_reasons.get(input("Select reason number: "), "Unknown")
        print("\nCard options:")
        for k, v in card_types.items(): print(f"{k}. {v}")
        card = card_types.get(input("Select card number: "), "None")

        kwargs.update({
            "team_involved": selected_team_name,
            "player": player_name,
            "player_info": player_info,
            "player_stats": player_stats,
            "reason": reason,
            "card": card
        })

    elif event_type == "attempted_shot":
        selected_team_name, selected_team_players, _ = select_team_and_players(home_team, team_players_home, away_team, team_players_away)
        if not selected_team_name:
            return

        print("\nSelect shooter from this team:")
        for idx, player in enumerate(selected_team_players, 1):
            print(f"{idx}. {player['name']}")
        shooter_idx = int(input("Enter shooter number: ").strip()) - 1
        shooter_name = selected_team_players[shooter_idx]['name']
        shooter_info, shooter_stats, shooter_achievements = fetch_player_data(shooter_name)

        shot_outcomes = {"1": "Saved", "2": "Missed", "3": "Blocked"}
        shot_positions = {"1": "Inside box", "2": "Outside box", "3": "Penalty spot", "4": "Free kick"}
        print("\nShot outcome options:")
        for k, v in shot_outcomes.items(): print(f"{k}. {v}")
        outcome = shot_outcomes.get(input("Select outcome number: "), "Unknown")

        print("\nShot position options:")
        for k, v in shot_positions.items(): print(f"{k}. {v}")
        shot_position = shot_positions.get(input("Select position number: "), "Unknown")

        kwargs.update({
            "team_involved": selected_team_name,
            "shooter": shooter_name,
            "shooter_info": shooter_info,
            "shooter_stats": shooter_stats,
            "shooter_achievements": shooter_achievements,
            "outcome": outcome,
            "shot_position": shot_position
        })

    elif event_type == "var_call":
        selected_team_name, selected_team_players, _ = select_team_and_players(
            home_team, team_players_home, away_team, team_players_away
        )
        if not selected_team_name:
            return

        var_reasons = {
            "1": "Potential penalty",
            "2": "Offside",
            "3": "Handball",
            "4": "Foul",
            "5": "Goal review",
            "6": "Mistaken identity",
            "7": "Other"
        }
        # add outcome of var call
        print("\nVAR call reason options:")
        for k, v in var_reasons.items():
            print(f"{k}. {v}")

        reason_choice = input("Select reason number: ").strip()
        reason = var_reasons.get(reason_choice, "Unknown")

        kwargs.update({
            "team_involved": selected_team_name,
            "reason": reason
        })

    elif event_type == "start_half_end_game":
        status_options = {
            "0": "Start First Half",
            "1": "End First Half",
            "2": "Start Second Half",
            "3": "End Second Half",
        }
        print("\nGame status options:")
        for k, v in status_options.items():
            print(f"{k}. {v}")

        status_choice = input("Select game status number: ").strip()
        game_status = status_options.get(status_choice, "Unknown")

        kwargs.update({
            "game_status": game_status
        })

    elif event_type == "substitution":
        selected_team_name, selected_team_players, _ = select_team_and_players(home_team, team_players_home, away_team, team_players_away)
        if not selected_team_name:
            return

        print("Select player coming in:")
        for idx, player in enumerate(selected_team_players, 1):
            print(f"{idx}. {player['name']}")
        in_idx = int(input("Enter player in number: ").strip()) - 1
        player_in = selected_team_players[in_idx]['name']
        in_info, in_stats, in_achievements = fetch_player_data(player_in)

        print("Select player going out:")
        for idx, player in enumerate(selected_team_players, 1):
            print(f"{idx}. {player['name']}")
        out_idx = int(input("Enter player out number: ").strip()) - 1
        player_out = selected_team_players[out_idx]['name']
        out_info, out_stats, out_achievements = fetch_player_data(player_out)

        kwargs.update({
            "team_involved": selected_team_name,
            "player_in": player_in,
            "player_in_info": in_info,
            "player_in_stats": in_stats,
            "player_in_achievements": in_achievements,
            "player_out": player_out,
            "player_out_info": out_info,
            "player_out_stats": out_stats,
            "player_out_achievements": out_achievements
        })

    print("\n✅ Event data collected successfully!")

    try:
        # Build the final prompt
        prompt = build_prompt(event_type, **kwargs)
        print("\n=== Generated Prompt ===")
        print(prompt)


    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
