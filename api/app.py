from flask import Flask
from flask_cors import CORS
from flask_restful import Api

from utils.init_sensors import init_sensors
from utils.aggregation import aggregate_sensors_data, distribute_coords
from src.db import session_maker
from src.sensors import Sensor
from src.aggregated_sensors import AggregatedSensor
from resources.hello import Hello
from resources.route import Route
from resources.zones import Zones
from resources.walking import WalkingRoute


app = Flask(__name__)
CORS(app)
api = Api(app)

api.add_resource(Hello, '/hello')
api.add_resource(Route, '/route')
api.add_resource(WalkingRoute, '/walking')
api.add_resource(Zones, "/zones")


if __name__ == '__main__':
    with session_maker() as session:
        if not session.query(Sensor).first():
            init_sensors()
        if not session.query(AggregatedSensor).first():
            aggregate_sensors_data()
            distribute_coords()
    app.run(host='0.0.0.0', port=5000, debug=True)
