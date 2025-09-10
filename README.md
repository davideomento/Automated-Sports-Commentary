# LLMs_for_Automated_Sports_Commentary
My Master's Thesis in Mathematical Engineering

## Procedure
- Find dataset to RAG
- Use ElasticSearch to RAG new events that are not in the dataset
- Find golden-standard dataset with accurate and rich comment

### Website, RAG dataset
For now I used FantasyPremierLeague, I only considered last 3 seasons and  generated textual description for each seasons and for each games week for each player.

1)	https://www.football-data.co.uk/
•  CSV con risultati, date, squadre, goal, xG, etc. (Serie A inclusa).
•  Perfetto per basi statistiche.
2)	https://github.com/statsbomb/open-data
•  Estremamente dettagliato (eventi in campo, passaggi, tiri).
•  Include alcuni campionati (non Serie A), ma puoi usarlo per prototipi.
3)	https://www.transfermarkt.com/
•  Profili giocatori, statistiche stagionali, cronologia gol, assist, etc.
•  Puoi costruirti un dataset RAG-friendly.
4)	https://www.kaggle.com/datasets/hugomathien/soccer
•  Database SQLite con partite, squadre, player data (2008–2016).
5)	https://www.whoscored.com/
•  Molto dettagliato ma da usare con cautela per TOS.


### Dataset BBC webscraping and Event kaggle
Limitations: Just a brief description of the event, not a real comment

### Dataset from youtube commentaries
Pro: Very rich comment, with insights, statistics ecc
Cons: Difficult allineate events and comment, but I could use gpt4 to do that for me

### Dataset from website trough API
Contacted them, waiting for a response:
- https://www.api-football.com/
- https://sportradar.com/
- https://www.statsperform.com/
- https://www.football-data.org/

# What I've done till now
- Youtube comment scraping(rich but dirty) and dataset from papers(poor but clean)
- retrieval ready dataset preprocessed and prepared from FantasyPremierLeague
- Indexing(faiss)+Embedding(SentenceTrasformer)
- created file .faiss and metadata.json
- Implement query retrieval functionality with FAISS and Sentence Transformers

# Simple Model()
# Input template
# Live Text Commentary Templates

Below are simple, factual templates (no emotion) for common football events. Fill in the placeholders (`{player}`, `{team}`, `{minute}`, etc.) as needed.

## Goal
- “{minute}’ Goal by {player} for {team}.”
- “Goal at {minute}’: {player} scores for {team}.”

## Assisted Goal
“{minute}’ Goal by {player} for {team}, assisted by {assist_player}.”
“Goal at {minute}’: {player} scores for {team}, assisted by {assist_player}.”

## Own Goal
- “{minute}’ Own goal by {player} (for {opponent}).”
- “Own goal at {minute}’ credited to {player}.”

## Penalty Awarded
- “{minute}’ Penalty awarded to {team}.”
- “Penalty at {minute}’ for {team}.”

## Penalty Scored
- “Penalty converted by {player} at {minute}’.”
- “{minute}’ Penalty scored by {player}.”

## Penalty Missed / Saved
- “{minute}’ Penalty by {player} missed.”
- “{minute}’ Penalty saved by {keeper}.”

## Shot on Target
- “{minute}’ Shot on target by {player}.”
- “{player} tests the keeper at {minute}’.”

## Shot off Target
- “{minute}’ Shot wide by {player}.”
- “{player} misses target at {minute}’.”

## Blocked Shot
- “{minute}’ Shot by {player} blocked.”
- “Blocked attempt at {minute}’ from {player}.”

## Corner
- “{minute}’ Corner to {team}.”
- “Corner awarded at {minute}’ for {team}.”

## Free Kick
- “{minute}’ Free kick to {team}.”
- “Free kick conceded by {player} at {minute}’.”

## Yellow Card
- “{minute}’ Yellow card shown to {player}.”
- “Booking for {player} at {minute}’.”

## Red Card
- “{minute}’ Red card shown to {player}.”
- “{player} sent off at {minute}’.”

## Substitution
- “{minute}’ Substitution for {team}: {player_off} off, {player_on} on.”
- “{team} change at {minute}’: {player_on} replaces {player_off}.”

## Offside
- “{minute}’ Offside called against {player}.”
- “{player} flagged offside at {minute}’.”

## Foul Committed
- “{minute}’ Foul by {player}.”
- “Foul at {minute}’ on {player}.”

## Foul Won
- “{minute}’ Foul won by {player}.”
- “{player} wins a free kick at {minute}’.”

## Injury / Treatment
- “{minute}’ Play stopped for treatment to {player}.”
- “{player} down injured at {minute}’.”

## VAR Check / Decision
- “{minute}’ VAR check underway.”
- “VAR overturns on-field decision at {minute}’.”

## Kick‑Off / Half‑Time / Full‑Time
- “Kick‑off.”
- “Half‑time.”
- “Full‑time.”

# Diagram
+--------------------------------------------+
| Input: sentences with pre-set templates    |
+----------------------+---------------------+
                       |
                       v
+----------------------+---------------------+
| Extraction of statistics and data           |
+----------------------+---------------------+
                       |
                       v
        +--------------+----------------+
        |                               |
        v                               v
+-------+---------+           +---------+---------+
| Extracted       |           | Template sentence  |
| statistics      |           |                   |
+-------+---------+           +---------+---------+
        \                            /
         \                          /
          \                        /
           v                      v
         +------------------------------------+
         | Generation via LLM                 |
         | (input: extracted stats + template)|
         +------------+-----------------------+
                      |
        +-------------+--------------+
        |                            |
        v                            v
+-------+---------+          +-------+----------+
| Fine-tuning LLM |          | Prompt Engineering|
| with real sports|          +-------------------+
| commentary data |
+-----------------+


Examples:

[1) Event Input]
“Goal by de Bruyne with a left-foot strike at 12’”
         │
         ▼
[2) Predefined queries based on the template sentence]
• extract: event_type, player, team, minute
• call → get_event_stats({event_type, player, team, season})
         │
         ▼
[3) Execute Query]
get_event_stats(…)
→ from CSV/DB:
  • goals_this_season = 15
  • left_foot_goals = 7
         │
         ▼
[4) LLM Generates Commentary]
**Input to LLM:**
• Event text
• Stats dict
**System Prompt:**
“You are a sports commentator. Generate a lively, natural-sounding sentence using only the provided data.”
**Output:**
“De Bruyne’s left-foot strike from outside the box is his 15th goal of the season, 7 of which have come from his left foot—what a campaign for him!”

# Transfer Market
https://github.com/felipeall/transfermarkt-api

# Extension
From video to commentary directly
Other sports in the same way
Voice of past telechronist
Eventi precedenti nel prompt+tiri in porta sostituzioni, infortuni ecc
Enfsasi sulla base del minuto, risultato, posizione in classifica, eventi precedenti