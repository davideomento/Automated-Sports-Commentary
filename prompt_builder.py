def prompt_goal(home_team, away_team, current_score, minute, scorer, assist, goal_type, shot_position, player_info, player_stats, player_achievements, team_profile_away, team_profile_home, team_involved):
    return f"""TASK:
Act as a live football commentator. Using only the provided match data, create a vivid,
energetic, exhaustive, and natural-sounding commentary describing the moment a goal is scored.

# STRICT GUIDELINES FOR GOAL COMMENTARY
1. Use ONLY the exact data provided in the input. Do NOT invent, guess, or add any extra context.
2. Do NOT describe events, actions, or outcomes that are not explicitly listed in the data.
3. Always include the current score as provided.
4. Use only the statistics or details present in the input to enrich the commentary.
5. If multiple stats are relevant, cite all of them in the commentary.
6. Avoid adding any assumptions about player movements, goals, fouls, or other events not specified.
7. You should choose the most relevant information from the input to include in the commentary.
8. If Goal Type is "Other", do not mention it in the commentary.
9. If Assist is "None", do not mention it in the commentary.


EXAMPLE 1 :
INPUT:
Match: HOME_TEAM vs AWAY_TEAM
Team Profile Away: TEAM_PROFILE_AWAY
Team Profile Home: TEAM_PROFILE_HOME
Current Score: CURRENT_SCORE
Event Minute: EVENT_MINUTE
Scorer: SCORER
Assister: ASSISTER
Goal Type: GOAL_TYPE
Shot Position: SHOT_POSITION
Scorer Goals this Season: GOALS
Scorer Assists this Season: ASSISTS

OUTPUT:
"GOAL at EVENT_MINUTE! SCORER finds the net from SHOT_POSITION — with GOALS goals and ASSISTS assists this season, 
he's proving to be a key man for HOME_TEAM. The score is now CURRENT_SCORE. Credit goes to ASSISTER for the assist.
---

EXAMPLE 2:
INPUT:
Match: HOME_TEAM vs AWAY_TEAM
Team Profile Away: TEAM_PROFILE_AWAY
Team Profile Home: TEAM_PROFILE_HOME
Current Score: CURRENT_SCORE
Event Minute: EVENT_MINUTE
Scorer: SCORER
Assister: ASSISTER
Goal Type: GOAL_TYPE
Shot Position: SHOT_POSITION
Scorer Age: AGE
Matches Played this Season: MATCHES_PLAYED

OUTPUT:
"Minute EVENT_MINUTE — SCORER scores from SHOT_POSITION with a brilliant GOAL_TYPE finish! 
At AGE years old and with MATCHES_PLAYED appearances this season, he's showing incredible form for HOME_TEAM. 
The score is now CURRENT_SCORE, thanks to a precise assist from ASSISTER."

---

INPUT:
Match: {home_team} vs {away_team}
Team Profile Home: {team_profile_home}
Team Profile Away: {team_profile_away}
Current Score: {current_score}
Event Minute: {minute}
Team Involved: {team_involved}
Scorer: {scorer}
Assist: {assist}
Goal Type: {goal_type}
Position of the shot: {shot_position}
{scorer} Info: {player_info}
{scorer} Stats: {player_stats}
{scorer} Achievements: {player_achievements}


OUTPUT:"""

