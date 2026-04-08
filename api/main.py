from fastapi import FastAPI
from models import PlayerEvent
import json

app = FastAPI()

@app.post("/telemetry")
async def receive_telemetry(event: PlayerEvent):
    data = event.dict()
    with open("telemetry_data.json", "a") as f:
        f.write(json.dumps(data) + "\n")
    print("Odebrano:", data)
    return {"message": "Telemetry data received"}