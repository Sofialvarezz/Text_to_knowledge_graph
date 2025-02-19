# from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from langchain_ollama import ChatOllama
from utils import graph_to_string


class Model:
    def __init__(self):
        self.chat = ChatOllama(model="llama2:7b", seed=100)
        #self.chat = ChatOllama(model="llama3.2:1b", seed=100)

    def relations_prompt_creator(self, context, entities):
        
        prompt= f""" Es muy importante que tu respuesta este completamente en idioma español!
               Dado el texto:

               {context}

               Y la lista de entidades extraídas:

               {', '.join(entities)}

               Tu tarea es identificar las conexiones entre pares de entidades de la lista y devolverlas como una lista de conexiones 
               Es muy importante que las conexiones tengan especificamente la estructura que te defino al final del prompt y cda conexion este completa, es decir, con 1.nodo origen, 2.relacion, 3.nodo destino.
               
               Sigue estas instrucciones con precisión:   
               ES MUY IMPORTANTE QUE TODAS LAS ENTIDADES DE LA LISTA APAREZCAN EN AL MENOS UNA CONEXION DE LAS QUE IDENTIFIQUES, NO PUEDE FALTAR NINGUNA, SINO ESTARÁ INCORRECTO.
               Es muy importante que no añadas informacion adicional a la del texto dado, las relaciones deben ser unicamente extraídas del texto.
               Es muy importante que respetes la lista de entidades y estas explicitamente sean los nodos del grafo sin cambios ni que dos entidades esten en un mismo nodo
               es imprescindible que la respuesta, cada conexion (trilpeta de dos nodos y relacion) esten una a continuacion de la otra, en el formato imprescindible que te especifico a continuación
               
               Todas las entidades de la lista deben aparecer como nodo en alguna conexion
                  - Analiza todas las combinaciones posibles de entidades para determinar si existe una relación entre ellas en el texto proporcionado y elaborar la conexion con la estructura necesaria.
                  - Si existe una relación, inclúyela. Si no existe, omítela. 
                  - No dejes ninguna entidad de la lista sin aparecer en ninguna conexion, una entidad se puede relacionar con más de una entidad.

               
               que serán los nodos:
                  - Los nodos deben ser exclusivamente las entidades de la lista proporcionada, todas las entidades deben aparecer representadas como nodos independientes.
                  - Cada nodo debe corresponder exactamente al nombre de las entidades listadas, sin modificaciones ni interpretaciones adicionales.
                  - El nodo origen debe ser el que "ejecuta la acción", es importante el orden de los nodos porque de esto depende el sentido de la relación

               que será la relación:
                  - Las relaciones deben ser **verbos o frases verbales** que describan cómo las entidades interactúan, están conectadas o se influyen entre sí, no deben ser oraciones largas, sustantivos ni conceptos abstractos. 
                  - Las relaciones deben unir dos entidades unicamente, son la conexión presente en el texto dado entre ambas entidades
                  - En la relación no debe aparecer el nombre de los nodos que conecta, solo la conexion entre ambos
                  
               

               
   
               
                  ES MUY IMPORTANTE, LO MAS IMPORTANTE DE TU TAREA, ES QUE LAS CONEXIONES DE TUS RESPUESTAS TENGAN ESTA ESTRUCTURA, DE LO CONTRARIO NO SIRVE PARA NADA:
               Cada conexion contiene estos tres elementos es sumamente importante, de eso depende que cumplas con tu tarea, que cada conexion este escrita exactamente con exta estructura:
                  1. Nodo origen: [Entidad A]
                  2. Relación: [Acción o vínculo de la Entidad A sobre la Entidad B (no incluye el nombre de las entidades en la relación)]
                  3. Nodo destino: [Entidad B]

                  1. Nodo origen: [Entidad A]
                  2. Relación: [Acción o vínculo de la Entidad A sobre la Entidad C (no incluye el nombre de las entidades en la relación)]
                  3. Nodo destino: [Entidad C]

                  ...y asi sucesivamente para todas las conexiones idenificadas entre todas las entidades. es IMPRESCINDIBLE que esten con esta estructura exacta ya que sino no podré procesarlo

               Procesa internamente en inglés si es necesario, pero devuelve la respuesta final en español.

                """
        
        

        return prompt
           
    



    def get_relations(self, context, entities):
        prompt = self.relations_prompt_creator( context, entities)
        response = self.chat.invoke(prompt)
        return response



