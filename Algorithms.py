# Graph Algorithm class
# Author: Siyang Xie
# Date: 04/04/2015


import heapq
import time
import DataStructure
from collections import deque



def preorder_iterative(source):
    """Iterative version of pre-order tree traversal

       no need to worry about visit first or mark first
       since the graph is a tree here
    """
    unvisited = [source]
    while len(unvisited)!=0:
        vex = unvisited.pop()
        print vex
        if vex.right is not None:
            unvisited.append(vex.right)
        if vex.left is not None:
            unvisited.append(vex.left)


def inorder_iterative(source):
    """Iterative version of in-order tree traversal

       no need to worry about visit first or mark first
       since the graph is a tree here
    """
    vex = source
    unvisited = []
    while len(unvisited)!=0 or vex is not None:
        if vex is not None:
            unvisited.append(vex)
            vex = vex.left
        else:
            vex = unvisited.pop()
            print vex
            vex = vex.right


def postorder_iterative(source):
    """Iterative version of post-order tree traversal

       no need to worry about visit first or mark first
       since the graph is a tree here
    """
    #============== version 1 use one stack ================
    # vex = source
    # lastVisited = None
    # unvisited = []
    # while len(unvisited)!=0 or vex is not None:
    #     if vex is not None:
    #         unvisited.append(vex)
    #         vex = vex.left
    #     else:
    #         vextemp = unvisited[-1]
    #         if vextemp.right is not None and vextemp.right != lastVisited:
    #             vex = vextemp.right
    #         else:
    #             vextemp.print_vertex()
    #             lastVisited = unvisited.pop()
    #============== version 2 use two stacks ================
    unvisited = [source] # stack 1
    sequence = [] # stack 2
    while len(unvisited)!=0:
        vex = unvisited.pop()
        # the parent vertex is always visited after its children
        sequence.append(vex)
        if vex.left is not None:
            unvisited.append(vex.left)
        if vex.right is not None:
            unvisited.append(vex.right)
    while len(sequence)!=0:
        vex = sequence.pop()
        print vex


# def bfs_recursive(graph, source):
#     """Recursive version of bfs
#     """
#     def bfs(vex):
#         vex.visited = True
#         for v in vex.adjvertices:
#             if !v.visited:
#                 bfs(vex)
#
#     vertices = graph.get_vertices()
#     for vex in vertices:
#         vex.visited = False
#     if



def bfs_iterative(graph, source):
    """Iterative version of bfs

       In BFS whether you mark nodes visited as they leave
       the Queue or as they enter, has no impact on the order,
       it is just that conventionally people mark it
       before entering the Queue
    """
    vertices = graph.get_vertices()
    for vex in vertices:
        vex.visited = False
    unvisited = deque([source])
    source.visited = True
    sequence = []
    while len(unvisited)>0:
        vex_pop = unvisited.popleft()
        sequence.append(vex_pop.id)
        for item in vex_pop.adjvexs:
            if not item.visited:
                item.visited = True
                unvisited.append(item)
    return sequence


def dfs_recursive(graph, source):
    """Recursive version of dfs
    """
    def dfs(vex):
        sequence.append(vex.id)
        vex.visited = True
        for adj in vex.adjvexs:
            if adj.visited == False:
                dfs(adj)
    sequence = []
    vexs = graph.get_vertices()
    for vex in vexs:
        vex.visited = False
    dfs(source)
    return sequence


def dfs_iterative(graph, source):
    """Iterative version of dfs

       mark each node visited after you pop it out

       if you were to mark a node visited each time
       you pushed it in the stack your order of visiting
       the nodes would not comply with the idea of
       a Depth First Search
    """
    vexs = graph.get_vertices()
    for vex in vexs: # mark all vertices as unvisited
        vex.visited = False
    unvisited = [source]
    sequence = []
    while len(unvisited)>0:
        vex_pop = unvisited.pop()
        if not vex_pop.visited:
            vex_pop.visited = True
            sequence.append(vex_pop.id)
            for item in vex_pop.adjvexs:
                unvisited.append(item)
    return sequence


