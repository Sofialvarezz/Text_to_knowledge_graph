import random

class Graph:
    def __init__(self, space_size=10):
        self.adjacency_list = {}  # Diccionario para almacenar vecinos y atributos de aristas
        self.coordinates = {}  # Coordenadas de los nodos
        self.space_size = space_size

    def add_node(self, node, coordinates=None):
        if node not in self.adjacency_list:
            self.adjacency_list[node] = []
            if coordinates is None:
                self.coordinates[node] = (
                    random.randint(0, self.space_size),
                    random.randint(0, self.space_size),
                )
            else:
                self.coordinates[node] = coordinates
        else:
            raise ValueError("Ya existe el nodo.")

    def connect_nodes(self, node1, node2, label=None):
        """
        Conecta dos nodos con un label opcional.
        """
        if node1 in self.adjacency_list and node2 in self.adjacency_list:
            # Verifica si la conexión ya existe
            if not any(edge["target"] == node2 for edge in self.adjacency_list[node1]):
                self.adjacency_list[node1].append({"target": node2, "label": label})
            if not any(edge["target"] == node1 for edge in self.adjacency_list[node2]):
                self.adjacency_list[node2].append({"target": node1, "label": label})
        else:
            raise ValueError(f"Algún nodo no existe. {node1}, o {node2}")

    def get_nodes(self):
        return list(self.adjacency_list.keys())

    def get_edges(self):
        """
        Retorna todas las aristas con sus atributos.
        """
        edges = []
        seen = set()  # Para evitar duplicados
        for node, neighbors in self.adjacency_list.items():
            for edge in neighbors:
                target = edge["target"]
                if (node, target) not in seen and (target, node) not in seen:
                    edges.append((node, target, {"label": edge["label"]}))
                    seen.add((node, target))
        return edges
