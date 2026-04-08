from pydantic import BaseModel

class Position(BaseModel):
    x: float
    y: float
    
class PlayerEvent(BaseModel):
    player_id: int
    weapon: str
    event_type: str
    timestamp: int
    position: Position