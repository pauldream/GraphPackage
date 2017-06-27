# Python code for constructing TSP tour
# Author: Siyang Xie (sxie13)
# Time: 11/25/2016

import time
import math
import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from mpl_toolkits.basemap import Basemap
from xlrd import open_workbook

import DataStructure
import Calculation
import Algorithms



def read_data(filename):
    book = open_workbook(filename)
    sheet = book.sheet_by_index(0) # Open the first sheet in the book
    # read the coordinate of each point
    index = sheet.col_values(0,3,153)
    lat = sheet.col_values(1,3,153)
    lon = sheet.col_values(2,3,153)
    # store the info into a dictionary
    points = np.empty((len(index), 2))
    for i in range(len(index)):
        points[i,0] = lat[i]
        points[i,1] = lon[i]
    return points


def treeortour_draw(points, links, method='cheapestInsertion'):
    plt.figure(figsize=(12,8))
    themap = Basemap(projection='gall',
              llcrnrlon = 70,              # lower-left corner longitude
              llcrnrlat = 20,               # lower-left corner latitude
              urcrnrlon = 125,               # upper-right corner longitude
              urcrnrlat = 50,               # upper-right corner latitude
              resolution = 'l',
              area_thresh = 100000.0,
              )
    themap.drawcoastlines()
    themap.drawcountries()
    themap.fillcontinents(color = 'gainsboro')
    themap.drawmapboundary(fill_color='steelblue')

    x1, y1 = themap(points[:,1], points[:,0])
    themap.plot(x1, y1,'H',                    # marker shape
                color = '#f1c40f',         # marker colour
                markersize = 6,          # marker size
                label = 4)
    for i, (x, y) in enumerate(zip(x1, y1), start=1):
        plt.annotate(str(i-1), (x,y),
        xytext=(5, 5),
        textcoords='offset points',
        fontsize=6)
    for (j,k) in links:
        x, y = themap([points[j,1],points[k,1]],[points[j,0],points[k,0]])
        themap.plot(x,y,markersize=3,linewidth=1,color='r')
    plt.xlabel('Latitude')
    plt.ylabel('Longitude')
    plt.title('TSP tour')
    plt.savefig(method+'.pdf')
    plt.show()


def CheapestInsertion(points, distances):
    """Use cheapest insertion heuristic to construct TSP tour

    """
    N = len(points)
    curr_vertices = [0] # set C of nodes that have been selected already
    remain_vertices = range(1,N) # set V\C of nodes that haven't been selected
    dist = distances[0,1:N]
    max_index = np.argmin(dist)+1 # find the longest/shortest distance
    curr_vertices.append(max_index)
    remain_vertices.remove(max_index)
    tsp_links = [(0,max_index),(max_index,0)]
    tsp_length = 2*distances[0,max_index] # length of current tsp tour
    while len(remain_vertices)!=0:
        tempMax, tempPrev, tempCurr, tempNext = 100000000.0, -1, -1, -1
        # find the closest node k in V\C that minimizes the smallest increase
        for k in remain_vertices:
            for (i,j) in tsp_links:
                increase = distances[i,k]+distances[j,k]-distances[i,j]
                if increase<=tempMax:
                    tempMax = increase
                    tempPrev, tempCurr, tempNext = i, k, j
        # insert k into the tour C in the best way
        curr_vertices.append(tempCurr)
        remain_vertices.remove(tempCurr)
        tsp_links.append((tempPrev, tempCurr))
        tsp_links.append((tempCurr, tempNext))
        tsp_links.remove((tempPrev, tempNext))
        tsp_length += (distances[tempPrev, tempCurr] + distances[tempCurr, tempNext] - distances[tempPrev, tempNext])
    return tsp_links, tsp_length


