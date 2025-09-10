import os
import glob
import pandas as pd
import json

# Helper to safely access a value or return 'unknown'
def safe_get(row, col):
    return row[col] if col in row and pd.notna(row[col]) else "unknown"

# Load team name mapping
team_map_df = pd.read_csv("data/RAG/fpl/data/master_team_list.csv")  # Update path if needed
team_name_lookup = {
    (str(row["season"]), int(row["team"])): row["team_name"]
    for _, row in team_map_df.iterrows()
}

all_data = []

# Process all gw*.csv files
for csv_file in glob.glob("data/RAG/fpl/data/*/gws/gw*.csv"):
    df = pd.read_csv(csv_file, encoding='latin1')
    season = csv_file.split(os.sep)[-3]
    gw = int(csv_file.split(os.sep)[-1].replace("gw", "").replace(".csv", ""))

    for _, row in df.iterrows():
        opponent_id = safe_get(row, "opponent_team")
        opponent_name = team_name_lookup.get((season, int(opponent_id)) if opponent_id != "unknown" else None, "unknown")
        result = f"{safe_get(row, 'team_h_score')} - {safe_get(row, 'team_a_score')}"
        home_away = "home" if str(safe_get(row, "was_home")).lower() == "true" else "away"

        description = (
            f"In the {season} season, gameweek {gw}, {safe_get(row, 'name')} played {safe_get(row, 'minutes')} minutes "
            f"{home_away} against {opponent_name} (final score: {result}). "
            f"He scored {safe_get(row, 'goals_scored')} goals, assisted {safe_get(row, 'assists')} times. "
            f"Defensively, they conceded {safe_get(row, 'goals_conceded')} goals. "
            f"He also made {safe_get(row, 'saves')} saves, and received {safe_get(row, 'yellow_cards')} yellow cards and {safe_get(row, 'red_cards')} red cards. "
            f"Other stats include {safe_get(row, 'own_goals')} own goals, and {safe_get(row, 'penalties_missed')} penalties missed."
        ).strip()

        record = {
            "player": safe_get(row, "name"),
            "season": season,
            "gameweek": gw,
            "stats": {
                "minutes": safe_get(row, "minutes"),
                "position": safe_get(row, "position"),
                "goals": safe_get(row, "goals_scored"),
                "assists": safe_get(row, "assists"),
                "goals_conceded": safe_get(row, "goals_conceded"),
                "saves": safe_get(row, "saves"),
                "clean_sheets": safe_get(row, "clean_sheets"),
                "own_goals": safe_get(row, "own_goals"),
                "penalties_missed": safe_get(row, "penalties_missed"),
                "penalties_saved": safe_get(row, "penalties_saved"),
                "yellow_cards": safe_get(row, "yellow_cards"),
                "red_cards": safe_get(row, "red_cards"),
                "ict_index": safe_get(row, "ict_index"),
                "influence": safe_get(row, "influence"),
                "threat": safe_get(row, "threat"),
                "creativity": safe_get(row, "creativity"),
                "xP": safe_get(row, "xP"),
                "starts": safe_get(row, "starts"),
                "kickoff_time": safe_get(row, "kickoff_time")
            },
            "description": description
        }

        all_data.append(record)

# Save to JSON
os.makedirs("data/RAG", exist_ok=True)
with open("data/RAG/players_week_docs_clean.json", "w", encoding="utf-8") as f:
    json.dump(all_data, f, indent=2, ensure_ascii=False)

print(f"✅ Saved {len(all_data)} records to players_week_docs_clean.json")
