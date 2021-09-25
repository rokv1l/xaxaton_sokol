import os
from collections import defaultdict

import numpy as np
import osmnx as ox

import config
from src.db import session_maker
from src.sensors import Sensor
from src.aggregated_sensors import AggregatedSensor


def aggregate_sensors_data():
    streets = defaultdict(dict)
    for file in os.listdir(config.sensors_data_path):
        street_name = file.replace('.xls', '').split('_')[0]
        sensor_num = file.replace('.xls', '').split('_')[1]
        streets[street_name][sensor_num] = {'pollution': 0}

    for street_name in streets:
        for sensor_num in streets[street_name]:
            with session_maker() as session:
                sensors = session.query(Sensor).filter(Sensor.street == street_name, 
                                                       Sensor.sensor_num == sensor_num).all()
                sensor_mean_aqi = np.mean([sensor.aqi for sensor in sensors])
                streets[street_name][sensor_num] = {'pollution': sensor_mean_aqi}

    for street_name in distribute_coords(streets):
        for sensor_num in streets[street_name]:
            with session_maker() as session:
                sensor = streets[street_name][sensor_num]
                try:
                    agg_sensor = AggregatedSensor(street=street_name, sensor_num=sensor_num,
                                                  lng=sensor['coords']['x'], lat=sensor['coords']['y'],
                                                  aggregated_time=0, time_interval=0,
                                                  aggregated_aqi=sensor['pollution'])
                except:
                    print(f'sensor {sensor_num} for {street_name} didn\'t distributed')
                else:
                    session.add(agg_sensor)
                    session.commit()


def distribute_coords(streets):
    g = ox.graph_from_place('Россия, Москва', network_type='walk')
    print('Graph downloaded')

    # street name hash to real street name
    street_name_hashes = {
        frozenset(street_name.split()): street_name for street_name in streets.keys()
    }

    street_nodes = defaultdict(list)  # street name hash to nodes
    for u, _, e in g.edges(data=True):
        street_name = e.get('name')
        if isinstance(street_name, str):
            street_name_hash = frozenset(street_name.lower().split())
            if street_name_hash in street_name_hashes:
                node = g.nodes[u]
                street_nodes[street_name_hash].append(node['x'], node['y'])

    for street_name_hash, street_name in street_name_hashes.items():
        nodes = street_nodes[street_name_hash]
        nodes.sort()
        total_sensors = len(streets[street_name])

        sensor_num = 1
        for i in range(0, total_sensors, len(nodes) // total_sensors):
            sensor_coords = nodes[i]
            streets[street_name][sensor_num]['coords'] = sensor_coords
            sensor_num += 1

    return streets