def MSTBased(points, distances, mst_links):
    """Use MST-based heuristic to construct TSP tour

    """
    N = len(points)
    links = {} # construct the multi-graph corresponding to the MST with repetitions
    for (j,k) in mst_links:
        if j not in links:
            links[j] = [k]
        else:
            links[j].append(k)
        if k not in links:
            links[k] = [j]
        else:
            links[k].append(j)

    # take shortcuts using dfs
    init = random.randint(0, N-1)
    curr_vertices = [init]
    tsp_links = []
    tsp_length = 0.0
    while len(curr_vertices)!=0: # iterative dfs
        curr = curr_vertices.pop()
        if curr!=init:
            tsp_links.append((prev,curr))
            tsp_length += distances[prev,curr]
        prev = curr
        for next in links[curr]:
            links[next].remove(curr)
            curr_vertices.append(next) # push the vertice into the stack
        links[curr] = []
    tsp_links.append((curr, init)) # add the last link
    tsp_length += distances[curr, init]
    return tsp_links, tsp_length


def Christofide(points, distances, mst_links):
    """Use christofide's heuristic to construct TSP tour

    """
    # find the set N1 of all nodes that have odd degrees
    odd_degree = []
    for (i,j) in mst_links:
        if i in odd_degree:
            odd_degree.remove(i)
        else:
            odd_degree.append(i)
        if j in odd_degree:
            odd_degree.remove(j)
        else:
            odd_degree.append(j)
    odd_degree.sort()

    N = len(points)
    links = {} # construct the multi-graph corresponding to the (MST + shortest complete matching)
    for (j,k) in mst_links:
        if j not in links:
            links[j] = [k]
        else:
            links[j].append(k)
        if k not in links:
            links[k] = [j]
        else:
            links[k].append(j)
    extra_pair = [(28,143),(104,140),(13,93),(10,70),(117,128),
                (60,145),(8,136),(36,83),(27,106),(26,146),
                (87,149),(76,148),(32,123),(40,78),(43,62),
                (14,100),(34,82),(98,109),(105,142),(2,12),
                (42,85),(15,38),(6,22),(33,126),(71,127),
                (72,110),(19,103),(97,121),(0,53)]  # manually construct complete matching
    for (i,j) in extra_pair:
        links[i].append(j)
        links[j].append(i)

    # construct an Euler tour, Fleury's Algorithm
    graph = DataStructure.Graph()
    for ori in links:
        for des in links[ori]:
            graph.add_edge(ori, des, 1)
    euler = Algorithms.euler_tour(graph)

    # take shortcut from the euler tour to form a TSP tour
    curr_vertices = [euler[0]]
    tsp_links = []
    tsp_length = 0.0
    i = 0
    while i<len(euler)-2:
        ori = euler[i]
        j = i+1
        while j<len(euler)-2 and euler[j] in curr_vertices:
            j += 1
        des = euler[j]
        curr_vertices.append(des)
        tsp_links.append((ori,des))
        tsp_length += distances[ori,des]
        i = j
    tsp_links.append((euler[i], euler[i+1]))
    return tsp_links, tsp_length



def main():
    filename = "data150cities.xls"
    print '\nReading data ...\n'
    points = read_data(filename)

    print 'Calculating distances ...\n'
    distances = Calculation.distances_lonlat(points)

    # Construct TSP tour using cheapest insertion heuristic
    internal_time1 = time.time()
    tsp_links, tsp_length = CheapestInsertion(points, distances)
    internal_time2 = time.time()
    print 'Cheapest insertion time: ', internal_time2 - internal_time1, 'seconds'
    print 'Cheapest insertion tsp length: ', tsp_length, '\n'
    treeortour_draw(points, tsp_links, 'cheapestInsertion')

    # Construct TSP tour using MST-based heuristic
    internal_time3 = time.time()
    mst_links = Algorithms.prim(points, distances)
    tsp_links, tsp_length = MSTBased(points, distances, mst_links)
    internal_time4 = time.time()
    print 'MST based time: ', internal_time4 - internal_time3, 'seconds'
    print 'MST based tsp length: ', tsp_length, '\n'
    treeortour_draw(points, tsp_links, 'MSTBased')

    # Construct TSP tour using Christofide's heuristic
    internal_time5 = time.time()
    mst_links = Algorithms.prim(points, distances)
    tsp_links, tsp_length = Christofide(points, distances, mst_links)
    internal_time6 = time.time()
    print 'Christofide time: ', internal_time6 - internal_time5, 'seconds'
    print 'Christofide tsp length: ', tsp_length, '\n'
    treeortour_draw(points, tsp_links, 'christofide')



if __name__ == "__main__":
    main()
