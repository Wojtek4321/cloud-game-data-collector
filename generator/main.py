import random
import time
import json 
import dotenv
import os
import requests

dotenv.load_dotenv("../.env")
URL = os.getenv("URL")

if not URL:
    raise ValueError("URL not found in .env file")


def get_weapon_for_phase(players_remaining):
    weapons = ["knife", "ak-47", "m4a1", "sniper", "usp-s"]
    
    if players_remaining > 70:
        # EARLY GAME (100 - 71 players):
        # More common weapons like pistols (usp-s) and knives, less snipers.
        weights = [40, 10, 10,  0, 40] 
    
    elif players_remaining > 20:
        # MID GAME (70 - 21 players):
        # Balanced mix, more rifles (ak-47, m4a1) and some snipers.
        weights = [ 5, 40, 40, 10,  5] 
        
    else:
        # LATE GAME (20 - 1 players):
        # High chance of powerful weapons (ak-47, m4a1) and snipers, no knives.
        weights = [ 2, 30, 28, 40,  0] 
        
    # Randomly select a weapon based on the defined weights for the current phase
    return random.choices(weapons, weights=weights, k=1)[0]


def run_match(match_number):
    print(f"\n MATCH {match_number} START")
    alive_players = [f"player_{i}" for i in range(1, 101)]
    max_map_size = 500.0

    # Simulate a match until one survivor remains
    while len(alive_players) > 1:
        killer = random.choice(alive_players)
        # Victim must be different from killer
        victim = random.choice([p for p in alive_players if p != killer])
        weapon = get_weapon_for_phase(len(alive_players))
        timestamp = int(time.time())

        # Victim is eliminated
        alive_players.remove(victim)

        # Zone shrinks
        current_zone_size = max_map_size * (len(alive_players) / 100.0) + 10.0
        position = {
            "x": round(random.uniform(-current_zone_size, current_zone_size), 2),
            "y": round(random.uniform(-current_zone_size, current_zone_size), 2),
        }
    
        event_data = {
            "player_id": killer,
            "victim_id": victim,
            "weapon": weapon,
            "event_type": "death",
            "timestamp": timestamp,
            "position": position,
            "players_remaining": len(alive_players)
        }

        try:
            response = requests.post(URL, json=event_data, timeout=3)
            print(f"sent: [{current_zone_size:3.0}m zone] {killer} eliminated {victim} using {weapon} remaining: {len(alive_players)} status: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"error: Connection failed: {e}")

        # Simulate time between events, faster as the match progresses
        time.sleep(random.uniform(0.5, 1.5))

    # Ktoś wygrał!
    winner = alive_players[0]
    print(f"👑 Match {match_number} finished with last survivor: {winner}!\n")

if __name__ == "__main__":
    match_counter = 1
    
    # Infinite loop to keep generating matches
    while True:
        run_match(match_counter)
        match_counter += 1
        
        print("⏳ Preparing new arena... starting next match in 10 seconds.")
        time.sleep(10)