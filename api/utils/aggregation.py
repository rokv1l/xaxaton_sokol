import os
from random import randint

import pandas as pd
import osmnx as ox
from datetime import datetime, timedelta

import config
from src.db import session_maker
from src.sensors import Sensor
from src.aggregated_sensors import AggregatedSensor


def aggregate_sensors_data(time_interval):

    files = os.listdir(config.sensors_data_path)

    for file in files:
        street = file.replace('.xls', '').split('_')[0]
        sensor_num = file.replace('.xls', '').split('_')[-1]

        with session_maker() as session:
            sensors_data = session.query(Sensor).filter(Sensor.street == street, Sensor.sensor_num == sensor_num).all()
            aggregated_data = {}
            for sensor_data in sensors_data:
                if aggregated_data and datetime.fromisoformat(sensor_data.measurement_datetime[:-1]) >= aggregated_data['datetime'] + timedelta(hours=time_interval):
                    AggregatedSensor(
                        street=street,
                        sensor_num=sensor_num,
                        coords={},
                        aggregated_time=aggregated_data['datetime'],
                        time_interval=time_interval,
                        aggregated_aqi=float(pd.DataFrame(aggregated_data['aqi']).describe().mean())
                    )
                    session.add(AggregatedSensor)
                    session.commit()
                    aggregated_data = {}

                if not aggregated_data:
                    aggregated_data['datetime'] = datetime.fromisoformat(sensor_data.measurement_datetime[:-1])
                    aggregated_data['aqi'] = []

                aggregated_data['aqi'].append(sensor_data.aqi)


def add_coords_to_aggregated_sensors_data():
    g = ox.graph_from_place('Россия, Москва', network_type='walk')

    with session_maker() as session:
        sensors_data = session.query(AggregatedSensor).filter(AggregatedSensor.coords == {}).all()
        for sensor_data in sensors_data:
            street_nodes = []
            for u, v, e in g.edges(data=True):
                if e.get('name') == sensor_data.street:
                    street_nodes.append(g.nodes[u])

            node = street_nodes[randint(0, len(street_nodes)) - 1]
            session.query(AggregatedSensor).filter(id=sensor_data.id).update({'coords': {'lat': node['y'], 'lng': node['x']}})
            session.commit()
