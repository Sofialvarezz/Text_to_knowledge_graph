import re
import csv
from datetime import datetime
import psutil
import GPUtil

def save_evaluation(save_text=False, text="", save_date= False, save_entities=False, entities=None, save_graph=False, graph=None, save_statistics=False, file_path="statistics.txt"):
    # Crear un archivo en modo de adición
    with open(file_path, "a", encoding='utf-8') as file:
        # Guardar estadísticas del sistema si save_statistics es True
        if save_text:

            file.write(f"Text:\n {text}\n")
            file.write(f"{'-' * 30}\n")

        if save_date:
            initial_time= datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file.write(f"Initial time: {initial_time}\n")
            file.write(f"{'-' * 30}\n")
            
            
        if save_statistics:
            # Obtener el uso de la CPU
            cpu_usage = psutil.cpu_percent(interval=1)

            # Obtener el uso de la memoria RAM
            memory = psutil.virtual_memory()
            ram_usage = memory.percent

            # Obtener información de los discos duros
            disk = psutil.disk_usage('/')
            hdd_usage = disk.percent

            # Obtener información de la GPU (si está disponible)
            gpus = GPUtil.getGPUs()
            gpu_usage = "No GPU detected" if not gpus else f"{gpus[0].load * 100:.2f}%"

            # Crear una marca de tiempo
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Crear el texto con la información del sistema
            stats = (
                f"Timestamp: {timestamp}\n"
                f"CPU Usage: {cpu_usage}%\n"
                f"RAM Usage: {ram_usage}%\n"
                f"HDD Usage: {hdd_usage}%\n"
                f"GPU Usage: {gpu_usage}\n"
                f"{'-' * 30}\n"
            )
            file.write(stats)

        # Guardar entidades si save_entities es True
        if save_entities and entities is not None:
            file.write("Entidades:\n")
            for entity in entities:
                file.write(f"- {entity}\n")
            file.write(f"{'-' * 30}\n")

        # Guardar grafo si save_graph es True
        if save_graph and graph is not None:
            file.write("Grafo:\n")
            for node1, node2, attributes in graph:
                relation = attributes.get('label', 'unknown')
                file.write(f"({node1}, '{relation}', {node2})\n")
            file.write(f"{'-' * 30}\n")




