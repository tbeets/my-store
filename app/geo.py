""" Essential geographic coordinate functions

Reference:

https://en.wikipedia.org/wiki/Great-circle_distance
https://en.wikipedia.org/wiki/Haversine_formula
http://stackoverflow.com/questions/365826/calculate-distance-between-2-gps-coordinates
https://github.com/mapado/haversine (MIT License)

"""

from haversine import haversine


def dist(p1, p2):
    """ Two point tuples (degrees) returning distance in miles """
    return haversine(p1, p2, miles=True)

