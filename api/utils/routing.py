import requests

import config
from exceptions import PointInRedZone, SurroundedByRedZones, UnknownError
from common import block_areas_to_string, mark_waypoints


def get_routes(departure, destination, vehicle='foot', block_areas=None, alternative_routes=None):
    payload = {
        'points': [departure, destination],
        'points_encoded': False,
        'vehicle': vehicle,
        # если True и добавить locale=ru, выдаст еще инструкции на русском
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
        
    response = requests.post(config.URL, json=payload)
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
