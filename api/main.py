from fastapi import FastAPI
from models import PlayerEvent
import json, os
from azure.storage.filedatalake import DataLakeServiceClient
from dotenv import load_dotenv

load_dotenv("../.env")

AZURE_CONNECTION_STRING = os.getenv("AZURE_CONNECTION_STRING")
CONTAINER_NAME = "telemetry"
FILE_NAME = "combatdata_logs.jsonl"

app = FastAPI()

service_client = DataLakeServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
file_system_client = service_client.get_file_system_client(file_system=CONTAINER_NAME)
file_client = file_system_client.get_file_client(FILE_NAME)


try:
    file_client.create_file()
    current_offset = 0
except Exception:
    props = file_client.get_file_properties()
    current_offset = props.size

@app.post("/telemetry")
async def receive_telemetry(event: PlayerEvent):
    global current_offset
    
    data = event.dict()
    encoded_data = json.dumps(data) + "\n"
    data_length = len(encoded_data)
    
    try:
        file_client.append_data(encoded_data, offset=current_offset, length=data_length)
        file_client.flush_data(current_offset + data_length)
        current_offset += data_length
    except Exception:
        
        file_client.create_file()
        file_client.append_data(encoded_data, offset=0, length=data_length)
        file_client.flush_data(data_length)
        current_offset = data_length

    return {"status": "success", "offset": current_offset}