def prompt_attempted_shot(home_team, away_team, current_score, minute, shooter, outcome, shot_position, shooter_info, shooter_stats, shooter_achievements, team_profile_away, team_profile_home, team_involved):
    return f"""TASK:
Act as a live football commentator. Using only the provided match data, create a lively, exhaustive, accurate commentary describing an attempted shot.

# STRICT GUIDELINES FOR SHOT COMMENTARY
1. Always mention the shooter, the outcome of the shot, and the position from which it was taken.
2. Do NOT invent, guess, or add any extra details not present in the data.
3. Use only the input data to enrich the commentary; do not assume context or events.
4. You should choose the most relevant information from the input to include in the commentary.
5. If multiple stats are relevant, cite all of them in the commentary.


EXAMPLES:

Example 1:
INPUT:
Match: HOME_TEAM vs AWAY_TEAM
Team Profile Away: TEAM_PROFILE_AWAY
Team Profile Home: TEAM_PROFILE_HOME
Current Score: CURRENT_SCORE
Event Minute: EVENT_MINUTE
Shooter: SHOOTER
Outcome: OUTCOME
Position of the shot: SHOT_POSITION
SHOOTER Info: SHOOTER_INFO
SHOOTER Stats: SHOOTER_STATS
SHOOTER Achievements: SHOOTER_ACHIEVEMENTS

OUTPUT:
"SHOOTER fires a shot from SHOT_POSITION, but it’s OUTCOME. Score remains CURRENT_SCORE."

Example 2:
INPUT:
Match: HOME_TEAM vs AWAY_TEAM
Team Profile Away: TEAM_PROFILE_AWAY
Team Profile Home: TEAM_PROFILE_HOME
Current Score: CURRENT_SCORE
Event Minute: EVENT_MINUTE
Shooter: SHOOTER
Outcome: OUTCOME
Position of the shot: SHOT_POSITION
Shooter Info: SHOOTER_INFO
Shooter Stats: SHOOTER_STATS
Shooter Achievements: SHOOTER_ACHIEVEMENTS

OUTPUT:
"SHOOTER attempts a shot from SHOT_POSITION, but it goes OUTCOME. The score is still CURRENT_SCORE at minute EVENT_MINUTE."

---

Match: {home_team} vs {away_team}
Team Profile Home: {team_profile_home}
Team Profile Away: {team_profile_away}
Current Score: {current_score}
Event Minute: {minute}
Team Involved: {team_involved}
Shooter: {shooter}
Outcome: {outcome}
Position of the shot: {shot_position}
{shooter} Info: {shooter_info}
{shooter} Stats: {shooter_stats}
{shooter} Achievements: {shooter_achievements}

OUTPUT:"""

def prompt_dribbling(home_team, away_team, current_score, minute, dribbler, opponent, dribbler_info, dribbler_stats, success, team_profile_away, team_profile_home, team_involved):
    return f"""TASK:
Act as a live football commentator. Using only the provided match data, create a lively, exhaustive, accurate commentary describing the moment a player dribbled past an opponent.

# STRICT GUIDELINES FOR DRIBBLE COMMENTARY
1. State clearly who dribbled past whom.
2. Do NOT invent, guess, or add any extra details not present in the data.
3. You should choose the most relevant information from the input to include in the commentary.
4. If multiple stats are relevant, cite all of them in the commentary.


EXAMPLES:

Example 1:
INPUT:
Match: HOME_TEAM vs AWAY_TEAM
Team Profile Away: TEAM_PROFILE_AWAY
Team Profile Home: TEAM_PROFILE_HOME
Current Score: CURRENT_SCORE
Event Minute: EVENT_MINUTE
Dribbler: DRIBBLER
Defender: DEFENDER
Successful Dribbles: SUCCESSFUL_DRIBBLES

OUTPUT:
"DRIBBLER skilfully dribbles past DEFENDER, adding to his SUCCESSFUL_DRIBBLES successful dribbles this season."

Example 2:
INPUT:
Match: HOME_TEAM vs AWAY_TEAM
Team Profile Away: TEAM_PROFILE_AWAY
Team Profile Home: TEAM_PROFILE_HOME
Current Score: CURRENT_SCORE
Event Minute: EVENT_MINUTE
Dribbler: DRIBBLER
Defender: DEFENDER

OUTPUT:
"At minute EVENT_MINUTE DRIBBLER elegantly dribbles past DEFENDER, keeping the pressure on at CURRENT_SCORE."

---

Match: {home_team} vs {away_team}
Team Profile Home: {team_profile_home}
Team Profile Away: {team_profile_away}
Current Score: {current_score}
Event Minute: {minute}
Team Involved: {team_involved}
Dribbler: {dribbler}
Defender: {opponent}
{dribbler} Info: {dribbler_info}
{dribbler} Stats: {dribbler_stats}
Outcome: {success}

OUTPUT:"""


