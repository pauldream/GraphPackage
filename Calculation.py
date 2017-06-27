import math
import numpy as np


def distance_lonlat(lon1, lat1, lon2, lat2):
    radius = 6371 #3961
    lon1 /= 180./math.pi
    lon2 /= 180./math.pi
    lat1 /= 180./math.pi
    lat2 /= 180./math.pi
    # First calculation method
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = (math.sin(dlat/2.))**2 + math.cos(lat1) * math.cos(lat2) * (math.sin(dlon/2.))**2
    dist = 2 * radius * math.atan2(math.sqrt(a), math.sqrt(1-a))
    
    # Second calculation method
    # a1 = math.sin(lat1*math.pi/180) * math.sin(lat2*math.pi/180)
    # a2 = math.cos(lat1*math.pi/180) * math.cos(lat2*math.pi/180) * math.cos(lon1*math.pi/180) * math.cos(lon2*math.pi/180)
    # a2 = math.cos(lat1*math.pi/180) * math.cos(lat2*math.pi/180) * math.sin(lon1*math.pi/180) * math.sin(lon2*math.pi/180)
    # dist = radius * math.acos(a1 + a2 + a3)
    return dist


def distances_lonlat(points):
    N = len(points)
    distances = np.empty((N, N))
    for i in xrange(N):
        lati = points[i, 0]
        loni = points[i, 1]
        for j in xrange(N):
            latj = points[j, 0]
            lonj = points[j, 1]
            if i==j:
                distances[i, j] = 10000.0
            else:
                distances[i, j] = distance_lonlat(loni, lati, lonj, latj)
    return distances


def distance_xy(x1, y1, x2, y2):
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)


def distances_xy(points):
    N = len(points)
    distances = np.empty((N, N))
    for i in xrange(N):
        xi = points[i, 0]
        yi = points[i, 1]
        for j in xrange(N):
            xj = points[j, 0]
            yj = points[j, 1]
            if i==j:
                distances[i, j] = 10000.0
            else:
                distances[i, j] = distance_xy(x1,y1,x2,y2)
    return distances
