from pydantic import BaseModel

class SensorBase(BaseModel):
    username: str
    type: str
    value: str
    timestamp: str

class SensorCreate(SensorBase):
    pass

class SensorResponse(SensorBase):
    id: int

    class Config:
        from_attributes = True
