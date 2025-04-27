from sqlalchemy import Column, Integer, String
from .database import Base

class Sensor(Base):
    __tablename__ = "sensors_data"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), index=True)
    type = Column(String(50))
    value = Column(String(50))
    timestamp = Column(String(50))