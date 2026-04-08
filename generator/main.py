import random
import time 
import dotenv
import requests

dotenv.load_dotenv("../.env")

URL = os.getenv("URL")

weapons = ["knife","ak-47","m4a1","sniper","usp-s"]

def generate_telemetry_data():
    return {
        "player_id": random.randint(1, 1000),
        "weapon": random.choice(weapons),
        "event_type": "death",
        "timestamp": int(time.time()),
        "position":{
            "x": random.uniform(-100, 100),
            "y": random.uniform(-100, 100),
        },
    }
while True:
    data = generate_telemetry_data()
    try:
        response = requests.post(URL, json=data)
        print("Data sent:", data, "Response:", response.status_code)
    except Exception as e:
        print("Error sending data:", e)
    time.sleep(1)