def prompt_tackle(home_team, away_team, current_score, minute, tackler, opponent, success, team_profile_away, team_profile_home, team_involved):
    return f"""TASK:
Act as a live football commentator. Using only the provided match data, create a lively, exhaustive, accurate commentary describing the moment a tackle is made.

# STRICT GUIDELINES FOR TACKLE COMMENTARY
1. Mention the tackler and the opponent involved.
2. Do NOT invent, guess, or add any extra context not present in the data.
3. You should choose the most relevant information from the input to include in the commentary.
4. If multiple stats are relevant, cite all of them in the commentary.


EXAMPLES:

Example 1:
INPUT:
Match: HOME_TEAM vs AWAY_TEAM
Team Profile Away: TEAM_PROFILE_AWAY
Team Profile Home: TEAM_PROFILE_HOME
Current Score: CURRENT_SCORE
Event Minute: EVENT_MINUTE
Tackler: TACKLER
Opponent: OPPONENT

OUTPUT:
"TACKLER executes a clean tackle against OPPONENT, halting the attack and keeping the score at CURRENT_SCORE."

Example 2:
INPUT:
Match: HOME_TEAM vs AWAY_TEAM
Team Profile Away: TEAM_PROFILE_AWAY
Team Profile Home: TEAM_PROFILE_HOME
Current Score: CURRENT_SCORE
Event Minute: EVENT_MINUTE
Tackler: TACKLER
Opponent: OPPONENT

OUTPUT:
"TACKLER successfully challenges OPPONENT, disrupting their play and maintaining the current score of CURRENT_SCORE."

---

Match: {home_team} vs {away_team}
Team Profile Home: {team_profile_home}
Team Profile Away: {team_profile_away}
Current Score: {current_score}
Team Involved: {team_involved}
Event Minute: {minute}
Tackler: {tackler}
Opponent: {opponent}
Success: {success}

OUTPUT:"""


def prompt_foul(home_team, away_team, current_score, minute, player, reason, card, player_info, player_stats, team_profile_away, team_profile_home, team_involved):
    return f"""TASK:
Act as a live football commentator. Using only the provided match data, create a lively, exhaustive, accurate commentary describing the moment a foul is committed.

STRICT RULES:
# STRICT GUIDELINES FOR FOUL COMMENTARY
1. Mention the fouling player, the reason for the foul, and if given, the card color.
2. Do NOT invent, guess, or add any extra details not present in the data.
3. You should choose the most relevant information from the input to include in the commentary.
4. If multiple stats are relevant, cite all of them in the commentary.
5. If the foul reason is "Other", DO NOT MENTION IT in the commentary.


EXAMPLES:

Example 1:
INPUT:
Match: HOME_TEAM vs AWAY_TEAM
Team Profile Away: TEAM_PROFILE_AWAY
Team Profile Home: TEAM_PROFILE_HOME
Current Score: CURRENT_SCORE
Event Minute: EVENT_MINUTE
Player: PLAYER
Reason: REASON
Card: CARD
Player Info: PLAYER_INFO
Player Stats: PLAYER_STATS  

OUTPUT:
"PLAYER commits a foul for REASON, receiving a CARD card. The score remains CURRENT_SCORE."

Example 2:
INPUT:
Match: HOME_TEAM vs AWAY_TEAM
Team Profile Away: TEAM_PROFILE_AWAY
Team Profile Home: TEAM_PROFILE_HOME
Current Score: CURRENT_SCORE
Event Minute: EVENT_MINUTE
Player: PLAYER
Reason: REASON
Card: None
Player Info: PLAYER_INFO
Player Stats: PLAYER_STATS

OUTPUT:
"PLAYER is penalized for REASON but avoids a card. The score is still CURRENT_SCORE."

---

Match: {home_team} vs {away_team}
Team Profile Home: {team_profile_home}
Team Profile Away: {team_profile_away}
Current Score: {current_score}
Team Involved: {team_involved}
Event Minute: {minute}
Player: {player}
Reason: {reason}
Card: {card}
{player} Info: {player_info}
{player} Stats: {player_stats}

OUTPUT:"""


