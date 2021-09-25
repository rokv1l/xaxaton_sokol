import json

from src.db import session_maker
from src.interest_places import InterestPlace


def add_place_to_db():
    with open('files_to_db/interesting_places.json', 'r') as file:
        places_data = json.load(file)
    for data in places_data:
        with session_maker() as session:
            place = InterestPlace(
                name=data['name'],
                lat=data['pos']['Lat'],
                lng=data['pos']['Lon'],
                img=data['img']
            )
            session.add(place)
            session.commit()
