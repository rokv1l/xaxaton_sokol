from flask_restful import Resource, reqparse
from utils.graphhopper import get_routes, PointInRedZone, SurroundedByRedZones
from utils.graphhopper import get_sensor_zones, yellow_and_red_zones, only_red_zones
from utils.places_nearby import get_bike_bases_nearby


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

        zones = get_sensor_zones()
        yellow_red_zones = yellow_and_red_zones(zones)
        try:
            routes = get_routes([args['from'], args['to']], args['vehicle'], block_areas=yellow_red_zones)
            return routes, 200
        except PointInRedZone:
            return {'error': 'point in red zone'}, 404
        except SurroundedByRedZones:
            red_zones = green_and_yellow_zones(zones)
            try:
                routes = get_routes([args['from'], args['to']], args['vehicle'], block_areas=red_zones)
            except SurroundedByRedZones:
                routes = get_routes([args['from'], args['to']], args['vehicle'])
            return routes