def reverse_shortest(target, path):
    if target.previous:
        path.append(target.previous.get_id())
        reverse_shortest(target.previous, path)


def dijkstra(graph, source):
    """ Dijkstra algorithm to calculate single source
    shortest path problem

    source: the single source vertex
    """
    start_time = time.clock()
    source.distance = 0
    unvisited = [(vertex.distance, vertex) for vertex in graph]
    heapq.heapify(unvisited)

    while len(unvisited)>0:
        vex_pop = heapq.heappop(unvisited)[1]
        vex_pop.visited = True
        for item in vex_pop.adjacent:
            if item.visited:
                continue
            new_distance = vex_pop.get_distance() + vex_pop.get_linklength(item)
            if new_distance < item.get_distance():
                item.distance = new_distance
                item.previous = vex_pop
        while len(unvisited):
            heapq.heappop(unvisited)
        unvisited = [(vertex.distance, vertex) for vertex in graph if not vertex.visited]
        heapq.heapify(unvisited)
    end_time = time.clock()
    print 'Running time for dijkstra algorithm: ' + str(end_time - start_time)


def floyd_warshall(graph):
    start_time = time.clock()
    vertices = graph.get_vertices()
    distance = {}
    for n in vertices:
        v_n = n.get_id()
        distance[v_n] = {}
        for m in vertices:
            v_m = m.get_id()
            if v_n==v_m:
                distance[v_n][v_m] = 0
            elif graph.vertex_dict[v_m] in graph.vertex_dict[v_n].adjacent:
                distance[v_n][v_m] = graph.vertex_dict[v_n].get_linklength(graph.vertex_dict[v_m])
            else:
                distance[v_n][v_m] = 10000
    for k in vertices:
        v_k = k.get_id()
        for i in vertices:
            v_i = i.get_id()
            for j in vertices:
                v_j = j.get_id()
                if distance[v_i][v_k] + distance[v_k][v_j] < distance[v_i][v_j]:
                    distance[v_i][v_j] = distance[v_i][v_k] + distance[v_k][v_j]
    end_time = time.clock()
    print 'Running time for floyd warshall algorithm: ' + str(end_time - start_time)
    return distance


def prim(points, distances):
    """Use prim algorithm to construct a minimum spanning tree

    """
    N = len(points)
    curr_vertices = [0]
    mst_links = []
    for i in xrange(N-1):
        tempMax, tempCurr, tempOther = 100000000.0, -1, -1
        for j in curr_vertices:
            other_vertices = list(set(range(N))-set(curr_vertices))
            for k in other_vertices:
                if distances[j,k]<=tempMax:
                    tempMax = distances[j,k]
                    tempCurr, tempOther = j, k
        curr_vertices.append(tempOther)
        mst_links.append((tempCurr, tempOther))
    return mst_links


def is_connected(graph, flag):
    """Check whether a graph is connected or not, using dfs

    """
    vertices = graph.get_vertices()
    if len(vertices) == 0:
        return False
    seq = dfs_iterative(graph, vertices[0])
    return len(seq)==len(vertices)


def euler_tour(graph):
    """Use Fleury's Algorithm to find an Euler tour

    """
    vertices = graph.get_vertices()
    num_edges = graph.num_edges/2
    source = vertices[0].id
    sequence = [source]
    count_edges = 0
    while count_edges<num_edges:
        flag = False
        adjacent = [vex.id for vex in graph.get_vertex(source).adjvexs]
        for vex in adjacent:
            graph.remove_biedge(source, vex)
            is_conn = is_connected(graph, source)
            if is_conn:
                sequence.append(vex)
                source = vex
                count_edges = count_edges+1
                flag = True
                break
            else:
                graph.add_biedge(source, vex, 1)
        if not flag:
            for vex in adjacent:
                graph.remove_biedge(source, vex)
                sequence.append(vex)
                source = vex
                count_edges = count_edges+1
    return sequence
