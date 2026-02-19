from sqlalchemy import Column, Integer, Float, String, DateTime
from database import Base
from datetime import datetime

class Metric(Base):
    __tablename__ = "metrics"

    id = Column(Integer, primary_key=True, index=True)

    device_id = Column(String, index=True)
    session_id = Column(String, index=True)

    timestamp = Column(DateTime, default=datetime.utcnow)

    ear = Column(Float)
    yaw = Column(Float)
    pitch = Column(Float)
    blink_rate = Column(Float)
    risk_score = Column(Float)
    state = Column(String)
