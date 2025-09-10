import json
import re

# Carica i documenti
with open("data/raw/player_season_docs_clean.json") as f:
    docs = json.load(f)

# Filtra per stagione 2016-2017
season_docs = [doc for doc in docs if "Season: 2023-24" in doc]

top_scorer = None
max_goals = -1

# Regex per trovare gol segnati
goals_re = re.compile(r"Goals Scored:\s*(\d+)")

for doc in season_docs:
    match = goals_re.search(doc)
    if match:
        goals = int(match.group(1))
        if goals > max_goals:
            max_goals = goals
            top_scorer = doc

# Output
if top_scorer:
    print("🎯 Top scorer in 2016–2017:")
    print(top_scorer)
else:
    print("❌ Nessun dato trovato per la stagione 2016–2017.")