def prompt_pass(home_team, away_team, current_score, minute, passer, receiver, pass_type, success, team_profile_away, team_profile_home, team_involved):
    return f"""TASK:
Act as a live football commentator. Using only the provided match data, create a lively, exhaustive, accurate commentary describing a pass.

# STRICT GUIDELINES FOR PASS COMMENTARY
1. Mention the passer, the receiver, the type of pass, and the outcome.
2 Do NOT invent, guess, or add any extra details not present in the data.
3. You should choose the most relevant information from the input to include in the commentary.
4. If multiple stats are relevant, cite all of them in the commentary.


EXAMPLES:

Example 1:
INPUT:
Match: HOME_TEAM vs AWAY_TEAM
Team Profile Away: TEAM_PROFILE_AWAY
Team Profile Home: TEAM_PROFILE_HOME
Current Score: CURRENT_SCORE
Event Minute: EVENT_MINUTE
Passer: PASSER
Receiver: RECEIVER
Pass Type: PASS_TYPE
Outcome: SUCCESS

OUTPUT:
"PASSER delivers a PASS_TYPE pass to RECEIVER, resulting in a successful play. The score remains CURRENT_SCORE."

Example 2:
INPUT:
Match: HOME_TEAM vs AWAY_TEAM
Team Profile Away: TEAM_PROFILE_AWAY
Team Profile Home: TEAM_PROFILE_HOME
Current Score: CURRENT_SCORE
Event Minute: EVENT_MINUTE
Passer: PASSER
Receiver: RECEIVER
Pass Type: PASS_TYPE
Outcome: FAILURE

OUTPUT:
"PASSER attempts a PASS_TYPE pass to RECEIVER, but it fails to connect. The score stays at CURRENT_SCORE."

---

Match: {home_team} vs {away_team}
Team Profile Home: {team_profile_home}
Team Profile Away: {team_profile_away}
Current Score: {current_score}
Event Minute: {minute}
Team Involved: {team_involved}
Passer: {passer}
Receiver: {receiver}
Pass Type: {pass_type}
Outcome: {success}

OUTPUT:"""


def prompt_var_call(home_team, away_team, current_score, minute, reason, team_profile_away, team_profile_home, team_involved):
    return f"""TASK:
Act as a live football commentator. Using only the provided match data, create a lively, exhaustive, accurate commentary describing a VAR review moment.

# STRICT GUIDELINES FOR REVIEW COMMENTARY
1. Mention the reason for the review.
2. Do NOT invent, guess, or add any extra details not present in the data.
3. You should choose the most relevant information from the input to include in the commentary.
4. If multiple stats are relevant, cite all of them in the commentary.


EXAMPLES:

Example 1:
INPUT:
Match: HOME_TEAM vs AWAY_TEAM
Team Profile Away: TEAM_PROFILE_AWAY
Team Profile Home: TEAM_PROFILE_HOME
Current Score: CURRENT_SCORE
Event Minute: EVENT_MINUTE
Reason: REASON

OUTPUT:
"The referee pauses the game for a VAR review due to REASON. The tension is palpable as everyone awaits the decision."

Example 2:
INPUT:
Match: HOME_TEAM vs AWAY_TEAM
Team Profile Away: TEAM_PROFILE_AWAY
Team Profile Home: TEAM_PROFILE_HOME
Current Score: CURRENT_SCORE
Event Minute: EVENT_MINUTE
Reason: REASON

OUTPUT:
"VAR review underway following REASON. The match momentarily halts as officials review the play."

---

Match: {home_team} vs {away_team}
Team Profile Home: {team_profile_home}
Team Profile Away: {team_profile_away}
Current Score: {current_score}
Event Minute: {minute}
Team Involved: {team_involved}
Reason: {reason}

OUTPUT:"""


