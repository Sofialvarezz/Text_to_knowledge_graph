import random
import math

class Heuristic:
    def __init__(self, graph):
        self.graph = graph 
        
    #---------------------------------------------------------------------------
    # Función objetivo
    #---------------------------------------------------------------------------
    def objective_function(self):
        return (2 * self.count_crossings() +           
                self.count_node_overlap() + 
                self.count_node_edge_overlap() + 
                self.count_small_edge() +
                self.count_small_angles() + 
                self.coefficient_of_variation_edge()) 
    
    #---------------------------------------------------------------------------
    # Métodos para calcular criterios 
    #---------------------------------------------------------------------------

    # Cantidad de cruces
    def count_crossings(self):
        edges = self.graph.get_edges()
        crossings = 0
        for i in range(len(edges)):
            for j in range(i + 1, len(edges)):
                u1, v1, _ = edges[i]  # Descomponer los atributos adicionales
                u2, v2, _ = edges[j]

                if u1 == u2 or u1 == v2 or v1 == u2 or v1 == v2:
                    continue

                if self.do_edges_cross(u1, v1, u2, v2):
                    crossings += 1
        return crossings

    def do_edges_cross(self, u1, v1, u2, v2):
        u1_coords = self.graph.coordinates[u1]
        v1_coords = self.graph.coordinates[v1]
        u2_coords = self.graph.coordinates[u2]
        v2_coords = self.graph.coordinates[v2]

        def orientation(p, q, r):
            val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
            return 0 if val == 0 else (1 if val > 0 else -1)

        o1 = orientation(u1_coords, v1_coords, u2_coords)
        o2 = orientation(u1_coords, v1_coords, v2_coords)
        o3 = orientation(u2_coords, v2_coords, u1_coords)
        o4 = orientation(u2_coords, v2_coords, v1_coords)

        if o1 != o2 and o3 != o4:
            return True

        if o1 == 0 and self.on_segment(u1_coords, u2_coords, v1_coords):
            return True
        if o2 == 0 and self.on_segment(u1_coords, v2_coords, v1_coords):
            return True
        if o3 == 0 and self.on_segment(u2_coords, u1_coords, v2_coords):
            return True
        if o4 == 0 and self.on_segment(u2_coords, v1_coords, v2_coords):
            return True

        return False

    def on_segment(self, p, q, r):
        return (min(p[0], r[0]) <= q[0] <= max(p[0], r[0]) and 
                min(p[1], r[1]) <= q[1] <= max(p[1], r[1]))

    # Cantidad de solapamientos entre nodos
    def count_node_overlap(self):
        umbral = self.graph.space_size * 0.04
        nodes = self.graph.get_nodes()
        total_closeness = 0

        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                try:
                    dist = self.distance_between_nodes(nodes[i], nodes[j])
                    if dist <= umbral:
                        total_closeness += 1
                except ValueError:
                    continue

        return total_closeness
    
    def distance_between_nodes(self, node1, node2):
        coord1 = self.graph.coordinates[node1]
        coord2 = self.graph.coordinates[node2]
        return math.sqrt((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2)
    
    # Cantidad de aristas pequeñas
    def count_small_edge(self):
        umbral = self.graph.space_size * 0.08
        total_small_edges = 0
        edges = self.graph.get_edges()

        for edge in edges:
            node1, node2, _ = edge  # Descomponer atributos adicionales
            try:
                dist = self.distance_between_nodes(node1, node2)
                if dist <= umbral:
                    total_small_edges += 1
            except ValueError:
                continue  

        return total_small_edges
    
    # Cantidad de solapamientos entre nodos y aristas
    def count_node_edge_overlap(self):
        umbral = self.graph.space_size * 0.028
        total_overlaps = 0

        for node in self.graph.get_nodes():
            node_coords = self.graph.coordinates[node]

            for edge in self.graph.get_edges():
                node1, node2, _ = edge  # Descomponer atributos adicionales
                if node1 == node or node2 == node:
                    continue

                node1_coords = self.graph.coordinates[node1]
                node2_coords = self.graph.coordinates[node2]

                distance = self.distance_point_to_segment(node_coords, node1_coords, node2_coords)

                if distance <= umbral:
                    total_overlaps += 1

        return total_overlaps

    def distance_point_to_segment(self, p, p1, p2):
        x, y = p
        x1, y1 = p1
        x2, y2 = p2
        dx, dy = x2 - x1, y2 - y1

        if dx == 0 and dy == 0:
            return math.sqrt((x - x1) ** 2 + (y - y1) ** 2)

        t = ((x - x1) * dx + (y - y1) * dy) / (dx * dx + dy * dy)
        if t < 0:
            return math.sqrt((x - x1) ** 2 + (y - y1) ** 2)
        elif t > 1:
            return math.sqrt((x - x2) ** 2 + (y - y2) ** 2)
        else:
            proj_x, proj_y = x1 + t * dx, y1 + t * dy
            return math.sqrt((x - proj_x) ** 2 + (y - proj_y) ** 2)

    # Cantidad de ángulos pequeños
    def count_small_angles(self):
        count = 0
        nodes = self.graph.get_nodes()
        
        for node in nodes:
            neighbors = [n['target'] for n in self.graph.adjacency_list[node]]  # Extraer `target`
            num_neighbors = len(neighbors)
            
            for i in range(num_neighbors):
                for j in range(i + 1, num_neighbors):
                    node1, node2 = neighbors[i], neighbors[j]
                    v0, v1, v2 = (self.graph.coordinates[node],
                                  self.graph.coordinates[node1],
                                  self.graph.coordinates[node2])
                    
                    vec1 = (v1[0] - v0[0], v1[1] - v0[1])
                    vec2 = (v2[0] - v0[0], v2[1] - v0[1])
                    
                    dot_product = vec1[0] * vec2[0] + vec1[1] * vec2[1]
                    magnitude1 = math.sqrt(vec1[0]**2 + vec1[1]**2)
                    magnitude2 = math.sqrt(vec2[0]**2 + vec2[1]**2)
                    
                    if magnitude1 > 0 and magnitude2 > 0:
                        cos_angle = dot_product / (magnitude1 * magnitude2)
                        cos_angle = max(min(cos_angle, 1.0), -1.0)
                        angle_deg = math.degrees(math.acos(cos_angle))
                        
                        if angle_deg < 15:
                            count += 1
                            
        return count
    
    # Coeficiente de variación de la longitud de las aristas
    def coefficient_of_variation_edge(self):
        lengths = self.edge_lengths()
        if len(lengths) < 2:
            return float('nan') 
        
        mean_length = sum(lengths) / len(lengths)
        variance = sum((x - mean_length) ** 2 for x in lengths) / len(lengths)
        std_dev = math.sqrt(variance)
        
        return std_dev / mean_length
    
    def edge_lengths(self):
        lengths = []
        for node, neighbors in self.graph.adjacency_list.items():
            for neighbor in neighbors:
                target = neighbor["target"]
                length = self.distance_between_nodes(node, target)
                lengths.append(length)
        return lengths


    
    #-------------------------------------------------------------------------------------------------------------------------------------------
    # Metodos para generar coordenadas 
    #-------------------------------------------------------------------------------------------------------------------------------------------
    
    # Elige la mejor luego de iteraciones asignando coordenadas de manera aleatoria 
    def optimize_coordinates_random(self, iterations=100):
        best = float('inf')
        best_coordinates = self.graph.coordinates.copy()
        
        for _ in range(iterations):
            self.randomize_coordinates()
            value = self.objective_function()
            
            if value < best:
                best = value
                best_coordinates = self.graph.coordinates.copy()
        
        self.graph.coordinates = best_coordinates
        return best, best_coordinates
    
    def randomize_coordinates(self):
        for node in self.graph.adjacency_list:
            self.graph.coordinates[node] = (random.randint(0, self.graph.space_size), random.randint(0, self.graph.space_size))
            
    # Elige la peor luego de iteraciones asignando coordenadas de manera aleatoria
    def deoptimize_coordinates_random(self, iterations=100):
       worst = float('-inf')
       worst_coordinates = self.graph.coordinates.copy()
        
       for _ in range(iterations):
          self.randomize_coordinates()
          value = self.objective_function()
            
          if value > worst:
            worst = value
            worst_coordinates = self.graph.coordinates.copy()
        
       self.graph.coordinates = worst_coordinates
       return worst, worst_coordinates
  
        
    # Coloca los nodos en círculos concéntricos y luego realiza intercambios.      
    def optimize_coordinates_concentric_circles(self, iterations=100):
        nodes = self.graph.get_nodes()
        num_nodes = len(nodes)
        radius_outer = self.graph.space_size / 2.0

        if num_nodes <= 5:
            # Si hay 5 nodos o menos, distribuir en un solo círculo
            for i, node in enumerate(nodes):
                angle = (2 * math.pi * i) / num_nodes
                x = radius_outer * math.cos(angle) + radius_outer
                y = radius_outer * math.sin(angle) + radius_outer
                self.graph.coordinates[node] = (x, y)
        else:
            # Distribuir en dos círculos concéntricos
            radius_inner = radius_outer / 2.0

            for i, node in enumerate(nodes):
                if i < num_nodes // 2:
                    # Nodos en el círculo interior
                    angle = (2 * math.pi * i) / (num_nodes // 2)
                    x = radius_inner * math.cos(angle) + radius_outer
                    y = radius_inner * math.sin(angle) + radius_outer
                else:
                    # Nodos en el círculo exterior
                    angle = (2 * math.pi * (i - num_nodes // 2)) / (num_nodes - num_nodes // 2)
                    x = radius_outer * math.cos(angle) + radius_outer
                    y = radius_outer * math.sin(angle) + radius_outer
                self.graph.coordinates[node] = (x, y)
                
        for _ in range(iterations):
            # Seleccionar dos nodos aleatorios para intercambiar
            node1, node2 = random.sample(nodes, 2)
            self.swap_nodes(node1, node2)

    def swap_nodes(self, node1, node2):
        current_objective = self.objective_function()

        # Realizar el intercambio de coordenadas
        temp_coordinates = self.graph.coordinates[node1]
        self.graph.coordinates[node1] = self.graph.coordinates[node2]
        self.graph.coordinates[node2] = temp_coordinates

        new_objective = self.objective_function()

        # Si la nueva función objetivo es mejor, aceptar el intercambio
        if new_objective < current_objective:
            return True
        else:
            # Revertir el intercambio
            temp_coordinates = self.graph.coordinates[node1]
            self.graph.coordinates[node1] = self.graph.coordinates[node2]
            self.graph.coordinates[node2] = temp_coordinates
            return False

 
    # Metodo heurístico (Baricentro)
    def optimize_coordinates_heuristic(self, iterations=50):
        best = float('inf')
        best_coordinates = self.graph.coordinates.copy()
        i=1
        for _ in range(iterations):
            
            print(f"Iteración de la heurística: {i}/{iterations}")
            i=i+1
            self.heuristic_coordinates()
            value = self.reduce_crossings()

            if value < best:
                best = value
                best_coordinates = self.graph.coordinates.copy()

        self.graph.coordinates = best_coordinates
        return best, best_coordinates

    def heuristic_coordinates(self):
        centroid = self.calculate_centroid()
        for node in self.graph.adjacency_list:
            self.graph.coordinates[node] = (random.randint(0, self.graph.space_size) + centroid[0] / 2, random.randint(0, self.graph.space_size) + centroid[1] / 2)

    def calculate_centroid(self):
        x_coords = [coord[0] for coord in self.graph.coordinates.values()]
        y_coords = [coord[1] for coord in self.graph.coordinates.values()]
        centroid = (sum(x_coords) / len(x_coords), sum(y_coords) / len(y_coords))
        return centroid

    def reduce_crossings(self):
        nodes = list(self.graph.adjacency_list.keys())
        best_value = self.objective_function()
        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                self.graph.coordinates[nodes[i]], self.graph.coordinates[nodes[j]] = self.graph.coordinates[nodes[j]], self.graph.coordinates[nodes[i]]
                new_value = self.objective_function()
                if new_value < best_value:
                    best_value = new_value
                else:
                    self.graph.coordinates[nodes[i]], self.graph.coordinates[nodes[j]] = self.graph.coordinates[nodes[j]], self.graph.coordinates[nodes[i]]
        return best_value

