import random
import time 
import dotenv
import requests
import os

dotenv.load_dotenv("../.env")

URL = os.getenv("URL")

if not URL:
    raise ValueError("URL nie został znaleziony w .env")

WEAPONS = ["knife","ak-47","m4a1","sniper","usp-s"]



def get_unique_players(limit=1000):
    ids = list(range(1, limit + 1))
    random.shuffle(ids)
    for p_id in ids:
        yield p_id

player_pool = get_unique_players(1000)

def generate_telemetry_data(p_id):
    return {
        "player_id": p_id,
        "weapon": random.choice(WEAPONS),
        "event_type": "death",
        "timestamp": int(time.time()),
        "position": {
            "x": round(random.uniform(-100, 100), 2),
            "y": round(random.uniform(-100, 100), 2),
        },
    }
while True:
    for p_id in player_pool:
        data = generate_telemetry_data(p_id)
        
        try:
            response = requests.post(URL, json=data, timeout=3)
            print(f"SENT Player {p_id} died Status: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"ERROR Connection failed: {e}")

        time.sleep(1) 

