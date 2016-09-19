""" my-store service implementation """

import os, geo, storedb
from flask import Flask
from flask_restful import Api, Resource, reqparse, abort

DEFAULT_RADIUS = 25
DEFAULT_MAXSTORES = 10

app = Flask(__name__)
api = Api(app)

"""
In a production service, we could go grab this file/data from an object store or a data service. We'd want
a live refresh scheme that is sensitive to the process/threads scale model of our service too.
"""
db = storedb.StoreDB()
db.parseinputfile('data/stores.csv')

@api.resource('/stores')
class Stores(Resource):
    def __init__(self):
        super(Stores, self).__init__()

    def get(self):
        return db.datarows

@api.resource('/store/<int:store_id>')
class Store(Resource):

    global db

    def __init__(self):
        super(Store, self).__init__()

    def get(self, store_id):
        # args = self.parser.parse_args()
        store = db.getstore(store_id)
        if store is None:
            abort(404, message="Store {} doesn't exist".format(store_id))
        return db.getstore(store_id)


@api.resource('/stores/nearest')
class Nearest(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()

        """
         We'll use a geo format that is Googlish, e.g. q=loc:30.4+-113.2
        """
        self.parser.add_argument('q',
                                 type=str,
                                 required=True,
                                 help='location (deg) in format loc:lat+long')
        self.parser.add_argument('r',
                                 type=int,
                                 required=False,
                                 default=DEFAULT_RADIUS,
                                 help='radius in miles (int)')
        self.parser.add_argument('max',
                                 type=int,
                                 required=False,
                                 default=DEFAULT_MAXSTORES,
                                 help='max stores returned (int)')
        super(Nearest, self).__init__()

    def get(self):
        args = self.parser.parse_args()

        custp = ()

        try:
            coords = args['q'][4:].split('+')
            custp = (float(coords[0]), float(coords[1]))
        except:
            abort(400, message="Geo coordinate could not be parsed.")

        hits = []
        nearby = []
        radius = args['r']
        maxhits = args['max']

        """
        Possibly inefficient if there are many stores; could filter by country and state...
        And/or create some Store graphs with edges representing distance from each other.
        Basically, avoid computing customer distance over the world of stores looking for near(ish) hits.
        """
        for i, storep in enumerate(db.geolist):
            if len(hits) == maxhits:
                break

            dist = geo.dist(custp,storep)
            if dist <= radius:
                hits.append((i, dist))

        """
        copy() because we are going to add some request specific fields and threads happen...

        Reference on maps.google.com:
        http://stackoverflow.com/questions/2660201/what-parameters-should-i-use-in-a-google-maps-url-to-go-to-a-lat-lon
        """
        for _, item in enumerate(hits):
            store = db.getstore(item[0]).copy()
            store['dist'] = item[1]
            nearby.append(store)

        nearby.sort(key=lambda store: store['dist'])

        return nearby


if __name__ == '__main__':

    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)