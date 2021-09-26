from copy import deepcopy

from flask_restful import Resource, reqparse

from utils.multi_modal import enrich_foot_route
from utils.graphhopper import get_eco_walking_route


AVG_BIKE_SPEED = 250  # м/мин
AVG_FOOT_SPEED = 100  # м/мин


class WalkingRoute(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('from', required=True)
        parser.add_argument('distance', type=int)
        parser.add_argument('time', type=int)
        parser.add_argument('vehicle', default='foot')
        parser.add_argument('limit', type=int, default=3)

        args = parser.parse_args()
        print(args)
        try:
            args['from'] = list(map(float, args['from'].split(',')))
        except:
            return {'error': 'invalid coordinates'}, 404
        
        distance = args.get('distance', 0)
        if distance:
            distance *= 1000
        
        if not distance:
            time = args.get('time')
            if not time:
                return {'error': 'either distance or time must be specified'}, 404
            
            if args['vehicle'] == 'bike':
                distance = int(time * AVG_BIKE_SPEED)
            else:
                distance = int(time * AVG_FOOT_SPEED)
        
        routes = []
        for seed in range(args['limit']):
            route = get_eco_walking_route(args['from'], distance, args['vehicle'], seed=seed)
            route["points"] = []
            if len(routes) > 2:
                route["waypoints"] = [{ "waypoint" : route["waypoints"], "color" : "#62cc00"}]
                routes.append(route)
                break
            
            if args['vehicle'] == 'foot':
                multi_route = enrich_foot_route(deepcopy(route))
                if multi_route:
                    routes.append(multi_route)
            
            route["waypoints"] = [{ "waypoint" : route["waypoints"], "color" : "#62cc00"}]
            routes.append(route)
        return routes, 200
