from flask_restful import Resource, reqparse

from utils.multi_modal import enrich_foot_route
from utils.graphhopper import get_walking_route, PointInRedZone, SurroundedByRedZones


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

        distance = args.get('distance')
        if not distance:
            time = args.get('time')
            if not time:
                return {'error': 'either distance or time must be specified'}, 404
            
            if args['vehicle'] == 'bike':
                distance = int(time * AVG_BIKE_SPEED)
            else:
                distance = int(time * AVG_FOOT_SPEED)
                
        distance *= 1000
        
        # нужно добавить логику получения красных зон
        try:
            routes = []
            for seed in range(args['limit']):
                route = get_walking_route(args['from'], distance, args['vehicle'], seed=seed)
                
                if args['vehicle'] == 'foot':
                    multi_route = enrich_foot_route(deepcopy(eco_route))
                    if multi_route:
                        routes.append(multi_route)
                
                route["waypoints"] = [{ "waypoint" : eco_route["waypoints"], "color" : "#62cc00"}]
                routes.append(route)
            return routes, 200
        except PointInRedZone:
            return {'error': 'point in red zone'}, 404
        except SurroundedByRedZones:
            return {'error': 'surrounded'}, 404
        