def prompt_offside(home_team, away_team, current_score, minute, passer, receiver, team_profile_away, team_profile_home, team_involved):
    return f"""TASK:
Act as a live football commentator. Using only the provided match data, create a lively, exhaustive, accurate commentary describing an offside call.

# STRICT GUIDELINES FOR OFFSIDE COMMENTARY
1. Mention the passer and the receiver.
2. Do NOT invent, guess, or add any extra details not present in the data.
3. You should choose the most relevant information from the input to include in the commentary.
4. If multiple stats are relevant, cite all of them in the commentary.


EXAMPLES:

Example 1:
INPUT:
Match: HOME_TEAM vs AWAY_TEAM
Team Profile Away: TEAM_PROFILE_AWAY
Team Profile Home: TEAM_PROFILE_HOME
Current Score: CURRENT_SCORE
Event Minute: EVENT_MINUTE
Passer: PASSER
Receiver: RECEIVER

OUTPUT:
"The assistant referee raises the flag for offside against RECEIVER after a pass from PASSER. The attack is stopped immediately."

Example 2:
INPUT:
Match: HOME_TEAM vs AWAY_TEAM
Team Profile Away: TEAM_PROFILE_AWAY
Team Profile Home: TEAM_PROFILE_HOME
Current Score: CURRENT_SCORE
Event Minute: EVENT_MINUTE
Passer: PASSER
Receiver: RECEIVER

OUTPUT:
"RECEIVER is caught offside following a through ball from PASSER, halting the promising move."

---

Match: {home_team} vs {away_team}
Team Profile Home: {team_profile_home}
Team Profile Away: {team_profile_away}
Current Score: {current_score}
Event Minute: {minute}
Team Involved: {team_involved}
Passer: {passer}
Receiver: {receiver}

OUTPUT:"""


def prompt_start_half_end_game(home_team, away_team, minute, current_score, game_status, team_profile_away, team_profile_home):
    return f"""TASK:
Provide a detailed commentary on the start or end of the game, including relevant information about the teams if the game has just started, or the current/final score if the game has ended.
# STRICT GUIDELINES FOR MATCH START/END COMMENTARY
1. Mention whether it is the start or end of the match.
2. Mention the minute if it is relevant.
3. Do NOT invent, guess, or add any extra match events not present in the data.
4. You should choose the most relevant information from the input to include in the commentary.
5. If multiple stats are relevant, cite all of them in the commentary.


EXAMPLES:

Example 1:
INPUT:
Match: HOME_TEAM vs AWAY_TEAM
Team Profile Away: TEAM_PROFILE_AWAY
Team Profile Home: TEAM_PROFILE_HOME
Event Minute: 0
Game Status: start

OUTPUT:
"The match between HOME_TEAM and AWAY_TEAM kicks off at minute 0, with both teams eager to make their mark."

Example 2:
INPUT:
Match: HOME_TEAM vs AWAY_TEAM
Team Profile Home: TEAM_PROFILE_AWAY
Team Profile Away: TEAM_PROFILE_HOME
Event Minute: 90
Game Status: end

OUTPUT:
"The final whistle blows at minute 90, bringing the exciting contest between HOME_TEAM and AWAY_TEAM to a close."

---

Match: {home_team} vs {away_team}
Team Profile Home: {team_profile_home}
Team Profile Away: {team_profile_away}
Event Minute: {minute}
Game Status: {game_status}
Current Score: {current_score}

OUTPUT:"""


def prompt_substitution(home_team, away_team, current_score, minute, player_in, player_out, player_in_info, player_in_stats, player_out_info, player_out_stats, player_in_achievements, player_out_achievements,team_profile_away, team_profile_home, team_involved):
    return f"""TASK:
Act as a live football commentator. Using only the provided match data, create a lively, exhaustive, accurate commentary describing a substituition.

# STRICT GUIDELINES FOR SUBSTITUTION COMMENTARY
1. Mention the player coming in and the player going out.
2. Always include the exact event minute as provided.
3. Use only the player information and stats provided in the input.
4. Do NOT invent, guess, or add any extra details not present in the data.
5. You should choose the most relevant information from the input to include in the commentary.
6. If multiple stats are relevant, cite all of them in the commentary.


EXAMPLES:

Example 1:
INPUT:
Match: HOME_TEAM vs AWAY_TEAM
Team Profile Home: TEAM_PROFILE_HOME
Team Profile Away: TEAM_PROFILE_AWAY
Current Score: CURRENT_SCORE
Event Minute: EVENT_MINUTE
Player In: PLAYER_IN
Player Out: PLAYER_OUT
PLAYER_IN Info: AGE: 28, POSITION: MIDFIELDER
PLAYER_IN Stats: Appearances: 15, Goals: 3
PLAYER_OUT Info: AGE: 32, POSITION: MIDFIELDER
PLAYER_OUT Stats: Appearances: 20, Goals: 1
Player In Achievements: PLAYER_IN_ACHIEVEMENTS
Player Out Achievements: PLAYER_OUT_ACHIEVEMENTS

OUTPUT:
"Minute EVENT_MINUTE — PLAYER_IN replaces PLAYER_OUT, bringing fresh energy to HOME_TEAM's midfield."

Example 2:
INPUT:
Match: HOME_TEAM vs AWAY_TEAM
Team Profile Home: TEAM_PROFILE_HOME
Team Profile Away: TEAM_PROFILE_AWAY
Current Score: CURRENT_SCORE
Event Minute: EVENT_MINUTE
Player In: PLAYER_IN
Player Out: PLAYER_OUT
Player In Info: AGE: 22, POSITION: FORWARD
Player In Stats: Appearances: 10, Goals: 7
Player Out Info: AGE: 30, POSITION: FORWARD
Player Out Stats: Appearances: 18, Goals: 5
Player In Achievements: PLAYER_IN_ACHIEVEMENTS
Player Out Achievements: PLAYER_OUT_ACHIEVEMENTS

OUTPUT:
"At minute EVENT_MINUTE, PLAYER_IN comes on for PLAYER_OUT to bolster HOME_TEAM's attacking options."

---

Match: {home_team} vs {away_team}
Team Profile Home: {team_profile_home}
Team Profile Away: {team_profile_away}
Current Score: {current_score}
Event Minute: {minute}
Team Involved: {team_involved}
Player In: {player_in}
Player Out: {player_out}
{player_in} Info: {player_in_info}
{player_in} Stats: {player_in_stats}
{player_in} Achievements: {player_in_achievements}
{player_out} Info: {player_out_info}
{player_out} Stats: {player_out_stats}
{player_out} Achievements: {player_out_achievements}


OUTPUT:"""


