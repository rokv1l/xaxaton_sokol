from copy import deepcopy
from flask_restful import Resource, reqparse
from utils.graphhopper import get_eco_route
from utils.multi_modal import enrich_foot_route, get_green_route
from utils.colors import colorize

FOOT_COLOR = '#007bff'
BIKE_COLOR = '#00ff55'


class Route(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('from', required=True)
        parser.add_argument('to', required=True)
        parser.add_argument('vehicle', default='foot')

        args = parser.parse_args()        
        try:
            args['from'] = list(map(float, args['from'].split(',')))
            args['to'] = list(map(float, args['to'].split(',')))
        except:
            return {'error': 'invalid coordinates'}, 404

        routes = []

        eco_route = get_eco_route([args['from'], args['to']], args['vehicle'])
        eco_route['points'] = [{
                "lat": 55.74603,
                "lng": 37.57995,
                "type": "intres"
            }]
        
        green_place = get_green_route(eco_route)['waypoints']
        for place, point in green_place.items():
            green_route = get_eco_route([[point['lng'], point['lat']], list(reversed(place))])
            green_route['waypoints'].append({
                'waypoint': green_route['waypoints'],
                'color': '#ffed00'
            })
            routes.append(green_route)
        if args['vehicle'] == 'foot' and eco_route["dist"] > 2000:
            multi_route = enrich_foot_route(deepcopy(eco_route))
            if multi_route:
                routes.append(multi_route)
        
        eco_route["waypoints"] = [{ "waypoint" : eco_route["waypoints"], "color" : "#62cc00"}]
        routes.append(eco_route)

        return routes, 200
