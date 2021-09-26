from math import radians, cos, sin, asin, sqrt

from src.db import session_maker
from src.interest_places import InterestPlace
from src.bike_base import BikeBase
from src.aggregated_sensors import AggregatedSensor


def haversine(lat1, lng1, lat2, lng2):
    R = 6371.0  # this is in km

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
            if not is_place_green(place.lat, place.lng):
                continue
            length = haversine(lat, lng, place.lat, place.lng) * 1000
            if length < radius:
                result.append({
                    'name': place.name,
                    'lat': place.lat,
                    'lng': place.lng,
                    'img': place.img,
                    'lenth': length
                })
    return result


def get_bike_bases_nearby(lat, lng, radius):
    with session_maker() as session:
        bike_bases = session.query(BikeBase).all()
        result = []
        for base in bike_bases:
            if not is_place_green(base.lat, base.lng):
                continue
            length = haversine(lat, lng, base.lat, base.lng) * 1000
            if length < radius:
                result.append({
                    'address': base.address,
                    'lat': base.lat,
                    'lng': base.lng,
                    'is_open': base.is_open,
                    'lenth': length
                })
    return result


def is_place_green(lat, lng):
    with session_maker() as session:
        red_zones = session.query(AggregatedSensor).filter(AggregatedSensor.aggregated_aqi > 70).all()
        for zone in red_zones:
            length = haversine(lat, lng, zone.lat, zone.lng) * 1000
            if length < 850:
                return False
    return True


def get_green_zones(lat, lng, radius):
    with session_maker() as session:
        green_zones = session.query(AggregatedSensor).filter(AggregatedSensor.aggregated_aqi < 70).all()
        result = []
        for base in green_zones:
            if not is_place_green(base.lat, base.lng):
                continue
            length = haversine(lat, lng, base.lat, base.lng) * 1000
            if length < radius:
                result.append({
                    'lat': base.lat,
                    'lng': base.lng,
                    'lenth': length
                })
                break
    return result

def get_bad_zones_in_place(lat, lng):
    with session_maker() as session:
        red_zones = session.query(AggregatedSensor).filter(AggregatedSensor.aggregated_aqi > 70).all()
        bad_zones = []
        for zone in red_zones:
            length = haversine(lat, lng, zone.lat, zone.lng) * 1000
            if length < 850:
                bad_zones.append({
                    'lat': zone.lat,
                    'lng': zone.lng,
                    'radius': 850,
                    'pollution': zone.aggregated_aqi
                })
    return bad_zones
