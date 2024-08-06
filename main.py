from graphHelpers import Graph, Matching
from blossomAlgo import compute_maximum_matching, GraphVisualizer

def test_blossom_algorithm():
    # Create a graph instance
    graph = Graph()

    # Add nodes to the graph
    graph.nodes = [0, 1, 2, 3, 4, 5]

    # Add edges to the graph (forming a specific structure)
    graph.edges = [
        [0, 1],
        [1, 2],
        [2, 3],
        [3, 4],
        [4, 5],
        [0, 3],
        [2, 5]
    ]

    # Create a matching instance
    matching = Matching()

    # Create a GraphVisualizer instance
    visualizer = GraphVisualizer(600, 600)

    # Draw nodes and edges
    positions = {
        0: (100, 100), 
        1: (200, 100), 
        2: (300, 100), 
        3: (100, 200), 
        4: (200, 200),
        5: (300, 200)
    }
    for node, (x, y) in positions.items():
        visualizer.draw_node(node, x, y)
    for edge in graph.edges:
        visualizer.draw_edge(edge[0], edge[1])

    # Compute the maximum matching
    max_matching = compute_maximum_matching(graph, matching, visualizer)

    # Print the results
    print("Maximum Matching:")
    for edge in max_matching.edges:
        print(edge)

    visualizer.wait_for_click()
    visualizer.close()

# Run the test
if __name__ == "__main__":
    test_blossom_algorithm()
