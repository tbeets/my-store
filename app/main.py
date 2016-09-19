""" my-store service implementation """

import os, geo, storedb
from flask import Flask
from flask_restful import Api, Resource, reqparse, abort

DEFAULT_RADIUS = 25
DEFAULT_MAXSTORES = 10

app = Flask(__name__)
api = Api(app)
db = storedb.StoreDB()


@api.resource('/api/stores')
class Stores(Resource):
    def __init__(self):
        super(Stores, self).__init__()

    def get(self):
        return db.datarows


@api.resource('/api/store/<int:store_id>')
class Store(Resource):

    global db

    def __init__(self):
        # self.parser = reqparse.RequestParser()
        # self.parser.add_argument('store_id', type=int, required=True, help='data index (int)')
        super(Store, self).__init__()


    def get(self, store_id):
        # args = self.parser.parse_args()
        store = db.getstore(store_id)
        if store is None:
            abort(404, message="Store {} doesn't exist".format(store_id))
        return db.getstore(store_id)


@api.resource('/api/nearest')
class Nearest(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('q', type=str, required=True, help='location (deg) in format loc:lat+long')
        # q=loc%3A30.4%2B-113.2
        self.parser.add_argument('r', type=int, required=False,
                                 default=DEFAULT_RADIUS, help='radius in miles (int)')
        self.parser.add_argument('max', type=int, required=False,
                                 default=DEFAULT_MAXSTORES, help='max stores returned (int)')
        super(Nearest, self).__init__()

    def get(self):
        args = self.parser.parse_args()

        coords = ''
        custp = ()

        try:
            coords = args['q'][4:].split('+')
            custp = (float(coords[0]), float(coords[1]))
        except:
            abort(400, message="Geo coordinate could not be parsed.")

        hits = []
        radius = int(args['r'])
        maxhits = int(args['max'])

        for i, storep in enumerate(db.geolist):
            if len(hits) == maxhits:
                break
            elif geo.dist(custp,storep) <= radius:
                hits.append(i)

        nearby = [db.getstore(i) for i in hits]
        # return {'hello': args['r'], 'bye': args['max'], 'geo': args['q']}
        return nearby


@app.route('/', methods=['GET'])
def site():
    return "<html><body>Hello world.</body></html>"


if __name__ == '__main__':

    db.parseinputfile('data/stores.csv')

    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)