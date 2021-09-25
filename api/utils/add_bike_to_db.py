import json

from src.db import session_maker
from src.bike_base import BikeBase


def add_bike_base_to_db():
    with open('files_to_db/bike_new.json', 'r') as file:
        bike_base_data = json.load(file)
    for data in bike_base_data:
        with session_maker() as session:
            bike = BikeBase(
                address=data['addres'],
                lat=data['pos']['Lat'],
                lng=data['pos']['Lon'],
                is_open=True
            )
            session.add(bike)
            session.commit()
