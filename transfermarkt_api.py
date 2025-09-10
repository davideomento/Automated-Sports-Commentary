import requests
import time

BASE_URL = "http://127.0.0.1:8000"
MAX_RETRIES = 10
RETRY_DELAY = 1  # secondi


def safe_get(url):
    """Esegue GET con retry, restituisce None se non va a buon fine"""
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = requests.get(url)
            if response.ok:
                return response.json()
            else:
                print(f"[Attempt {attempt}] Error {response.status_code} for URL: {url}")
        except requests.exceptions.RequestException as e:
            print(f"[Attempt {attempt}] RequestException: {e} for URL: {url}")
        time.sleep(RETRY_DELAY)
    print(f"Failed to get data from {url} after {MAX_RETRIES} attempts.")
    return None


def search_team_by_name(name):
    results = safe_get(f"{BASE_URL}/clubs/search/{name}")
    if results and 'results' in results and len(results['results']) > 0:
        return results['results'][0]['id']
    return None


def search_player_by_name(name):
    results = safe_get(f"{BASE_URL}/players/search/{name}")
    if results and 'results' in results and len(results['results']) > 0:
        return results['results'][0]['id']
    return None


def get_team_info(club_id):
    return safe_get(f"{BASE_URL}/clubs/{club_id}/profile")


def get_team_players(club_id):
    data = safe_get(f"{BASE_URL}/clubs/{club_id}/players")
    if data and "players" in data:
        return data["players"]
    return []


def get_player_info(player_id):
    return safe_get(f"{BASE_URL}/players/{player_id}/profile")


def get_player_stats(player_id):
    return safe_get(f"{BASE_URL}/players/{player_id}/stats")


def get_player_achievements(player_id):
    return safe_get(f"{BASE_URL}/players/{player_id}/achievements")


def search_competition_by_name(name):
    results = safe_get(f"{BASE_URL}/competitions/search/{name}")
    if results and 'results' in results and len(results['results']) > 0:
        return results['results'][0]['id']
    return None


def get_competition_clubs(competition_id):
    return safe_get(f"{BASE_URL}/competitions/{competition_id}/clubs")

if __name__ == "__main__":
    # Get competition info
    competition_name = input("Enter competition name: ")
    competition_id = search_competition_by_name(competition_name)

    if competition_id:
        comp_info = get_competition_clubs(competition_id)
        if comp_info and "clubs" in comp_info:
            clubs = comp_info["clubs"]
            print(f"\nClubs in {competition_name}:")  # usa il nome inserito dall'utente
            for i, club in enumerate(clubs, start=1):
                print(f"{i}. {club['name']}")
        else:
            # Mostra nome e ID per chiarezza
            print(f"❌ Could not retrieve clubs for {competition_name} (ID: {competition_id})")

    # Get teams
    team_a_name = input("\nEnter Team A name (or number from list above): ")
    team_b_name = input("Enter Team B name (or number from list above): ")

    # Convert numeric selection to club name if user enters a number
    if team_a_name.isdigit() and comp_info and "clubs" in comp_info:
        index = int(team_a_name) - 1
        if 0 <= index < len(comp_info["clubs"]):
            team_a_name = comp_info["clubs"][index]["name"]

    if team_b_name.isdigit() and comp_info and "clubs" in comp_info:
        index = int(team_b_name) - 1
        if 0 <= index < len(comp_info["clubs"]):
            team_b_name = comp_info["clubs"][index]["name"]

    # Search for teams and player as before
    team_a_id = search_team_by_name(team_a_name)
    team_b_id = search_team_by_name(team_b_name)
    player_name = input("Enter player name: ")
    player_id = search_player_by_name(player_name)

    if team_a_id:
        print("\nTEAM A INFO:")
        team_a_info = get_team_info(team_a_id)
        team_a_players = get_team_players(team_a_id)
        print(team_a_info)
        print("\nTeam A Players:")
        print(team_a_players)

    if team_b_id:
        print("\nTEAM B INFO:")
        team_b_info = get_team_info(team_b_id)
        team_b_players = get_team_players(team_b_id)
        print(team_b_info)
        print("\nTeam B Players:")
        print(team_b_players)

    if player_id:
        print("\nPLAYER INFO:")
        player_info = get_player_info(player_id)
        print(player_info)

        print("\nPLAYER STATS:")
        player_stats = get_player_stats(player_id)
        print(player_stats)

        print("\nPLAYER ACHIEVEMENTS:")
        player_achievements = get_player_achievements(player_id)
        print(player_achievements)


def clean_team_profile(team_profile):
    """Pulisce il profilo della squadra, restituisce None se team_profile è None"""
    if team_profile is None:
        return None

    clean_profile = team_profile.copy()
    
    keys_to_remove = [
        "id", "url", "fax", "addressLine1", "addressLine2", "addressLine3",
        "tel", "website", "email", "members", "membersDate", "legalForm",
        "colors", "historicalCrests", "otherSports", "confederation", "fifaWorldRanking"
    ]
    
    for key in keys_to_remove:
        clean_profile.pop(key, None)
    
    return clean_profile


def clean_player_profile(player_profile):
    """Pulisce il profilo del giocatore, restituisce None se player_profile è None"""
    if player_profile is None:
        return None

    clean_profile = player_profile.copy()
    
    keys_to_remove = [
        "id", "url", "imageUrl", "outfitter", "socialMedia", "trainerProfile",
        "relatives"
    ]
    
    for key in keys_to_remove:
        clean_profile.pop(key, None)
    
    return clean_profile


def clean_player_stats_achievements(player_stats):
    """Pulisce le statistiche o achievements del giocatore, restituisce None se player_stats è None"""
    if player_stats is None:
        return None

    clean_stats = player_stats.copy()
    
    keys_to_remove = [
        "id"
    ]
    
    for key in keys_to_remove:
        clean_stats.pop(key, None)
    
    return clean_stats
