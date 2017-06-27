from graph_syx import *


# #=====================================
# #   Tree Test Case
# #         A
# #        / \
# #       B   C
# #      / \   \
# #     D   E   G
# #        /
# #       F
# root = DataStructure.BinaryTreeVertex('A')
# nodeB = DataStructure.BinaryTreeVertex('B')
# nodeC = DataStructure.BinaryTreeVertex('C')
# nodeD = DataStructure.BinaryTreeVertex('D')
# nodeE = DataStructure.BinaryTreeVertex('E')
# nodeF = DataStructure.BinaryTreeVertex('F')
# nodeG = DataStructure.BinaryTreeVertex('G')
# root.children(nodeB, nodeC)
# nodeB.children(nodeD, nodeE)
# nodeC.right = nodeG
# nodeE.left = nodeF
# print root
# print 'Pre-order: '
# Algorithms.preorder_iterative(root)
# print '\nIn-order: '
# Algorithms.inorder_iterative(root)
# print '\nPost-order: '
# Algorithms.postorder_iterative(root)
# #======================================



# #=====================================
# #   Graph Test Case
# #      1 --- 2 --- 5 --- 6
# #      |   / |     | \   |
# #      | /   |     |   \ |
# #      4 --- 3     8 --- 7
# #      |               /
# #      9 --- 10      /
# #      | \   |     /
# #      |   \ |   /
# #      12 -- 11
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
