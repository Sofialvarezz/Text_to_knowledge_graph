import spacy
import re

class EntityExtractor:
    def __init__(self):
        """
        Initialize the EntityExtractor with the spaCy Spanish model and stop phrases.
        """
        self.nlp = spacy.load("es_core_news_sm")
        self.stop_phrases = {
            "con respecto", "preciso instante", "en vista", "con vista", "con visión", "a propósito", "de paso",
            "en efecto", "por otra parte", "sin embargo", "en otras palabras", "por su parte", "por ende",
            "al día siguiente", "por la tarde", "de madrugada", "en ese momento", "no obstante", "a pesar de",
            "por lo tanto", "de hecho", "es decir", "en consecuencia", "a ciencia cierta", "de vez en cuando", 
            "a duras penas", "ni más ni menos", "por si acaso", "en primer lugar", "en segundo lugar", "en tercer lugar", 
            "en cuarto lugar", "en último lugar", "por un lado", "por el otro", "por otro lado", "por último",
            "a continuación", "por el contrario", "cosa", "cosas", "en cambio", "continuación", 
            "de todas formas", "de todas maneras", "de todos modos", "de igual forma", "de igual manera", 
            "de igual modo", "con otras palabras", "de otra forma", "de otra manera", "ejemplo", "conclusión", 
            "a fin de cuentas", "en resumen", "resumidas cuentas", "en pocas palabras", "de forma", "un día", 
            "había una vez", "otro día", "aquel día", "ese día", "día siguiente", "día anterior", "a través", "durante", 
            "debido a", "hacia" 
        }



    def is_entity_start(self, token, next_token=None):
        """
        Checks if the token starts a new entity.

        Parameters:
            token (Token): The current token to evaluate.
            next_token (Token, optional): The next token in the sequence for context.

        Returns:
            bool: True if the token starts a new entity, False otherwise.
        """
        if token.pos_ in {"NOUN", "PROPN"}:
            return True
        if token.pos_ in {"ADP", "CCONJ", "VERB", "DET"}:
            return False
        if (token.pos_ == "ADJ" or "NUM") and next_token is not None:
            return next_token.pos_ in {"NOUN", "PROPN"}

        return False

    def is_valid_entity(self, entity_tokens):
        """
        Checks if the current set of tokens form a valid entity.

        Parameters:
            entity_tokens (list): List of tokens forming a potential entity.

        Returns:
            bool: True if the entity contains at least one noun or proper noun, False otherwise.
        """
        contains_noun = any(t.pos_ in {"NOUN", "PROPN"} for t in entity_tokens)
        return contains_noun

    def extract_entities(self, text):
        """
        Extracts valid entities from the input text based on specified linguistic patterns.

        Parameters:
            text (str): The input text to process.

        Returns:
            list: List of extracted entities.
        """
        text = text.lower()
        sentences = re.split(r'[.?!,;]', text)  # Fragmenta el texto en oraciones usando signos de puntuación
        entities = []

        for sentence in sentences:  # Procesa cada oración fragmentada
            doc = self.nlp(sentence.strip())
            current_entity = []

            for i, token in enumerate(doc):
                print(f"'{token}', [{token.pos_}]")
                next_token = doc[i + 1] if i + 1 < len(doc) else None

                if self.is_entity_start(token, next_token):
                    for j in range(i, len(doc)):
                        next_word = doc[j]
                        if next_word.pos_ == "PUNCT":  
                            continue
                        if next_word.pos_ in {"NOUN", "PROPN", "ADJ", "DET"} or (
                            next_word.pos_ == "ADP"
                            and j + 1 < len(doc)
                            and doc[j + 1].pos_ in {"NOUN", "PROPN", "DET"}
                        ):
                            current_entity.append(next_word)
                        else:
                            break

                    if self.is_valid_entity(current_entity):
                        candidate_entity = " ".join(
                            [t.text.strip() for t in current_entity if t.pos_ != "PUNCT" and t.text.strip()]
                        )
                        if all(candidate_entity not in stop_phrase for stop_phrase in self.stop_phrases):
                            entities.append(candidate_entity)

                    current_entity = []

        unique_entities = []
        for entity in entities:
            if not any(entity in other and entity != other for other in entities):
                unique_entities.append(entity)

        return unique_entities
