import ollama
from datadashr.llm.base import BaseLLM
from datadashr.config import *


class OllamaLLM(BaseLLM):
    """
    OllamaLLM class
    """

    def __init__(self, model, params, verbose=False):
        """
        Constructor for OllamaLLM
        :param model:
        :param params:
        """
        super().__init__(model, params, verbose=verbose)

    def chat(self, messages):
        """
        Chat with the model
        :param messages:
        :return:
        """
        try:
            if self.verbose:
                logger.info(f"OllamaLLM message: {messages}")
                logger.info(f"Model: {self.model}")
            response = ollama.chat(model=self.model, messages=messages)
            if self.verbose:
                logger.info(f"OllamaLLM response: {response['message']['content']}")
            return response['message']['content']
        except Exception as e:
            if self.verbose:
                logger.error(f"OllamaLLM chat failed: {e}")
            return None
