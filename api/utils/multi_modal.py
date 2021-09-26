from collections import defaultdict
from datetime import datetime

from .places_nearby import get_bike_bases_nearby
from .graphhopper import get_eco_route
from .places_nearby import get_places_nearby, haversine, get_green_zones

FOOT_COLOR = '#007bff'
BIKE_COLOR = '#00ff55'


def enrich_foot_route(route):
    _route = route.copy()
    transfers = find_transfers_to_bike(route)
    if not transfers:
        return 
        
    
    bike_segment = get_eco_route(
        [transfers['start']['base'], transfers['end']['base']], 
        vehicle='bike'
    )
    segment_1 = get_eco_route([tuple(route['waypoints'][0].values()),  transfers['start']['base']], vehicle="foot")
    segment_2 = get_eco_route([transfers['end']['base'], tuple(route['waypoints'][-1].values())], vehicle="foot")
    route['waypoints'] = [
        {
            "waypoint": segment_1["waypoints"],
            "color": FOOT_COLOR,
        },
        {
            "waypoint": bike_segment['waypoints'],
            "color": BIKE_COLOR,
        },
        {
            "waypoint": segment_2["waypoints"],
            "color": FOOT_COLOR,
        },
    ]
    route['dist'] = bike_segment['dist'] + segment_1['dist'] + segment_2['dist']
    
    route['time'] = bike_segment['time'] + segment_1['time'] + segment_2['time']

    route['points'] = [
        {'lat': transfers['start']['base'][1], 'lng': transfers['start']['base'][0], 'type': 'bike'},
        {'lat': transfers['end']['base'][1], 'lng': transfers['end']['base'][0], 'type': 'bike'}
    ]

    for i in (0, 2):
        interesting_places = find_interesting_places(route['waypoints'][i]['waypoint'])
        for place, point in interesting_places.items():
            route['waypoints'].append({
                'waypoint': get_eco_route([[point['lng'], point['lat']], list(reversed(place))])['waypoints'],
                'color': '#7027b6'
            })

            route['points'].append({
                'lat': point['lat'],
                'lng': point['lng'],
                'type': 'intres',
            })
    
    for i in (0, 2):
        green_place = get_green_route(route['waypoints'][i]['waypoint'])
        for place, point in green_place.items():
            route['waypoints'].append({
                'waypoint': get_eco_route([[point['lng'], point['lat']], list(reversed(place))])['waypoints'],
                'color': '#ffed00'
            })

    
    return route


def get_green_route(route):
    total_len = len(route)
    step = total_len // 10
    if step == 0:
        step = 2
    place_to_points = defaultdict(list)
    for i in range(0, total_len, step):
        point = route[i]
        print(point)
        places = get_green_zones(point['lat'], point['lng'], 300)
        for place in places:
            place_to_points[(point['lat'], point['lng'])].append(place)

    for place, points in place_to_points.items():
        place_to_points[place] = min(points, 
                                     key=lambda p: haversine(p['lat'], p['lng'], *place))
    
    return place_to_points



def find_transfers_to_bike(route):
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

    return {
        'start': {'idx': start_point_idx,
                  'base': (start_base['lng'], start_base['lat'])},
        'end': {'idx': end_point_idx,
                'base': ( end_base['lng'], end_base['lat'])}
    }


def find_interesting_places(route):
    total_len = len(route)
    step = total_len // 10
    if step == 0:
        step = 2
    place_to_points = defaultdict(list)
    for i in range(0, total_len, step):
        point = route[i]
        print(point)
        places = get_places_nearby(point['lat'], point['lng'], 300)
        for place in places:
            place_to_points[(point['lat'], point['lng'])].append(place)

    for place, points in place_to_points.items():
        place_to_points[place] = min(points, 
                                     key=lambda p: haversine(p['lat'], p['lng'], *place))
    
    return place_to_points
