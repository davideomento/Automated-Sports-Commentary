from youtube_transcript_api import YouTubeTranscriptApi
import json
import re
import os

# Function to create a safe filename by removing/replacing invalid characters
def safe_filename(s):
    return re.sub(r'[^\w\-]', '_', s)

video_id = "7yvlN9H3RQc"

# Define match metadata
match_name = "Newcastle VS Arsenal"
match_date = "2025-04-25"
competition_stage = "Premier League Matchday 25"

# Define start times in seconds
start_seconds = 0

# Fetch available transcripts for the video
transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

try:
    # Try to get manually created English transcript
    transcript = transcript_list.find_transcript(['en'])
except:
    # If not available, fallback to auto-generated English transcript
    transcript = transcript_list.find_generated_transcript(['en'])

# Fetch the transcript data (list of transcript entries)
transcript_data = transcript.fetch()

# Collect commentary in chronological order
all_texts = []

for entry in transcript_data:
    start_time = entry.start  # start time in seconds

    # Skip entries outside the desired time range
    if start_time < start_seconds:
        continue

    # Clean subtitle text (remove line breaks)
    text = entry.text.replace('\n', ' ')
    all_texts.append(text)

# Concatenate everything into one single commentary string
full_commentary = " ".join(all_texts)

# Combine metadata and commentary in one dictionary
output = {
    "metadata": {
        "match_name": match_name,
        "match_date": match_date,
        "competition_stage": competition_stage,
        "start_time_seconds": start_seconds,
        "video_id": video_id
    },
    "commentary": full_commentary
}

# File name
filename = f"{safe_filename(match_name)}_{match_date}_{safe_filename(competition_stage)}.json"

# Ensure the 'data/youtube' folder exists
os.makedirs("data/youtube", exist_ok=True)

# Save dataset as JSON file inside the 'data/youtube' folder
filepath = os.path.join("data/youtube", filename)
with open(filepath, "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print(f"Saved unified commentary for {match_name} on {match_date}, {competition_stage}.")
print(f"File saved as: {filepath}")
