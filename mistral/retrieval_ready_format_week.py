import json
import re
import os

# Load your raw match-level data
with open("data/RAG/players_week_docs_clean.json", "r", encoding="utf-8") as f:
    raw_data = json.load(f)

converted_data = []

for entry in raw_data:
    desc = entry["description"]
    stats = entry["stats"]

    # Extract home/away, opponent, and score using regex
    match = re.search(r"(home|away) against (.+?) \(final score: ([\d ]+-[\d ]+)\)", desc)
    if match:
        home_away = match.group(1)
        opponent = match.group(2)
        score = match.group(3)
    else:
        home_away, opponent, score = "unknown", "unknown", "unknown"

    converted_data.append({
        "content": desc,
        "metadata": {
            "player": entry["player"],
            "season": entry["season"],
            "gameweek": entry["gameweek"],
            "position": stats["position"],
            "minutes": stats["minutes"],
            "goals": stats["goals"],
            "assists": stats["assists"],
            "team_home_or_away": home_away,
            "opponent": opponent,
            "score": score,
            "kickoff_time": stats["kickoff_time"]
        }
    })

os.makedirs("data/RAG/retrieval_ready_data", exist_ok=True)
# Save output
with open("data/RAG/retrieval_ready_data/rag_documents_week.json", "w", encoding="utf-8") as f:
    json.dump(converted_data, f, indent=2)
