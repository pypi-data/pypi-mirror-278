import uuid
import chromadb
from datadashr.config import *


class VectorManager:
    def __init__(self, vector_dir, verbose=False, connector_type='pandas'):
        self.vector_dir = vector_dir
        self.verbose = verbose
        self.connector_type = connector_type
        self.client = chromadb.PersistentClient(self.vector_dir)
        self.collection = self.client.get_or_create_collection('datadashr')

    def _clean_prompt(self, prompt):
        """
        Clean the prompt
        :param prompt:
        :return:
        """
        return prompt.lower().strip()

    def _clean_columns(self, columns):
        """
        Clean the columns
        :param columns:
        :return:
        """
        if columns:
            columns = ','.join(columns)
            return columns.lower().strip()
        return None

    def _clean_code(self, code):
        """
        Clean the code
        :param code:
        :return:
        """
        return code.lower().strip()

    def _clean_connector_type(self, connector_type):
        """
        Clean the connector type
        :param connector_type:
        :return:
        """
        return connector_type.lower().strip()

    def _create_document(self, prompt, columns, code):
        """
        Create a document
        :param prompt:
        :param columns:
        :param code:
        :return:
        """
        return f"""
        QUERY: {self._clean_prompt(prompt)}
        RESPONSE: {self._clean_code(code)}
        """

    def verify_if_document_exists(self, prompt, columns):
        """
        Verify if document exists
        :param prompt:
        :param columns:
        :return:
        """
        try:
            cleaned_prompt = self._clean_prompt(prompt)
            cleaned_columns = self._clean_columns(columns)
            query_results = self.collection.query(
                query_texts=[cleaned_prompt],
                n_results=10,  # Aumenta il numero di risultati per un controllo più accurato
                include=["metadatas"]
            )

            if query_results and 'metadatas' in query_results:
                for metadata_list in query_results['metadatas']:
                    for metadata in metadata_list:
                        if (metadata.get('prompt') == cleaned_prompt and
                                metadata.get('columns') == cleaned_columns):
                            return True
            return False
        except Exception as e:
            if self.verbose:
                logger.error(f"Error verifying if document exists: {e}")
            return False

    def set_vector(self, prompt, columns, data):
        """
        Set a vector
        :param prompt:
        :param columns:
        :param data:
        :return:
        """
        try:
            if self.verify_if_document_exists(prompt, columns):
                if self.verbose:
                    logger.info(f"Document already exists for prompt: {prompt}")
                return

            self.collection.add(
                documents=[self._create_document(prompt, columns, data['code'])],
                metadatas=[{
                    'prompt': self._clean_prompt(prompt),
                    'columns': self._clean_columns(columns),
                    'connector_type': self._clean_connector_type(self.connector_type),
                    'code': self._clean_code(data['code'])
                }],
                ids=[str(uuid.uuid4())],
            )
        except Exception as e:
            if self.verbose:
                logger.error(f"Error setting vector: {e}")

    def get_by_vector(self, prompt):
        """
        Get by vector
        :param prompt:
        :return:
        """
        try:
            results = self.collection.query(
                query_texts=[self._clean_prompt(prompt)],
                n_results=3,  # Cambiato a 3 per ottenere più esempi
                where={"connector_type": self._clean_connector_type(self.connector_type)},
                include=["metadatas", "distances"]
            )

            if results and 'metadatas' in results and results['metadatas']:
                formatted_results = ""
                example_counter = 1
                seen_results = set()
                for metadata_list in results['metadatas']:
                    for res in metadata_list:
                        prompt_example = res.get('prompt')
                        code_example = res.get('code')
                        combined_example = (prompt_example, code_example)
                        if combined_example not in seen_results:
                            formatted_results += f"**Example {example_counter}:**\n"
                            formatted_results += f"QUERY: {prompt_example}\n"
                            formatted_results += "RESPONSE:\n"
                            formatted_results += "```python\n"
                            formatted_results += f"{code_example}\n"
                            formatted_results += "```\n\n"
                            seen_results.add(combined_example)
                            example_counter += 1
                return formatted_results
            return None
        except Exception as e:
            if self.verbose:
                logger.error(f"Error getting by vector: {e}")
            return None

    def get_all_vectors(self):
        """
        Get all vectors
        :return:
        """
        try:
            return self.collection.get()
        except Exception as e:
            if self.verbose:
                logger.error(f"Error getting all vectors: {e}")
            return None
