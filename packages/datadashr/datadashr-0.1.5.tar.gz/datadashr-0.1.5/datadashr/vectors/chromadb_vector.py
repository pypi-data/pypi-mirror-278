import uuid
import chromadb
from loguru import logger


class VectorManager:
    def __init__(self, vector_dir, verbose=False, connector_type='pandas'):
        self.vector_dir = vector_dir
        self.verbose = verbose
        self.connector_type = connector_type
        self.client = chromadb.PersistentClient(self.vector_dir)
        logger.info(f"Available collections: {self.client.list_collections()}")
        self.collection = self.client.get_or_create_collection('datadashr')

    def _clean_prompt(self, prompt):
        return prompt.lower().strip()

    def _clean_columns(self, columns):
        if columns:
            columns = ','.join(columns)
            return columns.lower().strip()
        return None

    def _clean_code(self, code):
        return code.lower().strip()

    def _clean_connector_type(self, connector_type):
        return connector_type.lower().strip()

    def _create_document(self, prompt, columns, code):
        return f"""
        Prompt: {self._clean_prompt(prompt)}
        Code: {self._clean_code(code)}
        """

    def verify_if_document_exists(self, prompt, columns):
        try:

            if results := self.collection.query(
                query_texts=[prompt],
                n_results=1,
                where={
                    "connector_type": self._clean_connector_type(
                        self.connector_type
                    )
                },
                include=["metadatas"],
            ):
                res = results.get('metadatas')[0]
                for r in res:
                    if r.get('prompt') == self._clean_prompt(prompt) and r.get('columns') == self._clean_columns(columns):
                        return True
            return False
        except Exception as e:
            if self.verbose:
                logger.error(f"Error verifying if document exists: {e}")
            return False

    def set_vector(self, prompt, columns, data):
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
        try:
            results = self.collection.query(
                query_texts=[self._clean_prompt(prompt)],
                where={"connector_type": self._clean_connector_type(self.connector_type)},
                include=["metadatas", "distances"]
            )

            res = results.get('metadatas')[0]
            return ''.join(
                f"QUERY: {r.get('prompt')}\nRESPONSE: {r.get('code')}\n\n"
                for r in res
            )
        except Exception as e:
            if self.verbose:
                logger.error(f"Error getting by vector: {e}")
            return None

    def get_all_vectors(self):
        return self.collection.get()
