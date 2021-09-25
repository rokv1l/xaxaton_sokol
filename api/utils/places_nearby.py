from math import radians, cos, sin, asin, sqrt

from src.db import session_maker
from src.interest_places import InterestPlace
from src.bike_base import BikeBase


def haversine(lat1, lng1, lat2, lng2):
    R = 6372.8  # this is in km

    dLat = radians(lat2 - lat1)
    dLng = radians(lng2 - lng1)
    lat1 = radians(lat1)
    lat2 = radians(lat2)

    a = sin(dLat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dLng / 2) ** 2
    c = 2 * asin(sqrt(a))

    return R * c


def get_places_nearby(lat, lng, radius):
    with session_maker() as session:
        places = session.query(InterestPlace).all()
        result = []
        for place in places:
            if haversine(lat, lng, place.lat, place.lng) * 1000 < radius:
                result.append({
                    'name': place.name,
                    'lat': place.lat,
                    'lng': place.lng,
                    'img': place.img
                })
    return result


def get_bike_bases_nearby(lat, lng, radius):
    with session_maker() as session:
        bike_bases = session.query(BikeBase).all()
        result = []
        for base in bike_bases:
            if haversine(lat, lng, base.lat, base.lng) * 1000 < radius:
                result.append({
                    'address': base.address,
                    'lat': base.lat,
                    'lng': base.lng,
                    'is_open': base.is_open
                })
    return result
