from pydantic import BaseModel

class Sensor(BaseModel):
    id: int
    name: str
    latitude: float
    longitude: float
    joined_at: str
    last_seen: str
    temperature: float
    humidity: float
    battery_level: float
    
    class Config:
        orm_mode = True
        
class SensorCreate(BaseModel):
    name: str
    longitude: float
    latitude: float
    
class SensorData(BaseModel):
    temperature: float
    humidity: float
    battery_level: float
    last_seen: str