def export_graph_to_csv(graph, file_name= ""):

    if not file_name:
        current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M")
        file_name = f"graph_{current_datetime}.csv"
    else:
        file_name = f"{file_name}.csv"

    # Create and write the CSV file
    with open(file_name, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # Write headers
        writer.writerow(['Nodo Origen', 'Nodo Destino', 'Relación'])

        # Write rows from the graph
        for source_node, destination_node, attributes in graph:
            writer.writerow([source_node, destination_node, attributes['label']])

def truncate_text(text, max_tokens):
    """
    Truncates the text to fit within the token limits for the model.

    Args:
        text (str): The input text to truncate.
        max_tokens (int): The maximum number of tokens allowed.

    Returns:
        str: Truncated text.
    """
    max_chars = max_tokens * 4
    if len(text) > max_chars:
        truncated_text = text[:max_chars]
        last_space = truncated_text.rfind(" ")
        return truncated_text[:last_space] if last_space != -1 else truncated_text
    return text


def remove_duplicate_connections(graph):
    unique_connections = set()  # To store unique connections
    processed_graph = []  # Final graph without duplicates
    
    for node1, node2, data in graph:
        # Create a sorted tuple to ensure node order doesn't matter
        connection = tuple(sorted([node1, node2]))
        
        if connection not in unique_connections:
            unique_connections.add(connection)  # Mark the connection as unique
            processed_graph.append((node1, node2, data))  # Add the connection to the final graph
    
    return processed_graph

def extract_nodes(graph):
    """
    Extracts a list of unique nodes from a graph.

    Parameters:
        graph (list): List of tuples representing the graph (source, target, properties).

    Returns:
        list: List of unique nodes in the graph.
    """
    nodes = []

    for source, target, _ in graph:
        if source not in nodes:
            nodes.append(source)
        if target not in nodes:
            nodes.append(target)

    return nodes




def output_to_graph(output):
    """
    Converts text output into a structured graph.

    Parameters:
        output (str): Text output containing node and relationship information.

    Returns:
        list: List of tuples representing the graph (node_origin, node_destination, {"label": relation}).
    """
    lines = output.split('\n')
    connections = []

    current_source = None
    current_relation = None
    current_target = None

    for line in lines:
        line = line.strip()

        if re.match(r"^(Nodo.*origen|Node.*origin|Origin.*Node|Entidad.*origen|^\*\s*Nodo.*origen):", line, re.IGNORECASE):
            current_source = re.sub(r"^(Nodo.*origen|Node.*origin|Origin.*Node|Entidad.*origen|^\*\s*Nodo.*origen):\s*", "", line, flags=re.IGNORECASE).strip()
        
        elif re.match(r"^(Relaci[oó]n|Relation|^\*\s*Relaci[oó]n):", line, re.IGNORECASE):
            current_relation = re.sub(r"^(Relaci[oó]n|Relation|^\*\s*Relaci[oó]n):\s*", "", line, flags=re.IGNORECASE).strip()
        
        elif re.match(r"^(Nodo.*destino|Node.*destination|Destination.*Node|Entidad.*destino|^\*\s*Nodo.*destino):", line, re.IGNORECASE):
            current_target = re.sub(r"^(Nodo.*destino|Node.*destination|Destination.*Node|Entidad.*destino|^\*\s*Nodo.*destino):\s*", "", line, flags=re.IGNORECASE).strip()

            if current_source and current_relation and current_target:
                connections.append((current_source, current_target, {"label": current_relation}))
                current_source, current_relation, current_target = None, None, None
        
        elif re.match(r"^\d+\.\s*(Nodo.*origen|Node.*origin|Origin.*Node):", line, re.IGNORECASE):
            current_source = re.sub(r"^\d+\.\s*(Nodo.*origen|Node.*origin|Origin.*Node):\s*", "", line, flags=re.IGNORECASE).strip()
        
        elif re.match(r"^\d+\.\s*(Relaci[oó]n|Relation):", line, re.IGNORECASE):
            current_relation = re.sub(r"^\d+\.\s*(Relaci[oó]n|Relation):\s*", "", line, flags=re.IGNORECASE).strip()
        
        elif re.match(r"^\d+\.\s*(Nodo.*destino|Node.*destination|Destination.*Node):", line, re.IGNORECASE):
            current_target = re.sub(r"^\d+\.\s*(Nodo.*destino|Node.*destination|Destination.*Node):\s*", "", line, flags=re.IGNORECASE).strip()

            if current_source and current_relation and current_target:
                connections.append((current_source, current_target, {"label": current_relation}))
                current_source, current_relation, current_target = None, None, None
    
        if re.search(r"nodo.*origen|node.*origin|origin.*node", line, re.IGNORECASE) and \
           re.search(r"relaci[oó]n|relation", line, re.IGNORECASE) and \
           re.search(r"nodo.*destino|node.*destination|destination.*node", line, re.IGNORECASE):
            
            # Extract node_origin
            origin_match = re.search(r"(nodo.*origen|node.*origin|origin.*node):\s*([^(\.,;)]+)", line, re.IGNORECASE)
            # Extract relation (stopping at the first punctuation mark or parenthesis)
            relation_match = re.search(r"(relaci[oó]n|relation):\s*([^(\.,;)]+)", line, re.IGNORECASE)
            # Extract node_destination
            destination_match = re.search(r"(nodo.*destino|node.*destination|destination.*node):\s*([^(\.,;)]+)", line, re.IGNORECASE)

            if origin_match and relation_match and destination_match:
                node_origin = origin_match.group(2).strip()
                relation = relation_match.group(2).strip()
                node_destination = destination_match.group(2).strip()
                # Add the connection to the graph
                connections.append((node_origin, node_destination, {'label': relation}))




    unique_connections = list({(src, dst, tuple(rel.items())) for src, dst, rel in connections})
    graph = [(src, dst, {"label": rel[0][1]}) for src, dst, rel in unique_connections]
    graph_whithout_duplicate_connections= remove_duplicate_connections(graph)
    clean_graph= remove_parentheses(graph_whithout_duplicate_connections)
    return clean_graph

def remove_parentheses(graph):
    cleaned_graph = []
    
    for node1, node2, data in graph:
        clean_node1 = re.sub(r'\s*\(.*?\)', '', node1)
        clean_node2 = re.sub(r'\s*\(.*?\)', '', node2)
        
        clean_label = re.sub(r'\s*\(.*?\)', '', data['label'])
        
        cleaned_graph.append((clean_node1, clean_node2, {'label': clean_label}))
    
    return cleaned_graph

    
def graph_to_string(connections):
        """
        Converts a graph represented as a list of tuples into a formatted string.

        Parameters:
            connections (list): List of tuples in the format (node_origin, node_destination, {"label": relation})

        Returns:
            str: Formatted string representation of the graph.
        """
        formatted_connections = []
        for connection in connections:
            node_origin = connection[0]
            node_destination = connection[1]
            relation = connection[2]["label"]
            formatted_connection = (
                f"Nodo origen: {node_origin}\n"
                f"Relación: {relation}\n"
                f"Nodo destino: {node_destination}\n"
                f"Dirección: {node_origin} -> {node_destination}\n"
            )
            formatted_connections.append(formatted_connection)

        return "\n".join(formatted_connections)










