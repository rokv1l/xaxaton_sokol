from datetime import datetime

from .places_nearby import get_bike_bases_nearby
from .graphhopper import get_eco_route
from .colors import colorize

FOOT_COLOR = '#007bff'
BIKE_COLOR = '#00ff55'


def enrich_foot_route(route):
    transfers = find_transfers_to_bike(route)
    if not transfers:
        return 
        
    
    bike_segment = get_eco_route(
        [transfers['start']['base'], transfers['end']['base']], 
        vehicle='bike'
    )
    route['waypoints'] = [
        {
            "waypoint": get_eco_route([tuple(route['waypoints'][0].values()),  transfers['start']['base']], vehicle="foot")["waypoints"],
            "color": FOOT_COLOR,
        },
        {
            "waypoint": bike_segment['waypoints'],
            "color": BIKE_COLOR,
        },
        {
            "waypoint": get_eco_route([transfers['end']['base'], tuple(route['waypoints'][-1].values())], vehicle="foot")["waypoints"],
            "color": FOOT_COLOR,
        },
    ]


    route['points'] = [
        {'lat': transfers['start']['base'][1], 'lng': transfers['start']['base'][0], 'type': 'bike'},
        {'lat': transfers['end']['base'][1], 'lng': transfers['end']['base'][0], 'type': 'bike'}
    ]

    return route


def find_transfers_to_bike(route):
    
    start_time = datetime.now()
    total_len = len(route['waypoints'])

    start = int(total_len * 0.1)
    start_point_idx = None
    start_base = None

    for i in range(start, total_len, 3):
        point = route['waypoints'][i]
        bike_bases = get_bike_bases_nearby(point['lat'], point['lng'], radius=600)
        if bike_bases:
            start_point_idx = i
            start_base = bike_bases[0]
            break
    
    if not start_base:
        return
    
    print(f"1 {datetime.now() - start_time}")
    
    end_point_idx = None
    end_base = None

    for i in range(total_len-1, start_point_idx, -3):
        point = route['waypoints'][i]
        bike_bases = get_bike_bases_nearby(point['lat'], point['lng'], radius=600)
        if bike_bases:
            for bike_base in bike_bases:
                if bike_base["address"] != start_base["address"]:
                    end_point_idx = i
                    end_base = bike_base
                    break
            if end_base:
                break

    if not end_base:
        return

    print(f"2 {datetime.now() - start_time}")
    return {
        'start': {'idx': start_point_idx,
                  'base': (start_base['lng'], start_base['lat'])},
        'end': {'idx': end_point_idx,
                'base': ( end_base['lng'], end_base['lat'])}
    }
