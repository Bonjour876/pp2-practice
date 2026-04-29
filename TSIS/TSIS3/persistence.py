import json
import os

SETTINGS_PATH = r"C:\Users\tamer\OneDrive\Documents\PP2\TSIS\TSIS3\settings.json"
LEADERBOARD_PATH = r"C:\Users\tamer\OneDrive\Documents\PP2\TSIS\TSIS3\leaderboard.json"

def load_settings():
    default = {"sound": True, "car_color": "Red", "difficulty": "Medium", "speed_boost": 5}
    if os.path.exists(SETTINGS_PATH):
        try:
            with open(SETTINGS_PATH, "r") as f:
                return json.load(f)
        except: return default
    return default

def save_settings(settings):
    with open(SETTINGS_PATH, "w") as f:
        json.dump(settings, f, indent=4)

def load_leaderboard():
    if os.path.exists(LEADERBOARD_PATH):
        try:
            with open(LEADERBOARD_PATH, "r") as f:
                return json.load(f)
        except: return []
    return []

def add_to_leaderboard(name, score, distance):
    data = load_leaderboard()
    data.append({"name": name, "score": score, "distance": int(distance)})
    # Sort by score (descending) and keep top 10
    data = sorted(data, key=lambda x: x['score'], reverse=True)[:10]
    with open(LEADERBOARD_PATH, "w") as f:
        json.dump(data, f, indent=4)