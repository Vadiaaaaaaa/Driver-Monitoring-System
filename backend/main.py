from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from backend.database import SessionLocal, engine
from backend import models, schemas
from datetime import datetime

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/metrics", response_model=schemas.MetricResponse)
def create_metric(metric: schemas.MetricCreate, db: Session = Depends(get_db)):
    db_metric = models.Metric(
        device_id=metric.device_id,
        session_id=metric.session_id,
        timestamp=metric.timestamp,
        ear=metric.ear,
        yaw=metric.yaw,
        pitch=metric.pitch,
        blink_rate=metric.blink_rate,
        risk_score=metric.risk_score,
        state=metric.state,
    )

    db.add(db_metric)
    db.commit()
    db.refresh(db_metric)
    return db_metric


@app.get("/metrics", response_model=list[schemas.MetricResponse])
def get_metrics(db: Session = Depends(get_db)):
    return db.query(models.Metric).all()
