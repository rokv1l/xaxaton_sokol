from src.db import session_maker
from src.aggregated_sensors import AggregatedSensor


GREEN_THRESHOLD = 70
YELLOW_THRESHOLD = 99
RADIUS = 850


def get_sensor_zones():
    with session_maker() as session:
        sensors = session.query(AggregatedSensor).filter(AggregatedSensor.lat != 0).all()
        blocks = []
        for sensor in sensors:
            blocks.append(
                {'lat': sensor.lat,
                 'lng': sensor.lng,
                 'radius': RADIUS,
                 'pollution': sensor.aggregated_aqi}
            )
    return blocks


def yellow_and_red_zones(blocks):
    return list(filter(lambda block: block['pollution'] > GREEN_THRESHOLD, blocks))


def only_red_zones(blocks):
    return list(filter(lambda block: block['pollution'] > YELLOW_THRESHOLD, blocks))
