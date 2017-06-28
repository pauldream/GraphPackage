# Graph Data structure class
# Author: Siyang Xie
# Date: 04/03/2015


class Vertex(object):
    """
    Class for graph vertex.
    """
    def __init__(self, vertex):
        self.id = vertex  # (String/Int) index of the vertex
        self.adjvexs = [] # to allow multi-graph
        self.adjlinks = {}  # Key: (Vertex)adjacent vertices; Value: (Float)link length
        # For dijkstra's Algorithm
        self.distance = 1000000  # Distance from the specified source
        self.visited = False  # Whether is has been visited in the dijkstra algorithm
        self.previous = None  # Track its precessor in the shortest path

    def add_adjacent(self, neighbor, length):  #
        """ add (Vertex)neighbor as an adjacent vertex. """
        self.adjvexs.append(neighbor)
        self.adjlinks[neighbor] = length

    def remove_adjacent(self, neighbor):
        """ remove (Vertex)neighbor from the adjacent list. """
        self.adjvexs.remove(neighbor)
        del self.adjlinks[neighbor]

    def get_linklength(self, neighbor):  # get the length from (Vertex)itself to (Vertex)neighbor
        return self.adjlinks[neighbor]

    def __str__(self):
        """ Printout when calling *print vertex* """
        return "Vertex: " + str(self.id) + '; Adjacent vertices: ' + str([x.id for x in self.adjvexs])



class BinaryTreeVertex(object):
    def __init__(self, vertex):
        self.id = vertex  # (String/Int)index of the vertex
        self.left = None
        self.right = None
        self.data = []

    def children(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        """ Printout when calling "print vertex"
        """
        strVertex = "Vertex " + str(self.id) + "; "
        strLeft = "Left child: " + (self.left.id if self.left!=None else " ") + "; "
        strRight = "Right child: " + (self.right.id if self.right!=None else " ") + "; "
        return strVertex + strLeft + strRight



class Graph:
    def __init__(self):
        self.numVexs = 0
        self.numLinks = 0
        self.vertex_dict = {}  # Key:(String/int)index of vertex; Value:(Vertex)vertex in the graph

    def __iter__(self):
        return iter(self.vertex_dict.values())

    def get_vertex(self, id):  # Given vertex index, return (Vertex)vertex
        if id in self.vertex_dict:
            return self.vertex_dict[id]
        else:
            return None

    def add_vertex(self, vertex):
        self.numVexs = self.numVexs + 1
        newVertex = Vertex(vertex)
        self.vertex_dict[vertex] = newVertex
        return newVertex

    def remove_vertex(self, vertex):
        self.numVexs = self.numVexs - 1
        del self.vertex_dict[vertex]

    def add_link(self, vertexOri, vertexDes, length):
        self.numLinks = self.numLinks + 1
        if vertexOri not in self.vertex_dict:
            self.add_vertex(vertexOri)
        if vertexDes not in self.vertex_dict:
            self.add_vertex(vertexDes)
        self.vertex_dict[vertexOri].add_adjacent(self.vertex_dict[vertexDes], length)

    def add_bilink(self, vertexOri, vertexDes, length):
        self.numLinks = self.numLinks + 2
        if vertexOri not in self.vertex_dict:
            self.add_vertex(vertexOri)
        if vertexDes not in self.vertex_dict:
            self.add_vertex(vertexDes)
        self.vertex_dict[vertexOri].add_adjacent(self.vertex_dict[vertexDes], length)
        self.vertex_dict[vertexDes].add_adjacent(self.vertex_dict[vertexOri], length)

    def remove_link(self, vertexOri, vertexDes):
        self.numLinks = self.numLinks - 1
        self.vertex_dict[vertexOri].remove_adjacent(self.vertex_dict[vertexDes])
        if len(self.vertex_dict[vertexOri].get_adjacent()) == 0: # if vertexOri becomes isolated, remove it
            self.remove_vertex(vertexOri)

    def remove_bilink(self, vertexOri, vertexDes):
        self.numLinks = self.numLinks - 2
        self.vertex_dict[vertexOri].remove_adjacent(self.vertex_dict[vertexDes])
        self.vertex_dict[vertexDes].remove_adjacent(self.vertex_dict[vertexOri])
        if len(self.vertex_dict[vertexOri].adjlinks) == 0:
            self.remove_vertex(vertexOri) # only remove the original node of the edge, if necessary
        if len(self.vertex_dict[vertexDes].adjlinks) == 0:
            self.remove_vertex(vertexDes) # only remove the original node of the edge, if necessary

    def get_vexs(self):
        return self.vertex_dict.values()

    def set_distance_all(self, distance=1000000.0):
        for vex in self:
            vex.set_distance(distance)

    def set_visited_all(self):
        for vex in self:
            vex.set_visited(False)

    def set_previous_all(self):
        for vex in self:
            vex.set_previous(None)

    def print_graph(self):
        print 'Graph data:'
        print '  Start     End     Length'
        for v in self:
            for w in v.get_adjacent():
                vid = v.get_id()
                wid = w.get_id()
                print '(%3s   ,  %3s   ,  %1f   )' % ( vid, wid, v.get_linklength(w))

    def __str__(self):
        return "Graph with " + str(self.numNodes) + " nodes and " + str(self.numLinks) + " links."
