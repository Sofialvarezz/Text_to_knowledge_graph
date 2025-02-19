import networkx as nx
import matplotlib.pyplot as plt
from Graph import Graph
from Heuristic import Heuristic
import textwrap
import math

class GraphVisualizer:
    def __init__(self, nodes, connections, space_size=100):
        self.nodes = nodes
        self.connections = connections
        self.space_size = space_size
        self.graph = Graph(space_size)
        self._create_graph()
        self.heuristic = Heuristic(self.graph)

    def _create_graph(self):
        for node in self.nodes:
            self.graph.add_node(node)

        for source, target, attributes in self.connections:
            self.graph.connect_nodes(source, target, **attributes)

    def optimize_layout(self, heuristic="concentric_circles", iterations=50):
        if heuristic == "baricentro":
            self.heuristic.optimize_coordinates_heuristic(iterations)
        elif heuristic == "concentric_circles":
            self.heuristic.optimize_coordinates_concentric_circles(iterations)

    def _split_text(self, text, max_line_length):
        """
        Splits text into multiple lines without breaking words.
        """
        return "\n".join(
            textwrap.wrap(text, max_line_length, break_long_words=False)
        )

    def _calculate_node_size(self, text, max_line_length, font_size):
        """
        Calculates the required node size based on text dimensions.
        """
        wrapped_text = self._split_text(text, max_line_length)
        lines = wrapped_text.split("\n")
        num_lines = len(lines)
        max_line_width = max(len(line) for line in lines)

        # Calculate the approximate radius required
        char_width = font_size * 0.6  # Estimate: each character is 0.6 * font size
        line_height = font_size * 1.2  # Line height as 1.2 times font size

        text_width = max_line_width * char_width
        text_height = num_lines * line_height

        # Use the larger dimension (width or height) to determine the circle radius
        radius = max(text_width, text_height) / 2
        area = math.pi * radius**2

        # Scale up the area slightly to ensure text fits comfortably
        return area * 1.5, wrapped_text

    def display_graph(self, layout_seed=42, k=1.5, figsize=(16, 12)):
        nx_graph = nx.DiGraph()

        # Add nodes and edges to the networkx graph
        for node in self.nodes:
            nx_graph.add_node(node)

        for source, target, attributes in self.connections:
            label = attributes.get('label', '')
            nx_graph.add_edge(source, target, label=label)

        # Use coordinates from the internal graph
        pos = {node: (x, y) for node, (x, y) in self.graph.coordinates.items()}

        # If no positions are available, fall back to spring layout
        if not pos:
            pos = nx.spring_layout(nx_graph, seed=layout_seed, k=k)

        # Calculate dynamic node sizes and text wrapping
        node_sizes = []
        node_labels = {}
        max_line_length = 12  # Adjust max characters per line
        font_size = 6  # Reduce font size for better readability with many nodes

        for node in self.nodes:
            # Calculate node size and wrapped text
            node_area, wrapped_text = self._calculate_node_size(node, max_line_length, font_size)
            node_labels[node] = wrapped_text
            node_sizes.append(node_area)

        # Create the plot
        plt.figure(figsize=figsize)

        # Draw the nodes
        nx.draw_networkx_nodes(
            nx_graph, pos, node_size=node_sizes, node_color='#87CEEB', edgecolors='black'
        )

        # Draw the edges with arrows
        scaled_margins = [math.sqrt(size) * 0.1 for size in node_sizes]  # Margins proportional to node size
        nx.draw_networkx_edges(
            nx_graph,
            pos,
            edge_color='gray',
            arrowstyle='-|>',
            arrowsize=50,  # Aumenta el tamaño de la flecha
            min_source_margin=max(scaled_margins),  # Márgenes dinámicos para origen
            min_target_margin=max(scaled_margins) + 10   # Despega las flechas del nodo
        )

        # Draw the node labels with wrapped text
        nx.draw_networkx_labels(nx_graph, pos, labels=node_labels, font_size=font_size, font_weight='bold', font_color='black')

        # Draw the edge labels
        edge_labels = nx.get_edge_attributes(nx_graph, 'label')
        nx.draw_networkx_edge_labels(nx_graph, pos, edge_labels=edge_labels, font_size=font_size + 1, font_color='red')

        # Finalize the plot
        plt.title("Knowledge Graph", fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.show()
