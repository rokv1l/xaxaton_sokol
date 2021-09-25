from src.db import session_maker
from src.aggregated_sensors import AggregatedSensor


def get_block_areas():
    with session_maker() as session:
        sensors = session.query(AggregatedSensor).all()
        blocks = []
        for sensor in sensors:
            blocks.append(
                {'lat': sensor.lat,
                 'lng': sensor.lng,
                 'radius': 1000,
                 'pollution': sensor.aggregated_aqi}
            )
    return blocks


def only_red_zones(blocks):
    return list(filter(lambda block: block['pollution'] > 200, blocks))
