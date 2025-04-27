from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas, crud
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Optional: Enable CORS if you need it
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

@app.post("/api/post/sensors/", response_model=schemas.SensorResponse)
def create_sensor(sensor: schemas.SensorCreate, db: Session = Depends(get_db)):
    return crud.create_sensor(db, sensor)


@app.post("/api/post/sensors/bulk/")
def create_sensors_bulk(sensors: List[schemas.SensorCreate], db: Session = Depends(get_db)):
    db_sensors = [models.Sensor(**sensor.model_dump(exclude_unset=True)) for sensor in sensors]
    db.add_all(db_sensors)
    db.commit()
    return {"message": "✅ Bulk insert successful", 
            "count": len(db_sensors)
            }

@app.get("/api/get_all/sensors/", response_model=list[schemas.SensorResponse])
def get_all_sensors(db: Session = Depends(get_db)):
    result = crud.get_all_sensors(db)
    result.append({"message": "success"})
    return result

@app.get("/get/sensors/{sensor_type}", response_model=schemas.SensorResponse,)
def get_sensor(sensor_type: str, db: Session = Depends(get_db)):
    sensor = crud.get_sensor_by_type(db, sensor_type)
    if not sensor:
        raise HTTPException(status_code=404, detail="Data not found")
    return sensor
