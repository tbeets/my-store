""" Basic routines for a storedb abstraction """

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

        print('parseinputfile()')

        with open(file_obj, 'r') as f:
           reader = csv.DictReader(f, fieldnames=COLHEADERS, quotechar='"', delimiter=',')
           for row in reader:
              self.datarows.append(row)

        print self.datarows

        for _, elem in enumerate(self.datarows):
            self.geolist.append((float(elem[LATITUDE]), float(elem[LONGITUDE])))

if __name__ == '__main__':

    mystore = StoreDB()
    mystore.parseinputfile('./data/stores.csv')

    print mystore.getgeolist()



