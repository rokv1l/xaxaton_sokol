from flask_restful import Resource, reqparse
from utils.graphhopper import get_routes, PointInRedZone, SurroundedByRedZones


class Route(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('from', required=True)
        parser.add_argument('to', required=True)
        parser.add_argument('vehicle', default='foot')
        parser.add_argument('limit', type=int, default=3)

        args = parser.parse_args()        
        try:
            print(args)
            args['from'] = list(map(float, args['from'].split(',')))
            args['to'] = list(map(float, args['to'].split(',')))
        except:
            return {'error': 'invalid coordinates'}, 404


        # нужно добавить логику получения красных зон
        try:
            routes = get_routes(args['from'], args['to'], args['vehicle'], alternative_routes=args['limit'])
            return routes, 200
        except PointInRedZone:
            return {'error': 'point in red zone'}, 404
        except SurroundedByRedZones:
            return {'error': 'surrounded'}, 404