from .places_nearby import get_bike_bases_nearby
from .graphhopper import get_eco_route
from .colors import colorize

FOOT_COLOR = '#007bff'
BIKE_COLOR = '#00ff55'


def enrich_foot_route(route):
    transfers = find_transfers_to_bike(route)
    if not transfers:
        return 

    bike_segment = get_eco_route([[transfers['start']['base']], transfers['end']['base']], vehicle='bike')
        
    multi_route_waypoints = colorize(route['waypoints'][:transfers['start']['idx']-1], FOOT_COLOR)
    multi_route_waypoints.extend(colorize(bike_segment, BIKE_COLOR))
    multi_route_waypoints.extend(colorize(route['waypoints'][transfers['end']['idx']+1:]))

    route['waypoints'] = multi_route_waypoints

    route['points'] = [
        {'lat': transfers['start']['base']['lat'], 'lng': transfers['start']['base']['lng'], 'type': 'bike'},
        {'lat': transfers['end']['base']['lat'], 'lng': transfers['end']['base']['lng'], 'type': 'bike'}
    ]

    return route


def find_transfers_to_bike(route):
    total_len = len(route['waypoints'])

    start = int(total_len * 0.2)
    start_point_idx = None
    start_base = None

    for i in range(start, total_len):
        point = route['waypoints'][i]
        bike_bases = get_bike_bases_nearby(point['lat'], point['lng'], radius=1000)
        if bike_bases:
            start_point_idx = i
            start_base = bike_bases[0]
            break
    
    if not start_base:
        return
    
    end_point_idx = None
    end_base = None

    for i in range(total_len, start_point_idx, -1):
        point = route['waypoints'][i]
        bike_bases = get_bike_bases_nearby(point['lat'], point['lng'], radius=1000)
        if bike_bases:
            for bike_base in bike_bases:
                if bike_base != start_base:
                    end_point_idx = i
                    end_base = bike_base
                    break

    if not end_base:
        return

    return {
        'start': {'idx': start_point_idx,
                  'base': (start_base['lat'], start_base['lng'])},
        'end': {'idx': end_point_idx,
                'base': (end_base['lat'], end_base['lng'])}
    }
