import json
import re
import os

# Load your file
with open("data/RAG/player_season_docs_clean.json", "r") as f:
    raw_data = json.load(f)

prepared_data = []

for item in raw_data:
    text = item["text"]
    
    # Try to extract 'status' from the text (last sentence)
    match = re.search(r"status was '(\w)'", text)
    status = match.group(1) if match else "unknown"

    # Create the RAG-compatible document
    prepared_data.append({
        "content": text,
        "metadata": {
            "player": item["player"],
            "team": item["team"],
            "season": item["season"],
            "position": item["position"],
            "status": status
        }
    })

os.makedirs("data/RAG/retrieval_ready_data", exist_ok=True)
# Save or continue with embedding
with open("data/RAG/retrieval_ready_data/rag_documents_season.json", "w") as f:
    json.dump(prepared_data, f, indent=2)
