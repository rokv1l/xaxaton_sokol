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
                print(street_name, sensor_num, sensor_mean_aqi)
                tmp = AggregatedSensor(street=street_name, sensor_num=sensor_num,
                                       lng=0, lat=0,
                                       aggregated_aqi=sensor_mean_aqi)
                session.add(tmp)
                session.commit()


def distribute_coords():
    print('start loading graph')
    g = ox.load_graphml(f'{config.sensors_data_path}/G_moscow_walk.graphml')
    print('graph downloaded')

    streets = defaultdict(list)
    with session_maker() as session:
        sensors = session.query(AggregatedSensor).all()
        for sensor in sensors:
            streets[sensor.street].append(sensor.sensor_num)

    street_name_hashes = {frozenset(street_name.lower().split()): street_name for street_name in streets.keys()}

    street_nodes = defaultdict(list)  # street name hash to nodes
    for u, _, e in g.edges(data=True):
        street_name = e.get('name')
        if isinstance(street_name, str):
            street_name_hash = frozenset(street_name.lower().split())
            if street_name_hash in street_name_hashes:
                node = g.nodes[u]
                street_name = street_name_hashes[street_name_hash]
                street_nodes[street_name].append([node['x'], node['y']])

    for street_name, nodes in street_nodes.items():
        nodes.sort()
        total_nodes = len(nodes)
        total_sensors = len(streets[street_name])
        step = total_nodes // total_sensors

        with session_maker() as session:
            sensor_num = 1
            for i in range(0, total_nodes, step):
                sensor_coords = nodes[i]
                session.query(AggregatedSensor).filter(AggregatedSensor.street == street_name,
                                                       AggregatedSensor.sensor_num == sensor_num).update(
                                                           {'lat': sensor_coords[0], 'lng': sensor_coords[1]}
                                                       )
                sensor_num += 1
                print(street_name, sensor_num, sensor_coords)
            session.commit()
