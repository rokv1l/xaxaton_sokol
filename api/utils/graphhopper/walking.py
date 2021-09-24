import requests

import config
from exceptions import PointInRedZone, SurroundedByRedZones, UnknownError
from common import block_areas_to_string, mark_waypoints


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
    path = data['paths'][0]
    return {
        'waypoints': mark_waypoints(path['points']['coordinates']),
        'dist': path['distance'],
        'time': path['time'],
    }
