from src.db import session_maker
from src.aggregated_sensors import AggregatedSensor


GREEN_THRESHOLD = 70
YELLOW_THRESHOLD = 99


def get_block_areas():
    with session_maker() as session:
        sensors = session.query(AggregatedSensor).filter(AggregatedSensor.lat != 0).all()
        blocks = []
        for sensor in sensors:
            blocks.append(
                {'lat': sensor.lat,
                 'lng': sensor.lng,
                 'radius': 700,
                 'pollution': sensor.aggregated_aqi}
            )
    return blocks


def only_green_zones(blocks):
    return list(filter(lambda block: block['pollution'] > GREEN_THRESHOLD, blocks))


def green_and_yellow_zones(blocks):
    return list(filter(lambda block: block['pollution'] > YELLOW_THRESHOLD, blocks))
