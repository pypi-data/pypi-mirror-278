import os
import pandas as pd
from datadashr.sandbox import Sandbox
from datadashr.llm.base import BaseLLM
from datadashr.utilities.cache import CacheManager
from datadashr.prompt.pandas_prompt import PromptManager
from datadashr.utilities import Utilities
from datadashr.connectors.base import DataConnector
from datadashr.vectors.chromadb_vector import VectorManager
from datadashr.response_manager import ResponseFormatter
from loguru import logger


class DataDashr:
    def __init__(self, llm_instance: BaseLLM, data_connector: DataConnector, **kwargs):
        self.llm_instance = llm_instance
        self.data_connector = data_connector
        self.path = kwargs.get('path', os.path.dirname(os.path.realpath(__file__)))
        self.data_connector_type = self.data_connector.connector_type
        self.cache_dir = os.path.join(self.path, "data", "cache_dir")
        self.vector_dir = os.path.join(self.path, "data", "vectors")
        os.makedirs(self.cache_dir, exist_ok=True)
        os.makedirs(self.vector_dir, exist_ok=True)
        self.verbose = kwargs.get('verbose', False)
        self.df = self.data_connector.read_data()
        self.vector_manager = VectorManager(self.vector_dir, self.verbose, self.data_connector_type)
        self.cache_manager = CacheManager(self.cache_dir, self.verbose)
        self.prompt_manager = PromptManager(self.df, kwargs.get('custom_prompt', ""),
                                            kwargs.get('prompt_override', False), verbose=self.verbose)
        self.ut = Utilities(self.verbose)
        self.enable_cache = kwargs.get('enable_cache', False)
        self.enable_vector = kwargs.get('enable_vector', False)
        self.format_type = kwargs.get('format_type', 'api')

        self.request = None

    def chat(self, request):
        if self.verbose:
            logger.info(f"Executing pipeline for request: {request}")
        self.request = request
        if self.enable_cache:
            if cached_result := self.cache_manager.get(request, list(self.df.columns)):
                if self.verbose:
                    logger.info(f"Cache hit for request: {request}")
                    logger.info(f"Cached code: {cached_result['code']}")
                response = self.exec_in_sandbox(cached_result['code'], cached=True)
                if self.verbose:
                    logger.info(f"Cache hit response: {response}")
                return self.format_response(response.get('result'), response.get('full_code'))

        response = self.llm_request(request)
        if 'error' in response and response.get('error'):
            response = self.handle_error(response)

        self.save_cache(response.get('full_code'), request)
        self.save_vector(response.get('full_code'), request)
        return self.format_response(response.get('result'), response.get('full_code'))

    def llm_request(self, request):
        try:
            messages = self.build_prompt_messages(request)
            response = self.llm_instance.chat(messages)
            return self.handle_llm_response(response)
        except Exception as e:
            if self.verbose:
                logger.error(f"LLM request failed: {e}")
            return {'error': str(e)}

    def handle_error(self, response):
        error = response.get('error')
        full_code = response.get('full_code')
        if self.verbose:
            logger.error(f"Error in response: {error}")
        error_response = self.llm_request_error(full_code, error)
        return error_response if error_response.get('error') else error_response

    def llm_request_error(self, full_code, error):
        try:
            message = self.build_prompt_error_messages(full_code, error)
            response = self.llm_instance.chat(message)
            return self.handle_llm_response(response)
        except Exception as e:
            if self.verbose:
                logger.error(f"LLM request failed: {e}")
            return {'error': str(e)}

    def get_examples_from_vectors(self, request) -> list:
        if not self.enable_vector:
            return []
        logger.info(f"Getting examples from vectors for request: {request}")
        return self.vector_manager.get_by_vector(request)

    def build_prompt_messages(self, request) -> list:
        examples = []
        if self.enable_vector:
            examples = self.get_examples_from_vectors(request)
        prompt_content = self.prompt_manager.build_prompt_for_df(request)
        if examples:
            prompt_content += f"\n\nYou can utilize these examples as a reference for generating code.\n{examples}"

        if self.verbose:
            logger.info(f"Prompt content: {prompt_content}")
        return [
            {"role": "system", "content": self.prompt_manager.build_prompt_for_role()},
            {"role": "user", "content": prompt_content}
        ]

    def build_prompt_error_messages(self, full_code, error) -> list:
        return [
            {"role": "user", "content": self.prompt_manager.build_prompt_for_error_correction(error, full_code)}
        ]

    def handle_llm_response(self, response) -> dict:
        if self.verbose:
            logger.info(f"handle_llm_response response: {response}")
        code = self.ut.clean_code(response)
        if self.verbose:
            logger.info(f"handle_llm_response clean code: {code}")
        return self.exec_in_sandbox(code) if code else {'error': 'No code to execute'}

    def exec_in_sandbox(self, code, cached=False) -> dict:
        sandbox_instance = Sandbox(self.verbose)
        sandbox_instance.allow_import("pandas")
        sandbox_instance.allow_import("numpy")
        sandbox_instance.allow_import("matplotlib")
        if cached:
            full_code = code
        else:
            full_code = f"import pandas as pd\nimport numpy as np\n{code}"
        response = sandbox_instance.execute(full_code, {"df": self.df})
        if response.get('error'):
            response = {
                "error": response.get('error'),
                "result": None,
                "full_code": full_code,
            }
        else:
            response = {
                "result": response.get('result'),
                "error": None,
                "full_code": full_code,
            }
        if self.verbose:
            logger.info(f"exec_in_sandbox response {response}")
        return response

    def save_cache(self, full_code, prompt) -> None:
        if self.enable_cache:
            self.cache_manager.set(prompt, list(self.df.columns), {'prompt': prompt, 'code': full_code})

    def save_vector(self, full_code, prompt) -> None:
        if self.enable_vector:
            self.vector_manager.set_vector(prompt, list(self.df.columns), {'prompt': prompt, 'code': full_code})

    def format_response(self, result, full_code) -> dict:
        formatter = ResponseFormatter(result, full_code, self.data_connector_type, self.df.columns.tolist(),
                                      self.request)
        return formatter.format(self.format_type)
