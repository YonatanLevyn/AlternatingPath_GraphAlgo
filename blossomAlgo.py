import copy
from graphHelpers import Graph, Matching, add_edge_to_matching, remove_edge_from_matching, shortest_path, shortest_distance, contract_nodes, aux_add_edge_to_matching, Forest, Tree
from typing import List
from graph_visualizer import GraphVisualizer


def compute_maximum_matching(graph: Graph, matching: Matching, visualizer: GraphVisualizer) -> List[int]:
    """
    Computes the maximum matching for a given graph with visualization.

    Args:
        graph (Graph): An instance of the Graph class defined in graph_helpers.py.
        matching (Matching): An instance of the Matching class defined in graph_helpers.py.
        visualizer (GraphVisualizer): An instance of the GraphVisualizer class for visualization.

    Returns:
        List[int]: A list of edges that form the maximum matching in the given graph.
    """
    aug_path = find_augmenting_path(graph, matching, visualizer)
    if not aug_path:
        return matching
    for index in range(len(aug_path) - 1):
        if index % 2 == 0:
            add_edge_to_matching(matching, aug_path[index], aug_path[index + 1])
            visualizer.update_edge(aug_path[index], aug_path[index + 1], "red")
        else:
            remove_edge_from_matching(matching, aug_path[index], aug_path[index + 1])
            visualizer.update_edge(aug_path[index], aug_path[index + 1], "black")
        visualizer.wait_for_click()
    return compute_maximum_matching(graph, matching, visualizer)

