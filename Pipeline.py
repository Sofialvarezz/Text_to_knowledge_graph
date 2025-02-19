from utils import extract_nodes, output_to_graph, export_graph_to_csv
from EntityExtraction import EntityExtractor
from GraphVisualization import GraphVisualizer
from Model import Model
from utils import save_evaluation


class TextToGraphPipeline:
    """
    Manages the complete process of converting text into a graph representation,
    including entity extraction, relationship identification, graph creation, 
    processing, and visualization.
    """

    def __init__(self, progress_callback=None):
        self.extractor = EntityExtractor()
        self.model = Model()
        self.visualizer = None
        self.progress_callback = progress_callback

    def create_graph(self, text, file_name, saveEvaluation=False):
        def update_progress(message):
            if self.progress_callback:
                self.progress_callback(message)

        try:
            if (saveEvaluation):
                save_evaluation(save_date=True,file_path=f"{file_name}.txt", save_text=True, text=text)
            # Step 1: Entity extraction
            update_progress("Extrayendo entidades y conceptos del texto\n")
            entities = self.extractor.extract_entities(text)
            if not entities:
                raise ValueError("No se pudieron extraer entidades del texto.")
            print(f"Entidades extraídas: {entities}")

            # Step 2: Relationship extraction
            update_progress("Identificando relaciones entre las entidades extraídas del texto\n")
            relations_response = self.model.get_relations(context=text, entities=entities)
            if not relations_response or not relations_response.content:
                raise ValueError("No se pudieron identificar relaciones entre las entidades extraídas.")
            print(f"Relaciones identificadas:\n{relations_response.content}")

            # Step 3: Graph creation and optimization
            update_progress("Preparando visualización del grafo\n")
            final_graph = output_to_graph(relations_response.content)
            if not final_graph:
                raise ValueError("No se pudo generar el grafo a partir de las relaciones identificadas.")
            print(f"Grafo extraído:\n{final_graph}")
            
            export_graph_to_csv(final_graph, file_name)


            nodes = extract_nodes(final_graph)
            if not nodes:
                raise ValueError("No se pudieron extraer nodos del grafo generado.")
            
            print("Mejorando la visualización con método heurístico")
            self.visualizer = GraphVisualizer(nodes, final_graph)
            self.visualizer.optimize_layout()
            
            # Step 4: Graph visualizationand exporting
            self.visualizer.display_graph() 
            if(saveEvaluation):
                save_evaluation(save_entities=True, entities=entities, save_graph=True, graph= final_graph, save_statistics=True, file_path=f"{file_name}.txt")
            update_progress("Grafo generado correctamente.")

        except Exception as e:
            error_message = f"Error durante la creación del grafo: {str(e)}"
            print(error_message)
            update_progress(error_message)
            # print(f"Error durante la creación del grafo: {e}")
            # update_progress("Ocurrió un error durante la creación del grafo. Revisa los datos e intenta nuevamente.\n")
            # print("Ocurrió un error durante la creación del grafo. Revisa los datos e intenta nuevamente.\n")

            



    def visualize(self):
        """
        Displays the graph if it has already been created and processed.

        Returns:
            None
        """
        if self.visualizer:
            self.visualizer.display_graph()
        else:
            print("No hay grafo disponible para visualizar.")
