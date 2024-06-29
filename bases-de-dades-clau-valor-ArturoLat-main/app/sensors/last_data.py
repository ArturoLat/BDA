from pydantic import BaseModel

class SensorData(BaseModel):
    temperature: float
    humidity: float
    battery_level: float
    last_seen: str
    