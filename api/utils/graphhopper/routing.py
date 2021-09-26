import requests

import config
from .exceptions import PointInRedZone, SurroundedByRedZones, UnknownError
from .common import block_areas_to_string, mark_waypoints
from .block_areas import get_sensor_zones, yellow_and_red_zones, only_red_zones
from ..places_nearby import get_bad_zones_in_place


def get_eco_route(points, vehicle='foot'):
    zones = get_sensor_zones()

    # удаляем зоны, если какая-либо точка маршрута в плохой зоне
    zones_to_delete = []
    for point in points:
        zones_to_delete.extend(get_bad_zones_in_place(point[1], point[0]))

    clear_zones = []
    for zone in zones:
        if zone in zones_to_delete:
            continue
        clear_zones.append(zone)

    # сначала строим с учетом красных и зеленых зон
    yellow_red_zones = yellow_and_red_zones(clear_zones)
    try:
        routes = get_routes(points, vehicle, block_areas=yellow_red_zones)
        return routes[0]
    # если не получилось, строим только с учетом красных зон
    except SurroundedByRedZones:
        red_zones = only_red_zones(clear_zones)
        try:
            routes = get_routes(points, vehicle, block_areas=red_zones)
        # если опять не получилось, строим простой маршрут
        except SurroundedByRedZones:
            routes = get_routes(points, vehicle)
            
        return routes[0]


def get_routes(points, vehicle='foot', block_areas=None, alternative_routes=None):
    payload = {
        'points': points,
        'points_encoded': False,
        'vehicle': vehicle,
        'instructions': False,  
    }
    
    if block_areas:
        payload['ch.disable'] = True
        payload['block_area'] = block_areas_to_string(block_areas)

    if alternative_routes:
        payload['ch.disable'] = True
        payload['algorithm'] = 'alternative_route'
        payload['alternative_route.max_paths'] = alternative_routes
        # ниже просто большие параметры, чтобы было больше маршрутов
        payload['alternative_route.max_share_factor'] = 1000
        payload['alternative_route.max_weight_factor'] = 1000
        
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
    routes = []
    for path in data['paths']:
        route = {
            'waypoints': mark_waypoints(path['points']['coordinates']),
            'dist': path['distance'],
            'time': path['time'],
        }
        routes.append(route)

    return routes
