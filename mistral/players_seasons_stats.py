import pandas as pd
import json
import os
import zipfile

# Percorso allo zip
zip_path = "data/RAG/FantasyPremierLeague.zip"
extract_to = "data/RAG/fpl"

# Estrai ZIP se non esiste
if not os.path.exists(extract_to):
    os.makedirs(extract_to, exist_ok=True)
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

# Posizioni
element_types = {
    1: "Goalkeeper",
    2: "Defender",
    3: "Midfielder",
    4: "Forward"
}

# Anni da considerare
seasons = [f"{y}-{str(y+1)[-2:]}" for y in range(2022, 2025)]

documents = []

for season in seasons:
    player_path = f"data/RAG/fpl/data/{season}/players_raw.csv"
    team_path = f"data/RAG/fpl/data/{season}/teams.csv"

    # Salta la stagione se i file non esistono
    if not os.path.exists(player_path) or not os.path.exists(team_path):
        print(f"Skipping missing season: {season}")
        continue

    players = pd.read_csv(player_path)
    teams = pd.read_csv(team_path)

    team_map = dict(zip(teams['id'], teams['name']))

    for _, row in players.iterrows():
        name = f"{row['first_name']} {row['second_name']}"
        team = team_map.get(row['team'], "Unknown")
        position = element_types.get(row['element_type'], "Unknown")

        doc = f"""
        Name: {name}
        Team: {team}
        Position: {position}
        Season: {season}
        
        Minutes Played: {row['minutes']}
        Goals Scored: {row['goals_scored']}
        Assists: {row['assists']}
        Clean Sheets: {row['clean_sheets']}
        Yellow Cards: {row['yellow_cards']}
        Red Cards: {row['red_cards']}

        
        Status: {row['status']}
        """
        description = (
            f"{name} played for {team} as a {position} during the {season} season. "
            f"He played {row['minutes']} minutes, scored {row['goals_scored']} goals, "
            f"provided {row['assists']} assists, and kept {row['clean_sheets']} clean sheets. "
            f"He received {row['yellow_cards']} yellow cards and {row['red_cards']} red cards. "
            f"His status was '{row['status']}' at the end of the season."
        )
        documents.append({
            "player": name,
            "season": season,
            "team": team,
            "position": position,
            "text": description
        })

# Salva in JSON
os.makedirs("data/RAG", exist_ok=True)
with open("data/RAG/player_docs_clean.json", "w") as f:
    json.dump(documents, f, indent=2)

print(f"✅ Salvati {len(documents)} documenti da {len(seasons)} stagioni.")
