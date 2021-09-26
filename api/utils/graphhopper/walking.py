import requests

import config
from .exceptions import PointInRedZone, SurroundedByRedZones, UnknownError
from .common import block_areas_to_string, mark_waypoints
from .block_areas import get_sensor_zones, yellow_and_red_zones, only_red_zones
from ..places_nearby import get_bad_zones_in_place


def get_eco_walking_route(point, distance, vehicle='foot', seed=None):
    zones = get_sensor_zones()

    # удаляем зоны, если какая-либо точка маршрута в плохой зоне
    zones_to_delete = get_bad_zones_in_place(point[1], point[0])

    clear_zones = []
    for zone in zones:
        if zone in zones_to_delete:
            continue
        clear_zones.append(zone)

    # сначала строим с учетом красных и зеленых зон
    yellow_red_zones = yellow_and_red_zones(clear_zones)
    try:
        route = get_walking_route(point, distance, vehicle, block_areas=yellow_red_zones, seed=seed)
        return route
    # если не получилось, строим только с учетом красных зон
    except SurroundedByRedZones:
        red_zones = only_red_zones(clear_zones)
        try:
            route = get_walking_route(point, vehicle, block_areas=red_zones, seed=seed)
        # если опять не получилось, строим простой маршрут
        except SurroundedByRedZones:
            route = get_walking_route(point, vehicle, seed=None)
            
        return route


def get_walking_route(departure, distance, vehicle='foot', block_areas=None, seed=None):
    payload = {
        'points': [departure],
        'points_encoded': False,
        'vehicle': vehicle,
        'instructions': False,
        'ch.disable': True,
        'algorithm': 'round_trip',
        'round_trip.distance': distance,
    }
    
    if block_areas:
        payload['block_area'] = block_areas_to_string(block_areas)
    if seed:
        payload['round_trip.seed'] = seed
                
    response = requests.post(config.gh_url, json=payload)
    if response.status_code != 200:
        error = response.json()
        if error['message'] == 'Connection between locations not found':
            raise SurroundedByRedZones
        elif 'Request with block_area contained query point' in error['message']:
            coords = (error['message']
                         .strip('Request with block_area contained query point ')
                         .strip('. This is not allowed.'))
            point = list(map(float, coords.split(',')))
            raise PointInRedZone(point)
        else:
            raise UnknownError(error['message'])
    
    data = response.json()
    path = data['paths'][0]
    return {
        'waypoints': mark_waypoints(path['points']['coordinates']),
        'dist': path['distance'],
        'time': path['time'],
    }
