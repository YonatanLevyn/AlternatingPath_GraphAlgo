import copy
from collections import deque
from typing import List, Dict, Tuple, Any

def bfs_util(graph: Dict[int, List[int]], source: int, destination: int) -> Tuple[Dict[int, Any], int]:
    """
    Perform BFS to find the shortest path and distance between source and destination in the graph.
    
    Args:
        graph (Dict[int, List[int]]): The adjacency list representation of the graph.
        source (int): The source node.
        destination (int): The destination node.
    
    Returns:
        Tuple[Dict[int, Any], int]: A tuple containing the parent dictionary for path reconstruction
                                     and the shortest distance to the destination node.
    """
    bfs_queue = deque([source])
    visited = {node: False for node in graph}
    parent = {node: None for node in graph}
    distance = {node: float('inf') for node in graph}
    
    visited[source] = True
    distance[source] = 0

    while bfs_queue:
        current = bfs_queue.popleft()
        for neighbour in graph[current]:
            if not visited[neighbour]:
                visited[neighbour] = True
                distance[neighbour] = distance[current] + 1
                parent[neighbour] = current
                bfs_queue.append(neighbour)
                if neighbour == destination:
                    return parent, distance[destination]
    return parent, distance[destination]

def shortest_path(graph: Dict[int, List[int]], source: int, destination: int) -> List[int]:
    """
    Find the shortest path between source and destination using BFS.
    
    Args:
        graph (Dict[int, List[int]]): The adjacency list representation of the graph.
        source (int): The source node.
        destination (int): The destination node.
    
    Returns:
        List[int]: A list of nodes representing the shortest path from source to destination.
    """
    parent, _ = bfs_util(graph, source, destination)
    path = []
    current = destination
    while current is not None:
        path.append(current)
        current = parent[current]
    return path[::-1]

def shortest_distance(graph: Dict[int, List[int]], source: int, destination: int) -> int:
    """
    Find the shortest distance between source and destination using BFS.
    
    Args:
        graph (Dict[int, List[int]]): The adjacency list representation of the graph.
        source (int): The source node.
        destination (int): The destination node.
    
    Returns:
        int: The shortest distance from source to destination.
    """
    _, distance = bfs_util(graph, source, destination)
    return distance

def contract_nodes(graph: 'Graph', node1: int, node2: int) -> 'Graph':
    """
    Contract two nodes into a single node in the graph.
    
    Args:
        graph (Graph): The graph object.
        node1 (int): The first node to contract.
        node2 (int): The second node to contract.
    
    Returns:
        Graph: A new graph object with the nodes contracted.
    """
    new_graph = copy.deepcopy(graph)
    new_graph.nodes.remove(node1)
    for edge in new_graph.edges:
        if node1 == edge[0]:
            edge[0] = node2
        elif node1 == edge[1]:
            edge[1] = node2
    new_graph.edges = [list(edge) for edge in set(tuple(edge) for edge in new_graph.edges)]
    if [node2, node2] in new_graph.edges:
        new_graph.edges.remove([node2, node2])
    return new_graph

def add_edge_to_matching(matching: 'Matching', vertex1: int, vertex2: int) -> 'Matching':
    """
    Add an edge to the matching.
    
    Args:
        matching (Matching): The matching object.
        vertex1 (int): The first vertex of the edge.
        vertex2 (int): The second vertex of the edge.
    
    Returns:
        Matching: The updated matching object.
    """
    if vertex1 in matching.nodes or vertex2 in matching.nodes or [vertex1, vertex2] in matching.edges or [vertex2, vertex1] in matching.edges:
        return matching
    matching.edges.append([vertex1, vertex2])
    matching.nodes.extend([vertex1, vertex2])
    return matching

def aux_add_edge_to_matching(matching: 'Matching', vertex1: int, vertex2: int) -> 'Matching':
    """
    Auxiliary function to add an edge to the matching without ensuring validity.
    
    Args:
        matching (Matching): The matching object.
        vertex1 (int): The first vertex of the edge.
        vertex2 (int): The second vertex of the edge.
    
    Returns:
        Matching: The updated matching object.
    """
    if [vertex1, vertex2] not in matching.edges and [vertex2, vertex1] not in matching.edges:
        matching.edges.append([vertex1, vertex2])
        if vertex1 not in matching.nodes:
            matching.nodes.append(vertex1)
        if vertex2 not in matching.nodes:
            matching.nodes.append(vertex2)
    return matching

def remove_edge_from_matching(matching: 'Matching', vertex1: int, vertex2: int) -> 'Matching':
    """
    Remove an edge from the matching.
    
    Args:
        matching (Matching): The matching object.
        vertex1 (int): The first vertex of the edge.
        vertex2 (int): The second vertex of the edge.
    
    Returns:
        Matching: The updated matching object.
    """
    if [vertex1, vertex2] in matching.edges:
        matching.edges.remove([vertex1, vertex2])
    elif [vertex2, vertex1] in matching.edges:
        matching.edges.remove([vertex2, vertex1])
    if vertex1 in matching.nodes:
        matching.nodes.remove(vertex1)
    if vertex2 in matching.nodes:
        matching.nodes.remove(vertex2)
    return matching

