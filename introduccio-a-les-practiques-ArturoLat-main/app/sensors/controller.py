from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from . import models, schemas, repository
from app.database import SessionLocal, engine

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter(
    prefix="/sensors",
    responses={404: {"description": "Not found"}},
    tags=["sensors"],
)


@router.get("")
def get_sensors(db: Session = Depends(get_db)):
    return db.query(models.Sensor).all()

@router.get("/{sensor_id}")
def get_sensor(sensor_id: int, db: Session = Depends(get_db)):
    db_sensor = repository.get_sensor(db, sensor_id)
    if db_sensor is None:
        raise HTTPException(status_code=404, detail="Sensor not found")
    return db_sensor

@router.post("")
def create_sensor(sensor: schemas.SensorCreate, db: Session = Depends(get_db)):
    db_sensor = repository.get_sensor_by_name(db, sensor.name)
    if db_sensor:
        raise HTTPException(status_code=400, detail="Sensor with same name already registered")
    return repository.create_sensor(db=db, sensor=sensor)

@router.post("/{sensor_id}/data")
def record_data(sensor_id: int, data: schemas.SensorData, db: Session = Depends(get_db)):
    db_sensor = repository.get_sensor(db, sensor_id)
    if db_sensor is None:
        raise HTTPException(status_code=404, detail="Sensor not found")
    return repository.record_data(db=db, sensor_id=sensor_id, data=data)

@router.delete("/{sensor_id}")
def delete_sensor(sensor_id: int, db: Session = Depends(get_db)):
    db_sensor = repository.get_sensor(db, sensor_id)
    if db_sensor is None:
        raise HTTPException(status_code=404, detail="Sensor not found")
    return repository.delete_sensor(db=db, sensor_id=sensor_id)
    
