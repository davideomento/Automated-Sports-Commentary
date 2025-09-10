import requests

BASE_URL = "http://127.0.0.1:8000"

def search_team_by_name(name):
    url = f"{BASE_URL}/clubs/search/{name}"
    response = requests.get(url)
    if response.ok:
        results = response.json()
        if results and 'results' in results and len(results['results']) > 0:
            return results['results'][0]['id']
        else:
            print(f"No team found with the name '{name}'")
            return None
    else:
        print(f"Error searching team: {response.status_code}")
        return None


def search_player_by_name(name):
    url = f"{BASE_URL}/players/search/{name}"
    response = requests.get(url)
    if response.ok:
        results = response.json()
        if results and 'results' in results and len(results['results']) > 0:
            return results['results'][0]['id']
        else:
            print(f"No player found with the name '{name}'")
            return None
    else:
        print(f"Error searching player: {response.status_code}")
        return None

def get_team_info(club_id):
    url = f"{BASE_URL}/clubs/{club_id}/profile"
    response = requests.get(url)
    if response.ok:
        return response.json()
    else:
        print(f"Error retrieving team info for {club_id}: {response.status_code}")
        return None
    
def get_team_players(club_id):
    url = f"{BASE_URL}/clubs/{club_id}/players"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        # Assumiamo che la chiave principale sia 'players' e sia una lista
        return data.get('players', [])  
    except requests.exceptions.RequestException as e:
        print(f"Errore nel recupero dei giocatori per il club {club_id}: {e}")
        return []  # lista vuota in caso di errore
    
def get_player_info(player_id):
    url = f"{BASE_URL}/players/{player_id}/profile"
    response = requests.get(url)
    if response.ok:
        return response.json()
    else:
        print(f"Error retrieving player info for {player_id}: {response.status_code}")
        return None

def get_player_stats(player_id):
    url = f"{BASE_URL}/players/{player_id}/stats"
    response = requests.get(url)
    if response.ok:
        return response.json()
    else:
        print(f"Error retrieving player stats for {player_id}: {response.status_code}")
        return None

def get_player_achievements(player_id):
    url = f"{BASE_URL}/players/{player_id}/achievements"
    response = requests.get(url)
    if response.ok:
        return response.json()
    else:
        print(f"Error retrieving player achievements for {player_id}: {response.status_code}")
        return None
    
def search_competition_by_name(name):
    """Cerca la competizione per nome e restituisce l'ID."""
    url = f"{BASE_URL}/competitions/search/{name}"
    response = requests.get(url)
    if response.ok:
        results = response.json()
        if results and 'results' in results and len(results['results']) > 0:
            return results['results'][0]['id']
        else:
            print(f"No competition found with the name '{name}'")
            return None
    else:
        print(f"Error searching competition: {response.status_code}")
        return None

def get_competition_clubs(competition_id):
    """Restituisce info dettagliate della competizione."""
    url = f"{BASE_URL}/competitions/{competition_id}/clubs"
    response = requests.get(url)
    if response.ok:
        return response.json()
    else:
        print(f"Error retrieving competition info for {competition_id}: {response.status_code}")
        return None

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
    clean_profile = team_profile.copy()
    
    keys_to_remove = [
        "id", "url", "fax", "addressLine1", "addressLine2", "addressLine3",
         "tel", "fax", "website", "email", "members", "membersDate", "legalForm"
        "colors", "historicalCrests", "otherSports", "confederation", "fifaWorldRanking"
    ]
    
    for key in keys_to_remove:
        clean_profile.pop(key, None)  
    
    return clean_profile

def clean_player_profile(player_profile):
    if player_profile is None:
        raise ValueError("player_profile is None — fetch_player_data likely failed to get player data")
    clean_profile = player_profile.copy()
    
    keys_to_remove = [
        "id", "url", "imageUrl", "outfitter", "socialMedia", "trainerProfile",
         "relatives"
    ]
    
    for key in keys_to_remove:
        clean_profile.pop(key, None) 
    
    return clean_profile

def clean_player_stats_achievements(player_stats):
    clean_stats = player_stats.copy()
    
    keys_to_remove = [
        "id"
    ]
    
    for key in keys_to_remove:
        clean_stats.pop(key, None) 
    
    return clean_stats