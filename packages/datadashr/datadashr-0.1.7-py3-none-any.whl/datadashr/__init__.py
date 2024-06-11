from datadashr.llm.base import BaseLLM
from datadashr.utilities.cache import CacheManager
from datadashr.prompt.pandas_prompt import PromptManager
from datadashr.utilities import Utilities
from datadashr.connectors.base import DataConnector
from datadashr.vectors.chromadb_vector import VectorManager
from datadashr.pipeline import Pipeline, ReadDataStep, CacheStep, PromptGenerationStep, LLMRequestStep, \
    SandboxExecutionStep, ErrorHandlingStep, FormatResponseStep, SaveVectorStep, SaveCacheStep
from datadashr.config import *


class DataDashr:
    def __init__(self, llm_instance: BaseLLM, data_connector: DataConnector, **kwargs):
        self.llm_instance = llm_instance
        self.data_connector = data_connector
        self.path = kwargs.get('path', os.path.dirname(os.path.realpath(__file__)))
        self.data_connector_type = self.data_connector.connector_type
        self.cache_dir = CACHE_DIR
        self.vector_dir = VECTOR_DIR
        self.chart_dir = CHART_DIR
        self.log_dir = LOG_DIR
        self.logger = LogManager(self.log_dir)
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

        context = {
            'llm_instance': self.llm_instance,
            'data_connector': self.data_connector,
            'cache_manager': self.cache_manager,
            'prompt_manager': self.prompt_manager,
            'vector_manager': self.vector_manager,
            'utilities': self.ut,
            'df': self.df,
            'request': request,
            'enable_cache': self.enable_cache,
            'enable_vector': self.enable_vector,
            'format_type': self.format_type,
            'chart_dir': self.chart_dir,
            'data_connector_type': self.data_connector_type,
            'verbose': self.verbose,
        }

        step = Pipeline(**context)
        step.add_step(ReadDataStep("ReadData"))
        step.add_step(CacheStep("Cache"))
        step.add_step(PromptGenerationStep("PromptGeneration"))
        step.add_step(LLMRequestStep("LLMRequest"))
        step.add_step(SandboxExecutionStep("SandboxExecution"))
        step.add_step(ErrorHandlingStep("ErrorHandling"))
        step.add_step(SaveCacheStep("SaveCache"))
        step.add_step(SaveVectorStep("SaveVector"))
        step.add_step(FormatResponseStep("FormatResponse"))

        final_context = step.run()
        if self.verbose:
            logger.info(f"Final context: {final_context}")

        formatted_response = final_context.get('formatted_response')
        if self.verbose:
            logger.info(f"Formatted response: {formatted_response}")
        if formatted_response is not None:
            return formatted_response
        else:
            return {'error': 'No formatted response available'}
