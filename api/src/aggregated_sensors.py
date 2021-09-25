
from sqlalchemy import Column, Text, Integer, Float, JSON, DateTime

from src.db import base, engine


class AggregatedSensor(base):
    __tablename__ = 'aggregated_sensors'

    id = Column(Integer, primary_key=True)

    street = Column(Text)
    sensor_num = Column(Integer)
    coords = Column(JSON)

    aggregated_time = Column(DateTime)
    time_interval = Column(Integer)

    aggregated_aqi = Column(Float)


base.metadata.create_all(engine)
