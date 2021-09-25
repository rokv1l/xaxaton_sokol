
from sqlalchemy import Column, Text, Integer, Float

from src.db import base, engine


class InterestPlace(base):
    __tablename__ = 'interest_places'

    id = Column(Integer, primary_key=True)

    name = Column(Text)
    lat = Column(Float)
    lng = Column(Float)

    img = Column(Text)


base.metadata.create_all(engine)
