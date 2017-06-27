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
        self.num_vertices = 0
        self.num_edges = 0
        self.vertex_dict = {}  # Key:(String/int)index of vertex; Value:(Vertex)vertex in the graph

    def __iter__(self):
        return iter(self.vertex_dict.values())

    def get_vertex(self, vertex):  # Given vertex index, return (Vertex)vertex
        if vertex in self.vertex_dict:
            return self.vertex_dict[vertex]
        else:
            return None

    def add_vertex(self, vertex):
        self.num_vertices = self.num_vertices + 1
        new_vertex = Vertex(vertex)
        self.vertex_dict[vertex] = new_vertex
        return new_vertex

    def remove_vertex(self, vertex):
        self.num_vertices = self.num_vertices - 1
        del self.vertex_dict[vertex]

    def add_edge(self, vertex_ori, vertex_des, length):
        self.num_edges = self.num_edges + 1
        if vertex_ori not in self.vertex_dict:
            self.add_vertex(vertex_ori)
        if vertex_des not in self.vertex_dict:
            self.add_vertex(vertex_des)
        self.vertex_dict[vertex_ori].add_adjacent(self.vertex_dict[vertex_des], length)

    def add_biedge(self, vertex_ori, vertex_des, length):
        self.num_edges = self.num_edges + 2
        if vertex_ori not in self.vertex_dict:
            self.add_vertex(vertex_ori)
        if vertex_des not in self.vertex_dict:
            self.add_vertex(vertex_des)
        self.vertex_dict[vertex_ori].add_adjacent(self.vertex_dict[vertex_des], length)
        self.vertex_dict[vertex_des].add_adjacent(self.vertex_dict[vertex_ori], length)

    def remove_edge(self, vertex_ori, vertex_des):
        self.num_edges = self.num_edges - 1
        self.vertex_dict[vertex_ori].remove_adjacent(self.vertex_dict[vertex_des])
        if len(self.vertex_dict[vertex_ori].get_adjacent()) == 0:
            self.remove_vertex(vertex_ori)

    def remove_biedge(self, vertex_ori, vertex_des):
        self.num_edges = self.num_edges - 2
        self.vertex_dict[vertex_ori].remove_adjacent(self.vertex_dict[vertex_des])
        self.vertex_dict[vertex_des].remove_adjacent(self.vertex_dict[vertex_ori])
        if len(self.vertex_dict[vertex_ori].adjlinks) == 0:
            self.remove_vertex(vertex_ori) # only remove the original node of the edge, if necessary

    def get_vertices(self):
        return self.vertex_dict.values()

    def set_distance_all(self, distance):
        for v in self:
            v.set_distance(distance)

    def set_visited_all(self):
        for v in self:
            v.set_visited(False)

    def set_previous_all(self):
        for v in self:
            v.set_previous(None)

    def print_graph(self):
        print 'Graph data:'
        print '  Start     End     Length'
        for v in self:
            for w in v.get_adjacent():
                vid = v.get_id()
                wid = w.get_id()
                print '(%3s   ,  %3s   ,  %1f   )' % ( vid, wid, v.get_linklength(w))

    def __str__(self):
        return "Graph with " + str(self.num_vertices) + " vertices and " + str(self.num_edges) + " edges."
