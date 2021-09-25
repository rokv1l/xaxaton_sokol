
from sqlalchemy import Column, Text, Integer, Float, Boolean

from src.db import base, engine


class BikeBase(base):
    __tablename__ = 'bake_base'

    id = Column(Integer, primary_key=True)

    address = Column(Text)
    lat = Column(Float)
    lng = Column(Float)

    is_open = Column(Boolean)


base.metadata.create_all(engine)
