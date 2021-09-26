from copy import deepcopy
from flask_restful import Resource, reqparse
from utils.graphhopper import get_eco_route
from utils.multi_modal import enrich_foot_route
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
        eco_route['points'] = []
#         routes.append(eco_route)

        if args['vehicle'] == 'foot':
            multi_route = enrich_foot_route(deepcopy(eco_route))
            if multi_route:
                routes.append(multi_route)

        return routes, 200
