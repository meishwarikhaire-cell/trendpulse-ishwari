import requests
import json
import time
from datetime import datetime
import os

# Step 1: Define API links
top_stories_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
story_detail_url = "https://hacker-news.firebaseio.com/v0/item/{}.json"

# Custom header
headers = {"User-Agent": "TrendPulse/1.0"}

# Step 2: Define categories with keywords
category_keywords = {
    "technology": ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"],
    "entertainment": ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"]
}

# Step 3: Create storage variables
stories_data = []   # list to store final results
category_counter = {cat: 0 for cat in category_keywords}

print("Fetching top stories from Hacker News...")

# Step 4: Fetch top story IDs
response = requests.get(top_stories_url, headers=headers)
top_ids = response.json()[:500]

print("Processing stories...")

# Step 5: Loop through each story ID
for story_id in top_ids:
    try:
        # Fetch story details
        res = requests.get(story_detail_url.format(story_id), headers=headers)
        story = res.json()

        # Skip if data is missing
        if not story or "title" not in story:
            continue

        # Convert title to lowercase for keyword matching
        title_text = story["title"].lower()

        # Step 6: Assign category
        for category, keywords in category_keywords.items():

            # Skip if category already has 25 stories
            if category_counter[category] >= 25:
                continue

            # Check each keyword manually
            for word in keywords:
                if word in title_text:

                    # Create data dictionary
                    story_info = {
                        "post_id": story.get("id"),
                        "title": story.get("title"),
                        "category": category,
                        "score": story.get("score", 0),
                        "num_comments": story.get("descendants", 0),
                        "author": story.get("by"),
                        "collected_at": datetime.now().isoformat()
                    }

                    # Add to list
                    stories_data.append(story_info)
                    category_counter[category] += 1
                    break

            else:
                continue
            break

    except Exception as error:
        print("Failed to fetch story:", error)

    # Stop when enough data collected
    if sum(category_counter.values()) >= 125:
        break

# Step 7: Create folder if not exists
os.makedirs("data", exist_ok=True)

# Create filename with date
file_name = f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"

# Step 8: Save data into JSON file
with open(file_name, "w") as file:
    json.dump(stories_data, file, indent=4)

# Final output
print("Total stories collected:", len(stories_data))
print("Data saved successfully at:", file_name)