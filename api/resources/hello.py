from datetime import datetime

from flask_restful import Resource


class Hello(Resource):
    def get(self):
        return {
            "now": datetime.now().isoformat()
        }, 200