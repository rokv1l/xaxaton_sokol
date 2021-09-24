from flask import Flask
from flask_restful import Api

from resources.hello import Hello


app = Flask(__name__)
api = Api(app)

api.add_resource(Hello, '/hello')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)