import pandas as pd

# Load Fantasy Premier League player statistics
df = pd.read_csv("data/raw/extracted_data_fpl/2024-25/cleaned_players.csv")  # Replace with your actual CSV filename

# Clean names for lookup
df["full_name"] = df["first_name"].str.strip() + " " + df["second_name"].str.strip()
df["full_name"] = df["full_name"].str.lower()

def get_player_context(name):
    """
    Retrieves a few key stats useful for generating realistic football commentary
    based on a player's recent performance.
    """
    name = name.lower()
    matches = df[df["full_name"].str.contains(name)]

    if matches.empty:
        return f"No stats found for player: {name}"

    # If multiple players found, choose the first one (or add logic to disambiguate)
    player = matches.iloc[0]

    # Extract only useful stats for natural language commentary
    context = {
        "name": player["full_name"].title(),
        "position": player["element_type"],  # You might want to map int to POS string
        "goals": int(player["goals_scored"]),
        "assists": int(player["assists"]),
        "minutes_played": int(player["minutes"]),
        "goals_conceded": int(player["goals_conceded"]),
        "clean_sheets": int(player["clean_sheets"]),
        "yellow_cards": int(player["yellow_cards"]),
        "red_cards": int(player["red_cards"]),
        "influence": round(player["influence"], 1),
        "threat": round(player["threat"], 1),
        "creativity": round(player["creativity"], 1),
        "total_points": int(player["total_points"])
    }

    return context

# Example usage
if __name__ == "__main__":
    player_name = input("Enter player name: ")
    result = get_player_context(player_name)
    print(result)
