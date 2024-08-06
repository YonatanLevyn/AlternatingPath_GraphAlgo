from graphics import GraphWin, Point, Line, Circle, Text

class GraphVisualizer:
    def __init__(self, width, height):
        self.win = GraphWin("Blossom Algorithm Visualization", width, height)
        self.node_objects = {}
        self.edge_objects = {}

    def draw_node(self, node_id, x, y):
        node = Circle(Point(x, y), 20)
        node.setFill("white")
        node.draw(self.win)
        label = Text(Point(x, y), str(node_id))
        label.draw(self.win)
        self.node_objects[node_id] = node

    def draw_edge(self, node1_id, node2_id):
        node1 = self.node_objects[node1_id].getCenter()
        node2 = self.node_objects[node2_id].getCenter()
        edge = Line(node1, node2)
        edge.draw(self.win)
        self.edge_objects[(node1_id, node2_id)] = edge

    def update_edge(self, node1_id, node2_id, color):
        edge = self.edge_objects[(node1_id, node2_id)]
        edge.setFill(color)

    def update_node(self, node_id, color):
        node = self.node_objects[node_id]
        node.setFill(color)

    def wait_for_click(self):
        self.win.getMouse()

    def close(self):
        self.win.close()
