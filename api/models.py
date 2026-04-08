from pydantic import BaseModel

class Position(BaseModel):
    x: float
    y: float
    
class PlayerEvent(BaseModel):
    
    player_id: str
    victim_id: str

    weapon: str
    event_type: str
    timestamp: int
    position: Position
    
    players_remaining: int