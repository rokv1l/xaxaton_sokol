import random

from flask_restful import Resource

from src.db import session_maker
from src.aggregated_sensors import AggregatedSensor


class Zones(Resource):
    def get(self):
        with session_maker() as session:
            coords = session.query(AggregatedSensor).filter(AggregatedSensor.lat != 0).all()
            result = {
                "sensors": []
            }
            for coord in coords:
                result["sensors"].append({
                    "center": [coord.lat, coord.lng],
                    "radius": 700,
                    "pollution": coord.aggregated_aqi
                })
            return result, 200