class Forest:
    def __init__(self):
        self.tree_list = []

    def add_tree(self, tree: 'Tree'):
        self.tree_list.append(tree)

    def get_tree_by_node(self, node: int) -> int:
        for index, tree in enumerate(self.tree_list):
            if node in tree.nodes:
                return index
        return -1

    def is_in_forest(self, node: int) -> bool:
        return any(node in tree.nodes for tree in self.tree_list)

    def tree(self, tree_index: int) -> 'Tree':
        return self.tree_list[tree_index]

    def tree_graph(self, tree_index: int) -> Dict[int, List[int]]:
        return self.tree_list[tree_index].graph

    def get_root(self, node: int) -> int:
        for tree in self.tree_list:
            if node in tree.nodes:
                return tree.root
        return -1

class Tree:
    def __init__(self, root: int):
        self.root = root
        self.nodes = [root]
        self.graph = {root: []}

    def add_edge(self, vertex1: int, vertex2: int):
        if vertex1 not in self.nodes:
            self.nodes.append(vertex1)
        if vertex2 not in self.nodes:
            self.nodes.append(vertex2)
        if vertex1 not in self.graph:
            self.graph[vertex1] = []
        if vertex2 not in self.graph:
            self.graph[vertex2] = []
        if vertex2 not in self.graph[vertex1]:
            self.graph[vertex1].append(vertex2)
        if vertex1 not in self.graph[vertex2]:
            self.graph[vertex2].append(vertex1)

class Graph:
    def __init__(self):
        self.edges = []
        self.nodes = []

    def has_edge(self, vertex1: int, vertex2: int) -> bool:
        return [vertex1, vertex2] in self.edges or [vertex2, vertex1] in self.edges

    def get_edges(self, node: int) -> List[List[int]]:
        return [edge for edge in self.edges if node in edge]

class Matching(Graph):
    def get_edges(self, node: int) -> List[int]:
        for edge in self.edges:
            if node in edge:
                return edge
        return []



"""
1. import copy:
   - Purpose: Provides functions for deep and shallow copying of objects.
   - Usage: Used in the contract_nodes function to create a deep copy of the graph when contracting nodes, ensuring the original graph remains unchanged.

2. from collections import deque:
   - Purpose: Provides a double-ended queue that supports adding and removing elements from both ends efficiently.
   - Usage: Used in the bfs_util function to implement the breadth-first search (BFS) queue.

3. from typing import List, Dict, Tuple, Any:
   - Purpose: Provides type hints for function arguments and return values.
   - Usage: Used throughout the code to specify the expected types of variables and function return values, improving code readability and type checking.
"""

# Explanation of bfs_util Function Arguments
"""
1. graph:
   - Type: Dict[int, List[int]]
   - Explanation: The graph is represented as a dictionary where the keys are node identifiers (integers), and the values are lists of integers representing the adjacent nodes (neighbors) of each node. This is known as an adjacency list representation of the graph.
   - Definition: This type of graph representation is not explicitly defined within the function but is a common convention in graph-related algorithms. Here is an example of such a graph:
     graph = {
         0: [1, 2],
         1: [0, 3],
         2: [0, 3],
         3: [1, 2]
     }

2. source:
   - Type: int
   - Explanation: The source is the starting node for the BFS. It is an integer representing the node identifier in the graph.
   - Value: The integer value should correspond to a valid node identifier within the graph.

3. destination:
   - Type: int
   - Explanation: The destination is the target node for which the shortest path and distance are to be found from the source node. It is also an integer representing the node identifier.
   - Value: The integer value should correspond to a valid node identifier within the graph.
"""

# Explanation of BFS Execution and Path Finding
"""
Let's walk through an example of how the bfs_util function works using a simple graph:

graph = {
    0: [1, 2],
    1: [0, 3],
    2: [0, 3],
    3: [1, 2]
}
source = 0
destination = 3

1. Initialization:
   - bfs_queue: Initialized with the source node [0].
   - visited: {0: True, 1: False, 2: False, 3: False}.
   - parent: {0: None, 1: None, 2: None, 3: None}.
   - distance: {0: 0, 1: inf, 2: inf, 3: inf}.

2. BFS Execution:
   - Dequeue node 0, explore neighbors 1 and 2.
   - Mark 1 and 2 as visited, set their distance to 1, set their parent to 0.
   - Enqueue nodes 1 and 2.
   - Dequeue node 1, explore neighbors 0 and 3.
   - Mark 3 as visited, set its distance to 2, set its parent to 1.
   - Enqueue node 3.
   - Destination 3 is found, return parent and distance.

3. Output:
   - parent: {0: None, 1: 0, 2: 0, 3: 1}
   - distance: 2

This BFS traversal finds the shortest path from node 0 to node 3, with a distance of 2 and the path being reconstructed using the parent dictionary.
"""