def find_augmenting_path(graph: Graph, matching: List[int], visualizer: GraphVisualizer, blossoms: List[List[int]] = []) -> List[int]:
    """
    Finds an augmenting path in the graph given a current matching.

    Args:
        graph (Graph): An instance of the Graph class defined in graph_helpers.py.
        matching (Matching): An instance of the Matching class defined in graph_helpers.py.
        visualizer (GraphVisualizer): An instance of the GraphVisualizer class for visualization.
        blossoms (List[List[int]], optional): A list of blossoms detected in previous calls to this function.

    Returns:
        List[int]: A list of nodes that form an augmenting path if one exists. Returns an empty list if no augmenting path is found.
    """
    def initialize_forest_and_unmatched_nodes():
        forest = Forest()
        unmatched_nodes = []
        for node in graph.nodes:
            if all(node not in edge for edge in matching.edges):
                forest.add_tree(Tree(node))
                unmatched_nodes.append(node)
        return forest, unmatched_nodes

    def get_unmarked_edges():
        unmarked_edges = []
        for node in graph.nodes:
            for edge in graph.get_edges(node):
                if edge not in matching.edges and edge[::-1] not in matching.edges:
                    unmarked_edges.append(edge)
        return unmarked_edges

    def process_unmatched_node(vertex, vertex_tree_index, unmarked_edges):
        vertex_edges = graph.get_edges(vertex)
        for edge in vertex_edges:
            neighbor = edge[1] if vertex == edge[0] else edge[0]
            if edge in unmarked_edges or edge[::-1] in unmarked_edges:
                neighbor_in_forest = forest.is_in_forest(neighbor)
                if not neighbor_in_forest:
                    handle_new_neighbor(vertex_tree_index, edge, neighbor)
                else:
                    neighbor_tree_index = forest.get_tree_by_node(neighbor)
                    if (
                        shortest_distance(
                            forest.tree_graph(neighbor_tree_index),
                            neighbor,
                            forest.get_root(neighbor),
                        )
                        % 2 == 0
                    ):
                        if neighbor_tree_index != vertex_tree_index:
                            return find_path_between_trees(vertex_tree_index, neighbor_tree_index, vertex, neighbor)
                        else:
                            # if both the current vertex and its neighbor are in the same BFS tree 
                            # and the distance from the root to the neighbor is even, the distance 
                            # from the root to the current vertex must also be even
                            return handle_blossom(vertex, neighbor, vertex_tree_index)
        return None

    def handle_new_neighbor(vertex_tree_index, edge, neighbor):
        forest.tree(vertex_tree_index).add_edge(edge[0], edge[1])
        neighbor_matching = matching.get_edges(neighbor)
        forest.tree(vertex_tree_index).add_edge(neighbor_matching[0], neighbor_matching[1])
        neighbor_of_neighbor = neighbor_matching[0] if neighbor_matching[0] != neighbor else neighbor_matching[1]
        unmatched_nodes.append(neighbor_of_neighbor)
        visualizer.update_node(neighbor, "yellow")

    def find_path_between_trees(vertex_tree_index, neighbor_tree_index, vertex, neighbor):
        path_v = shortest_path(forest.tree_graph(vertex_tree_index), forest.get_root(vertex), vertex)
        path_n = shortest_path(forest.tree_graph(neighbor_tree_index), neighbor, forest.get_root(neighbor))
        return path_v + path_n

    def handle_blossom(vertex, neighbor, vertex_tree_index):
        blossom_cycle = shortest_path(forest.tree_graph(vertex_tree_index), vertex, neighbor)
        blossom_cycle.append(vertex)
        temp_contracted_graph, temp_contracted_matching = contract_blossom(graph, matching, blossom_cycle, neighbor)
        blossoms.append(neighbor)
        aug_path = find_augmenting_path(temp_contracted_graph, temp_contracted_matching, visualizer, blossoms)
        blossoms.pop()
        if neighbor in aug_path:
            return expand_blossom(aug_path, blossom_cycle, neighbor)
        return aug_path

    def contract_blossom(graph, matching, blossom_cycle, neighbor):
        temp_contracted_graph = copy.deepcopy(graph)
        temp_contracted_matching = copy.deepcopy(matching)
        for index in range(len(blossom_cycle) - 1):
            if blossom_cycle[index] != neighbor:
                temp_contracted_graph = contract_nodes(temp_contracted_graph, blossom_cycle[index], neighbor)
                if blossom_cycle[index] in temp_contracted_matching.nodes:
                    remove_edge = matching.get_edges(blossom_cycle[index])
                    remove_edge_from_matching(temp_contracted_matching, remove_edge[0], remove_edge[1])
                    if not (remove_edge[0] in blossom_cycle and remove_edge[1] in blossom_cycle):
                        vertex_outside_blossom = remove_edge[0] if remove_edge[0] != blossom_cycle[index] else remove_edge[1]
                        aux_add_edge_to_matching(temp_contracted_matching, neighbor, vertex_outside_blossom)
        return temp_contracted_graph, temp_contracted_matching

    def expand_blossom(aug_path, blossom_cycle, neighbor):
        left_path = aug_path[:aug_path.index(neighbor)]
        right_path = aug_path[aug_path.index(neighbor) + 1:]
        base_blossom, blossom_base_vertex = get_base_blossom(blossom_cycle, matching)
        return combine_paths(left_path, right_path, base_blossom, blossom_base_vertex)

    def get_base_blossom(blossom_cycle, matching):
        base_index, blossom_base_vertex = -1, None
        extended_blossom = blossom_cycle + [blossom_cycle[1]]
        count = 0
        while blossom_base_vertex is None and count < len(blossom_cycle) - 1:
            if not matching.has_edge(blossom_cycle[count], blossom_cycle[count + 1]):
                if not matching.has_edge(blossom_cycle[count + 1], extended_blossom[count + 2]):
                    blossom_base_vertex = blossom_cycle[count + 1]
                    base_index = count + 1
                else:
                    count += 2
            else:
                count += 1
        base_blossom = blossom_cycle[base_index:] + blossom_cycle[:base_index] + [blossom_base_vertex]
        return base_blossom, blossom_base_vertex

    def combine_paths(left_path, right_path, base_blossom, blossom_base_vertex):
        if not left_path or not right_path:
            return handle_single_path(left_path, right_path, base_blossom, blossom_base_vertex)
        if matching.has_edge(blossom_base_vertex, left_path[-1]):
            if graph.has_edge(blossom_base_vertex, right_path[0]):
                return left_path + [blossom_base_vertex] + right_path
            return handle_lifted_cycle(base_blossom, right_path, left_path + [blossom_base_vertex])
        if graph.has_edge(blossom_base_vertex, left_path[-1]):
            return left_path + [blossom_base_vertex] + right_path
        return handle_lifted_cycle(base_blossom, left_path, right_path)

    def handle_single_path(left_path, right_path, base_blossom, blossom_base_vertex):
        if left_path:
            return handle_left_path(left_path, base_blossom, blossom_base_vertex)
        return handle_right_path(right_path, base_blossom, blossom_base_vertex)

    def handle_left_path(left_path, base_blossom, blossom_base_vertex):
        if graph.has_edge(blossom_base_vertex, left_path[-1]):
            return left_path + [blossom_base_vertex]
        return lift_cycle(base_blossom, left_path, reversed=True)

    def handle_right_path(right_path, base_blossom, blossom_base_vertex):
        if graph.has_edge(blossom_base_vertex, right_path[-1]):
            return [blossom_base_vertex] + right_path
        return lift_cycle(base_blossom, right_path)

    def handle_lifted_cycle(base_blossom, path, other_path):
        lifted_cycle = lift_cycle(base_blossom, path)
        return other_path + lifted_cycle

    def lift_cycle(base_blossom, path, reversed=False):
        count, lifted_cycle = 1, []
        while not lifted_cycle:
            if graph.has_edge(base_blossom[count], path[-1] if reversed else path[0]):
                lifted_cycle = (list(reversed(base_blossom)) if reversed else base_blossom)[-count - 1:] if count % 2 == 0 else base_blossom[count:]
            count += 1
        return lifted_cycle

    forest, unmatched_nodes = initialize_forest_and_unmatched_nodes()
    unmarked_edges = get_unmarked_edges()

    for vertex in unmatched_nodes:
        vertex_tree_index = forest.get_tree_by_node(vertex)
        aug_path = process_unmatched_node(vertex, vertex_tree_index, unmarked_edges)
        if aug_path:
            return aug_path

    return []
