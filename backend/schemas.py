from pydantic import BaseModel
from datetime import datetime

class MetricCreate(BaseModel):
    device_id: str
    session_id: str
    timestamp: datetime
    ear: float
    yaw: float
    pitch: float
    blink_rate: float
    risk_score: float
    state: str


class MetricResponse(MetricCreate):
    id: int

    class Config:
        from_attributes = True
