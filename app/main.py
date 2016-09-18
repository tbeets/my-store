""" my-store service implementation """

import os, geo
from flask import Flask
from flask_restful import Api, Resource, reqparse, abort

app = Flask(__name__)
api = Api(app)


@api.resource('/api/stores')
class Stores(Resource):
    def get(self):
        return {'hello': 'world'}


@api.resource('/api/store/<string:store_id>')
class Store(Resource):
    def get(self, store_id):
        return {'hello': 'world'}


@api.resource('/api/nearest')
class Nearest(Resource):
    def get(self):
        return {'hello': 'world'}


@app.route('/', methods=['GET'])
def site():
    return "<html><body>Hello world.</body></html>"


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)