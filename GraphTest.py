from graph_syx import *


def testTreeTraversal():
    #=====================================
    #   Tree Test Case
    #         A
    #        / \
    #       B   C
    #      / \   \
    #     D   E   G
    #        /
    #       F
    root = DataStructure.BinaryTreeVertex('A')
    nodeB = DataStructure.BinaryTreeVertex('B')
    nodeC = DataStructure.BinaryTreeVertex('C')
    nodeD = DataStructure.BinaryTreeVertex('D')
    nodeE = DataStructure.BinaryTreeVertex('E')
    nodeF = DataStructure.BinaryTreeVertex('F')
    nodeG = DataStructure.BinaryTreeVertex('G')
    root.children(nodeB, nodeC)
    nodeB.children(nodeD, nodeE)
    nodeC.right = nodeG
    nodeE.left = nodeF
    print root
    print 'Pre-order: '
    Algorithms.preorder_iterative(root)
    print '\nIn-order: '
    Algorithms.inorder_iterative(root)
    print '\nPost-order: '
    Algorithms.postorder_iterative(root)


def testGraphTraversal():
    #=====================================
    #   Graph Test Case
    #      1 --- 2 --- 5 --- 6
    #      |   / |     | \   |
    #      | /   |     |   \ |
    #      4 --- 3     8 --- 7
    #      |               /
    #      9 --- 10      /
    #      | \   |     /
    #      |   \ |   /
    #      12 -- 11
    links = [(1,2),(2,3),(3,4),(4,1),(2,4),
            (5,6),(6,7),(7,8),(8,5),(5,7),
            (9,10),(10,11),(11,12),(12,9),(9,11),
            (2,5),(4,9),(7,11)]
    graph = DataStructure.Graph()
    for (ori, des) in links:
        graph.add_biedge(ori, des, 1)
    source = graph.get_vertices()[0]
    seq_bfs = Algorithms.bfs_iterative(graph, source)
    print 'BFS sequence: ', seq_bfs
    seq_dfs = Algorithms.dfs_recursive(graph, source)
    print 'DFS sequence: ', seq_dfs
    seq_euler = Algorithms.euler_tour(graph)
    print 'Euler tour: ', seq_euler


def testTSPHeuristic():
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
    testTreeTraversal()
