"""
Basic routines for a store database abstraction and parsing input CSV file.
See README.md for field mapping
"""

import csv

COLHEADERS = ('C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10',
              'C11', 'C12', 'C13', 'C14', 'C15', 'C16', 'C17', 'C18', 'C19', 'C20',
              'C21', 'C22', 'C23', 'C24')
LATITUDE = 'C16'
LONGITUDE = 'C17'

class StoreDB:
    def __init__(self):
        self.datarows = []
        self.geolist = []

    def getstore(self, row_id):
        if row_id >= 0 and row_id < len(self.datarows):
            return self.datarows[row_id]
        return None

    def getgeolist(self):
        return self.geolist

    def parseinputfile(self, file_obj):

        # reset to allow on-demand refresh, refresh makes more sense in a non-trivial storedb implementation...
        self.datarows = []
        self.geolist = []

        print 'Parsing input file...'

        with open(file_obj, 'r') as f:
           reader = csv.DictReader(f, fieldnames=COLHEADERS, quotechar='"', delimiter=',')
           for row in reader:
              self.datarows.append(row)

        """
        Add a Google map link for each store as a downstream UX aid.
        Reference: http://stackoverflow.com/questions/2660201/what-parameters-should-i-use-in-a-google-maps-url-to-go-to-a-lat-lon

        Create a separate list of geo tuples as a comparison and convenience index using haversine calculation.
        """
        for _, elem in enumerate(self.datarows):
            elem['map_url'] = "".join(('http://maps.google.com/maps?z=12&t=m&q=loc:',
                                        elem[LATITUDE], '+', elem[LONGITUDE]))
            self.geolist.append((float(elem[LATITUDE]), float(elem[LONGITUDE])))

        print 'Parse complete'

if __name__ == '__main__':

    # For testing
    mystore = StoreDB()
    mystore.parseinputfile('./data/stores.csv')

    print mystore.getgeolist()



