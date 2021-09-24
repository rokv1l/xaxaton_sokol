from flask import Flask
from flask_cors import CORS
from flask_restful import Api

from utils.init_sensors import init_sensors
from resources.hello import Hello
from resources.route import Route
from resources.walking import WalkingRoute


app = Flask(__name__)
CORS(app)
api = Api(app)

api.add_resource(Hello, '/hello')
api.add_resource(Route, '/route')
api.add_resource(WalkingRoute, '/walking')


if __name__ == '__main__':
    # init_sensors()
    app.run(host='0.0.0.0', port=5000, debug=True)