def build_prompt(event_type, **kwargs):
    event_type = event_type.lower()

    events = {
        "goal": (prompt_goal, ["home_team", "away_team", "current_score", "minute", "scorer", "assist", "goal_type", "shot_position", "scorer_info", "scorer_stats", "scorer_achievements", "team_profile_away", "team_profile_home", "team_involved"]),
        "attempted_shot": (prompt_attempted_shot, ["home_team", "away_team", "current_score", "minute", "shooter", "outcome", "shot_position", "shooter_info", "shooter_stats", "shooter_achievements", "team_profile_away", "team_profile_home", "team_involved"]),
        "dribbling": (prompt_dribbling, ["home_team", "away_team", "current_score", "minute", "dribbler", "opponent", "dribbler_info", "dribbler_stats", "success", "team_profile_away", "team_profile_home", "team_involved"]),
        "tackle": (prompt_tackle, ["home_team", "away_team", "current_score", "minute", "tackler", "opponent", "success", "team_profile_away", "team_profile_home", "team_involved"]),
        "foul": (prompt_foul, ["home_team", "away_team", "current_score", "minute", "player", "reason", "card", "player_info", "player_stats",  "team_profile_away", "team_profile_home", "team_involved"]),
        "pass": (prompt_pass, ["home_team", "away_team", "current_score", "minute", "passer", "receiver", "pass_type", "success", "team_profile_away", "team_profile_home", "team_involved"]),
        "var_call": (prompt_var_call, ["home_team", "away_team", "current_score", "minute", "reason", "team_profile_away", "team_profile_home", "team_involved"]),
        "offside": (prompt_offside, ["home_team", "away_team", "current_score", "minute", "passer", "receiver", "team_profile_away", "team_profile_home", "team_involved"]),
        "start_half_end_game": (prompt_start_half_end_game, ["home_team", "away_team", "minute", "current_score", "game_status", "team_profile_away", "team_profile_home"]),
        "substitution": (prompt_substitution, ["home_team", "away_team", "current_score", "minute", "player_in", "player_out", "player_in_info", "player_in_stats", "player_out_info", "player_out_stats", "player_in_achievements", "player_out_achievements", "team_profile_away", "team_profile_home", "team_involved"])
    }

    if event_type not in events:
        raise ValueError(f"❌ Unknown event type: {event_type}")

    func, required_params = events[event_type]

    missing = [p for p in required_params if p not in kwargs]
    if missing:
        raise ValueError(f"❌ Missing parameters for {event_type}: {missing}")

    # Richiama la funzione passando i parametri nell'ordine corretto
    return func(*[kwargs[p] for p in required_params])


