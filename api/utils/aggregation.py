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
                if aggregated_data and sensor_data.measurement_datetime >= aggregated_data['datetime'] + timedelta(hours=time_interval):
                    tmp = AggregatedSensor(
                        street=street,
                        sensor_num=sensor_num,
                        lng=0,
                        lat=0,
                        aggregated_time=aggregated_data['datetime'],
                        time_interval=time_interval,
                        aggregated_aqi=float(pd.DataFrame(aggregated_data['aqi']).describe().mean())
                    )
                    session.add(tmp)
                    session.commit()
                    aggregated_data = {}

                if not aggregated_data:
                    aggregated_data['datetime'] = sensor_data.measurement_datetime
                    aggregated_data['aqi'] = []

                aggregated_data['aqi'].append(sensor_data.aqi)


def add_coords_to_aggregated_sensors_data():
    g = ox.graph_from_place('Россия, Москва', network_type='walk')
    print('Graph downloaded')

    with session_maker() as session:
        sensors_data = session.query(AggregatedSensor).filter(AggregatedSensor.lat == 0).all()
        for sensor_data in sensors_data:
            street_nodes = []
            for u, v, e in g.edges(data=True):
                if e.get('name') == sensor_data.street:
                    street_nodes.append(g.nodes[u])

            node = street_nodes[randint(0, len(street_nodes)) - 1]
            session.query(AggregatedSensor).filter(AggregatedSensor.id == sensor_data.id).update({'lat': node['y'], 'lng': node['x']})
            session.commit()
