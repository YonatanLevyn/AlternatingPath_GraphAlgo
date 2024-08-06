import unittest
from graphHelpers import Graph, Matching
from blossomAlgo import compute_maximum_matching, GraphVisualizer

class TestBlossomAlgorithm(unittest.TestCase):
    """
    Unit test class for the Blossom algorithm.
    Contains various test cases to verify the correctness of the maximum matching implementation.
    """

    def setUp(self):
        """
        Sets up the visualizer for each test.
        """
        self.visualizer = GraphVisualizer(600, 600)

    def tearDown(self):
        """
        Closes the visualizer after each test.
        """
        self.visualizer.close()

    def draw_graph(self, graph):
        """
        Draws the graph using the visualizer.
        """
        positions = {i: (100 + 100 * (i % 3), 100 + 100 * (i // 3)) for i in graph.nodes}
        for node, (x, y) in positions.items():
            self.visualizer.draw_node(node, x, y)
        for edge in graph.edges:
            self.visualizer.draw_edge(edge[0], edge[1])

    def test_basic_matching(self):
        """
        Ensures the maximum matching is found correctly.
        """
        graph = Graph()
        graph.nodes = [0, 1, 2, 3, 4, 5]
        graph.edges = [
            [0, 1],
            [1, 2],
            [2, 3],
            [3, 0],
            [1, 3],
            [3, 4],
            [4, 5]
        ]
        self.draw_graph(graph)
        matching = Matching()
        max_matching = compute_maximum_matching(graph, matching, self.visualizer)
        expected_edges = [
            [0, 1],
            [2, 3],
            [4, 5]
        ]
        self.assertCountEqual(max_matching.edges, expected_edges)

    def test_no_edges(self):
        """
        Ensures the function handles an edge-less graph correctly and returns an empty matching.
        """
        graph = Graph()
        graph.nodes = [0, 1, 2, 3]
        graph.edges = []
        self.draw_graph(graph)
        matching = Matching()
        max_matching = compute_maximum_matching(graph, matching, self.visualizer)
        expected_edges = []
        self.assertCountEqual(max_matching.edges, expected_edges)

    def test_fully_connected(self):
        """
        Ensures the algorithm finds the maximum matching, which should be half the number of nodes.
        """
        graph = Graph()
        graph.nodes = [0, 1, 2, 3]
        graph.edges = [
            [0, 1],
            [0, 2],
            [0, 3],
            [1, 2],
            [1, 3],
            [2, 3]
        ]
        self.draw_graph(graph)
        matching = Matching()
        max_matching = compute_maximum_matching(graph, matching, self.visualizer)
        # Only two edges can be in the maximum matching due to fully connected graph properties
        self.assertEqual(len(max_matching.edges), 2)

    def test_disconnected_graph(self):
        """
        Ensures the algorithm correctly finds the maximum matching within each component.
        """
        graph = Graph()
        graph.nodes = [0, 1, 2, 3, 4, 5]
        graph.edges = [
            [0, 1],
            [2, 3],
            [4, 5]
        ]
        self.draw_graph(graph)
        matching = Matching()
        max_matching = compute_maximum_matching(graph, matching, self.visualizer)
        expected_edges = [
            [0, 1],
            [2, 3],
            [4, 5]
        ]
        self.assertCountEqual(max_matching.edges, expected_edges)

    def test_blossom_case(self):
        graph = Graph()
        graph.nodes = [0, 1, 2, 3, 4]
        graph.edges = [
            [0, 1],
            [1, 2],
            [2, 3],
            [3, 0],
            [1, 3],
            [3, 4]
        ]
        self.draw_graph(graph)
        matching = Matching()
        max_matching = compute_maximum_matching(graph, matching, self.visualizer)
        self.assertEqual(len(max_matching.edges), 2)

    def test_single_edge(self):
        """
        Ensures the algorithm finds the single matching edge.
        """
        graph = Graph()
        graph.nodes = [0, 1]
        graph.edges = [[0, 1]]
        self.draw_graph(graph)
        matching = Matching()
        max_matching = compute_maximum_matching(graph, matching, self.visualizer)
        expected_edges = [[0, 1]]
        self.assertCountEqual(max_matching.edges, expected_edges)

    def test_no_nodes(self):
        """
        Ensures the function handles an empty graph correctly and returns an empty matching.
        """
        graph = Graph()
        graph.nodes = []
        graph.edges = []
        self.draw_graph(graph)
        matching = Matching()
        max_matching = compute_maximum_matching(graph, matching, self.visualizer)
        expected_edges = []
        self.assertCountEqual(max_matching.edges, expected_edges)

if __name__ == "__main__":
    unittest.main()
