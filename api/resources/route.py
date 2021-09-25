from flask_restful import Resource, reqparse
from utils.graphhopper import get_eco_route


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

        eco_route = get_eco_route([args['from'], args['to']], args['vehicle'])
        return [eco_route], 200
