
from sqlalchemy import Column, Text, Integer, Float, JSON, DateTime

from src.db import base, engine


class Sensor(base):
    __tablename__ = 'sensors'

    id = Column(Integer, primary_key=True)

    street = Column(Text)
    sensor_num = Column(Integer)
    coords = Column(JSON)

    measurement_datetime = Column(DateTime)
    temperature = Column(Float)
    humidity = Column(Float)
    co2 = Column(Float)
    los = Column(Float)
    pm1 = Column(Float)
    pm2_5 = Column(Float)
    pm10 = Column(Float)
    pressure = Column(Float)
    aqi = Column(Float)
    formaldehyde = Column(Float)


base.metadata.create_all(engine)
