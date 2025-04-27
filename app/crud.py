from sqlalchemy.orm import Session
from . import models, schemas

def create_sensor(db: Session, sensor: schemas.SensorCreate):
    db_sensor = models.Sensor(**sensor.model_dump())
    db.add(db_sensor)
    db.commit()
    db.refresh(db_sensor)
    return db_sensor

def get_all_sensors(db: Session):
    return db.query(models.Sensor).all()

def get_sensor_by_type(db: Session, sensor_type: str):
    return db.query(models.Sensor).filter(models.Sensor.type == sensor_type).first()
